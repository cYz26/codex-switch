from __future__ import annotations

import argparse

from codex_switch_constants import SwitchError
from codex_switch_doctor_active import active_profile_problems
from codex_switch_doctor_desktop import desktop_switching_problems
from codex_switch_doctor_profile import profile_health_problems
from codex_switch_io import read_json
from codex_switch_running_app import collect_store_runtime_observation
from codex_switch_runtime_binding import (
    RuntimeBinding,
    RuntimeBindingError,
    RuntimeObservation,
    manifest_uses_canonical_binding,
    resolve_store_runtime_binding,
)
from codex_switch_store import Store, make_store
from codex_switch_verify import (
    collect_parity_report,
    parity_problem_messages,
    print_parity_diagnostics,
)


def collect_doctor_problems(
    store: Store,
    runtime_observation: RuntimeObservation | None = None,
    runtime_binding: RuntimeBinding | None = None,
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
        )
    )
    problems.extend(desktop_switching_problems(store))
    return problems


def active_runtime_binding_for_observation(store: Store) -> RuntimeBinding | None:
    if not store.active_path.exists():
        return None
    try:
        active = read_json(store.active_path)
        profile = active.get("profile")
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
            active_record=active,
        )
    except (SwitchError, RuntimeBindingError):
        return None


def cmd_doctor(args: argparse.Namespace) -> None:
    store = make_store(args)
    binding = active_runtime_binding_for_observation(store)
    observation = collect_store_runtime_observation(store, binding)
    problems = collect_doctor_problems(store, observation, binding)
    if binding is not None and binding.profile == "internal":
        parity_report = collect_parity_report(store, binding)
        print_parity_diagnostics(parity_report)
        problems.extend(parity_problem_messages(parity_report))
    if problems:
        print("Doctor found issues:")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)
    print("Doctor passed")
