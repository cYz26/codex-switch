from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

from codex_switch_config import (
    build_base_config_text,
    build_profile_seed_config_text,
    is_profile_specific_table,
    merge_preserved_shared_config_overlay,
    merge_shared_config_overlay,
    string_assignment_value,
)
from codex_switch_constants import PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE, SwitchError
from codex_switch_io import atomic_write, ensure_private_dir
from codex_switch_toml_edit import top_level_assignment
from codex_switch_toml_scan import toml_table_name
from codex_switch_toml_validate import validate_toml_text


RUNTIME_STATE_NAMES = {
    "sessions",
    "session_index.jsonl",
    "history.jsonl",
    "archived_sessions",
    "log",
    "tmp",
    ".tmp",
    "process_manager",
    "node_repl",
    "shell_snapshots",
    "browser",
    "ambient-suggestions",
}
NON_SHAREABLE_HOME_ENTRY_NAMES = {
    ".codex-global-state.json",
    ".codex-global-state.json.bak",
    ".credentials.json",
    "agent-kb",
    "automations",
    "cache",
    "chrome-native-hosts-v2.json",
    "chrome-native-hosts.json",
    "computer-use",
    "installation_id",
    "model-catalogs",
    "models_cache.json",
    "pets",
    "plugins",
    "secrets",
    "sqlite",
    "update-backups",
    "vendor_imports",
    "version.json",
}
MANAGED_COMMENT_PREFIX = "# codex-switch:"


def is_runtime_state_name(name: str) -> bool:
    return (
        name in RUNTIME_STATE_NAMES
        or name.endswith(".sqlite")
        or name.endswith(".sqlite-shm")
        or name.endswith(".sqlite-wal")
        or ".sqlite.corrupt." in name
        or ".sqlite-shm.corrupt." in name
        or ".sqlite-wal.corrupt." in name
    )


def is_profile_state_name(name: str) -> bool:
    return name == "config.toml" or name == "auth.json" or name.endswith(".config.toml")


def is_non_shareable_home_entry_name(name: str) -> bool:
    return name in NON_SHAREABLE_HOME_ENTRY_NAMES


def is_shareable_home_entry(path: Path) -> bool:
    name = path.name
    return (
        not is_profile_state_name(name)
        and not is_runtime_state_name(name)
        and not is_non_shareable_home_entry_name(name)
    )


def shared_support_entries(source_home: Path) -> list[Path]:
    if not source_home.exists():
        return []
    return sorted(
        (path for path in source_home.iterdir() if is_shareable_home_entry(path)),
        key=lambda path: path.name,
    )


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def absolute_symlink_target(path: Path) -> Path:
    target = Path(os.readlink(path))
    if not target.is_absolute():
        target = path.parent / target
    return Path(os.path.abspath(target))


def path_is_within(path: Path, parent: Path) -> bool:
    try:
        Path(os.path.abspath(path)).relative_to(Path(os.path.abspath(parent)))
        return True
    except ValueError:
        return False


def symlink_points_within(path: Path, parent: Path) -> bool:
    return path.is_symlink() and path_is_within(absolute_symlink_target(path), parent)


def symlink_points_to_itself(path: Path) -> bool:
    return path.is_symlink() and absolute_symlink_target(path) == Path(os.path.abspath(path))


def unsafe_copytree_symlinks(target_home: Path):
    def ignore(directory: str, names: list[str]) -> set[str]:
        skipped: set[str] = set()
        for name in names:
            path = Path(directory) / name
            if symlink_points_to_itself(path) or symlink_points_within(path, target_home):
                skipped.add(name)
        return skipped

    return ignore


