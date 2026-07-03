from __future__ import annotations

from pathlib import Path

from codex_switch_constants import PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE
from codex_switch_toml_edit import (
    append_toml_block,
    top_level_assignment,
    upsert_top_level_assignment,
)
from codex_switch_toml_scan import (
    extract_toml_table_block,
    first_table_index,
    toml_table_name,
)
from codex_switch_toml_validate import validate_toml_text
from codex_switch_toml_validate import commentless_line

PROFILE_TABLE_PREFIXES = (
    "model_providers.",
    "profiles.",
)
PRESERVED_SHARED_TABLES = (
    "skills.config",
)
PRESERVED_SHARED_TABLE_PREFIXES = (
    "marketplaces.",
    "plugins.",
    "hooks.state.",
)


def is_profile_specific_table(table_name: str) -> bool:
    return table_name == "model_providers" or table_name == "profiles" or any(
        table_name.startswith(prefix) for prefix in PROFILE_TABLE_PREFIXES
    )


def remove_top_level_assignment(text: str, key: str) -> str:
    kept: list[str] = []
    in_top_level = True
    for line in text.splitlines():
        if toml_table_name(line):
            in_top_level = False
        stripped = line.strip()
        if in_top_level and (stripped.startswith(f"{key} ") or stripped.startswith(f"{key}=")):
            continue
        kept.append(line)
    return "\n".join(kept).rstrip() + "\n"


def remove_legacy_profile_tables(text: str) -> str:
    kept: list[str] = []
    skipping = False
    for line in text.splitlines():
        table = toml_table_name(line)
        if table:
            skipping = table == "profiles" or table.startswith("profiles.")
        if not skipping:
            kept.append(line)
    return "\n".join(kept).rstrip() + "\n"


def remove_toml_table_block(text: str, table_name: str) -> str:
    kept: list[str] = []
    skipping = False
    nested_prefix = f"{table_name}."
    for line in text.splitlines():
        table = toml_table_name(line)
        if table:
            skipping = table == table_name or table.startswith(nested_prefix)
        if not skipping:
            kept.append(line)
    return "\n".join(kept).rstrip() + "\n"


def is_preserved_shared_table(table_name: str) -> bool:
    return table_name in PRESERVED_SHARED_TABLES or any(
        table_name.startswith(prefix) for prefix in PRESERVED_SHARED_TABLE_PREFIXES
    )


def matching_toml_table_blocks(text: str, predicate) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []
    current_matches = False
    for line in text.splitlines():
        table = toml_table_name(line)
        if table:
            if current_matches and current:
                blocks.append("\n".join(current).rstrip() + "\n")
            current = [line]
            current_matches = predicate(table)
            continue
        if current:
            current.append(line)
    if current_matches and current:
        blocks.append("\n".join(current).rstrip() + "\n")
    return blocks


def remove_matching_toml_table_blocks(text: str, predicate) -> str:
    kept: list[str] = []
    skipping = False
    for line in text.splitlines():
        table = toml_table_name(line)
        if table:
            skipping = predicate(table)
        if not skipping:
            kept.append(line)
    return "\n".join(kept).rstrip() + "\n"


def merge_preserved_shared_config_blocks(updated: str, preserve_source_text: str) -> str:
    blocks = matching_toml_table_blocks(preserve_source_text, is_preserved_shared_table)
    if not blocks:
        return updated
    merged = remove_matching_toml_table_blocks(updated, is_preserved_shared_table)
    for block in blocks:
        merged = append_toml_block(merged, block)
    validate_toml_text(merged, "preserved shared config")
    return merged


def top_level_assignments(text: str) -> list[tuple[str, str]]:
    lines = text.splitlines()
    assignments: list[tuple[str, str]] = []
    for line in lines[: first_table_index(lines)]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key = stripped.split("=", 1)[0].strip()
        if key:
            assignments.append((key, stripped))
    return assignments


def merge_toml_table_overlay(updated: str, overlay_text: str, predicate, label: str) -> str:
    overlay_blocks = matching_toml_table_blocks(overlay_text, predicate)
    if not overlay_blocks:
        return updated

    merged_blocks: list[str] = matching_toml_table_blocks(updated, predicate)
    table_indexes: dict[str, int] = {}
    for index, block in enumerate(merged_blocks):
        table = toml_table_name(block.splitlines()[0])
        if table:
            table_indexes[table] = index

    for block in overlay_blocks:
        table = toml_table_name(block.splitlines()[0])
        if not table:
            continue
        if block.lstrip().startswith("[["):
            if block not in merged_blocks:
                merged_blocks.append(block)
            continue
        existing_index = table_indexes.get(table)
        if existing_index is None:
            table_indexes[table] = len(merged_blocks)
            merged_blocks.append(block)
        else:
            merged_blocks[existing_index] = merge_table_assignments_overlay(
                merged_blocks[existing_index],
                block,
            )

    merged = remove_matching_toml_table_blocks(updated, predicate)
    for block in merged_blocks:
        merged = append_toml_block(merged, block)
    validate_toml_text(merged, label)
    return merged


