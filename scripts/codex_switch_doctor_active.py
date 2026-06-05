from __future__ import annotations

from codex_switch_constants import APP_CLI_ENV, SwitchError
from codex_switch_io import read_json
from codex_switch_launch import read_launch_agent_cli_path
from codex_switch_paths import detect_current_app_cli_path, equivalent_paths, profile_app_cli_path
from codex_switch_running_app import running_desktop_problems
from codex_switch_store import Store


def active_app_cli_observation(store: Store) -> tuple[str, str]:
    launch_agent_cli = read_launch_agent_cli_path(store.launch_agent_path)
    if launch_agent_cli:
        return (f"LaunchAgent {APP_CLI_ENV}", launch_agent_cli)
    current_app_cli = detect_current_app_cli_path()
    if current_app_cli:
        return (f"GUI {APP_CLI_ENV}", current_app_cli)
    return ("", "")


def active_profile_problems(store: Store) -> list[str]:
    if not store.active_path.exists():
        return []
    active_profile = read_json(store.active_path).get("profile")
    if not isinstance(active_profile, str):
        return []
    try:
        active_manifest = store.load_manifest(active_profile)
    except SwitchError as exc:
        return [str(exc)]

    expected_app_cli = profile_app_cli_path(active_manifest)
    observed_label, current_app_cli = active_app_cli_observation(store)
    problems: list[str] = []
    if (
        expected_app_cli
        and current_app_cli
        and not equivalent_paths(current_app_cli, expected_app_cli)
    ):
        problems.append(
            f"active profile {active_profile}: {observed_label} is "
            f"{current_app_cli}, expected {expected_app_cli}"
        )
    problems.extend(running_desktop_problems(store, active_profile, expected_app_cli))
    return problems
