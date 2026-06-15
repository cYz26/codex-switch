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
        validate_toml_text(path.read_text(), str(path))
        return
    try:
        tomllib.loads(path.read_text())
    except Exception as exc:  # tomllib.TOMLDecodeError only exists when imported
        raise SwitchError(f"Invalid TOML: {path}: {exc}") from exc


def validate_toml_text(text: str, label: str) -> None:
    if tomllib is None:
        validate_toml_text_basic(text, label)
        return
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


def scan_line_structure(
    line: str,
    *,
    bracket_depth: int,
    brace_depth: int,
) -> tuple[int, int]:
    quote: str | None = None
    escaped = False
    for char in line:
        if quote is None and char == "#":
            break
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
            continue
        if quote is not None:
            continue
        if char == "[":
            bracket_depth += 1
        elif char == "]":
            bracket_depth -= 1
        elif char == "{":
            brace_depth += 1
        elif char == "}":
            brace_depth -= 1
        if bracket_depth < 0 or brace_depth < 0:
            raise ValueError("unbalanced closing delimiter")
    if quote is not None:
        raise ValueError("unterminated string")
    return bracket_depth, brace_depth


def table_name_from_header(line: str) -> str | None:
    stripped = line.strip()
    if stripped.startswith("[[") and stripped.endswith("]]"):
        return None
    if stripped.startswith("[") and stripped.endswith("]"):
        return stripped[1:-1].strip()
    if stripped.startswith("["):
        raise ValueError("invalid table header")
    return None


def validate_toml_text_basic(text: str, label: str) -> None:
    current_table = ""
    regular_tables: set[str] = set()
    assignments_by_table: dict[str, set[str]] = {"": set()}
    bracket_depth = 0
    brace_depth = 0
    line_number = 0

    try:
        for line_number, line in enumerate(text.splitlines(), start=1):
            parse_assignments = bracket_depth == 0 and brace_depth == 0
            bare = commentless_line(line).strip()
            bracket_depth, brace_depth = scan_line_structure(
                line,
                bracket_depth=bracket_depth,
                brace_depth=brace_depth,
            )
            if not bare:
                continue
            if parse_assignments:
                if bare.startswith("[[") and bare.endswith("]]"):
                    table = bare[2:-2].strip()
                    if not table:
                        raise ValueError("empty array table header")
                    current_table = f"{table}[]:{line_number}"
                    assignments_by_table.setdefault(current_table, set())
                    continue
                table_name = table_name_from_header(bare)
                if table_name is not None:
                    if table_name in regular_tables:
                        raise ValueError(f"duplicate table [{table_name}]")
                    regular_tables.add(table_name)
                    current_table = table_name
                    assignments_by_table.setdefault(current_table, set())
                    continue
                if bare.startswith("["):
                    table_name_from_header(bare)
                if "=" in bare:
                    key = bare.split("=", 1)[0].strip()
                    if not key:
                        raise ValueError("empty assignment key")
                    table_assignments = assignments_by_table.setdefault(current_table, set())
                    if key in table_assignments:
                        raise ValueError(f"duplicate key {key!r}")
                    table_assignments.add(key)
        if bracket_depth != 0 or brace_depth != 0:
            raise ValueError("unclosed array or inline table")
    except ValueError as exc:
        raise SwitchError(
            f"Invalid TOML after updating {label}: line {line_number}: {exc}"
        ) from exc