def copy_or_link_shared_entry(source: Path, target: Path, prefer_link: bool) -> None:
    if source.is_symlink():
        if symlink_points_to_itself(source):
            if symlink_points_to_itself(target) or symlink_points_within(target, target.parent):
                remove_path(target)
            return
        if symlink_points_within(source, target.parent):
            if symlink_points_within(target, target.parent):
                remove_path(target)
            return
        link_target = os.readlink(source)
        if target.is_symlink() and os.readlink(target) == link_target:
            return
        if target.exists() or target.is_symlink():
            remove_path(target)
        ensure_private_dir(target.parent)
        target.symlink_to(link_target)
        return

    if prefer_link and source.is_dir():
        if path_is_within(source, target.parent):
            if symlink_points_within(target, target.parent):
                remove_path(target)
            return
        if target.is_symlink() and Path(os.readlink(target)) == source:
            return
        if target.is_symlink():
            remove_path(target)
        if not target.exists() and not target.is_symlink():
            ensure_private_dir(target.parent)
            target.symlink_to(source, target_is_directory=True)
        return

    if source.is_file():
        atomic_write(target, source.read_bytes(), mode=source.stat().st_mode & 0o777)
        return

    if source.is_dir() and not target.exists() and not target.is_symlink():
        ensure_private_dir(target.parent)
        shutil.copytree(
            source,
            target,
            symlinks=True,
            ignore=unsafe_copytree_symlinks(target.parent),
        )


def shared_support_targets(source_home: Path, target_home: Path) -> list[Path]:
    return [target_home / entry.name for entry in shared_support_entries(source_home)]


def sync_shared_support(source_home: Path, target_home: Path, prefer_link: bool) -> list[Path]:
    mutated: list[Path] = []
    for source in shared_support_entries(source_home):
        target = target_home / source.name
        before_exists = target.exists() or target.is_symlink()
        copy_or_link_shared_entry(source, target, prefer_link=prefer_link)
        if before_exists or target.exists() or target.is_symlink():
            mutated.append(target)
    return mutated


def stale_runtime_links(home: Path, source_home: Path) -> list[Path]:
    if not home.exists():
        return []
    stale: list[Path] = []
    source_prefix = str(source_home)
    for path in home.iterdir():
        if not is_runtime_state_name(path.name) or not path.is_symlink():
            continue
        link_target = os.readlink(path)
        if link_target.startswith(source_prefix):
            stale.append(path)
    return stale


def remove_stale_runtime_links(home: Path, source_home: Path) -> list[Path]:
    removed: list[Path] = []
    for path in stale_runtime_links(home, source_home):
        path.unlink()
        removed.append(path)
    return removed


def strip_managed_comments(text: str) -> str:
    lines = [
        line
        for line in text.splitlines()
        if not line.startswith(MANAGED_COMMENT_PREFIX)
    ]
    return "\n".join(lines).strip() + "\n"


def top_level_key(line: str) -> str | None:
    stripped = line.strip()
    if not stripped or stripped.startswith("#") or "=" not in stripped:
        return None
    return stripped.split("=", 1)[0].strip()


def append_section_header(lines: list[str], section: str) -> None:
    if lines and lines[-1].strip():
        lines.append("")
    lines.append(f"{MANAGED_COMMENT_PREFIX} {section} settings")


def annotate_config_sections(text: str) -> str:
    annotated: list[str] = []
    current_section: str | None = None
    in_top_level = True

    for line in text.strip().splitlines():
        table = toml_table_name(line)
        if table:
            in_top_level = False
            section = "profile-specific" if is_profile_specific_table(table) else "shared"
        elif in_top_level:
            key = top_level_key(line)
            if key is None:
                section = current_section
            else:
                section = (
                    "profile-specific"
                    if key in PROFILE_TOP_LEVEL_KEYS_FROM_PROFILE
                    else "shared"
                )
        else:
            section = current_section

        if section != current_section and section in {"profile-specific", "shared"}:
            append_section_header(annotated, section)
            current_section = section
        annotated.append(line)

    return "\n".join(annotated).strip() + "\n"


def annotate_runtime_config(
    text: str,
    profile_name: str,
    shared_source: Path,
    profile_source: str,
) -> str:
    body = strip_managed_comments(text)
    body = annotate_config_sections(body)
    annotated = (
        f"{MANAGED_COMMENT_PREFIX} managed runtime config for profile {profile_name}\n"
        f"{MANAGED_COMMENT_PREFIX} shared settings are merged from {shared_source}\n"
        f"{MANAGED_COMMENT_PREFIX} profile-specific settings are preserved from {profile_source}\n"
        "\n"
        f"{body}"
    )
    validate_toml_text(annotated, f"annotated runtime config for {profile_name}")
    return annotated


