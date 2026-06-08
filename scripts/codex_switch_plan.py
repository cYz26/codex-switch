from __future__ import annotations

from pathlib import Path
from typing import Any

from codex_switch_constants import APP_CLI_ENV, CONFIG_MODE_SHARED, CONFIG_MODE_SNAPSHOT, SwitchError
from codex_switch_store import Store
from codex_switch_toml_validate import validate_toml


def resolve_base_config_path(
    store: Store,
    config_mode: str,
    shared_config_base: str | None,
) -> Path:
    base_config_path = store.live_codex_home / "config.toml"
    if config_mode == CONFIG_MODE_SHARED:
        if shared_config_base:
            store.load_manifest(shared_config_base)
            base_config_path = store.profile_dir(shared_config_base) / "config.toml"
        if not base_config_path.exists():
            raise SwitchError(
                f"Shared config base is missing: {base_config_path}. "
                f"Use --config-mode {CONFIG_MODE_SNAPSHOT} or --shared-config-base <profile>."
            )
        validate_toml(base_config_path)
    elif config_mode != CONFIG_MODE_SNAPSHOT:
        raise SwitchError(f"Unsupported config mode: {config_mode}")
    return base_config_path


def switch_plan_actions(
    store: Store,
    name: str,
    manifest: dict[str, Any],
    config_path: Path,
    auth_path: Path,
    app_cli_path: str,
    writes_auth: bool,
    removes_auth: bool,
    config_mode: str,
    shared_config_base: str | None,
    clear_missing_auth: bool,
    skip_shim: bool,
    skip_app_cli: bool,
    skip_launchctl: bool,
) -> list[str]:
    actions = [f"backup live files from {store.live_codex_home}"]
    if config_mode == CONFIG_MODE_SHARED:
        if shared_config_base:
            actions.append(
                f"rewrite shared config.toml from base profile {shared_config_base} "
                f"without embedding profile-specific keys for {name!r}"
            )
            actions.append(
                f"write profile-v2 {name}.config.toml after validating "
                f"shared base profile {shared_config_base}"
            )
        else:
            actions.append(
                f"rewrite live config.toml as shared base without profile-specific keys"
            )
    else:
        actions.append(f"rewrite live config.toml from snapshot base without profile-specific keys")
    actions.append("preserve live non-auth shared config")
    actions.append(f"write {name}.config.toml profile layer")
    if writes_auth:
        actions.append(f"write auth.json from {auth_path}")
    elif removes_auth or clear_missing_auth:
        actions.append("remove live auth.json")
    if not skip_shim:
        actions.append(f"update codex shim using {manifest.get('codex_bin') or '<missing>'}")
    if not skip_app_cli:
        actions.append(f"set Codex Desktop {APP_CLI_ENV} to {app_cli_path or '<missing>'}")
        actions.append(f"write LaunchAgent {store.launch_agent_path}")
        if skip_launchctl:
            actions.append("skip launchctl apply")
    return actions
