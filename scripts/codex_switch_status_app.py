from __future__ import annotations

from codex_switch_constants import APP_CLI_ENV, DEFAULT_APP_BUNDLE_CODEX, SwitchError
from codex_switch_launch import read_launch_agent_cli_path
from codex_switch_paths import detect_current_app_cli_path, equivalent_paths, profile_app_cli_path
from codex_switch_running_app import print_running_desktop_status
from codex_switch_status_shell import print_codex_version
from codex_switch_store import Store


def print_app_codex_status(store: Store, active_profile: str | None) -> None:
    app_env = detect_current_app_cli_path()
    active_app_cli = ""
    print(f"GUI {APP_CLI_ENV}: {app_env or '<unset>'}")
    if active_profile and app_env:
        try:
            active_app_cli = profile_app_cli_path(store.load_manifest(active_profile))
            if active_app_cli and not equivalent_paths(app_env, active_app_cli):
                print(f"GUI {APP_CLI_ENV} expected profile path: {active_app_cli}")
        except SwitchError:
            pass
    print(f"LaunchAgent: {store.launch_agent_path if store.launch_agent_path.exists() else '<missing>'}")
    launch_agent_cli = read_launch_agent_cli_path(store.launch_agent_path)
    if launch_agent_cli:
        print(f"LaunchAgent {APP_CLI_ENV}: {launch_agent_cli}")
    if DEFAULT_APP_BUNDLE_CODEX.exists():
        print(f"Bundled app codex: {DEFAULT_APP_BUNDLE_CODEX}")
        print_codex_version("Bundled app codex version", str(DEFAULT_APP_BUNDLE_CODEX))
    print_running_desktop_status(store, active_app_cli)
