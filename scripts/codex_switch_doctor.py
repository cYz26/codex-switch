from __future__ import annotations

import argparse

from codex_switch_doctor_active import active_profile_problems
from codex_switch_doctor_desktop import desktop_switching_problems
from codex_switch_doctor_profile import profile_health_problems
from codex_switch_store import Store, make_store


def collect_doctor_problems(store: Store) -> list[str]:
    problems: list[str] = []
    if not store.root.exists():
        problems.append("store has not been initialized")
    for name in store.list_profiles():
        problems.extend(profile_health_problems(store, name))
    problems.extend(active_profile_problems(store))
    problems.extend(desktop_switching_problems(store))
    return problems


def cmd_doctor(args: argparse.Namespace) -> None:
    problems = collect_doctor_problems(make_store(args))
    if problems:
        print("Doctor found issues:")
        for problem in problems:
            print(f"- {problem}")
        raise SystemExit(1)
    print("Doctor passed")