def annotate_canonical_profile_config(text: str, profile_name: str) -> str:
    body = annotate_config_sections(strip_managed_comments(text))
    annotated = (
        f"{MANAGED_COMMENT_PREFIX} canonical fallback config for profile {profile_name}\n"
        f"{MANAGED_COMMENT_PREFIX} profile-specific settings only; shared settings stay in active homes\n"
        "\n"
        f"{body}"
    )
    validate_toml_text(annotated, f"canonical profile config for {profile_name}")
    return annotated


def managed_runtime_profile_name(text: str) -> str | None:
    prefix = f"{MANAGED_COMMENT_PREFIX} managed runtime config for profile "
    for line in text.splitlines()[:5]:
        if line.startswith(prefix):
            value = line[len(prefix) :].strip()
            return value or None
    return None


def read_valid_config(path: Path, label: str) -> str:
    text = path.read_text()
    validate_toml_text(text, label)
    return text


def catalog_models(data) -> list[dict]:
    models = data.get("models") if isinstance(data, dict) else data
    if not isinstance(models, list):
        return []
    return [model for model in models if isinstance(model, dict)]


def model_entry_matches(model: dict, model_slug: str) -> bool:
    for key in ("slug", "id", "name", "model"):
        if model.get(key) == model_slug:
            return True
    return False


def supported_reasoning_efforts_from_catalog(seed_text: str) -> set[str] | None:
    model_assignment = top_level_assignment(seed_text, "model")
    catalog_assignment = top_level_assignment(seed_text, "model_catalog_json")
    if not model_assignment or not catalog_assignment:
        return None

    model_slug = string_assignment_value(model_assignment)
    catalog_path = Path(string_assignment_value(catalog_assignment)).expanduser()
    if not model_slug or not catalog_path.is_absolute() or not catalog_path.exists():
        return None

    try:
        data = json.loads(catalog_path.read_text())
    except (OSError, json.JSONDecodeError):
        return None

    for model in catalog_models(data):
        if not model_entry_matches(model, model_slug):
            continue
        levels = model.get("supported_reasoning_levels")
        if not isinstance(levels, list):
            return None
        efforts: set[str] = set()
        for level in levels:
            if isinstance(level, str):
                efforts.add(level)
            elif isinstance(level, dict) and isinstance(level.get("effort"), str):
                efforts.add(level["effort"])
        return efforts or None
    return None


def validate_profile_seed_reasoning_effort(seed_text: str, label: str) -> None:
    effort_assignment = top_level_assignment(seed_text, "model_reasoning_effort")
    if not effort_assignment:
        return
    supported_efforts = supported_reasoning_efforts_from_catalog(seed_text)
    if supported_efforts is None:
        return
    effort = string_assignment_value(effort_assignment)
    if effort not in supported_efforts:
        supported = ", ".join(sorted(supported_efforts))
        raise SwitchError(
            f"Unsupported model_reasoning_effort {effort!r} in {label}; "
            f"supported values from model_catalog_json are: {supported}"
        )


