from __future__ import annotations

import argparse

from codex_switch_status_active import print_active_profile_status
from codex_switch_status_app import print_app_codex_status
from codex_switch_status_shell import print_shell_codex_status
from codex_switch_store import make_store


def cmd_status(args: argparse.Namespace) -> None:
    store = make_store(args)
    print(f"Store: {store.root}")
    print(f"Live CODEX_HOME target: {store.live_codex_home}")
    active_profile = print_active_profile_status(store)
    print_shell_codex_status(store)
    print_app_codex_status(store, active_profile)
