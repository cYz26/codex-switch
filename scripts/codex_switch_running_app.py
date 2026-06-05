from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from codex_switch_constants import APP_CLI_ENV, DEFAULT_LAUNCH_AGENT_LABEL
from codex_switch_io import run_quiet
from codex_switch_paths import equivalent_paths
from codex_switch_store import Store


DESKTOP_APP_MARKER = "/Applications/Codex.app/Contents/MacOS/Codex"
APP_SERVER_MARKER = " app-server"
LISTEN_ARG = "--listen"
PRIMARY_APP_SERVER_ARG = "--analytics-default-enabled"


@dataclass(frozen=True)
class RunningCodexProcess:
    pid: int
    kind: str
    command_path: str
    app_cli_env: str


def is_default_desktop_context(store: Store) -> bool:
    default_live = Path.home() / ".codex"
    default_agent = (
        Path.home() / "Library" / "LaunchAgents" / f"{DEFAULT_LAUNCH_AGENT_LABEL}.plist"
    )
    return (
        store.live_codex_home.expanduser() == default_live
        and store.launch_agent_path.expanduser() == default_agent
    )


def parse_ps_processes(output: str) -> list[tuple[int, str]]:
    processes: list[tuple[int, str]] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        parts = line.split(None, 1)
        if len(parts) != 2 or not parts[0].isdigit():
            continue
        processes.append((int(parts[0]), parts[1]))
    return processes


def parse_env_app_cli_path(output: str) -> str:
    match = re.search(rf"(?:^|\s){re.escape(APP_CLI_ENV)}=([^\s]+)", output)
    return match.group(1) if match else ""


def app_server_command_path(args: str) -> str:
    if APP_SERVER_MARKER not in args:
        return ""
    return args.split(APP_SERVER_MARKER, 1)[0]


def process_app_cli_env(pid: int) -> str:
    code, output = run_quiet(["/bin/ps", "eww", "-p", str(pid)])
    if code != 0:
        return ""
    return parse_env_app_cli_path(output)


def running_codex_processes() -> list[RunningCodexProcess]:
    code, output = run_quiet(["/bin/ps", "-axo", "pid=,args="])
    if code != 0:
        return []

    observations: list[RunningCodexProcess] = []
    for pid, args in parse_ps_processes(output):
        if DESKTOP_APP_MARKER in args:
            observations.append(
                RunningCodexProcess(
                    pid=pid,
                    kind="desktop",
                    command_path=DESKTOP_APP_MARKER,
                    app_cli_env=process_app_cli_env(pid),
                )
            )
            continue

        command_path = app_server_command_path(args)
        if not command_path:
            continue
        if LISTEN_ARG in args and PRIMARY_APP_SERVER_ARG not in args:
            continue
        observations.append(
            RunningCodexProcess(
                pid=pid,
                kind="app-server",
                command_path=command_path,
                app_cli_env=process_app_cli_env(pid),
            )
        )
    return observations


def running_desktop_problems(
    store: Store,
    active_profile: str,
    expected_app_cli: str,
    observations: list[RunningCodexProcess] | None = None,
    enforce_default_context: bool = True,
) -> list[str]:
    if not expected_app_cli:
        return []
    if enforce_default_context and not is_default_desktop_context(store):
        return []

    problems: list[str] = []
    for process in observations if observations is not None else running_codex_processes():
        if process.kind == "desktop":
            observed = process.app_cli_env
            if observed and not equivalent_paths(observed, expected_app_cli):
                problems.append(
                    f"running Codex Desktop pid {process.pid} has {APP_CLI_ENV}="
                    f"{observed}, but active profile {active_profile} expects "
                    f"{expected_app_cli}; quit Codex Desktop completely and reopen it"
                )
        elif process.kind == "app-server":
            if not equivalent_paths(process.command_path, expected_app_cli):
                problems.append(
                    f"running Codex app-server pid {process.pid} uses "
                    f"{process.command_path}, but active profile {active_profile} "
                    f"expects {expected_app_cli}; quit Codex Desktop completely "
                    "and reopen it"
                )
    return problems


def print_running_desktop_status(store: Store, expected_app_cli: str) -> None:
    if not is_default_desktop_context(store):
        return
    observations = running_codex_processes()
    for process in observations:
        if process.kind == "desktop":
            line = (
                f"Running Codex Desktop pid {process.pid} {APP_CLI_ENV}: "
                f"{process.app_cli_env or '<unset>'}"
            )
            if (
                expected_app_cli
                and process.app_cli_env
                and not equivalent_paths(process.app_cli_env, expected_app_cli)
            ):
                line += f" (expected {expected_app_cli})"
            print(line)
        elif process.kind == "app-server":
            line = f"Running Codex app-server pid {process.pid}: {process.command_path}"
            if expected_app_cli and not equivalent_paths(
                process.command_path, expected_app_cli
            ):
                line += f" (expected {expected_app_cli})"
            print(line)
