from __future__ import annotations

import ast
import json
import os
import subprocess
from dataclasses import dataclass
from typing import Any
from pathlib import Path

from codex_switch_constants import SwitchError
from codex_switch_home_select import profile_home_binding
from codex_switch_io import atomic_write
from codex_switch_store import Store, make_store
from codex_switch_toml_scan import toml_table_name
from codex_switch_toml_validate import commentless_line, validate_toml, validate_toml_text


@dataclass(frozen=True)
class PluginRequirement:
    selector: str
    plugin: str
    marketplace: str


def decode_toml_key_segment(raw: str) -> str:
    stripped = raw.strip()
    if len(stripped) >= 2 and stripped[0] in {"'", '"'} and stripped[-1] == stripped[0]:
        try:
            value = ast.literal_eval(stripped)
        except (SyntaxError, ValueError):
            return stripped[1:-1]
        if isinstance(value, str):
            return value
    return stripped


def plugin_selector_from_table(table_name: str) -> str | None:
    prefix = "plugins."
    if not table_name.startswith(prefix):
        return None
    selector = decode_toml_key_segment(table_name[len(prefix) :])
    return selector or None


def assignment_bool(line: str, key: str) -> bool | None:
    stripped = commentless_line(line).strip()
    if not (stripped.startswith(f"{key} ") or stripped.startswith(f"{key}=")):
        return None
    if "=" not in stripped:
        return None
    value = stripped.split("=", 1)[1].strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def plugin_requirement(selector: str) -> PluginRequirement | None:
    if "@" not in selector:
        return None
    plugin, marketplace = selector.rsplit("@", 1)
    if not plugin or not marketplace:
        return None
    return PluginRequirement(selector=selector, plugin=plugin, marketplace=marketplace)


def enabled_plugin_requirements(config_path: Path) -> list[PluginRequirement]:
    if not config_path.exists():
        return []
    validate_toml(config_path)
    requirements: list[PluginRequirement] = []
    seen: set[str] = set()
    current_selector: str | None = None
    current_enabled: bool | None = None

    def flush_current() -> None:
        if current_selector is None or current_enabled is False:
            return
        requirement = plugin_requirement(current_selector)
        if requirement is None or requirement.selector in seen:
            return
        seen.add(requirement.selector)
        requirements.append(requirement)

    for line in config_path.read_text().splitlines():
        table = toml_table_name(line)
        if table:
            flush_current()
            current_selector = plugin_selector_from_table(table)
            current_enabled = None
            continue
        if current_selector is not None:
            enabled = assignment_bool(line, "enabled")
            if enabled is not None:
                current_enabled = enabled
    flush_current()
    return requirements


def profile_home(store: Store, name: str) -> Path:
    manifest = store.load_manifest(name)
    return profile_home_binding(store, name, manifest).path


def profile_codex_bin(store: Store, name: str) -> str:
    manifest = store.load_manifest(name)
    codex_bin = str(manifest.get("codex_bin", ""))
    if not codex_bin:
        raise SwitchError(f"{name}: missing codex_bin")
    if not Path(codex_bin).expanduser().exists():
        raise SwitchError(f"{name}: codex_bin does not exist: {codex_bin}")
    return codex_bin


def plugin_cache_path(home: Path, requirement: PluginRequirement) -> Path:
    return home / "plugins" / "cache" / requirement.marketplace / requirement.plugin


def plugin_is_installed(home: Path, requirement: PluginRequirement) -> bool:
    cache_path = plugin_cache_path(home, requirement)
    if cache_path.is_dir() and any(cache_path.iterdir()):
        return True
    direct_path = home / "plugins" / requirement.plugin
    return direct_path.exists()


def missing_enabled_plugins(store: Store, name: str) -> list[PluginRequirement]:
    home = profile_home(store, name)
    return [
        requirement
        for requirement in enabled_plugin_requirements(home / "config.toml")
        if not plugin_is_installed(home, requirement)
    ]


