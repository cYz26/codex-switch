from __future__ import annotations

import json
import math
from collections import Counter
from collections.abc import Callable, Mapping
from dataclasses import dataclass
from typing import Any

from codex_switch_constants import SwitchError

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - exercised on Python 3.9
    tomllib = None  # type: ignore[assignment]


_KEY_SENTINEL = "codex-switch-config-document-key"


@dataclass(frozen=True)
class AssignmentSpan:
    path: tuple[str, ...]
    table_path: tuple[str, ...]
    statement_start: int
    statement_end: int
    statement_text: str
    value_start: int
    value_end: int
    value_text: str
    semantic_value: Any
    array_table_path: tuple[str, ...] | None = None
    array_index: int | None = None

    @property
    def identity(
        self,
    ) -> tuple[tuple[str, ...], tuple[str, ...] | None, int | None]:
        return self.path, self.array_table_path, self.array_index


@dataclass(frozen=True)
class TableSpan:
    path: tuple[str, ...]
    header_start: int
    header_end: int
    end: int
    text: str
    is_array: bool
    array_index: int | None = None


@dataclass(frozen=True)
class RecoveryDiagnostic:
    code: str
    path: tuple[str, ...]
    message: str


@dataclass(frozen=True)
class RecoveryResult:
    document: "ConfigDocument"
    restored_paths: tuple[tuple[str, ...], ...]
    diagnostics: tuple[RecoveryDiagnostic, ...]

    @property
    def text(self) -> str:
        return self.document.text


@dataclass(frozen=True)
class _Insertion:
    position: int
    source_order: int
    text: str
    is_table: bool