def merge_preserved_shared_config_overlay(updated: str, overlay_text: str) -> str:
    return merge_toml_table_overlay(
        updated,
        overlay_text,
        is_preserved_shared_table,
        "preserved shared config overlay",
    )


def build_preserved_shared_config_text_from_text(text: str, label: str) -> str:
    updated = ""
    for block in matching_toml_table_blocks(text, is_preserved_shared_table):
        updated = append_toml_block(updated, block)
    validate_toml_text(updated, label)
    return updated


def merge_shared_config_overlay(updated: str, overlay_text: str) -> str:
    overlay_shared = build_base_config_text_from_text(overlay_text, "shared config overlay")
    merged = updated
    for key, assignment in top_level_assignments(overlay_shared):
        merged = upsert_top_level_assignment(merged, key, assignment)
    merged = merge_toml_table_overlay(
        merged,
        overlay_shared,
        lambda table: not is_profile_specific_table(table),
        "shared config overlay",
    )
    validate_toml_text(merged, "shared config overlay")
    return merged


def is_array_toml_table_block(block: str) -> bool:
    lines = block.splitlines()
    return bool(lines) and lines[0].strip().startswith("[[")


def table_assignment_lines(block: str) -> list[tuple[str, str]]:
    assignments: list[tuple[str, str]] = []
    for line in block.splitlines()[1:]:
        bare = commentless_line(line).strip()
        if not bare or bare.startswith("[") or "=" not in bare:
            continue
        key = bare.split("=", 1)[0].strip()
        if key:
            assignments.append((key, line.strip()))
    return assignments


def merge_missing_table_assignments(existing_block: str, defaults_block: str) -> str:
    existing_keys = {key for key, _ in table_assignment_lines(existing_block)}
    missing_lines = [
        line
        for key, line in table_assignment_lines(defaults_block)
        if key not in existing_keys
    ]
    if not missing_lines:
        return existing_block
    return f"{existing_block.rstrip()}\n" + "\n".join(missing_lines) + "\n"


def merge_table_assignments_overlay(existing_block: str, overlay_block: str) -> str:
    overlay_assignments = table_assignment_lines(overlay_block)
    if not overlay_assignments:
        return existing_block

    overlay_by_key = {key: line for key, line in overlay_assignments}
    replaced: set[str] = set()
    merged_lines: list[str] = []
    for line in existing_block.splitlines():
        bare = commentless_line(line).strip()
        key = None
        if bare and not bare.startswith("[") and "=" in bare:
            key = bare.split("=", 1)[0].strip()
        if key in overlay_by_key:
            if key not in replaced:
                merged_lines.append(overlay_by_key[key])
                replaced.add(key)
            continue
        merged_lines.append(line)

    for key, line in overlay_assignments:
        if key not in replaced:
            merged_lines.append(line)
            replaced.add(key)

    return "\n".join(merged_lines).rstrip() + "\n"


def merge_missing_shared_config_defaults(updated: str, defaults_text: str) -> str:
    defaults_shared = build_base_config_text_from_text(
        defaults_text,
        "missing shared config defaults",
    )
    merged = updated
    for key, assignment in top_level_assignments(defaults_shared):
        if not top_level_assignment(merged, key):
            merged = upsert_top_level_assignment(merged, key, assignment)

    default_blocks = matching_toml_table_blocks(
        defaults_shared,
        lambda table: not is_profile_specific_table(table),
    )
    for defaults_block in default_blocks:
        table = toml_table_name(defaults_block.splitlines()[0])
        if not table:
            continue
        existing_blocks = matching_toml_table_blocks(merged, lambda name: name == table)
        if is_array_toml_table_block(defaults_block):
            if defaults_block not in existing_blocks:
                merged = append_toml_block(merged, defaults_block)
            continue
        if not existing_blocks:
            merged = append_toml_block(merged, defaults_block)
            continue
        existing_block = existing_blocks[0]
        merged_block = merge_missing_table_assignments(existing_block, defaults_block)
        if merged_block != existing_block:
            merged = merged.replace(existing_block, merged_block, 1)

    validate_toml_text(merged, "missing shared config defaults")
    return merged


def profile_table_assignments(profile_block: str) -> list[tuple[str, str]]:
    assignments: list[tuple[str, str]] = []
    for line in profile_block.splitlines()[1:]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or "=" not in stripped:
            continue
        key = stripped.split("=", 1)[0].strip()
        if key:
            assignments.append((key, stripped))
    return assignments


