from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import tempfile
from pathlib import Path
from typing import Any

from codex_switch_constants import SwitchError

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]


def expand_path(raw: str | None, default: Path) -> Path:
    if raw is None or raw.strip() == "":
        return default.expanduser()
    return Path(os.path.expandvars(raw)).expanduser()


def now_stamp() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def ensure_private_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    try:
        path.chmod(0o700)
    except PermissionError:
        pass


def atomic_write(path: Path, data: bytes, mode: int | None = None) -> None:
    if not path.parent.exists():
        ensure_private_dir(path.parent)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
            tmp.flush()
            if mode is not None:
                os.fchmod(tmp.fileno(), mode)
            os.fsync(tmp.fileno())
        os.replace(tmp_path, path)
        parent_descriptor = os.open(
            path.parent,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            os.fsync(parent_descriptor)
        finally:
            os.close(parent_descriptor)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()


def copy_file_atomic(src: Path, dst: Path, mode: int | None = None) -> None:
    atomic_write(dst, src.read_bytes(), mode=mode)


def run_quiet(command: list[str], env: dict[str, str] | None = None) -> tuple[int, str]:
    try:
        result = subprocess.run(
            command,
            check=False,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env=env,
        )
    except FileNotFoundError:
        return 127, f"not found: {command[0]}"
    return result.returncode, result.stdout.strip()


def read_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        raise SwitchError(f"Invalid JSON: {path}: {exc}") from exc


def write_json(path: Path, data: dict[str, Any], mode: int = 0o600) -> None:
    payload = json.dumps(data, indent=2, sort_keys=True).encode() + b"\n"
    atomic_write(path, payload, mode=mode)
