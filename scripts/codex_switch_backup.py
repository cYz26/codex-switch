from __future__ import annotations

from pathlib import Path
from typing import Any

from codex_switch_constants import MANAGED_FILES
from codex_switch_io import copy_file_atomic, ensure_private_dir, now_stamp, write_json
from codex_switch_paths import detect_current_app_cli_path
from codex_switch_store import Store


def backup_live_files(store: Store, profile_name: str) -> Path:
    backup_dir = store.backups_dir / f"{now_stamp()}-{profile_name}"
    ensure_private_dir(backup_dir)
    manifest: dict[str, Any] = {
        "profile": profile_name,
        "live_codex_home": str(store.live_codex_home),
        "launch_agent_path": str(store.launch_agent_path),
        "app_cli_env": detect_current_app_cli_path(),
        "created_at": now_stamp(),
        "files": [],
    }
    for file_name in MANAGED_FILES:
        src = store.live_codex_home / file_name
        if src.exists():
            copy_file_atomic(src, backup_dir / file_name, mode=0o600)
            manifest["files"].append(file_name)
    profile_config_name = f"{profile_name}.config.toml"
    profile_config = store.live_codex_home / profile_config_name
    if profile_config.exists():
        copy_file_atomic(profile_config, backup_dir / profile_config_name, mode=0o600)
        manifest["files"].append(profile_config_name)
    if store.launch_agent_path.exists():
        copy_file_atomic(
            store.launch_agent_path,
            backup_dir / store.launch_agent_path.name,
            mode=0o600,
        )
        manifest["files"].append(store.launch_agent_path.name)
    write_json(backup_dir / "backup.json", manifest)
    return backup_dir
