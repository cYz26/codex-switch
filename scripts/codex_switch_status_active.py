from __future__ import annotations

from codex_switch_constants import SwitchError
from codex_switch_io import read_json
from codex_switch_paths import profile_app_cli_path
from codex_switch_store import Store


def print_active_profile_status(store: Store) -> str | None:
    active_profile = None
    if store.active_path.exists():
        active = read_json(store.active_path)
        active_profile = active.get("profile")
        print(f"Active profile: {active_profile} ({active.get('switched_at')})")
        if active.get("config_mode"):
            print(f"Config mode: {active.get('config_mode')}")
        if active.get("shared_config_base"):
            print(f"Shared config base: {active.get('shared_config_base')}")
        if isinstance(active_profile, str):
            try:
                manifest = store.load_manifest(active_profile)
                print(f"Active configured CLI: {manifest.get('codex_bin', '')}")
                print(f"Active configured App CLI: {profile_app_cli_path(manifest)}")
            except SwitchError as exc:
                print(f"Active profile manifest: <unavailable: {exc}>")
    else:
        print("Active profile: <none recorded>")
    return active_profile if isinstance(active_profile, str) else None
