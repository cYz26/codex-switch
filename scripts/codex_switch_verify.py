from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import threading
import time
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


AZURE_RESPONSES_RESOURCE_MISMATCH = (
    "The requested item was created under a different Azure OpenAI resource"
)
RESPONSES_TOOL_SMOKE_PROMPT = (
    "Use the shell tool to run exactly: printf codex_switch_responses_tool_smoke. "
    "Then reply with exactly: done"
)
SAFE_SMOKE_HEADERS = {
    "x-account-id": "accounts",
    "x-account-deployment": "deployments",
    "x-model-request-id": "model_request_ids",
    "x-tt-logid": "tt_log_ids",
}
APP_SERVER_INITIALIZE_ID = "__codex_initialize__"
APP_SERVER_PLUGIN_LIST_ID = "plugin-list-smoke"
APP_SERVER_RESPONSE_TIMEOUT_SECONDS = 6.0
APP_SERVER_SETTLE_SECONDS = 1.5
APP_SERVER_OUTPUT_LINE_LIMIT = 8


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


def unique_preserve_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for value in values:
        if value in seen:
            continue
        seen.add(value)
        result.append(value)
    return result


def safe_header_values(output: str, header: str) -> list[str]:
    pattern = re.compile(rf"(?im)^\s*{re.escape(header)}\s*:\s*([^,\r\n ]+)")
    return unique_preserve_order(pattern.findall(output))


def responses_tool_smoke_args() -> list[str]:
    return [
        "exec",
        "--json",
        "--ephemeral",
        "--ignore-rules",
        "--skip-git-repo-check",
        "-c",
        'approval_policy="never"',
        "-s",
        "read-only",
        "-C",
        str(Path.cwd()),
        RESPONSES_TOOL_SMOKE_PROMPT,
    ]


def app_server_smoke_args() -> list[str]:
    return ["app-server", "--analytics-default-enabled"]


def app_server_initialize_message() -> dict[str, object]:
    return {
        "id": APP_SERVER_INITIALIZE_ID,
        "method": "initialize",
        "params": {
            "clientInfo": {
                "name": "codex-switch-smoke",
                "version": "0.0.0",
            },
            "capabilities": {
                "experimentalApi": True,
            },
        },
    }


def app_server_initialized_message() -> dict[str, object]:
    return {"method": "initialized"}


def app_server_plugin_list_message() -> dict[str, object]:
    return {
        "id": APP_SERVER_PLUGIN_LIST_ID,
        "method": "plugin/list",
        "params": {
            "marketplaceKinds": [
                "local",
                "vertical",
                "shared-with-me",
                "created-by-me-remote",
            ],
        },
    }


def write_app_server_message(process: subprocess.Popen[str], message: dict[str, object]) -> None:
    if process.stdin is None:
        raise BrokenPipeError("app-server stdin is unavailable")
    process.stdin.write(json.dumps(message, separators=(",", ":")) + "\n")
    process.stdin.flush()


def read_stream_lines(stream, lines: list[str]) -> None:
    if stream is None:
        return
    for line in stream:
        lines.append(line.rstrip("\n"))


def response_seen(lines: list[str], request_id: str) -> bool:
    for line in lines:
        try:
            message = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(message, dict) and message.get("id") == request_id:
            return True
    return False


def output_excerpt(lines: list[str]) -> str:
    selected = [line for line in lines if line][-APP_SERVER_OUTPUT_LINE_LIMIT:]
    if not selected:
        return "<no output>"
    return " | ".join(selected)


def wait_for_app_server_response(
    process: subprocess.Popen[str],
    stdout_lines: list[str],
    request_id: str,
    *,
    timeout_seconds: float = APP_SERVER_RESPONSE_TIMEOUT_SECONDS,
) -> str | None:
    deadline = time.monotonic() + timeout_seconds
    while time.monotonic() < deadline:
        returncode = process.poll()
        if returncode is not None:
            return f"app-server exited before `{request_id}` response (exit {returncode})"
        if response_seen(stdout_lines, request_id):
            return None
        time.sleep(0.05)
    return f"timed out waiting for `{request_id}` response"


def wait_for_app_server_settle(
    process: subprocess.Popen[str],
    *,
    settle_seconds: float = APP_SERVER_SETTLE_SECONDS,
) -> str | None:
    deadline = time.monotonic() + settle_seconds
    while time.monotonic() < deadline:
        returncode = process.poll()
        if returncode is not None:
            return f"app-server exited during startup settle window (exit {returncode})"
        time.sleep(0.05)
    return None