@dataclass(frozen=True)
class ConfigDocument:
    text: str
    label: str
    data: Mapping[str, Any]
    assignments: tuple[AssignmentSpan, ...]
    tables: tuple[TableSpan, ...]

    @classmethod
    def parse(cls, text: str, label: str) -> "ConfigDocument":
        parser = _require_tomllib(label)
        try:
            data = parser.loads(text)
        except parser.TOMLDecodeError as exc:
            raise SwitchError(f"Invalid TOML for {label}: {exc}") from exc
        try:
            assignments, tables = _scan_document(text, data)
        except ValueError as exc:
            raise SwitchError(
                f"Unable to locate complete TOML value spans for {label}: {exc}"
            ) from exc
        return cls(
            text=text,
            label=label,
            data=data,
            assignments=tuple(assignments),
            tables=tuple(tables),
        )

    @property
    def assignment_paths(self) -> tuple[tuple[str, ...], ...]:
        return tuple(assignment.path for assignment in self.assignments)

    def replace_values_from(self, overlay: "ConfigDocument") -> "ConfigDocument":
        current = _unique_regular_assignments(self.assignments)
        incoming = _unique_regular_assignments(overlay.assignments)
        replacements: list[tuple[int, int, str]] = []

        for identity, assignment in current.items():
            replacement = incoming.get(identity)
            if replacement is None or _semantic_equal(
                assignment.semantic_value,
                replacement.semantic_value,
            ):
                continue
            replacements.append(
                (
                    assignment.value_start,
                    assignment.value_end,
                    replacement.value_text,
                )
            )

        if not replacements:
            return self

        updated = self.text
        for start, end, replacement_text in sorted(replacements, reverse=True):
            updated = updated[:start] + replacement_text + updated[end:]
        return ConfigDocument.parse(
            updated,
            f"{self.label} with {overlay.label} overlay",
        )

    def remove_exact_scalar_assignment(
        self,
        *,
        path: tuple[str, ...],
        table_path: tuple[str, ...],
        label: str,
    ) -> "ConfigDocument":
        matches = [
            assignment
            for assignment in self.assignments
            if assignment.path == path
        ]
        if not matches:
            if _mapping_path_exists(self.data, path):
                raise SwitchError(
                    "config_exact_assignment_ambiguous: "
                    f"{'.'.join(path)} in {self.label} is not one exact "
                    "scalar table assignment"
                )
            return self
        if (
            len(matches) != 1
            or matches[0].array_table_path is not None
            or matches[0].table_path != table_path
            or isinstance(matches[0].semantic_value, (Mapping, list))
        ):
            raise SwitchError(
                "config_exact_assignment_ambiguous: "
                f"{'.'.join(path)} in {self.label} is not one exact "
                "scalar table assignment"
            )
        assignment = matches[0]
        updated = (
            self.text[: assignment.statement_start]
            + self.text[assignment.statement_end :]
        )
        return ConfigDocument.parse(updated, label)

    def select(
        self,
        *,
        include_top_level: Callable[[tuple[str, ...]], bool],
        include_table: Callable[[tuple[str, ...], bool], bool],
        label: str,
    ) -> "ConfigDocument":
        removals: list[tuple[int, int]] = []
        for assignment in self.assignments:
            if not assignment.table_path and not include_top_level(assignment.path):
                removals.append(
                    (assignment.statement_start, assignment.statement_end)
                )
        for table in self.tables:
            if not include_table(table.path, table.is_array):
                removals.append((table.header_start, table.end))
        if not removals:
            return self

        selected = self.text
        for start, end in sorted(removals, reverse=True):
            selected = selected[:start] + selected[end:]
        return ConfigDocument.parse(selected, label)

    def recover_missing_from(
        self,
        snapshot: "ConfigDocument",
        *,
        protected_paths: frozenset[tuple[str, ...]],
    ) -> RecoveryResult:
        diagnostics: list[RecoveryDiagnostic] = []
        restored_paths: list[tuple[str, ...]] = []
        insertions: list[_Insertion] = []

        current_skill_state = _skill_identity_state(self)
        snapshot_skill_state = _skill_identity_state(snapshot)
        diagnostics.extend(current_skill_state.diagnostics)
        diagnostics.extend(snapshot_skill_state.diagnostics)

        current_regular_paths = {
            assignment.path
            for assignment in self.assignments
            if assignment.array_table_path is None
        }
        current_regular_tables = {
            table.path: table for table in self.tables if not table.is_array
        }
        first_table_start = (
            self.tables[0].header_start if self.tables else len(self.text)
        )

        for assignment in snapshot.assignments:
            if assignment.table_path or assignment.array_table_path is not None:
                continue
            if (
                assignment.path in current_regular_paths
                or _path_is_protected(assignment.path, protected_paths)
            ):
                continue
            insertions.append(
                _Insertion(
                    position=first_table_start,
                    source_order=assignment.statement_start,
                    text=assignment.statement_text,
                    is_table=False,
                )
            )
            current_regular_paths.add(assignment.path)
            restored_paths.append(assignment.path)

        for table in snapshot.tables:
            if table.is_array:
                if table.path == ("skills", "config"):
                    identity = snapshot_skill_state.identities_by_index.get(
                        table.array_index
                    )
                    if identity is None:
                        continue
                    logical_path = ("skills", "config", identity)
                    if (
                        identity in current_skill_state.seen_identities
                        or _path_is_protected(logical_path, protected_paths)
                    ):
                        continue
                    insertions.append(
                        _Insertion(
                            position=len(self.text),
                            source_order=table.header_start,
                            text=table.text,
                            is_table=True,
                        )
                    )
                    current_skill_state.seen_identities.add(identity)
                    restored_paths.append(logical_path)
                    continue
                diagnostics.append(
                    RecoveryDiagnostic(
                        code="unknown_array_table",
                        path=table.path,
                        message=(
                            "Skipped unsupported array table "
                            f"[[{'.'.join(table.path)}]] from {snapshot.label}"
                        ),
                    )
                )
                continue

            if _path_is_protected(table.path, protected_paths):
                continue
            current_table = current_regular_tables.get(table.path)
            if current_table is None:
                insertions.append(
                    _Insertion(
                        position=len(self.text),
                        source_order=table.header_start,
                        text=table.text,
                        is_table=True,
                    )
                )
                current_regular_tables[table.path] = table
                restored_paths.append(table.path)
                continue

            for assignment in snapshot.assignments:
                if (
                    assignment.array_table_path is not None
                    or assignment.table_path != table.path
                    or assignment.path in current_regular_paths
                    or _path_is_protected(assignment.path, protected_paths)
                ):
                    continue
                insertions.append(
                    _Insertion(
                        position=current_table.end,
                        source_order=assignment.statement_start,
                        text=assignment.statement_text,
                        is_table=False,
                    )
                )
                current_regular_paths.add(assignment.path)
                restored_paths.append(assignment.path)

        if not insertions:
            return RecoveryResult(
                document=self,
                restored_paths=tuple(restored_paths),
                diagnostics=tuple(diagnostics),
            )

        recovered_text = _apply_insertions(self.text, insertions)
        recovered = ConfigDocument.parse(
            recovered_text,
            f"{self.label} recovered from {snapshot.label}",
        )
        return RecoveryResult(
            document=recovered,
            restored_paths=tuple(restored_paths),
            diagnostics=tuple(diagnostics),
        )


