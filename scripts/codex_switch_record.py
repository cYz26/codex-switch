from __future__ import annotations

from pathlib import Path

from codex_switch_constants import CONFIG_MODE_SHARED
from codex_switch_io import now_stamp
from codex_switch_selection import active_profile_fields, requested_profile_selection


def optional_path(path: Path | None) -> str | None:
    return str(path) if path else None


def active_record(
    name: str,
    codex_home: Path,
    config_mode: str,
    base_config_path: Path,
    backup_dir: Path,
    shim_path: Path | None,
    shell_cli_path: str | None,
    app_cli_path: str,
    launch_agent_path: Path | None,
    home_mode: str | None = None,
    shared_sync_source: Path | None = None,
    shared_sync_target: Path | None = None,
    app_profile: str | None = None,
) -> dict[str, str | None]:
    shared_config_base = str(base_config_path) if config_mode == CONFIG_MODE_SHARED else None
    selection = requested_profile_selection(name, app_profile)
    return {
        **active_profile_fields(selection),
        "switched_at": now_stamp(),
        "live_codex_home": str(codex_home),
        "codex_home": str(codex_home),
        "home_mode": home_mode,
        "config_mode": config_mode,
        "shared_config_base": shared_config_base,
        "backup_id": backup_dir.name,
        "backup_dir": str(backup_dir),
        "shim": optional_path(shim_path),
        "shim_path": optional_path(shim_path),
        "shell_cli_path": shell_cli_path,
        "app_cli_path": app_cli_path if launch_agent_path else None,
        "launch_agent": optional_path(launch_agent_path),
        "launch_agent_path": optional_path(launch_agent_path),
        "shared_sync_source": str(shared_sync_source) if shared_sync_source else None,
        "shared_sync_target": str(shared_sync_target) if shared_sync_target else None,
    }