def terminate_app_server_smoke(process: subprocess.Popen[str]) -> None:
    if process.stdin is not None:
        try:
            process.stdin.close()
        except OSError:
            pass
    if process.poll() is not None:
        return
    process.terminate()
    try:
        process.wait(timeout=2)
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait(timeout=2)


def run_app_server_smoke(codex_bin: str, home: Path) -> tuple[int, str]:
    env = dict(os.environ)
    env["CODEX_HOME"] = str(home)
    stdout_lines: list[str] = []
    stderr_lines: list[str] = []
    try:
        process = subprocess.Popen(
            [codex_bin, *app_server_smoke_args()],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env,
        )
    except FileNotFoundError:
        return 127, f"not found: {codex_bin}"
    except OSError as exc:
        return 1, str(exc)

    stdout_thread = threading.Thread(
        target=read_stream_lines,
        args=(process.stdout, stdout_lines),
        daemon=True,
    )
    stderr_thread = threading.Thread(
        target=read_stream_lines,
        args=(process.stderr, stderr_lines),
        daemon=True,
    )
    stdout_thread.start()
    stderr_thread.start()
    reason: str | None = None
    try:
        write_app_server_message(process, app_server_initialize_message())
        reason = wait_for_app_server_response(
            process,
            stdout_lines,
            APP_SERVER_INITIALIZE_ID,
        )
        if reason is None:
            write_app_server_message(process, app_server_initialized_message())
            write_app_server_message(process, app_server_plugin_list_message())
            reason = wait_for_app_server_response(
                process,
                stdout_lines,
                APP_SERVER_PLUGIN_LIST_ID,
            )
        if reason is None:
            reason = wait_for_app_server_settle(process)
    except (BrokenPipeError, OSError) as exc:
        returncode = process.poll()
        reason = f"unable to write app-server smoke request: {exc}"
        if returncode is not None:
            reason = f"{reason} (exit {returncode})"
    finally:
        terminate_app_server_smoke(process)
        stdout_thread.join(timeout=0.2)
        stderr_thread.join(timeout=0.2)

    if reason is not None:
        return (
            1,
            f"{reason}; stdout: {output_excerpt(stdout_lines)}; "
            f"stderr: {output_excerpt(stderr_lines)}",
        )
    return 0, "app-server smoke passed"


def azure_responses_resource_mismatch_diagnostic(output: str) -> dict[str, object] | None:
    if AZURE_RESPONSES_RESOURCE_MISMATCH not in output:
        return None
    diagnostic: dict[str, object] = {
        "kind": "azure_responses_resource_mismatch",
        "message": "Responses context follow-up must stay on the same Azure OpenAI resource",
    }
    for header, key in SAFE_SMOKE_HEADERS.items():
        diagnostic[key] = safe_header_values(output, header)
    return diagnostic


def format_responses_tool_smoke_problem(
    name: str,
    diagnostic: dict[str, object],
) -> str:
    parts = [
        f"{name}: internal Responses resource-stickiness failure",
        "Responses context follow-up must stay on the same Azure OpenAI resource",
    ]
    accounts = diagnostic.get("accounts")
    if isinstance(accounts, list) and accounts:
        parts.append(f"x-account-id route: {' -> '.join(str(account) for account in accounts)}")
    deployments = diagnostic.get("deployments")
    if isinstance(deployments, list) and deployments:
        parts.append(f"deployment: {', '.join(str(item) for item in deployments)}")
    model_request_ids = diagnostic.get("model_request_ids")
    if isinstance(model_request_ids, list) and model_request_ids:
        parts.append(f"x-model-request-id: {', '.join(str(item) for item in model_request_ids)}")
    tt_log_ids = diagnostic.get("tt_log_ids")
    if isinstance(tt_log_ids, list) and tt_log_ids:
        parts.append(f"x-tt-logid: {', '.join(str(item) for item in tt_log_ids)}")
    return "; ".join(parts)