def plugin_materialization_problems(store: Store, name: str) -> list[str]:
    home = profile_home(store, name)
    problems: list[str] = []
    for requirement in missing_enabled_plugins(store, name):
        expected = plugin_cache_path(home, requirement)
        problems.append(
            f"active profile {name}: enabled plugin is not installed in CODEX_HOME: "
            f"{requirement.selector} (expected cache under {expected}; "
            f"run: codex-switch repair-plugins {name}; if the refreshed catalog "
            f"does not contain this selector, run: codex-switch repair-plugins "
            f"{name} --disable-unavailable)"
        )
    return problems


def disable_plugin_selector_in_text(text: str, selector: str) -> tuple[str, bool]:
    lines = text.splitlines()
    updated: list[str] = []
    in_target_table = False
    saw_target_table = False
    saw_enabled = False
    changed = False

    def close_target_table() -> None:
        nonlocal changed, saw_enabled
        if in_target_table and not saw_enabled:
            updated.append("enabled = false")
            changed = True
            saw_enabled = True

    for line in lines:
        table = toml_table_name(line)
        if table:
            close_target_table()
            current_selector = plugin_selector_from_table(table)
            in_target_table = current_selector == selector
            saw_target_table = saw_target_table or in_target_table
            saw_enabled = False
            updated.append(line)
            continue

        if in_target_table:
            enabled = assignment_bool(line, "enabled")
            if enabled is not None:
                updated.append("enabled = false")
                saw_enabled = True
                if enabled is not False:
                    changed = True
                continue
        updated.append(line)

    close_target_table()
    if not saw_target_table:
        return text, False
    result = "\n".join(updated).rstrip() + "\n"
    validate_toml_text(result, "plugin selector cleanup")
    return result, changed


def profile_plugin_config_paths(store: Store, name: str, home: Path) -> list[Path]:
    candidates = [
        home / "config.toml",
        home / f"{name}.config.toml",
        store.profile_dir(name) / "config.toml",
        store.live_codex_home / "config.toml",
        store.live_codex_home / f"{name}.config.toml",
    ]
    internal_home = store.managed_home("internal")
    candidates.extend(
        [
            internal_home / "config.toml",
            internal_home / f"{name}.config.toml",
        ]
    )
    seen: set[Path] = set()
    paths: list[Path] = []
    for path in candidates:
        resolved = Path(path).expanduser().resolve(strict=False)
        if resolved in seen or not path.exists():
            continue
        seen.add(resolved)
        paths.append(path)
    return paths


def disable_unavailable_plugin_requirements(
    store: Store,
    name: str,
    home: Path,
    requirements: list[PluginRequirement],
) -> list[Path]:
    changed_paths: list[Path] = []
    selectors = [requirement.selector for requirement in requirements]
    for path in profile_plugin_config_paths(store, name, home):
        original = path.read_text()
        updated = original
        changed = False
        for selector in selectors:
            updated, selector_changed = disable_plugin_selector_in_text(updated, selector)
            changed = changed or selector_changed
        if not changed:
            continue
        atomic_write(path, updated.encode(), mode=0o600)
        changed_paths.append(path)
    return changed_paths


def run_profile_plugin_command(
    *,
    name: str,
    codex_bin: str,
    home: Path,
    args: list[str],
    description: str,
    dry_run: bool = False,
    echo_stdout: bool = True,
) -> str:
    command = [codex_bin, "plugin", *args]
    if dry_run:
        print("Dry run:", " ".join(command))
        return ""
    env = dict(os.environ)
    env["CODEX_HOME"] = str(home)
    result = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=env,
    )
    output = result.stdout.strip()
    if output and echo_stdout:
        print(output)
    if result.returncode != 0:
        if output and not echo_stdout:
            print(output)
        raise SwitchError(f"{name}: failed to {description} (exit {result.returncode})")
    return result.stdout