def _require_tomllib(label: str):
    if tomllib is None:
        raise SwitchError(
            f"Python 3.11+ with tomllib is required to parse {label}"
        )
    return tomllib


def _unique_regular_assignments(
    assignments: tuple[AssignmentSpan, ...],
) -> dict[tuple[tuple[str, ...], tuple[str, ...] | None, int | None], AssignmentSpan]:
    grouped: dict[
        tuple[tuple[str, ...], tuple[str, ...] | None, int | None],
        list[AssignmentSpan],
    ] = {}
    for assignment in assignments:
        if assignment.array_table_path is not None:
            continue
        grouped.setdefault(assignment.identity, []).append(assignment)
    return {
        identity: matches[0]
        for identity, matches in grouped.items()
        if len(matches) == 1
    }


def _semantic_equal(left: Any, right: Any) -> bool:
    if type(left) is not type(right):
        return False
    if isinstance(left, Mapping):
        return left.keys() == right.keys() and all(
            _semantic_equal(left[key], right[key]) for key in left
        )
    if isinstance(left, list):
        return len(left) == len(right) and all(
            _semantic_equal(left_item, right_item)
            for left_item, right_item in zip(left, right)
        )
    if isinstance(left, float) and math.isnan(left) and math.isnan(right):
        return True
    return left == right


def _mapping_path_exists(
    data: Mapping[str, Any],
    path: tuple[str, ...],
) -> bool:
    current: Any = data
    for part in path:
        if not isinstance(current, Mapping) or part not in current:
            return False
        current = current[part]
    return True


def _scan_document(
    text: str,
    data: Mapping[str, Any],
) -> tuple[list[AssignmentSpan], list[TableSpan]]:
    assignments: list[AssignmentSpan] = []
    tables: list[TableSpan] = []
    current_table: tuple[str, ...] = ()
    current_array_table: tuple[str, ...] | None = None
    current_array_index: int | None = None
    array_counts: dict[tuple[str, ...], int] = {}
    open_table: tuple[
        tuple[str, ...],
        int,
        int,
        bool,
        int | None,
    ] | None = None
    index = 0

    while True:
        index = _skip_space_and_comments(text, index)
        if index >= len(text):
            break

        if text[index] == "[":
            header_start = _line_start(text, index)
            if open_table is not None:
                _append_table_span(tables, text, open_table, header_start)
            header_end = _line_code_end(text, index)
            header = text[index:header_end].rstrip()
            is_array = header.startswith("[[")
            closing = "]]" if is_array else "]"
            opening_length = 2 if is_array else 1
            if not header.endswith(closing):
                raise ValueError("invalid table header")
            inner = header[opening_length : -len(closing)].strip()
            current_table = _decode_key_path(inner)
            if is_array:
                current_array_table = current_table
                current_array_index = array_counts.get(current_table, 0)
                array_counts[current_table] = current_array_index + 1
            elif not (
                current_array_table
                and current_table[: len(current_array_table)] == current_array_table
            ):
                current_array_table = None
                current_array_index = None
            index = _after_line(text, header_end)
            open_table = (
                current_table,
                header_start,
                index,
                is_array,
                current_array_index if is_array else None,
            )
            continue

        equals_index = _find_assignment_equals(text, index)
        key_source = text[index:equals_index].strip()
        if not key_source:
            raise ValueError("empty assignment key")
        local_path = _decode_key_path(key_source)
        path = current_table + local_path
        statement_start = _line_start(text, index)
        value_start = equals_index + 1
        while value_start < len(text) and text[value_start] in " \t":
            value_start += 1
        value_end, statement_end = _scan_value(text, value_start)
        assignments.append(
            AssignmentSpan(
                path=path,
                table_path=current_table,
                statement_start=statement_start,
                statement_end=statement_end,
                statement_text=text[statement_start:statement_end],
                value_start=value_start,
                value_end=value_end,
                value_text=text[value_start:value_end],
                semantic_value=_semantic_value(
                    data,
                    path,
                    current_array_table,
                    current_array_index,
                ),
                array_table_path=current_array_table,
                array_index=current_array_index,
            )
        )
        index = statement_end

    if open_table is not None:
        _append_table_span(tables, text, open_table, len(text))
    return assignments, tables


