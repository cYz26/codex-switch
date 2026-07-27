from __future__ import annotations

from pathlib import Path

from codex_switch_constants import MANAGED_FILES
from codex_switch_restore import create_switch_backup
from codex_switch_store import Store


def backup_live_files(store: Store, profile_name: str) -> Path:
    paths = [store.live_codex_home / name for name in MANAGED_FILES]
    profile_config_name = f"{profile_name}.config.toml"
    paths.extend(
        [
            store.live_codex_home / profile_config_name,
            store.launch_agent_path,
        ]
    )
    return create_switch_backup(
        store=store,
        operation="switch",
        from_profile=None,
        to_profile=profile_name,
        paths=paths,
    )
