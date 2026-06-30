from __future__ import annotations

import argparse
import os
import subprocess
from pathlib import Path

from codex_switch_home_select import profile_home_binding
from codex_switch_home_sync import (
    plugin_support_snapshot_name,
    refresh_profile_plugin_support_snapshot,
)
from codex_switch_io import ensure_private_dir, now_stamp, read_json, write_json
from codex_switch_launch import read_launch_agent_cli_path
from codex_switch_paths import equivalent_paths, profile_app_cli_path
from codex_switch_plugins import missing_enabled_plugins, repair_profile_plugins
from codex_switch_running_app import is_default_desktop_context, running_desktop_problems
from codex_switch_store import Store, make_store
from codex_switch_toml_scan import toml_table_name
from codex_switch_toml_validate import commentless_line, validate_toml
from codex_switch_constants import SwitchError


def has_assignment(text: str, key: str) -> bool:
    for line in text.splitlines():
        stripped = commentless_line(line).strip()
        if stripped.startswith(f"{key} ") or stripped.startswith(f"{key}="):
            return "=" in stripped
    return False


def has_plugin_support(text: str) -> bool:
    for line in text.splitlines():
        table = toml_table_name(line)
        if not table:
            continue
        if table == "skills.config":
            return True
        if table.startswith("marketplaces."):
            return True
        if table.startswith("plugins."):
            return True
        if table.startswith("hooks.state."):
            return True
    return False


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    result: list[Path] = []
    for path in paths:
        resolved = path.expanduser().resolve(strict=False)
        if resolved in seen:
            continue
        seen.add(resolved)
        result.append(path)
    return result


def profile_home(store: Store, name: str) -> Path:
    manifest = store.load_manifest(name)
    return profile_home_binding(store, name, manifest).path


def plugin_snapshot_paths(store: Store, name: str, home: Path) -> list[Path]:
    snapshot = plugin_support_snapshot_name(name)
    return unique_paths([home / snapshot, store.profile_dir(name) / snapshot])


def collect_plugin_snapshot_problems(
    store: Store,
    name: str,
    home: Path,
    runtime_text: str,
) -> list[str]:
    if not has_plugin_support(runtime_text):
        return []
    problems: list[str] = []
    for path in plugin_snapshot_paths(store, name, home):
        if not path.exists():
            problems.append(f"{name}: plugin support snapshot is missing: {path}")
            continue
        try:
            validate_toml(path)
        except SwitchError as exc:
            problems.append(str(exc))
            continue
        if not has_plugin_support(path.read_text()):
            problems.append(
                f"{name}: plugin support snapshot has no marketplace/plugin/skill/hook blocks: {path}"
            )
    return problems


def refresh_plugin_support_snapshots(
    store: Store,
    name: str,
    home: Path,
    messages: list[str],
) -> None:
    config_path = home / "config.toml"
    if not config_path.exists():
        return
    if not has_plugin_support(config_path.read_text()):
        return
    paths = plugin_snapshot_paths(store, name, home)
    refresh_profile_plugin_support_snapshot(name, config_path, paths)
    for path in paths:
        messages.append(f"Refreshed plugin support snapshot: {path}")


def run_safe_repair(store: Store, name: str, home: Path) -> list[str]:
    messages: list[str] = []
    refresh_plugin_support_snapshots(store, name, home, messages)
    if missing_enabled_plugins(store, name):
        messages.append(f"Running plugin repair for {name}")
        repair_profile_plugins(store, name)
    return messages


def collect_active_state_problems(store: Store, name: str, home: Path) -> list[str]:
    if not store.active_path.exists():
        return [f"{name}: active profile record is missing"]
    try:
        active = read_json(store.active_path)
    except SwitchError as exc:
        return [str(exc)]

    problems: list[str] = []
    active_profile = active.get("profile")
    if active_profile != name:
        problems.append(f"active profile is {active_profile or '<missing>'}, expected {name}")

    active_home = active.get("codex_home") or active.get("live_codex_home")
    if isinstance(active_home, str) and active_home:
        if not equivalent_paths(active_home, str(home)):
            problems.append(f"{name}: active CODEX_HOME is {active_home}, expected {home}")
    else:
        problems.append(f"{name}: active CODEX_HOME is missing")

    manifest = store.load_manifest(name)
    expected_shell_cli = str(manifest.get("codex_bin", ""))
    active_shell_cli = active.get("shell_cli_path")
    if expected_shell_cli and active_shell_cli and not equivalent_paths(
        str(active_shell_cli), expected_shell_cli
    ):
        problems.append(
            f"{name}: active shell CLI is {active_shell_cli}, expected {expected_shell_cli}"
        )

    active_app_cli = active.get("app_cli_path")
    expected_app_cli = str(active_app_cli) if active_app_cli else profile_app_cli_path(manifest)

    launch_agent_cli = read_launch_agent_cli_path(store.launch_agent_path)
    if expected_app_cli and launch_agent_cli and not equivalent_paths(
        launch_agent_cli, expected_app_cli
    ):
        problems.append(
            f"{name}: LaunchAgent CODEX_CLI_PATH is {launch_agent_cli}, expected {expected_app_cli}"
        )
    elif expected_app_cli and is_default_desktop_context(store):
        from codex_switch_paths import detect_current_app_cli_path

        gui_app_cli = detect_current_app_cli_path()
        if gui_app_cli and not equivalent_paths(gui_app_cli, expected_app_cli):
            problems.append(
                f"{name}: GUI CODEX_CLI_PATH is {gui_app_cli}, expected {expected_app_cli}"
            )

    if expected_app_cli:
        problems.extend(running_desktop_problems(store, name, expected_app_cli))
    return problems


