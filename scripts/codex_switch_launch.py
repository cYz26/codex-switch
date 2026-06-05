from __future__ import annotations

import os
import plistlib
from pathlib import Path

from codex_switch_core import APP_CLI_ENV, Store, SwitchError, atomic_write, run_quiet


def validate_executable_path(raw_path: str, field_name: str) -> Path:
    if not raw_path:
        raise SwitchError(f"Profile manifest has no {field_name}.")
    path = Path(raw_path).expanduser()
    if not path.is_absolute():
        raise SwitchError(f"{field_name} must be an absolute path: {raw_path}")
    if not path.exists():
        raise SwitchError(f"{field_name} does not exist: {path}")
    return path


def launch_agent_payload(label: str, app_cli_path: Path) -> bytes:
    payload = {
        "Label": label,
        "ProgramArguments": [
            "/bin/launchctl",
            "setenv",
            APP_CLI_ENV,
            str(app_cli_path),
        ],
        "RunAtLoad": True,
    }
    return plistlib.dumps(payload, fmt=plistlib.FMT_XML, sort_keys=False)


def write_app_cli_launch_agent(
    store: Store,
    app_cli_path: str,
    skip_launchctl: bool,
) -> Path:
    path = validate_executable_path(app_cli_path, "app_cli_path")
    atomic_write(
        store.launch_agent_path,
        launch_agent_payload(store.launch_agent_label, path),
        mode=0o644,
    )
    if skip_launchctl:
        return store.launch_agent_path

    code, output = run_quiet(["/bin/launchctl", "setenv", APP_CLI_ENV, str(path)])
    if code != 0:
        raise SwitchError(f"launchctl setenv failed: {output}")

    domain = f"gui/{os.getuid()}"
    run_quiet(["/bin/launchctl", "bootout", domain, str(store.launch_agent_path)])
    code, output = run_quiet(["/bin/launchctl", "bootstrap", domain, str(store.launch_agent_path)])
    if code != 0:
        raise SwitchError(f"launchctl bootstrap failed: {output}")
    return store.launch_agent_path


def read_launch_agent_cli_path(path: Path) -> str:
    if not path.exists():
        return ""
    try:
        payload = plistlib.loads(path.read_bytes())
    except Exception as exc:
        return f"<invalid plist: {exc}>"
    args = payload.get("ProgramArguments", [])
    if (
        isinstance(args, list)
        and len(args) >= 4
        and args[1] == "setenv"
        and args[2] == APP_CLI_ENV
    ):
        return str(args[3])
    return "<not managed by codex-switch>"