def merge_shared_with_profile_seed(
    shared_source_config: Path,
    profile_name: str,
    target_runtime_config: Path,
    canonical_config: Path,
    profile_layer_configs: list[Path] | None = None,
) -> str:
    shared_text = build_base_config_text(shared_source_config) if shared_source_config.exists() else ""
    errors: list[str] = []
    profile_layers = unique_paths(profile_layer_configs or [])
    profile_layer_texts: dict[Path, str] = {}
    for path in profile_layers:
        if not path.exists():
            continue
        try:
            profile_layer_text = read_valid_config(path, f"profile layer shared config: {path}")
            profile_layer_texts[path] = profile_layer_text
            shared_text = merge_preserved_shared_config_overlay(shared_text, profile_layer_text)
        except SwitchError as exc:
            errors.append(str(exc))

    candidates: list[tuple[Path, str, str | None]] = []
    if target_runtime_config.exists():
        try:
            runtime_text = read_valid_config(
                target_runtime_config,
                f"last runtime config: {target_runtime_config}",
            )
            if not should_skip_managed_runtime_seed(
                profile_name,
                runtime_text,
                profile_layer_texts,
            ):
                candidates.append((target_runtime_config, "last runtime config", runtime_text))
        except SwitchError as exc:
            errors.append(str(exc))
    for path in profile_layers:
        if path.exists():
            candidates.append((path, "profile layer config", None))
    candidates.append((canonical_config, "fallback canonical config", None))

    for path, label, preloaded_text in candidates:
        try:
            profile_text = preloaded_text
            if profile_text is None:
                profile_text = read_valid_config(path, f"{label}: {path}")
            seed_text = build_profile_seed_config_text(
                profile_name,
                profile_text,
                f"profile seed from {label}: {path}",
            )
            validate_profile_seed_reasoning_effort(seed_text, f"{label}: {path}")
            merged = merge_shared_config_overlay(seed_text, shared_text)
            validate_toml_text(merged, f"runtime config for {profile_name}")
            profile_source = "fallback canonical config" if label.startswith("fallback") else label
            return annotate_runtime_config(
                merged,
                profile_name=profile_name,
                shared_source=shared_source_config,
                profile_source=profile_source,
            )
        except SwitchError as exc:
            errors.append(str(exc))

    raise SwitchError(
        f"Unable to build runtime config for {profile_name}; "
        + "; ".join(errors)
    )


def should_skip_managed_runtime_seed(
    profile_name: str,
    runtime_text: str,
    profile_layer_texts: dict[Path, str],
) -> bool:
    if profile_name != "openai-official":
        return False
    if managed_runtime_profile_name(runtime_text) != profile_name:
        return False
    if not profile_layer_texts:
        return False
    if not top_level_assignment(runtime_text, "model_provider"):
        return False
    return not any(
        top_level_assignment(profile_layer_text, "model_provider")
        for profile_layer_text in profile_layer_texts.values()
    )


def unique_paths(paths: list[Path]) -> list[Path]:
    seen: set[Path] = set()
    unique: list[Path] = []
    for path in paths:
        resolved = Path(os.path.abspath(path))
        if resolved in seen:
            continue
        seen.add(resolved)
        unique.append(path)
    return unique


def build_internal_home_config(
    official_home: Path,
    profile_name: str,
    target_runtime_config: Path,
    canonical_config: Path,
) -> str:
    return merge_shared_with_profile_seed(
        official_home / "config.toml",
        profile_name,
        target_runtime_config,
        canonical_config,
        profile_layer_configs=[
            target_runtime_config.parent / f"{profile_name}.config.toml",
            official_home / f"{profile_name}.config.toml",
        ],
    )


def build_official_home_config_from_internal(
    official_home: Path,
    internal_home: Path,
    canonical_config: Path,
) -> str | None:
    official_config = official_home / "config.toml"
    internal_config = internal_home / "config.toml"
    if not internal_config.exists():
        return None
    return merge_shared_with_profile_seed(
        internal_config,
        "openai-official",
        official_config,
        canonical_config,
        profile_layer_configs=[
            official_home / "openai-official.config.toml",
            internal_home / "openai-official.config.toml",
        ],
    )


def refresh_profile_canonical_config(
    profile_name: str,
    runtime_config_path: Path,
    canonical_config_path: Path,
) -> str:
    runtime_text = runtime_config_path.read_text()
    fallback_text = canonical_config_path.read_text() if canonical_config_path.exists() else None
    seed_text = build_profile_seed_config_text(
        profile_name,
        runtime_text,
        f"canonical profile seed for {profile_name}",
        fallback_text=fallback_text,
        fallback_keys={"cli_auth_credentials_store"},
    )
    seed_text = annotate_canonical_profile_config(seed_text, profile_name)
    atomic_write(canonical_config_path, seed_text.encode(), mode=0o600)
    return seed_text
