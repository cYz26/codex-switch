from __future__ import annotations

import argparse

from codex_switch_constants import SwitchError
from codex_switch_doctor_active import active_profile_problems
from codex_switch_doctor_desktop import desktop_switching_problems
from codex_switch_doctor_profile import profile_health_problems
from codex_switch_running_app import collect_store_runtime_observation
from codex_switch_runtime_binding import (
    RuntimeBinding,
    RuntimeBindingError,
    RuntimeObservation,
    manifest_uses_canonical_binding,
    resolve_store_runtime_binding,
)
from codex_switch_selection import (
    ActiveProfileSelectionSnapshot,
    read_active_profile_selection_snapshot,
)
from codex_switch_shared_configuration import shared_configuration_report
from codex_switch_store import Store, make_store
from codex_switch_verify import (
    collect_parity_report,
    internal_app_parity_not_applicable_message,
    parity_problem_messages,
    print_parity_diagnostics,
    selection_uses_shared_configuration,
    shared_configuration_diagnostic_lines,
    shared_configuration_problem_messages,
)


_SHARED_CONFIGURATION_REPORT_UNSET = object()


def active_internal_app_profile(
    store: Store,
    *,
    snapshot: ActiveProfileSelectionSnapshot | None = None,
) -> str | None:
    active_snapshot = snapshot or read_active_profile_selection_snapshot(
        store.active_path
    )
    selection = active_snapshot.selection
    if active_snapshot.problem is not None or selection is None:
        return None
    if selection.cli_profile != "internal":
        return None
    return selection.app_profile


def active_shared_configuration_report(
    store: Store,
    *,
    snapshot: ActiveProfileSelectionSnapshot | None = None,
) -> object | None:
    active_snapshot = snapshot or read_active_profile_selection_snapshot(
        store.active_path
    )
    selection = active_snapshot.selection
    if active_snapshot.problem is not None or selection is None:
        return None
    if not selection_uses_shared_configuration(selection):
        return None
    return shared_configuration_report(store, selection)


def collect_doctor_problems(
    store: Store,
    runtime_observation: RuntimeObservation | None = None,
    runtime_binding: RuntimeBinding | None = None,
    shared_configuration: object = _SHARED_CONFIGURATION_REPORT_UNSET,
    snapshot: ActiveProfileSelectionSnapshot | None = None,
) -> list[str]:
    problems: list[str] = []
    if not store.root.exists():
        problems.append("store has not been initialized")
    for name in store.list_profiles():
        problems.extend(profile_health_problems(store, name))
    problems.extend(
        active_profile_problems(
            store,
            runtime_binding=runtime_binding,
            runtime_observation=runtime_observation,
            snapshot=snapshot,
        )
    )
    problems.extend(desktop_switching_problems(store))
    shared_report = shared_configuration
    if shared_report is _SHARED_CONFIGURATION_REPORT_UNSET:
        shared_report = active_shared_configuration_report(
            store,
            snapshot=snapshot,
        )
    if shared_report is not None:
        problems.extend(shared_configuration_problem_messages(shared_report))
    return problems


def active_runtime_binding_for_observation(
    store: Store,
    *,
    snapshot: ActiveProfileSelectionSnapshot | None = None,
) -> RuntimeBinding | None:
    active_snapshot = snapshot or read_active_profile_selection_snapshot(
        store.active_path
    )
    if active_snapshot.problem is not None or active_snapshot.selection is None:
        return None
    try:
        profile = active_snapshot.selection.app_profile
        if not isinstance(profile, str) or profile not in {
            "internal",
            "openai-official",
            "official",
        }:
            return None
        manifest = store.load_manifest(profile)
        if not manifest_uses_canonical_binding(profile, manifest):
            return None
        return resolve_store_runtime_binding(
            store,
            profile,
            manifest=manifest,
        )
    except (SwitchError, RuntimeBindingError):
        return None


def active_cli_runtime_binding_for_parity(
    store: Store,
    *,
    snapshot: ActiveProfileSelectionSnapshot | None = None,
) -> RuntimeBinding | None:
    active_snapshot = snapshot or read_active_profile_selection_snapshot(
        store.active_path
    )
    selection = active_snapshot.selection
    if active_snapshot.problem is not None or selection is None:
        return None
    try:
        if (
            selection.cli_profile != "internal"
            or selection.app_profile != "internal"
        ):
            return None
        profile = selection.cli_profile
        manifest = store.load_manifest(profile)
        if not manifest_uses_canonical_binding(profile, manifest):
            return None
        return resolve_store_runtime_binding(
            store,
            profile,
            manifest=manifest,
        )
    except (SwitchError, RuntimeBindingError):
        return None


def cmd_doctor(args: argparse.Namespace) -> None:
    store = make_store(args)
    snapshot = read_active_profile_selection_snapshot(store.active_path)
    binding = active_runtime_binding_for_observation(
        store,
        snapshot=snapshot,
    )
    observation = collect_store_runtime_observation(store, binding)
    shared_report = active_shared_configuration_report(
        store,
        snapshot=snapshot,
    )
    shared_problems = shared_configuration_problem_messages(shared_report)
    if shared_report is not None and not shared_problems:
        for line in shared_configuration_diagnostic_lines(shared_report):
            print(line)
    problems = collect_doctor_problems(
        store,
        observation,
        binding,
        shared_configuration=shared_report,
        snapshot=snapshot,
    )
    parity_binding = active_cli_runtime_binding_for_parity(
        store,
        snapshot=snapshot,
    )
    if parity_binding is not None:
        parity_report = collect_parity_report(store, parity_binding)
        print_parity_diagnostics(parity_report)
        problems.extend(parity_problem_messages(parity_report))
    else:
        app_profile = active_internal_app_profile(
            store,
            snapshot=snapshot,
        )
        if app_profile is not None and app_profile != "internal":
            print(internal_app_parity_not_applicable_message(app_profile))
    if problems:
        print("Doctor found issues:")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)
    print("Doctor passed")