def _append_table_span(
    tables: list[TableSpan],
    text: str,
    table: tuple[tuple[str, ...], int, int, bool, int | None],
    end: int,
) -> None:
    path, header_start, header_end, is_array, array_index = table
    tables.append(
        TableSpan(
            path=path,
            header_start=header_start,
            header_end=header_end,
            end=end,
            text=text[header_start:end],
            is_array=is_array,
            array_index=array_index,
        )
    )


def _line_start(text: str, index: int) -> int:
    newline = text.rfind("\n", 0, index)
    return 0 if newline == -1 else newline + 1


def _skip_space_and_comments(text: str, index: int) -> int:
    while index < len(text):
        if text[index] in " \t\r\n":
            index += 1
            continue
        if text[index] == "#":
            index = _after_line(text, index)
            continue
        return index
    return index


def _line_code_end(text: str, index: int) -> int:
    quote: str | None = None
    escaped = False
    while index < len(text):
        char = text[index]
        if char in "\r\n":
            return index
        if quote is None and char == "#":
            return index
        if escaped:
            escaped = False
            index += 1
            continue
        if quote == '"' and char == "\\":
            escaped = True
            index += 1
            continue
        if char in {"'", '"'}:
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
        index += 1
    return index


def _after_line(text: str, index: int) -> int:
    while index < len(text) and text[index] not in "\r\n":
        index += 1
    if index < len(text) and text[index] == "\r":
        index += 1
        if index < len(text) and text[index] == "\n":
            index += 1
    elif index < len(text):
        index += 1
    return index


def _find_assignment_equals(text: str, index: int) -> int:
    quote: str | None = None
    escaped = False
    while index < len(text):
        char = text[index]
        if char in "\r\n" or (quote is None and char == "#"):
            raise ValueError("assignment is missing '='")
        if escaped:
            escaped = False
            index += 1
            continue
        if quote == '"' and char == "\\":
            escaped = True
            index += 1
            continue
        if char in {"'", '"'}:
            if quote == char:
                quote = None
            elif quote is None:
                quote = char
            index += 1
            continue
        if quote is None and char == "=":
            return index
        index += 1
    raise ValueError("assignment is missing '='")


