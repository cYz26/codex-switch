from __future__ import annotations

import re

from codex_switch_toml_scan import first_table_index


def top_level_assignment(text: str, key: str) -> str | None:
    lines = text.splitlines()
    assignment_re = re.compile(rf"^\s*{re.escape(key)}\s*=")
    for line in lines[: first_table_index(lines)]:
        if assignment_re.match(line):
            return line.strip()
    return None


def upsert_top_level_assignment(text: str, key: str, assignment: str) -> str:
    lines = text.splitlines()
    table_index = first_table_index(lines)
    assignment_re = re.compile(rf"^\s*{re.escape(key)}\s*=")
    for index in range(table_index):
        if assignment_re.match(lines[index]):
            lines[index] = assignment
            return "\n".join(lines).rstrip() + "\n"

    insert_at = table_index
    if key != "profile":
        for index in range(table_index):
            if re.match(r"^\s*profile\s*=", lines[index]):
                insert_at = index + 1
                break
    lines.insert(insert_at, assignment)
    return "\n".join(lines).rstrip() + "\n"


def append_toml_block(text: str, block: str) -> str:
    prefix = text.rstrip()
    suffix = block.strip()
    if not prefix:
        return suffix + "\n"
    return f"{prefix}\n\n{suffix}\n"