def refresh_profile_plugin_catalogs(
    *,
    name: str,
    codex_bin: str,
    home: Path,
    dry_run: bool = False,
) -> set[str] | None:
    print(f"Refreshing plugin marketplaces for {name}")
    run_profile_plugin_command(
        name=name,
        codex_bin=codex_bin,
        home=home,
        args=["marketplace", "upgrade", "--json"],
        description="refresh plugin marketplaces",
        dry_run=dry_run,
        echo_stdout=False,
    )
    print(f"Priming available plugin catalog for {name}")
    output = run_profile_plugin_command(
        name=name,
        codex_bin=codex_bin,
        home=home,
        args=["list", "--available", "--json"],
        description="list available plugins",
        dry_run=dry_run,
        echo_stdout=False,
    )
    if dry_run:
        return None
    return available_plugin_selectors(output)


def available_plugin_selectors(output: str) -> set[str]:
    if not output.strip():
        return set()
    try:
        data = json.loads(output)
    except json.JSONDecodeError:
        return set()
    selectors: set[str] = set()
    collect_available_plugin_selectors(data, selectors)
    return selectors


def collect_available_plugin_selectors(value: Any, selectors: set[str]) -> None:
    if isinstance(value, list):
        for item in value:
            collect_available_plugin_selectors(item, selectors)
        return
    if not isinstance(value, dict):
        return

    for key in ("pluginId", "id", "selector"):
        selector = value.get(key)
        if isinstance(selector, str) and plugin_requirement(selector) is not None:
            selectors.add(selector)

    plugin = value.get("plugin") or value.get("name")
    marketplace = (
        value.get("marketplace")
        or value.get("marketplaceId")
        or value.get("marketplaceName")
    )
    if isinstance(plugin, str) and isinstance(marketplace, str):
        selector = f"{plugin}@{marketplace}"
        if plugin_requirement(selector) is not None:
            selectors.add(selector)

    for key in ("available", "plugins", "items", "data"):
        collect_available_plugin_selectors(value.get(key), selectors)


def repair_profile_plugins(
    store: Store,
    name: str,
    *,
    dry_run: bool = False,
    disable_unavailable: bool = False,
) -> int:
    codex_bin = profile_codex_bin(store, name)
    home = profile_home(store, name)
    available_selectors = refresh_profile_plugin_catalogs(
        name=name,
        codex_bin=codex_bin,
        home=home,
        dry_run=dry_run,
    )
    missing = missing_enabled_plugins(store, name)
    if not missing:
        print(f"No missing enabled plugins for {name}")
        return 0
    if dry_run:
        print(
            "Dry run: plugin catalog is not inspected; missing enabled plugins "
            "will only be installed when they appear in the refreshed available catalog."
        )
        for requirement in missing:
            print(f"Dry run: would install if available: {requirement.selector}")
        if disable_unavailable:
            print(
                "Dry run: would disable unavailable enabled plugins only after "
                "a real catalog refresh proves they are unavailable."
            )
        return 0

    installable = missing
    unavailable: list[PluginRequirement] = []
    if available_selectors is not None:
        installable = [
            requirement
            for requirement in missing
            if requirement.selector in available_selectors
        ]
        unavailable = [
            requirement
            for requirement in missing
            if requirement.selector not in available_selectors
        ]
        for requirement in missing:
            if requirement.selector not in available_selectors:
                print(
                    f"Skipping unavailable enabled plugin: {requirement.selector} "
                    "(not found in available plugin catalog)"
                )
    if disable_unavailable and unavailable:
        for requirement in unavailable:
            print(f"Disabling unavailable enabled plugin: {requirement.selector}")
        changed_paths = disable_unavailable_plugin_requirements(
            store,
            name,
            home,
            unavailable,
        )
        for path in changed_paths:
            print(f"Updated plugin config: {path}")

    for requirement in installable:
        print(f"Installing plugin: {requirement.selector}")
        run_profile_plugin_command(
            name=name,
            codex_bin=codex_bin,
            home=home,
            args=["add", requirement.selector],
            description=f"install plugin {requirement.selector}",
            dry_run=dry_run,
        )
    return 0


def cmd_repair_plugins(args) -> None:
    repair_profile_plugins(
        make_store(args),
        args.name,
        dry_run=args.dry_run,
        disable_unavailable=args.disable_unavailable,
    )
