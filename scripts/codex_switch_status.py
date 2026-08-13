from __future__ import annotations

import argparse

from codex_switch_status_active import print_active_profile_status
from codex_switch_status_app import print_app_codex_status
from codex_switch_status_shell import print_shell_codex_status
from codex_switch_shared_configuration import (
    shared_configuration_diagnostic_lines,
    shared_configuration_report,
)
from codex_switch_store import make_store
from codex_switch_verify import (
    collect_parity_report,
    internal_app_parity_not_applicable_message,
    print_parity_diagnostics,
    selection_uses_shared_configuration,
)


def cmd_status(args: argparse.Namespace) -> None:
    store = make_store(args)
    print(f"Store: {store.root}")
    print(f"Live CODEX_HOME target: {store.live_codex_home}")
    active_selection = print_active_profile_status(store)
    if (
        active_selection is not None
        and selection_uses_shared_configuration(active_selection)
    ):
        shared_report = shared_configuration_report(store, active_selection)
        for line in shared_configuration_diagnostic_lines(shared_report):
            print(line)
    print_shell_codex_status(store)
    active_app_profile = (
        active_selection.app_profile
        if active_selection is not None
        else None
    )
    print_app_codex_status(store, active_app_profile)
    active_cli_profile = (
        active_selection.cli_profile
        if active_selection is not None
        else None
    )
    if active_cli_profile == "internal" and active_app_profile == "internal":
        print_parity_diagnostics(collect_parity_report(store, None))
    elif active_cli_profile == "internal" and active_app_profile is not None:
        print(
            internal_app_parity_not_applicable_message(active_app_profile)
        )