def _scan_value(text: str, start: int) -> tuple[int, int]:
    if start >= len(text) or text[start] in "\r\n#":
        raise ValueError("assignment is missing a value")

    index = start
    bracket_depth = 0
    brace_depth = 0
    string_delimiter: str | None = None
    multiline = False

    while index < len(text):
        if string_delimiter is not None:
            quote = string_delimiter[0]
            if multiline:
                if quote == '"' and text[index] == "\\":
                    index += 1
                    if index < len(text):
                        index += 1
                    continue
                if text[index] == quote:
                    run_end = index
                    while run_end < len(text) and text[run_end] == quote:
                        run_end += 1
                    if run_end - index >= 3:
                        index = run_end
                        string_delimiter = None
                        multiline = False
                        continue
                    index = run_end
                    continue
                index += 1
                continue

            if quote == '"' and text[index] == "\\":
                index += 1
                if index < len(text):
                    index += 1
                continue
            if text[index] == quote:
                index += 1
                string_delimiter = None
                continue
            index += 1
            continue

        if text.startswith('"""', index):
            string_delimiter = '"""'
            multiline = True
            index += 3
            continue
        if text.startswith("'''", index):
            string_delimiter = "'''"
            multiline = True
            index += 3
            continue

        char = text[index]
        if char in {"'", '"'}:
            string_delimiter = char
            index += 1
            continue
        if char == "[":
            bracket_depth += 1
            index += 1
            continue
        if char == "]":
            bracket_depth -= 1
            if bracket_depth < 0:
                raise ValueError("unbalanced closing array delimiter")
            index += 1
            continue
        if char == "{":
            brace_depth += 1
            index += 1
            continue
        if char == "}":
            brace_depth -= 1
            if brace_depth < 0:
                raise ValueError("unbalanced closing inline-table delimiter")
            index += 1
            continue
        if char == "#":
            if bracket_depth or brace_depth:
                index = _after_line(text, index)
                continue
            return _trim_horizontal_space(text, start, index), _after_line(text, index)
        if char in "\r\n":
            if bracket_depth or brace_depth:
                index = _consume_newline(text, index)
                continue
            return _trim_horizontal_space(text, start, index), _consume_newline(
                text,
                index,
            )
        index += 1

    if string_delimiter is not None or bracket_depth or brace_depth:
        raise ValueError("unterminated assignment value")
    return _trim_horizontal_space(text, start, len(text)), len(text)


def _consume_newline(text: str, index: int) -> int:
    if text[index] == "\r":
        index += 1
        if index < len(text) and text[index] == "\n":
            index += 1
        return index
    return index + 1


def _trim_horizontal_space(text: str, start: int, end: int) -> int:
    while end > start and text[end - 1] in " \t":
        end -= 1
    return end


def _decode_key_path(source: str) -> tuple[str, ...]:
    if not source:
        raise ValueError("empty TOML key path")
    parser = _require_tomllib("TOML key path")
    payload = parser.loads(
        f"{source} = {json.dumps(_KEY_SENTINEL)}"
    )
    path = _find_value_path(payload, _KEY_SENTINEL)
    if path is None:
        raise ValueError(f"unable to decode TOML key path {source!r}")
    return path


def _find_value_path(value: Any, target: str) -> tuple[str, ...] | None:
    if not isinstance(value, Mapping):
        return () if value == target else None
    for key, child in value.items():
        suffix = _find_value_path(child, target)
        if suffix is not None:
            return (key, *suffix)
    return None


def _semantic_value(
    data: Mapping[str, Any],
    path: tuple[str, ...],
    array_table_path: tuple[str, ...] | None,
    array_index: int | None,
) -> Any:
    current: Any = data
    prefix: tuple[str, ...] = ()
    for part in path:
        if not isinstance(current, Mapping) or part not in current:
            raise ValueError(f"semantic path is missing: {'.'.join(path)}")
        current = current[part]
        prefix = (*prefix, part)
        if array_table_path == prefix:
            if (
                not isinstance(current, list)
                or array_index is None
                or array_index >= len(current)
            ):
                raise ValueError(f"array-table path is missing: {'.'.join(path)}")
            current = current[array_index]
    return current


@dataclass
class _SkillIdentityState:
    identities_by_index: dict[int | None, str]
    seen_identities: set[str]
    diagnostics: list[RecoveryDiagnostic]


