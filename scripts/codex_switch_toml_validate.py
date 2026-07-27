from __future__ import annotations

from pathlib import Path

from codex_switch_constants import SwitchError

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]


def validate_toml(path: Path) -> None:
    if not path.exists():
        return
    if tomllib is None:
        raise SwitchError(
            f"Python 3.11+ with tomllib is required to validate {path}"
        )
    try:
        tomllib.loads(path.read_text())
    except Exception as exc:  # tomllib.TOMLDecodeError only exists when imported
        raise SwitchError(f"Invalid TOML: {path}: {exc}") from exc


def validate_toml_text(text: str, label: str) -> None:
    if tomllib is None:
        raise SwitchError(
            f"Python 3.11+ with tomllib is required to validate {label}"
        )
    try:
        tomllib.loads(text)
    except Exception as exc:  # tomllib.TOMLDecodeError only exists when imported
        raise SwitchError(f"Invalid TOML after updating {label}: {exc}") from exc


def commentless_line(line: str) -> str:
    quote: str | None = None
    escaped = False
    result: list[str] = []
    for char in line:
        if quote is None and char == "#":
            break
        result.append(char)
        if escaped:
            escaped = False
            continue
        if quote == '"' and char == "\\":
            escaped = True
            continue
        if char in {"'", '"'}:
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
    return "".join(result)
