from __future__ import annotations

import argparse

from codex_switch_io import read_json
from codex_switch_paths import profile_app_cli_path
from codex_switch_store import make_store


def cmd_list(args: argparse.Namespace) -> None:
    store = make_store(args)
    active = None
    if store.active_path.exists():
        active = read_json(store.active_path).get("profile")
    for name in store.list_profiles():
        marker = "*" if name == active else " "
        manifest = store.load_manifest(name)
        print(
            f"{marker} {name}\t"
            f"cli={manifest.get('codex_bin', '')}\t"
            f"app={profile_app_cli_path(manifest)}"
        )