def collect_runtime_config_problems(store: Store, name: str, home: Path) -> list[str]:
    config_path = home / "config.toml"
    if not config_path.exists():
        return [f"{name}: runtime config is missing: {config_path}"]
    try:
        validate_toml(config_path)
    except SwitchError as exc:
        return [str(exc)]

    runtime_text = config_path.read_text()
    problems: list[str] = []
    if name == "openai-official" and has_assignment(runtime_text, "model_provider"):
        problems.append(
            "openai-official runtime config contains model_provider; "
            "official profile should not be seeded from internal provider settings"
        )
    problems.extend(collect_plugin_snapshot_problems(store, name, home, runtime_text))
    return problems


def run_profile_command(codex_bin: str, home: Path, args: list[str]) -> tuple[int, str]:
    env = dict(os.environ)
    env["CODEX_HOME"] = str(home)
    try:
        result = subprocess.run(
            [codex_bin, *args],
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        )
    except FileNotFoundError:
        return 127, f"not found: {codex_bin}"
    return result.returncode, result.stdout.strip()


def runtime_smoke_problems(
    store: Store,
    name: str,
    home: Path,
    *,
    exec_smoke: str | None = None,
) -> list[str]:
    manifest = store.load_manifest(name)
    codex_bin = str(manifest.get("codex_bin", ""))
    if not codex_bin:
        return [f"{name}: missing codex_bin for runtime smoke"]

    problems: list[str] = []
    commands = [["--version"], ["plugin", "list", "--json"]]
    if exec_smoke is not None:
        commands.append(["exec", "--json", exec_smoke])
    for args in commands:
        code, output = run_profile_command(codex_bin, home, args)
        if code != 0:
            problems.append(
                f"{name}: runtime smoke failed for `{codex_bin} {' '.join(args)}` "
                f"(exit {code}): {output}"
            )
    return problems


def collect_verification_problems(
    store: Store,
    name: str,
    *,
    runtime_smoke: bool = False,
    exec_smoke: str | None = None,
) -> list[str]:
    home = profile_home(store, name)
    problems: list[str] = []
    problems.extend(collect_active_state_problems(store, name, home))
    problems.extend(collect_runtime_config_problems(store, name, home))
    if runtime_smoke or exec_smoke is not None:
        problems.extend(runtime_smoke_problems(store, name, home, exec_smoke=exec_smoke))
    return problems


def write_verification_report(
    store: Store,
    *,
    name: str,
    repair: str,
    runtime_smoke: bool,
    exec_smoke: str | None,
    problems: list[str],
    repair_messages: list[str],
) -> Path:
    report_dir = store.root / "verification"
    ensure_private_dir(report_dir)
    path = report_dir / f"{now_stamp()}-{name}.json"
    write_json(
        path,
        {
            "profile": name,
            "ok": not problems,
            "repair": repair,
            "runtime_smoke": runtime_smoke,
            "exec_smoke": exec_smoke,
            "problems": problems,
            "repair_messages": repair_messages,
        },
    )
    return path


def cmd_verify(args: argparse.Namespace) -> None:
    store = make_store(args)
    home = profile_home(store, args.name)
    repair_messages: list[str] = []
    if args.repair == "safe":
        repair_messages = run_safe_repair(store, args.name, home)
        for message in repair_messages:
            print(message)

    problems = collect_verification_problems(
        store,
        args.name,
        runtime_smoke=args.runtime_smoke,
        exec_smoke=args.exec_smoke,
    )

    smoke_failed = any("runtime smoke failed" in problem for problem in problems)
    if args.runtime_smoke and not smoke_failed:
        print("Runtime smoke: passed")
    if args.exec_smoke is not None and not smoke_failed:
        print("Exec smoke: passed")

    report_path: Path | None = None
    if args.report:
        report_path = write_verification_report(
            store,
            name=args.name,
            repair=args.repair,
            runtime_smoke=args.runtime_smoke,
            exec_smoke=args.exec_smoke,
            problems=problems,
            repair_messages=repair_messages,
        )

    if problems:
        print("Verification found issues:")
        for problem in problems:
            print(f"- {problem}")
        if report_path is not None:
            print(f"Verification report: {report_path}")
        raise SystemExit(1)

    print(f"Verification passed for {args.name}")
    if report_path is not None:
        print(f"Verification report: {report_path}")
