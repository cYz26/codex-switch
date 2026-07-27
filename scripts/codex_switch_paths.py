from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from codex_switch_constants import APP_CLI_ENV, SwitchError
from codex_switch_io import expand_path, run_quiet


def resolve_codex_bin(raw: str | None) -> str:
    if raw:
        return str(expand_path(raw, Path(raw)))
    found = shutil.which("codex")
    return found or ""


def resolve_internal_codex_bin(raw: str | None) -> str:
    if not raw:
        raise SwitchError(
            "Internal codex_bin does not resolve to a regular executable: "
            "<missing>"
        )
    discovered = resolve_codex_bin(raw)
    if not discovered:
        raise SwitchError(
            "Internal codex_bin does not resolve to a regular executable: "
            f"{raw or '<missing>'}"
        )
    path = Path(discovered).expanduser()
    try:
        backend = path.resolve(strict=True)
    except OSError as exc:
        raise SwitchError(
            f"Internal codex_bin does not resolve to a regular executable: {path}"
        ) from exc
    if not backend.is_file() or not os.access(backend, os.X_OK):
        raise SwitchError(
            f"Internal codex_bin does not resolve to a regular executable: {path}"
        )
    return str(backend)


def resolve_path(raw: str | None) -> str:
    if not raw:
        return ""
    return str(expand_path(raw, Path(raw)))


def get_launchctl_env(name: str) -> str:
    code, output = run_quiet(["/bin/launchctl", "getenv", name])
    if code != 0:
        return ""
    return output.strip()


def detect_current_app_cli_path(fallback: str = "") -> str:
    return get_launchctl_env(APP_CLI_ENV) or os.environ.get(APP_CLI_ENV, "") or fallback


def profile_app_cli_path(manifest: dict[str, Any]) -> str:
    return str(manifest.get("app_cli_path") or manifest.get("codex_bin") or "")


def equivalent_paths(left: str, right: str) -> bool:
    if not left or not right:
        return False
    left_path = Path(left).expanduser()
    right_path = Path(right).expanduser()
    try:
        return left_path.resolve() == right_path.resolve()
    except OSError:
        return str(left_path) == str(right_path)
