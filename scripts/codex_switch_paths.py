from __future__ import annotations

import os
import shutil
from pathlib import Path
from typing import Any

from codex_switch_constants import APP_CLI_ENV, DEFAULT_APP_BUNDLE_CODEX
from codex_switch_io import expand_path, run_quiet


def resolve_codex_bin(raw: str | None) -> str:
    if raw:
        return str(expand_path(raw, Path(raw)))
    found = shutil.which("codex")
    return found or ""


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


def resolve_official_app_cli_path(raw: str | None, fallback: str = "") -> str:
    if raw:
        return resolve_path(raw)
    if DEFAULT_APP_BUNDLE_CODEX.exists():
        return str(DEFAULT_APP_BUNDLE_CODEX)
    return fallback or resolve_codex_bin(None)


def resolve_official_codex_bin(raw: str | None, app_cli_path: str) -> str:
    if raw:
        return resolve_codex_bin(raw)
    return app_cli_path or resolve_codex_bin(None)


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
