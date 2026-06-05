from __future__ import annotations

from pathlib import Path

from codex_switch_constants import SwitchError

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]


def validate_toml(path: Path) -> None:
    if tomllib is None or not path.exists():
        return
    try:
        tomllib.loads(path.read_text())
    except Exception as exc:  # tomllib.TOMLDecodeError only exists when imported
        raise SwitchError(f"Invalid TOML: {path}: {exc}") from exc


def validate_toml_text(text: str, label: str) -> None:
    if tomllib is None:
        return
    try:
        tomllib.loads(text)
    except Exception as exc:  # tomllib.TOMLDecodeError only exists when imported
        raise SwitchError(f"Invalid TOML after updating {label}: {exc}") from exc
