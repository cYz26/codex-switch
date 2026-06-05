from __future__ import annotations

from pathlib import Path

from codex_switch_constants import CONFIG_MODE_SHARED
from codex_switch_io import now_stamp


def optional_path(path: Path | None) -> str | None:
    return str(path) if path else None


def active_record(
    name: str,
    live_codex_home: Path,
    config_mode: str,
    base_config_path: Path,
    backup_dir: Path,
    shim_path: Path | None,
    app_cli_path: str,
    launch_agent_path: Path | None,
) -> dict[str, str | None]:
    shared_config_base = str(base_config_path) if config_mode == CONFIG_MODE_SHARED else None
    return {
        "profile": name,
        "switched_at": now_stamp(),
        "live_codex_home": str(live_codex_home),
        "config_mode": config_mode,
        "shared_config_base": shared_config_base,
        "backup_dir": str(backup_dir),
        "shim": optional_path(shim_path),
        "app_cli_path": app_cli_path if launch_agent_path else None,
        "launch_agent": optional_path(launch_agent_path),
    }
