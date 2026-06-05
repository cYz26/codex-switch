from __future__ import annotations


def toml_table_name(line: str) -> str | None:
    stripped = line.strip()
    if not stripped.startswith("["):
        return None
    if stripped.startswith("[["):
        end = stripped.find("]]")
        if end == -1:
            return None
        return stripped[2:end].strip()
    end = stripped.find("]")
    if end == -1:
        return None
    return stripped[1:end].strip()


def first_table_index(lines: list[str]) -> int:
    for index, line in enumerate(lines):
        if toml_table_name(line):
            return index
    return len(lines)


def has_toml_table(text: str, table_name: str) -> bool:
    return any(toml_table_name(line) == table_name for line in text.splitlines())


def extract_toml_table_block(text: str, table_name: str) -> str:
    lines = text.splitlines()
    start = None
    for index, line in enumerate(lines):
        if toml_table_name(line) == table_name:
            start = index
            break
    if start is None:
        return ""

    end = len(lines)
    nested_prefix = f"{table_name}."
    for index in range(start + 1, len(lines)):
        current_table = toml_table_name(lines[index])
        if (
            current_table
            and current_table != table_name
            and not current_table.startswith(nested_prefix)
        ):
            end = index
            break
    return "\n".join(lines[start:end]).rstrip() + "\n"