def runtime_smoke_problems(
    store: Store,
    name: str,
    home: Path,
    *,
    app_server_smoke: bool = False,
    exec_smoke: str | None = None,
    runtime_smoke: bool = False,
    responses_tool_smoke: bool = False,
) -> tuple[list[str], list[dict[str, object]]]:
    manifest = store.load_manifest(name)
    codex_bin = str(manifest.get("codex_bin", ""))
    if not codex_bin:
        return [f"{name}: missing codex_bin for runtime smoke"], []

    problems: list[str] = []
    smoke_diagnostics: list[dict[str, object]] = []
    commands: list[tuple[str, list[str]]] = []
    if runtime_smoke:
        commands.extend(
            [
                ("runtime smoke", ["--version"]),
                ("runtime smoke", ["plugin", "list", "--json"]),
            ]
        )
    if exec_smoke is not None:
        commands.append(("exec smoke", ["exec", "--json", exec_smoke]))
    if responses_tool_smoke:
        commands.append(("Responses tool smoke", responses_tool_smoke_args()))
    for label, args in commands:
        code, output = run_profile_command(codex_bin, home, args)
        if code != 0:
            if label == "Responses tool smoke":
                diagnostic = azure_responses_resource_mismatch_diagnostic(output)
                if diagnostic is not None:
                    smoke_diagnostics.append(diagnostic)
                    problems.append(format_responses_tool_smoke_problem(name, diagnostic))
                    continue
            problems.append(
                f"{name}: {label} failed for `{codex_bin} {' '.join(args)}` "
                f"(exit {code}): {output}"
            )
    if app_server_smoke:
        code, output = run_app_server_smoke(codex_bin, home)
        if code != 0:
            problems.append(
                f"{name}: app-server smoke failed for "
                f"`{codex_bin} {' '.join(app_server_smoke_args())}` "
                f"(exit {code}): {output}"
            )
    return problems, smoke_diagnostics


def collect_verification_problems(
    store: Store,
    name: str,
    *,
    app_server_smoke: bool = False,
    runtime_smoke: bool = False,
    exec_smoke: str | None = None,
    responses_tool_smoke: bool = False,
) -> tuple[list[str], list[dict[str, object]]]:
    home = profile_home(store, name)
    problems: list[str] = []
    smoke_diagnostics: list[dict[str, object]] = []
    problems.extend(collect_active_state_problems(store, name, home))
    problems.extend(collect_runtime_config_problems(store, name, home))
    if app_server_smoke or runtime_smoke or exec_smoke is not None or responses_tool_smoke:
        smoke_problems, smoke_diagnostics = runtime_smoke_problems(
            store,
            name,
            home,
            app_server_smoke=app_server_smoke,
            exec_smoke=exec_smoke,
            runtime_smoke=runtime_smoke,
            responses_tool_smoke=responses_tool_smoke,
        )
        problems.extend(smoke_problems)
    return problems, smoke_diagnostics


def write_verification_report(
    store: Store,
    *,
    name: str,
    repair: str,
    app_server_smoke: bool,
    runtime_smoke: bool,
    exec_smoke: str | None,
    responses_tool_smoke: bool,
    problems: list[str],
    smoke_diagnostics: list[dict[str, object]],
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
            "app_server_smoke": app_server_smoke,
            "runtime_smoke": runtime_smoke,
            "exec_smoke": exec_smoke,
            "responses_tool_smoke": responses_tool_smoke,
            "smoke_diagnostics": smoke_diagnostics,
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

    problems, smoke_diagnostics = collect_verification_problems(
        store,
        args.name,
        app_server_smoke=args.app_server_smoke,
        runtime_smoke=args.runtime_smoke,
        exec_smoke=args.exec_smoke,
        responses_tool_smoke=args.responses_tool_smoke,
    )

    app_server_failed = any("app-server smoke failed" in problem for problem in problems)
    runtime_failed = any("runtime smoke failed" in problem for problem in problems)
    exec_failed = any("exec smoke failed" in problem for problem in problems)
    responses_tool_failed = any(
        "Responses tool smoke failed" in problem
        or "internal Responses resource-stickiness failure" in problem
        for problem in problems
    )
    if args.app_server_smoke and not app_server_failed:
        print("App-server smoke: passed")
    if args.runtime_smoke and not runtime_failed:
        print("Runtime smoke: passed")
    if args.exec_smoke is not None and not exec_failed:
        print("Exec smoke: passed")
    if args.responses_tool_smoke and not responses_tool_failed:
        print("Responses tool smoke: passed")

    report_path: Path | None = None
    if args.report:
        report_path = write_verification_report(
            store,
            name=args.name,
            repair=args.repair,
            app_server_smoke=args.app_server_smoke,
            runtime_smoke=args.runtime_smoke,
            exec_smoke=args.exec_smoke,
            responses_tool_smoke=args.responses_tool_smoke,
            problems=problems,
            smoke_diagnostics=smoke_diagnostics,
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