def target_profile_assignments(
    profile_text: str,
    profile_name: str,
) -> dict[str, str]:
    assignments: dict[str, str] = {}
    for key in PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE:
        assignment = top_level_assignment(profile_text, key)
        if assignment:
            assignments[key] = assignment

    profile_block = extract_toml_table_block(profile_text, f"profiles.{profile_name}")
    for key, assignment in profile_table_assignments(profile_block):
        if key in PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE:
            assignments[key] = assignment
    return assignments


def string_assignment_value(assignment: str) -> str:
    value = assignment.split("=", 1)[1].strip()
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def append_target_model_provider_table(
    updated: str,
    profile_text: str,
    assignments: dict[str, str],
) -> str:
    provider_assignment = assignments.get("model_provider")
    if not provider_assignment:
        return updated
    provider = string_assignment_value(provider_assignment)
    if not provider:
        return updated
    table_name = f"model_providers.{provider}"
    provider_block = extract_toml_table_block(profile_text, table_name)
    if not provider_block:
        return updated
    updated = remove_toml_table_block(updated, table_name)
    return append_toml_block(updated, provider_block)


def build_profile_v2_config_text(profile_name: str, profile_config_path: Path) -> str:
    profile_text = profile_config_path.read_text()
    updated = remove_top_level_assignment(profile_text, "profile")
    updated = remove_legacy_profile_tables(updated)

    assignments = target_profile_assignments(profile_text, profile_name)
    for key, assignment in assignments.items():
        updated = upsert_top_level_assignment(updated, key, assignment)
    updated = append_target_model_provider_table(updated, profile_text, assignments)

    validate_toml_text(updated, str(profile_config_path))
    return updated


def append_model_provider_from_sources(
    updated: str,
    assignments: dict[str, str],
    sources: list[str],
) -> str:
    provider_assignment = assignments.get("model_provider")
    if not provider_assignment:
        return updated
    provider = string_assignment_value(provider_assignment)
    if not provider:
        return updated
    table_name = f"model_providers.{provider}"
    for source in sources:
        provider_block = extract_toml_table_block(source, table_name)
        if provider_block:
            updated = remove_toml_table_block(updated, table_name)
            return append_toml_block(updated, provider_block)
    return updated


def build_profile_seed_config_text(
    profile_name: str,
    profile_text: str,
    label: str,
    fallback_text: str | None = None,
    fallback_keys: set[str] | None = None,
) -> str:
    sources = [profile_text]
    if fallback_text is not None:
        sources.append(fallback_text)

    assignments = target_profile_assignments(profile_text, profile_name)
    if fallback_text is not None:
        fallback_assignments = target_profile_assignments(fallback_text, profile_name)
        for key, assignment in fallback_assignments.items():
            if fallback_keys is None or key in fallback_keys:
                assignments.setdefault(key, assignment)

    updated = ""
    for key in PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE:
        assignment = assignments.get(key)
        if assignment:
            updated = upsert_top_level_assignment(updated, key, assignment)
    updated = append_model_provider_from_sources(updated, assignments, sources)
    validate_toml_text(updated, label)
    return updated


def build_base_config_text_from_text(text: str, label: str) -> str:
    updated = text
    updated = remove_top_level_assignment(updated, "profile")
    updated = remove_legacy_profile_tables(updated)
    for key in PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE:
        updated = remove_top_level_assignment(updated, key)
    updated = remove_matching_toml_table_blocks(
        updated,
        is_profile_specific_table,
    )
    validate_toml_text(updated, label)
    return updated


def build_base_config_text(base_config_path: Path) -> str:
    return build_base_config_text_from_text(
        base_config_path.read_text(),
        str(base_config_path),
    )


def config_uses_file_auth(config_text: str) -> bool:
    assignment = top_level_assignment(config_text, "cli_auth_credentials_store")
    if not assignment:
        return False
    value = assignment.split("=", 1)[1].strip().strip('"').strip("'").lower()
    return value == "file"


def build_shared_config_text(
    base_config_path: Path,
    profile_name: str,
    profile_config_path: Path,
) -> str:
    profile_text = profile_config_path.read_text()
    updated = base_config_path.read_text()
    updated = remove_top_level_assignment(updated, "profile")
    updated = remove_legacy_profile_tables(updated)

    for key in PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE:
        updated = remove_top_level_assignment(updated, key)

    assignments = target_profile_assignments(profile_text, profile_name)
    for key, assignment in assignments.items():
        updated = upsert_top_level_assignment(updated, key, assignment)
    updated = append_target_model_provider_table(updated, profile_text, assignments)

    validate_toml_text(updated, str(base_config_path))
    return updated