def _skill_identity_state(document: ConfigDocument) -> _SkillIdentityState:
    skill_tables = [
        table
        for table in document.tables
        if table.is_array and table.path == ("skills", "config")
    ]
    raw_identities: dict[int | None, str] = {}
    diagnostics: list[RecoveryDiagnostic] = []

    for table in skill_tables:
        identity_assignments = [
            assignment
            for assignment in document.assignments
            if assignment.array_table_path == ("skills", "config")
            and assignment.array_index == table.array_index
            and assignment.path == ("skills", "config", "path")
        ]
        if not identity_assignments:
            diagnostics.append(
                RecoveryDiagnostic(
                    code="skills_config_missing_identity",
                    path=("skills", "config"),
                    message=(
                        "Skipped [[skills.config]] without path in "
                        f"{document.label}"
                    ),
                )
            )
            continue
        identity = identity_assignments[0].semantic_value
        if not isinstance(identity, str):
            diagnostics.append(
                RecoveryDiagnostic(
                    code="skills_config_non_string_identity",
                    path=("skills", "config", "path"),
                    message=(
                        "Skipped [[skills.config]] with non-string path in "
                        f"{document.label}"
                    ),
                )
            )
            continue
        raw_identities[table.array_index] = identity

    counts = Counter(raw_identities.values())
    duplicate_identities = {
        identity for identity, count in counts.items() if count > 1
    }
    for identity in sorted(duplicate_identities):
        diagnostics.append(
            RecoveryDiagnostic(
                code="skills_config_duplicate_identity",
                path=("skills", "config", identity),
                message=(
                    "Skipped duplicate [[skills.config]] path "
                    f"{identity!r} in {document.label}"
                ),
            )
        )

    return _SkillIdentityState(
        identities_by_index={
            index: identity
            for index, identity in raw_identities.items()
            if identity not in duplicate_identities
        },
        seen_identities=set(raw_identities.values()),
        diagnostics=diagnostics,
    )


def _path_is_protected(
    candidate: tuple[str, ...],
    protected_paths: frozenset[tuple[str, ...]],
) -> bool:
    return any(
        _is_prefix(candidate, protected) or _is_prefix(protected, candidate)
        for protected in protected_paths
    )


def _is_prefix(
    prefix: tuple[str, ...],
    path: tuple[str, ...],
) -> bool:
    return len(prefix) <= len(path) and path[: len(prefix)] == prefix


def _apply_insertions(text: str, insertions: list[_Insertion]) -> str:
    newline = "\r\n" if "\r\n" in text else "\n"
    grouped: dict[int, list[_Insertion]] = {}
    for insertion in insertions:
        grouped.setdefault(insertion.position, []).append(insertion)

    updated = text
    for position in sorted(grouped, reverse=True):
        ordered = sorted(
            grouped[position],
            key=lambda insertion: insertion.source_order,
        )
        payload = _join_insertion_payloads(ordered, newline)
        payload = _fit_insertion_boundaries(
            updated,
            position,
            payload,
            newline,
            starts_with_table=ordered[0].is_table,
            ends_with_table=ordered[-1].is_table,
        )
        updated = updated[:position] + payload + updated[position:]
    return updated


def _join_insertion_payloads(
    insertions: list[_Insertion],
    newline: str,
) -> str:
    payload = ""
    previous_was_table = False
    for insertion in insertions:
        piece = insertion.text
        if payload:
            separator_count = 2 if previous_was_table or insertion.is_table else 1
            payload = payload.rstrip("\r\n")
            piece = piece.lstrip("\r\n")
            payload += newline * separator_count
        payload += piece
        previous_was_table = insertion.is_table
    return payload


def _fit_insertion_boundaries(
    text: str,
    position: int,
    payload: str,
    newline: str,
    *,
    starts_with_table: bool,
    ends_with_table: bool,
) -> str:
    before = text[:position]
    after = text[position:]
    leading_required = 2 if starts_with_table and before else 1 if before else 0
    trailing_required = (
        2
        if ends_with_table and after
        else 1
        if after
        else 0
    )
    leading_count = _trailing_newline_count(before, newline)
    trailing_count = _leading_newline_count(after, newline)
    payload = (
        newline * max(0, leading_required - leading_count)
        + payload.lstrip("\r\n")
    )
    payload = payload.rstrip("\r\n") + newline * max(
        1 if payload else 0,
        trailing_required,
    )
    if trailing_required and trailing_count:
        payload = payload.rstrip("\r\n") + newline * max(
            0,
            trailing_required - trailing_count,
        )
    return payload


def _trailing_newline_count(text: str, newline: str) -> int:
    count = 0
    while text.endswith(newline * (count + 1)):
        count += 1
    return count


def _leading_newline_count(text: str, newline: str) -> int:
    count = 0
    while text.startswith(newline * (count + 1)):
        count += 1
    return count
