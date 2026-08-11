from __future__ import annotations

import ast
import hashlib
import json
import os
import stat
import subprocess
from dataclasses import dataclass, replace
from pathlib import Path
from types import MappingProxyType
from typing import Any, Mapping

from codex_switch_constants import SwitchError
from codex_switch_home_select import profile_home_binding
from codex_switch_home_sync import plugin_support_snapshot_name
from codex_switch_io import atomic_write
from codex_switch_running_app import (
    app_server_matches_expected_cli,
    collect_store_runtime_observation,
)
from codex_switch_runtime_binding import resolve_store_runtime_binding
from codex_switch_store import Store, make_store
from codex_switch_toml_scan import toml_table_name
from codex_switch_toml_validate import commentless_line, validate_toml, validate_toml_text


PRODUCT_PROFILES = frozenset({"internal", "openai-official"})
IGNORED_TREE_DIR_NAMES = frozenset(
    {".git", ".mypy_cache", ".pytest_cache", ".ruff_cache", "__pycache__"}
)
IGNORED_TREE_FILE_NAMES = frozenset({".DS_Store", ".coverage"})
IGNORED_TREE_FILE_SUFFIXES = (".pyc", ".pyo")
PLUGIN_CATALOG_COLLECTION_KEYS = (
    "installed",
    "available",
    "plugins",
    "items",
    "data",
)
SHARED_PLUGIN_POLICIES = frozenset({"portable_exact", "backend_managed"})
SHARED_MATERIALIZATION_ERROR_PREFIX = "shared_configuration.materialization."


@dataclass(frozen=True)
class PluginRequirement:
    selector: str
    plugin: str
    marketplace: str


@dataclass(frozen=True)
class PluginCatalogEntry:
    selector: str
    plugin: str
    marketplace: str
    version: str
    source_path: Path | None
    available_record_seen: bool = False
    available_version_seen: bool = False
    available_source_seen: bool = False
    installed_record_seen: bool = False
    installed_versions: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProfileCommandResult:
    stdout: str
    stderr: str
    returncode: int


@dataclass(frozen=True)
class CatalogResult:
    status: str
    entries: Mapping[str, PluginCatalogEntry]
    stdout: str
    stderr: str
    returncode: int
    detail: str = ""

    @property
    def verified(self) -> bool:
        return self.status == "verified"


@dataclass(frozen=True)
class PluginConfigUpdate:
    path: Path
    before: bytes
    after: bytes
    before_mode: int
    after_mode: int = 0o600


@dataclass(frozen=True)
class PluginRepairPlan:
    profile: str
    catalog_verified: bool
    conditional_install: tuple[PluginRequirement, ...] = ()
    installed: tuple[PluginRequirement, ...] = ()
    install: tuple[PluginRequirement, ...] = ()
    unavailable: tuple[PluginRequirement, ...] = ()
    disable: tuple[PluginRequirement, ...] = ()
    refresh: tuple[PluginRequirement, ...] = ()
    current: tuple[PluginRequirement, ...] = ()
    diagnostics: tuple[str, ...] = ()
    config_updates: tuple[PluginConfigUpdate, ...] = ()


@dataclass(frozen=True)
class PluginMaintenanceRuntime:
    codex_bin: Path
    home: Path
    binding: Any | None = None


@dataclass(frozen=True)
class SharedPluginDesiredIdentity:
    requirement: PluginRequirement
    policy: str
    cache_key: str
    manifest_version: str
    tree_sha256: str
    marketplace_config: Mapping[str, Any]


@dataclass(frozen=True)
class _SharedTargetConfigSnapshot:
    exists: bool
    data: bytes = b""
    mode: int = 0


def decode_toml_key_segment(raw: str) -> str:
    stripped = raw.strip()
    if len(stripped) >= 2 and stripped[0] in {"'", '"'} and stripped[-1] == stripped[0]:
        try:
            value = ast.literal_eval(stripped)
        except (SyntaxError, ValueError):
            return stripped[1:-1]
        if isinstance(value, str):
            return value
    return stripped


def plugin_selector_from_table(table_name: str) -> str | None:
    prefix = "plugins."
    if not table_name.startswith(prefix):
        return None
    selector = decode_toml_key_segment(table_name[len(prefix) :])
    return selector or None


def assignment_bool(line: str, key: str) -> bool | None:
    stripped = commentless_line(line).strip()
    if not (stripped.startswith(f"{key} ") or stripped.startswith(f"{key}=")):
        return None
    if "=" not in stripped:
        return None
    value = stripped.split("=", 1)[1].strip().lower()
    if value == "true":
        return True
    if value == "false":
        return False
    return None


def plugin_requirement(selector: str) -> PluginRequirement | None:
    if "@" not in selector:
        return None
    plugin, marketplace = selector.rsplit("@", 1)
    if not plugin or not marketplace:
        return None
    return PluginRequirement(selector=selector, plugin=plugin, marketplace=marketplace)


def enabled_plugin_requirements(config_path: Path) -> list[PluginRequirement]:
    if not config_path.exists():
        return []
    validate_toml(config_path)
    requirements: list[PluginRequirement] = []
    seen: set[str] = set()
    current_selector: str | None = None
    current_enabled: bool | None = None

    def flush_current() -> None:
        if current_selector is None or current_enabled is False:
            return
        requirement = plugin_requirement(current_selector)
        if requirement is None or requirement.selector in seen:
            return
        seen.add(requirement.selector)
        requirements.append(requirement)

    for line in config_path.read_text().splitlines():
        table = toml_table_name(line)
        if table:
            flush_current()
            current_selector = plugin_selector_from_table(table)
            current_enabled = None
            continue
        if current_selector is not None:
            enabled = assignment_bool(line, "enabled")
            if enabled is not None:
                current_enabled = enabled
    flush_current()
    return requirements


def profile_home(store: Store, name: str) -> Path:
    manifest = store.load_manifest(name)
    return profile_home_binding(store, name, manifest).path


def profile_codex_bin(store: Store, name: str) -> str:
    manifest = store.load_manifest(name)
    codex_bin = str(manifest.get("codex_bin", ""))
    if not codex_bin:
        raise SwitchError(f"{name}: missing codex_bin")
    if not Path(codex_bin).expanduser().exists():
        raise SwitchError(f"{name}: codex_bin does not exist: {codex_bin}")
    return codex_bin


def profile_plugin_runtime(store: Store, name: str) -> PluginMaintenanceRuntime:
    if name in PRODUCT_PROFILES:
        binding = resolve_store_runtime_binding(store, name)
        return PluginMaintenanceRuntime(
            codex_bin=binding.backend_cli,
            home=binding.codex_home,
            binding=binding,
        )
    return PluginMaintenanceRuntime(
        codex_bin=Path(profile_codex_bin(store, name)).expanduser(),
        home=profile_home(store, name),
    )


def plugin_cache_path(home: Path, requirement: PluginRequirement) -> Path:
    return home / "plugins" / "cache" / requirement.marketplace / requirement.plugin


def plugin_cache_version_is_materialized(
    version_path: Path,
    requirement: PluginRequirement,
    *,
    expected_cache_key: str | None = None,
) -> bool:
    if (
        version_path.is_symlink()
        or not version_path.is_dir()
        or not version_path.name
        or version_path.name in {".", ".."}
    ):
        return False
    return (
        plugin_manifest_version(version_path, requirement.plugin) is not None
        and (
            expected_cache_key is None
            or version_path.name == expected_cache_key
        )
    )


def plugin_is_installed(home: Path, requirement: PluginRequirement) -> bool:
    cache_path = plugin_cache_path(home, requirement)
    if cache_path.is_dir() and not cache_path.is_symlink():
        try:
            if any(
                plugin_cache_version_is_materialized(path, requirement)
                for path in cache_path.iterdir()
            ):
                return True
        except OSError:
            return False
    direct_path = home / "plugins" / requirement.plugin
    if direct_path.is_symlink() or not direct_path.is_dir():
        return False
    return plugin_manifest_version(direct_path, requirement.plugin) is not None


def missing_enabled_plugins(store: Store, name: str) -> list[PluginRequirement]:
    home = profile_home(store, name)
    return [
        requirement
        for requirement in enabled_plugin_requirements(home / "config.toml")
        if not plugin_is_installed(home, requirement)
    ]


def plugin_materialization_problems(store: Store, name: str) -> list[str]:
    home = profile_home(store, name)
    problems: list[str] = []
    for requirement in missing_enabled_plugins(store, name):
        expected = plugin_cache_path(home, requirement)
        problems.append(
            f"active profile {name}: enabled plugin is not installed in CODEX_HOME: "
            f"{requirement.selector} (expected cache under {expected}; "
            f"run: codex-switch repair-plugins {name}; if the refreshed catalog "
            f"does not contain this selector, run: codex-switch repair-plugins "
            f"{name} --disable-unavailable)"
        )
    return problems


def disable_plugin_selector_in_text(text: str, selector: str) -> tuple[str, bool]:
    lines = text.splitlines()
    updated: list[str] = []
    in_target_table = False
    saw_target_table = False
    saw_enabled = False
    changed = False

    def close_target_table() -> None:
        nonlocal changed, saw_enabled
        if in_target_table and not saw_enabled:
            updated.append("enabled = false")
            changed = True
            saw_enabled = True

    for line in lines:
        table = toml_table_name(line)
        if table:
            close_target_table()
            current_selector = plugin_selector_from_table(table)
            in_target_table = current_selector == selector
            saw_target_table = saw_target_table or in_target_table
            saw_enabled = False
            updated.append(line)
            continue

        if in_target_table:
            enabled = assignment_bool(line, "enabled")
            if enabled is not None:
                updated.append("enabled = false")
                saw_enabled = True
                if enabled is not False:
                    changed = True
                continue
        updated.append(line)

    close_target_table()
    if not saw_target_table:
        return text, False
    result = "\n".join(updated).rstrip() + "\n"
    validate_toml_text(result, "plugin selector cleanup")
    return result, changed


def profile_plugin_config_paths(store: Store, name: str, home: Path) -> list[Path]:
    plugin_support_name = plugin_support_snapshot_name(name)
    candidates = [
        home / "config.toml",
        home / plugin_support_name,
        home / f"{name}.config.toml",
        store.profile_dir(name) / "config.toml",
        store.profile_dir(name) / plugin_support_name,
        store.live_codex_home / "config.toml",
        store.live_codex_home / plugin_support_name,
        store.live_codex_home / f"{name}.config.toml",
    ]
    internal_home = store.managed_home("internal")
    candidates.extend(
        [
            internal_home / "config.toml",
            internal_home / plugin_support_name,
            internal_home / f"{name}.config.toml",
        ]
    )
    seen: set[Path] = set()
    paths: list[Path] = []
    for path in candidates:
        resolved = Path(path).expanduser().resolve(strict=False)
        if resolved in seen or not path.exists():
            continue
        seen.add(resolved)
        paths.append(path)
    return paths


def disable_unavailable_plugin_requirements(
    store: Store,
    name: str,
    home: Path,
    requirements: list[PluginRequirement],
) -> list[Path]:
    updates = build_plugin_config_updates(
        store,
        name,
        home,
        requirements,
    )
    apply_plugin_config_updates(updates)
    return [update.path for update in updates]


def build_plugin_config_updates(
    store: Store,
    name: str,
    home: Path,
    requirements: list[PluginRequirement],
) -> tuple[PluginConfigUpdate, ...]:
    updates: list[PluginConfigUpdate] = []
    selectors = [requirement.selector for requirement in requirements]
    for path in profile_plugin_config_paths(store, name, home):
        original_bytes = path.read_bytes()
        try:
            original = original_bytes.decode()
        except UnicodeDecodeError as error:
            raise SwitchError(f"Invalid UTF-8 plugin config: {path}: {error}") from error
        validate_toml_text(original, str(path))
        updated = original
        changed = False
        for selector in selectors:
            updated, selector_changed = disable_plugin_selector_in_text(updated, selector)
            changed = changed or selector_changed
        if not changed:
            continue
        updates.append(
            PluginConfigUpdate(
                path=path,
                before=original_bytes,
                after=updated.encode(),
                before_mode=stat.S_IMODE(path.stat().st_mode),
            )
        )
    return tuple(updates)


def apply_plugin_config_updates(
    updates: tuple[PluginConfigUpdate, ...],
) -> None:
    for update in updates:
        if update.path.read_bytes() != update.before:
            raise SwitchError(
                f"plugin config changed after planning: {update.path}"
            )
    attempted: list[PluginConfigUpdate] = []
    try:
        for update in updates:
            attempted.append(update)
            atomic_write(
                update.path,
                update.after,
                mode=update.after_mode,
            )
    except BaseException as error:
        rollback_errors: list[str] = []
        for update in reversed(attempted):
            try:
                atomic_write(
                    update.path,
                    update.before,
                    mode=update.before_mode,
                )
            except BaseException as rollback_error:
                rollback_errors.append(f"{update.path}: {rollback_error}")
        if rollback_errors:
            raise SwitchError(
                "plugin config update failed and rollback was incomplete: "
                + "; ".join(rollback_errors)
            ) from error
        raise


def run_profile_command(
    *,
    name: str,
    codex_bin: Path,
    home: Path,
    args: list[str],
    description: str,
    dry_run: bool = False,
    echo_stdout: bool = True,
) -> str:
    result = capture_profile_command(
        codex_bin=codex_bin,
        home=home,
        args=args,
        dry_run=dry_run,
    )
    output = "\n".join(
        part.strip()
        for part in (result.stdout, result.stderr)
        if part.strip()
    )
    if output and echo_stdout:
        print(output)
    if result.returncode != 0:
        if output and not echo_stdout:
            print(output)
        raise SwitchError(
            f"{name}: failed to {description} (exit {result.returncode})"
        )
    return result.stdout


def capture_profile_command(
    *,
    codex_bin: Path,
    home: Path,
    args: list[str],
    dry_run: bool = False,
) -> ProfileCommandResult:
    return _capture_profile_command(
        codex_bin=codex_bin,
        home=home,
        args=args,
        dry_run=dry_run,
        pass_fds=(),
    )


def _capture_profile_command(
    *,
    codex_bin: Path,
    home: Path,
    args: list[str],
    dry_run: bool = False,
    pass_fds: tuple[int, ...],
) -> ProfileCommandResult:
    command = [str(codex_bin), *args]
    if dry_run:
        print("Dry run:", " ".join(command))
        return ProfileCommandResult(stdout="", stderr="", returncode=0)
    env = dict(os.environ)
    env["CODEX_HOME"] = str(home)
    run_options: dict[str, Any] = {
        "check": False,
        "text": True,
        "stdout": subprocess.PIPE,
        "stderr": subprocess.PIPE,
        "env": env,
    }
    if pass_fds:
        run_options["pass_fds"] = pass_fds
    result = subprocess.run(command, **run_options)
    return ProfileCommandResult(
        stdout=result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
    )


def run_profile_plugin_command(
    *,
    name: str,
    codex_bin: Path,
    home: Path,
    args: list[str],
    description: str,
    dry_run: bool = False,
    echo_stdout: bool = True,
) -> str:
    return run_profile_command(
        name=name,
        codex_bin=codex_bin,
        home=home,
        args=["plugin", *args],
        description=description,
        dry_run=dry_run,
        echo_stdout=echo_stdout,
    )


def verify_profile_plugin_runtime(
    *,
    name: str,
    codex_bin: Path,
    home: Path,
    dry_run: bool = False,
) -> None:
    print(f"Verifying plugin maintenance CLI for {name}")
    output = run_profile_command(
        name=name,
        codex_bin=codex_bin,
        home=home,
        args=["--version"],
        description="verify plugin maintenance CLI",
        dry_run=dry_run,
        echo_stdout=False,
    )
    if dry_run:
        return
    version = next((line.strip() for line in output.splitlines() if line.strip()), "")
    if not version:
        raise SwitchError(f"{name}: plugin maintenance CLI returned no version")
    print(f"Plugin maintenance CLI for {name}: {codex_bin} ({version})")


def refresh_profile_plugin_catalogs(
    *,
    name: str,
    codex_bin: Path,
    home: Path,
    dry_run: bool = False,
) -> CatalogResult | None:
    print(f"Refreshing plugin marketplaces for {name}")
    run_profile_plugin_command(
        name=name,
        codex_bin=codex_bin,
        home=home,
        args=["marketplace", "upgrade", "--json"],
        description="refresh plugin marketplaces",
        dry_run=dry_run,
        echo_stdout=False,
    )
    print(f"Priming available plugin catalog for {name}")
    result = capture_profile_command(
        codex_bin=codex_bin,
        home=home,
        args=["plugin", "list", "--available", "--json"],
        dry_run=dry_run,
    )
    if dry_run:
        return None
    return available_plugin_catalog(
        result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
    )


def plugin_catalog_entry(
    value: dict[str, Any],
    *,
    provenance: str = "generic",
) -> PluginCatalogEntry | None:
    selector = ""
    for key in ("pluginId", "id", "selector"):
        candidate = value.get(key)
        if isinstance(candidate, str) and plugin_requirement(candidate) is not None:
            selector = candidate
            break
    if not selector:
        plugin = value.get("plugin") or value.get("name")
        marketplace = (
            value.get("marketplace")
            or value.get("marketplaceId")
            or value.get("marketplaceName")
        )
        if isinstance(plugin, str) and isinstance(marketplace, str):
            candidate = f"{plugin}@{marketplace}"
            if plugin_requirement(candidate) is not None:
                selector = candidate
    requirement = plugin_requirement(selector)
    if requirement is None:
        return None

    version_value = value.get("version") or value.get("pluginVersion")
    version = version_value if isinstance(version_value, str) else ""
    source_path: Path | None = None
    source = value.get("source")
    if isinstance(source, dict):
        source_kind = source.get("source") or source.get("type")
        path_value = source.get("path")
        if source_kind == "local" and isinstance(path_value, str) and path_value:
            source_path = Path(path_value).expanduser()
    explicit_installed = value.get("installed")
    installed_record_seen = explicit_installed is True or (
        provenance == "installed" and explicit_installed is not False
    )
    return PluginCatalogEntry(
        selector=requirement.selector,
        plugin=requirement.plugin,
        marketplace=requirement.marketplace,
        version=version,
        source_path=source_path,
        available_record_seen=provenance == "available",
        available_version_seen=(
            provenance == "available" and bool(version)
        ),
        available_source_seen=(
            provenance == "available" and source_path is not None
        ),
        installed_record_seen=installed_record_seen,
        installed_versions=(
            (version,) if installed_record_seen and version else ()
        ),
    )


def _catalog_version_projection_key(
    entry: PluginCatalogEntry,
) -> tuple[int, int, str]:
    return (
        0 if entry.available_version_seen else 1,
        0 if entry.version else 1,
        entry.version,
    )


def _catalog_source_path_projection_key(
    entry: PluginCatalogEntry,
) -> tuple[int, int, str]:
    return (
        0 if entry.available_source_seen else 1,
        0 if entry.source_path is not None else 1,
        str(entry.source_path or ""),
    )


def _merge_plugin_catalog_entries(
    previous: PluginCatalogEntry,
    current: PluginCatalogEntry,
) -> PluginCatalogEntry:
    version_projection = min(
        (previous, current),
        key=_catalog_version_projection_key,
    )
    source_path_projection = min(
        (previous, current),
        key=_catalog_source_path_projection_key,
    )
    return PluginCatalogEntry(
        selector=previous.selector,
        plugin=previous.plugin,
        marketplace=previous.marketplace,
        version=version_projection.version,
        source_path=source_path_projection.source_path,
        available_record_seen=(
            previous.available_record_seen or current.available_record_seen
        ),
        available_version_seen=version_projection.available_version_seen,
        available_source_seen=source_path_projection.available_source_seen,
        installed_record_seen=(
            previous.installed_record_seen or current.installed_record_seen
        ),
        installed_versions=tuple(
            sorted(
                set(previous.installed_versions)
                | set(current.installed_versions)
            )
        ),
    )


def collect_available_plugin_catalog(
    value: Any,
    entries: dict[str, PluginCatalogEntry],
    *,
    provenance: str = "generic",
) -> None:
    if isinstance(value, list):
        for item in value:
            collect_available_plugin_catalog(
                item,
                entries,
                provenance=provenance,
            )
        return
    if not isinstance(value, dict):
        return

    entry = plugin_catalog_entry(value, provenance=provenance)
    if entry is not None:
        previous = entries.get(entry.selector)
        if previous is None:
            entries[entry.selector] = entry
        else:
            entries[entry.selector] = _merge_plugin_catalog_entries(
                previous,
                entry,
            )

    for key in ("installed", "available", "plugins", "items", "data"):
        child_provenance = provenance
        if key in {"installed", "available"}:
            child_provenance = key
        collect_available_plugin_catalog(
            value.get(key),
            entries,
            provenance=child_provenance,
        )


def available_plugin_catalog(
    output: str,
    *,
    stderr: str = "",
    returncode: int = 0,
) -> CatalogResult:
    empty_entries: Mapping[str, PluginCatalogEntry] = MappingProxyType({})
    if returncode != 0:
        return CatalogResult(
            status="command_failed",
            entries=empty_entries,
            stdout=output,
            stderr=stderr,
            returncode=returncode,
            detail=f"plugin catalog command exited {returncode}",
        )
    if stderr.strip():
        return CatalogResult(
            status="stderr_output",
            entries=empty_entries,
            stdout=output,
            stderr=stderr,
            returncode=returncode,
            detail="plugin catalog command wrote stderr output",
        )
    if not output.strip():
        return CatalogResult(
            status="empty_output",
            entries=empty_entries,
            stdout=output,
            stderr=stderr,
            returncode=returncode,
            detail="plugin catalog command returned empty stdout",
        )
    try:
        data = json.loads(output)
    except json.JSONDecodeError as error:
        return CatalogResult(
            status="invalid_json",
            entries=empty_entries,
            stdout=output,
            stderr=stderr,
            returncode=returncode,
            detail=f"plugin catalog JSON is invalid: {error}",
        )
    if not isinstance(data, dict):
        return CatalogResult(
            status="unsupported_schema",
            entries=empty_entries,
            stdout=output,
            stderr=stderr,
            returncode=returncode,
            detail="plugin catalog root must be an object",
        )
    collection_keys = [
        key for key in PLUGIN_CATALOG_COLLECTION_KEYS if key in data
    ]
    if not collection_keys or any(
        not isinstance(data[key], (dict, list)) for key in collection_keys
    ):
        return CatalogResult(
            status="unsupported_schema",
            entries=empty_entries,
            stdout=output,
            stderr=stderr,
            returncode=returncode,
            detail="plugin catalog has no supported collection envelope",
        )
    entries: dict[str, PluginCatalogEntry] = {}
    collect_available_plugin_catalog(data, entries)
    return CatalogResult(
        status="verified",
        entries=MappingProxyType(entries),
        stdout=output,
        stderr=stderr,
        returncode=returncode,
    )


def plugin_manifest_version(root: Path, plugin: str) -> str | None:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        return None
    try:
        manifest = json.loads(manifest_path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(manifest, dict) or manifest.get("name") != plugin:
        return None
    version = manifest.get("version")
    if not isinstance(version, str) or not version:
        return None
    return version


def catalog_version_is_revision_key(version: str) -> bool:
    if not 7 <= len(version) <= 64:
        return False
    try:
        int(version, 16)
    except ValueError:
        return False
    return True


def inspectable_plugin_source(
    entry: PluginCatalogEntry,
) -> tuple[Path | None, str]:
    if (
        not entry.version
        or entry.version in {".", ".."}
        or "/" in entry.version
        or "\x00" in entry.version
    ):
        return None, "catalog version is not inspectable"
    source = entry.source_path
    if source is None or not source.is_absolute() or not source.is_dir():
        return None, "catalog source is not inspectable"
    try:
        resolved = source.resolve(strict=True)
    except (OSError, TypeError):
        return None, "catalog source is not inspectable"
    manifest_version = plugin_manifest_version(resolved, entry.plugin)
    if manifest_version is None:
        return None, "source manifest does not match catalog plugin identity"
    if (
        manifest_version != entry.version
        and not catalog_version_is_revision_key(entry.version)
    ):
        return None, "source manifest does not match catalog name/version"
    return resolved, ""


def _plugin_file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ignored_tree_entry(name: str, *, is_dir: bool) -> bool:
    if is_dir and name in IGNORED_TREE_DIR_NAMES:
        return True
    if not is_dir and name in IGNORED_TREE_FILE_NAMES:
        return True
    return not is_dir and name.endswith(IGNORED_TREE_FILE_SUFFIXES)


def raise_tree_walk_error(error: OSError) -> None:
    raise error


def plugin_tree_manifest(root: Path) -> dict[str, str]:
    if not root.is_dir():
        raise OSError(f"plugin tree is not a directory: {root}")
    manifest: dict[str, str] = {}
    for current_root, dir_names, file_names in os.walk(
        root,
        topdown=True,
        followlinks=False,
        onerror=raise_tree_walk_error,
    ):
        current = Path(current_root)
        retained_dirs: list[str] = []
        for name in sorted(dir_names):
            if ignored_tree_entry(name, is_dir=True):
                continue
            path = current / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                manifest[relative] = f"symlink:{os.readlink(path)}"
                continue
            manifest[relative] = "dir"
            retained_dirs.append(name)
        dir_names[:] = retained_dirs

        for name in sorted(file_names):
            if ignored_tree_entry(name, is_dir=False):
                continue
            path = current / name
            relative = path.relative_to(root).as_posix()
            if path.is_symlink():
                manifest[relative] = f"symlink:{os.readlink(path)}"
                continue
            if path.is_file():
                executable = "1" if path.stat().st_mode & 0o111 else "0"
                manifest[relative] = (
                    f"file:{executable}:{_plugin_file_sha256(path)}"
                )
                continue
            manifest[relative] = f"other:{path.lstat().st_mode}"
    return manifest


def plugin_tree_sha256(root: Path) -> str:
    """Hash the same residue-insensitive tree identity used by repair checks."""
    payload = json.dumps(
        plugin_tree_manifest(root),
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()
    return hashlib.sha256(payload).hexdigest()


def _shared_materialization_error(code: str) -> SwitchError:
    return SwitchError(f"{SHARED_MATERIALIZATION_ERROR_PREFIX}{code}")


def _desired_plugin_field(
    desired: object,
    name: str,
    default: object = None,
) -> object:
    if isinstance(desired, Mapping):
        return desired.get(name, default)
    return getattr(desired, name, default)


def _safe_cache_key(value: str) -> bool:
    return bool(
        value
        and value not in {".", ".."}
        and "\x00" not in value
        and Path(value).name == value
        and "/" not in value
        and "\\" not in value
    )


def _normalize_marketplace_config(value: object) -> Mapping[str, Any]:
    if value is None:
        return MappingProxyType({})
    if not isinstance(value, Mapping):
        raise _shared_materialization_error("unsafe_cache")
    normalized = {
        str(key): item
        for key, item in value.items()
        if str(key) not in {"name", "marketplace"}
    }
    return MappingProxyType(normalized)


def _normalize_shared_desired_plugin(
    desired: object,
) -> SharedPluginDesiredIdentity | None:
    if _desired_plugin_field(desired, "enabled", True) is False:
        return None
    selector = str(_desired_plugin_field(desired, "selector", ""))
    requirement = plugin_requirement(selector)
    if requirement is None or not all(
        _safe_cache_key(component)
        for component in (requirement.plugin, requirement.marketplace)
    ):
        raise _shared_materialization_error("unsafe_cache")
    declared_plugin = str(_desired_plugin_field(desired, "plugin", ""))
    declared_marketplace = str(
        _desired_plugin_field(desired, "marketplace", "")
    )
    if (
        (declared_plugin and declared_plugin != requirement.plugin)
        or (
            declared_marketplace
            and declared_marketplace != requirement.marketplace
        )
    ):
        raise _shared_materialization_error("unsafe_cache")
    policy = str(_desired_plugin_field(desired, "policy", ""))
    if policy not in SHARED_PLUGIN_POLICIES:
        raise _shared_materialization_error("unsafe_cache")
    cache_key = str(_desired_plugin_field(desired, "cache_key", ""))
    manifest_version = str(
        _desired_plugin_field(desired, "manifest_version", "")
    )
    tree_sha256 = str(_desired_plugin_field(desired, "tree_sha256", ""))
    marketplace_config = _desired_plugin_field(
        desired,
        "marketplace_config",
        _desired_plugin_field(desired, "marketplace_descriptor", None),
    )
    if policy == "portable_exact" and (
        not _safe_cache_key(cache_key)
        or not manifest_version
        or len(tree_sha256) != 64
        or any(character not in "0123456789abcdef" for character in tree_sha256)
    ):
        raise _shared_materialization_error("unsafe_cache")
    return SharedPluginDesiredIdentity(
        requirement=requirement,
        policy=policy,
        cache_key=cache_key,
        manifest_version=manifest_version,
        tree_sha256=tree_sha256,
        marketplace_config=_normalize_marketplace_config(marketplace_config),
    )


def _path_is_within(path: Path, root: Path) -> bool:
    try:
        path.relative_to(root)
    except ValueError:
        return False
    return True


def _validate_cache_root(home: Path) -> tuple[Path, Path]:
    try:
        resolved_home = home.expanduser().resolve(strict=True)
    except (OSError, RuntimeError):
        raise _shared_materialization_error("unsafe_cache") from None
    if not resolved_home.is_dir():
        raise _shared_materialization_error("unsafe_cache")
    plugins_root = home / "plugins"
    cache_root = plugins_root / "cache"
    for path in (plugins_root, cache_root):
        if path.is_symlink():
            raise _shared_materialization_error("unsafe_cache")
    resolved_cache = cache_root.resolve(strict=False)
    if not _path_is_within(resolved_cache, resolved_home):
        raise _shared_materialization_error("unsafe_cache")
    if cache_root.exists() and not cache_root.is_dir():
        raise _shared_materialization_error("unsafe_cache")
    return cache_root, resolved_cache


def _validate_independent_cache_roots(
    source_home: Path,
    target_home: Path,
) -> tuple[Path, Path]:
    source_cache, resolved_source = _validate_cache_root(source_home)
    target_cache, resolved_target = _validate_cache_root(target_home)
    if resolved_source == resolved_target:
        raise _shared_materialization_error("unsafe_cache")
    return source_cache, target_cache


def _validate_artifact_tree(
    root: Path,
    cache_root: Path,
    *,
    proof_error_code: str = "unsafe_cache",
) -> Path:
    try:
        root_stat = root.lstat()
    except OSError:
        raise _shared_materialization_error(proof_error_code) from None
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise _shared_materialization_error("unsafe_cache")
    try:
        resolved_cache = cache_root.resolve(strict=False)
        resolved_root = root.resolve(strict=True)
    except (OSError, RuntimeError):
        raise _shared_materialization_error(proof_error_code) from None
    if not _path_is_within(resolved_root, resolved_cache):
        raise _shared_materialization_error("unsafe_cache")

    try:
        for current_root, dir_names, file_names in os.walk(
            root,
            topdown=True,
            followlinks=False,
            onerror=raise_tree_walk_error,
        ):
            current = Path(current_root)
            for name in (*dir_names, *file_names):
                path = current / name
                path_stat = path.lstat()
                if stat.S_ISLNK(path_stat.st_mode):
                    try:
                        resolved_link = path.resolve(strict=True)
                    except (OSError, RuntimeError):
                        raise _shared_materialization_error(
                            "unsafe_cache"
                        ) from None
                    if not _path_is_within(resolved_link, resolved_root):
                        raise _shared_materialization_error("unsafe_cache")
                    continue
                if not (
                    stat.S_ISDIR(path_stat.st_mode)
                    or stat.S_ISREG(path_stat.st_mode)
                ):
                    raise _shared_materialization_error("unsafe_cache")
    except SwitchError:
        raise
    except (OSError, RuntimeError):
        raise _shared_materialization_error(proof_error_code) from None
    return resolved_root


def _plugin_manifest(
    root: Path,
    plugin: str,
    *,
    proof_error_code: str = "unsafe_cache",
) -> Mapping[str, Any]:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    try:
        manifest_stat = manifest_path.lstat()
    except OSError:
        raise _shared_materialization_error(proof_error_code) from None
    if stat.S_ISLNK(manifest_stat.st_mode) or not stat.S_ISREG(
        manifest_stat.st_mode
    ):
        raise _shared_materialization_error("unsafe_cache")
    try:
        value = json.loads(manifest_path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        raise _shared_materialization_error(proof_error_code) from None
    if not isinstance(value, dict) or value.get("name") != plugin:
        raise _shared_materialization_error(proof_error_code)
    version = value.get("version")
    if not isinstance(version, str) or not version:
        raise _shared_materialization_error(proof_error_code)
    return MappingProxyType(value)


def _plugin_skill_roots(
    root: Path,
    manifest: Mapping[str, Any],
    *,
    proof_error_code: str = "unsafe_cache",
) -> tuple[str, ...]:
    declared = manifest.get("skills", "./skills/")
    candidates: list[str] = []
    if isinstance(declared, str):
        candidates.append(declared)
    elif isinstance(declared, list) and all(
        isinstance(value, str) for value in declared
    ):
        candidates.extend(declared)
    elif declared is not None:
        raise _shared_materialization_error(proof_error_code)

    try:
        resolved_root = root.resolve(strict=True)
    except (OSError, RuntimeError):
        raise _shared_materialization_error(proof_error_code) from None
    skill_roots: set[str] = set()
    for candidate in candidates:
        relative = Path(candidate)
        if relative.is_absolute():
            raise _shared_materialization_error("unsafe_cache")
        location = root / relative
        if location.is_symlink():
            try:
                resolved_link = location.resolve(strict=True)
            except (OSError, RuntimeError):
                raise _shared_materialization_error("unsafe_cache") from None
            if not _path_is_within(resolved_link, resolved_root):
                raise _shared_materialization_error("unsafe_cache")
        if not location.exists():
            continue
        try:
            resolved_location = location.resolve(strict=True)
        except (OSError, RuntimeError):
            raise _shared_materialization_error(proof_error_code) from None
        if not _path_is_within(resolved_location, resolved_root):
            raise _shared_materialization_error("unsafe_cache")
        if resolved_location.is_file():
            if resolved_location.name != "SKILL.md":
                raise _shared_materialization_error("unsafe_cache")
            skill_roots.add(str(resolved_location.parent))
            continue
        if not resolved_location.is_dir():
            raise _shared_materialization_error(proof_error_code)
        direct_skill = resolved_location / "SKILL.md"
        if direct_skill.is_file() and not direct_skill.is_symlink():
            skill_roots.add(str(resolved_location))
        try:
            manifests = sorted(resolved_location.rglob("SKILL.md"))
        except OSError:
            raise _shared_materialization_error(proof_error_code) from None
        for skill_manifest in manifests:
            if skill_manifest.is_symlink() or not skill_manifest.is_file():
                raise _shared_materialization_error("unsafe_cache")
            resolved_skill = skill_manifest.resolve(strict=True)
            if not _path_is_within(resolved_skill, resolved_root):
                raise _shared_materialization_error("unsafe_cache")
            skill_roots.add(str(resolved_skill.parent))
    return tuple(sorted(skill_roots))


def _attest_shared_plugin_artifact(
    *,
    root: Path,
    cache_root: Path,
    identity: SharedPluginDesiredIdentity,
    require_exact: bool,
) -> dict[str, object]:
    _validate_artifact_tree(root, cache_root)
    manifest = _plugin_manifest(root, identity.requirement.plugin)
    manifest_version = str(manifest["version"])
    try:
        tree_sha256 = plugin_tree_sha256(root)
    except OSError:
        raise _shared_materialization_error("unsafe_cache") from None
    if require_exact and (
        root.name != identity.cache_key
        or manifest_version != identity.manifest_version
        or tree_sha256 != identity.tree_sha256
    ):
        raise _shared_materialization_error("unsafe_cache")
    return {
        "selector": identity.requirement.selector,
        "policy": identity.policy,
        "cache_key": root.name,
        "manifest_version": manifest_version,
        "tree_sha256": tree_sha256,
        "skill_roots": _plugin_skill_roots(root, manifest),
    }


def _attest_backend_managed_target(
    *,
    root: Path,
    cache_root: Path,
    identity: SharedPluginDesiredIdentity,
    target_cache_key: str,
) -> dict[str, object]:
    try:
        root_stat = root.lstat()
    except FileNotFoundError:
        raise _shared_materialization_error("unverified_target") from None
    except OSError:
        raise _shared_materialization_error("unverified_target") from None
    if stat.S_ISLNK(root_stat.st_mode) or not stat.S_ISDIR(root_stat.st_mode):
        raise _shared_materialization_error("unsafe_cache")

    _validate_artifact_tree(
        root,
        cache_root,
        proof_error_code="unverified_target",
    )
    manifest = _plugin_manifest(
        root,
        identity.requirement.plugin,
        proof_error_code="unverified_target",
    )
    manifest_version = str(manifest["version"])
    if (
        target_cache_key != manifest_version
        and not catalog_version_is_revision_key(target_cache_key)
    ):
        raise _shared_materialization_error("unverified_target")
    try:
        tree_sha256 = plugin_tree_sha256(root)
    except OSError:
        raise _shared_materialization_error("unverified_target") from None
    return {
        "selector": identity.requirement.selector,
        "policy": identity.policy,
        "cache_key": target_cache_key,
        "manifest_version": manifest_version,
        "tree_sha256": tree_sha256,
        "skill_roots": _plugin_skill_roots(
            root,
            manifest,
            proof_error_code="unverified_target",
        ),
    }


def _toml_key_segment(value: str) -> str:
    if value and all(
        character.isascii()
        and (character.isalnum() or character in {"_", "-"})
        for character in value
    ):
        return value
    return json.dumps(value, ensure_ascii=False)


def _toml_inline_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_inline_value(item) for item in value) + "]"
    if isinstance(value, Mapping):
        entries = ", ".join(
            f"{_toml_key_segment(str(key))} = {_toml_inline_value(item)}"
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        )
        return "{ " + entries + " }"
    raise _shared_materialization_error("unsafe_cache")


def _shared_marketplace_config_args(
    identities: tuple[SharedPluginDesiredIdentity, ...],
) -> list[str]:
    by_marketplace: dict[str, Mapping[str, Any]] = {}
    for identity in identities:
        if not identity.marketplace_config:
            continue
        marketplace = identity.requirement.marketplace
        previous = by_marketplace.get(marketplace)
        if previous is not None and dict(previous) != dict(identity.marketplace_config):
            raise _shared_materialization_error("unsafe_cache")
        by_marketplace[marketplace] = identity.marketplace_config

    args: list[str] = []
    for marketplace, config in sorted(by_marketplace.items()):
        prefix = f"marketplaces.{_toml_key_segment(marketplace)}"
        for key, value in sorted(config.items(), key=lambda pair: str(pair[0])):
            args.extend(
                (
                    "-c",
                    f"{prefix}.{_toml_key_segment(str(key))}="
                    f"{_toml_inline_value(value)}",
                )
            )
    return args


def _shared_available_catalog(
    *,
    runtime: PluginMaintenanceRuntime,
    config_args: list[str],
    store_lock_descriptor: int,
) -> CatalogResult:
    # Shared preflight may consume only the target backend's configured
    # snapshot. Marketplace upgrade remains an explicit repair operation.
    try:
        result = _capture_profile_command(
            codex_bin=runtime.codex_bin,
            home=runtime.home,
            args=[*config_args, "plugin", "list", "--available", "--json"],
            pass_fds=(store_lock_descriptor,),
        )
    except (OSError, SwitchError) as error:
        raise _shared_materialization_error("unverified_catalog") from error
    catalog = available_plugin_catalog(
        result.stdout,
        stderr=result.stderr,
        returncode=result.returncode,
    )
    if not catalog.verified:
        raise _shared_materialization_error("unverified_catalog")
    return catalog


def _catalog_source_is_exact(
    identity: SharedPluginDesiredIdentity,
    entry: PluginCatalogEntry,
) -> bool:
    source = entry.source_path
    if (
        source is None
        or not source.is_absolute()
        or source.is_symlink()
        or not source.is_dir()
    ):
        raise _shared_materialization_error("unsafe_cache")
    try:
        source = source.resolve(strict=True)
    except (OSError, RuntimeError):
        raise _shared_materialization_error("unsafe_cache") from None
    _validate_artifact_tree(
        source,
        source,
        proof_error_code="source_mismatch",
    )
    manifest = _plugin_manifest(
        source,
        identity.requirement.plugin,
        proof_error_code="source_mismatch",
    )
    try:
        tree_sha256 = plugin_tree_sha256(source)
    except OSError:
        raise _shared_materialization_error("source_mismatch") from None
    return (
        str(manifest["version"]) == identity.manifest_version
        and tree_sha256 == identity.tree_sha256
    )


def _shared_target_changed_error() -> SwitchError:
    return SwitchError("shared_configuration.target_changed_during_plan")


def _shared_target_config_snapshot(path: Path) -> _SharedTargetConfigSnapshot:
    try:
        before_stat = path.lstat()
    except FileNotFoundError:
        return _SharedTargetConfigSnapshot(exists=False)
    except OSError:
        raise _shared_target_changed_error() from None
    if stat.S_ISLNK(before_stat.st_mode) or not stat.S_ISREG(before_stat.st_mode):
        raise _shared_target_changed_error()
    try:
        data = path.read_bytes()
        after_stat = path.lstat()
        text = data.decode()
        validate_toml_text(text, str(path))
    except (OSError, UnicodeDecodeError, SwitchError):
        raise _shared_target_changed_error() from None
    before_identity = (
        before_stat.st_dev,
        before_stat.st_ino,
        before_stat.st_size,
        before_stat.st_mtime_ns,
        before_stat.st_mode,
    )
    after_identity = (
        after_stat.st_dev,
        after_stat.st_ino,
        after_stat.st_size,
        after_stat.st_mtime_ns,
        after_stat.st_mode,
    )
    if before_identity != after_identity:
        raise _shared_target_changed_error()
    return _SharedTargetConfigSnapshot(
        exists=True,
        data=data,
        mode=stat.S_IMODE(after_stat.st_mode),
    )


def _selector_table_spans(
    text: str,
    selector: str,
) -> tuple[list[str], tuple[tuple[int, int], ...]]:
    lines = text.splitlines(keepends=True)
    starts: list[int] = []
    target_starts: list[int] = []
    for index, line in enumerate(lines):
        table = toml_table_name(line)
        if table is None:
            continue
        starts.append(index)
        if (
            not line.lstrip().startswith("[[")
            and plugin_selector_from_table(table) == selector
        ):
            target_starts.append(index)
    spans: list[tuple[int, int]] = []
    for start in target_starts:
        end = len(lines)
        for next_start in starts:
            if next_start > start:
                end = next_start
                break
        spans.append((start, end))
    return lines, tuple(spans)


def _exact_added_activation_table(lines: list[str]) -> bool:
    if not lines:
        return False
    header = lines[0].strip()
    if not header or commentless_line(lines[0]).strip() != header:
        return False
    enabled_count = 0
    for line in lines[1:]:
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("#") or commentless_line(line).strip() != stripped:
            return False
        if assignment_bool(line, "enabled") is not True:
            return False
        enabled_count += 1
    return enabled_count == 1


def _restore_existing_activation_table(
    before_lines: list[str],
    after_lines: list[str],
) -> str | None:
    before_enabled = [
        index
        for index, line in enumerate(before_lines[1:], start=1)
        if assignment_bool(line, "enabled") is not None
    ]
    after_enabled = [
        index
        for index, line in enumerate(after_lines[1:], start=1)
        if assignment_bool(line, "enabled") is not None
    ]
    if len(after_enabled) != 1:
        return None
    after_index = after_enabled[0]
    if assignment_bool(after_lines[after_index], "enabled") is not True:
        return None

    if len(before_enabled) == 1:
        before_index = before_enabled[0]
        if assignment_bool(before_lines[before_index], "enabled") is not False:
            return None
        candidate = list(after_lines)
        candidate[after_index] = before_lines[before_index]
        if "".join(candidate) == "".join(before_lines):
            return "".join(before_lines)
        return None

    if before_enabled:
        return None
    candidate = list(after_lines)
    del candidate[after_index]
    if "".join(candidate) == "".join(before_lines):
        return "".join(before_lines)
    return None


def _scrub_expected_plugin_activation(
    *,
    before: bytes,
    after: bytes,
    selector: str,
) -> bytes | None:
    try:
        before_text = before.decode()
        after_text = after.decode()
        validate_toml_text(before_text, "shared target config before native add")
        validate_toml_text(after_text, "shared target config after native add")
    except (UnicodeDecodeError, SwitchError):
        return None

    before_lines, before_spans = _selector_table_spans(before_text, selector)
    after_lines, after_spans = _selector_table_spans(after_text, selector)
    if len(after_spans) != 1 or len(before_spans) > 1:
        return None

    after_start, after_end = after_spans[0]
    if not before_spans:
        if not _exact_added_activation_table(after_lines[after_start:after_end]):
            return None
        prefix = "".join(after_lines[:after_start])
        suffix = "".join(after_lines[after_end:])
        removal_prefix = prefix
        if prefix.startswith(before_text):
            inserted_spacing = prefix[len(before_text) :]
            if inserted_spacing and not inserted_spacing.strip():
                removal_prefix = before_text
        scrubbed = removal_prefix + suffix
    else:
        before_start, before_end = before_spans[0]
        restored_table = _restore_existing_activation_table(
            before_lines[before_start:before_end],
            after_lines[after_start:after_end],
        )
        if restored_table is None:
            return None
        scrubbed = (
            "".join(after_lines[:after_start])
            + restored_table
            + "".join(after_lines[after_end:])
        )

    try:
        validate_toml_text(scrubbed, "shared target config after selector restore")
    except SwitchError:
        return None
    return scrubbed.encode()


def _scrub_expected_plugin_activations(
    *,
    before: bytes,
    after: bytes,
    selectors: tuple[str, ...],
) -> tuple[bytes, bool] | None:
    """Remove only exact native-add activation deltas for bounded selectors.

    ``None`` means a bounded selector changed in a way that cannot be proven to
    be the native add operation's exact activation.  A successful result keeps
    all non-selector bytes from ``after`` and reports whether any bounded
    activation was removed.
    """
    try:
        before_text = before.decode()
        after_text = after.decode()
        validate_toml_text(before_text, "shared target config before native add")
        validate_toml_text(after_text, "shared target config after native add")
    except (UnicodeDecodeError, SwitchError):
        return None

    normalized = tuple(sorted(set(selectors)))
    if len(normalized) != len(selectors) or any(
        plugin_requirement(selector) is None for selector in normalized
    ):
        return None

    scrubbed = after
    changed = False
    for selector in normalized:
        try:
            current_text = scrubbed.decode()
        except UnicodeDecodeError:
            return None
        before_lines, before_spans = _selector_table_spans(before_text, selector)
        current_lines, current_spans = _selector_table_spans(current_text, selector)
        before_tables = tuple(
            "".join(before_lines[start:end]).rstrip()
            for start, end in before_spans
        )
        current_tables = tuple(
            "".join(current_lines[start:end]).rstrip()
            for start, end in current_spans
        )
        if current_tables == before_tables:
            continue
        candidate = _scrub_expected_plugin_activation(
            before=before,
            after=scrubbed,
            selector=selector,
        )
        if candidate is None:
            return None
        scrubbed = candidate
        changed = True
    return scrubbed, changed


def _replace_shared_target_config_if_unchanged(
    *,
    path: Path,
    observed: _SharedTargetConfigSnapshot,
    data: bytes,
    mode: int,
) -> None:
    if _shared_target_config_snapshot(path) != observed:
        raise _shared_target_changed_error()
    try:
        atomic_write(path, data, mode=mode)
    except OSError:
        raise _shared_materialization_error("failed") from None


def _restore_native_add_config(
    *,
    config_path: Path,
    selector: str,
    before: _SharedTargetConfigSnapshot,
) -> None:
    after = _shared_target_config_snapshot(config_path)
    if after == before:
        return
    if not after.exists:
        raise _shared_target_changed_error()

    scrubbed = _scrub_expected_plugin_activation(
        before=before.data if before.exists else b"",
        after=after.data,
        selector=selector,
    )
    if scrubbed is None:
        raise _shared_target_changed_error()

    only_expected_delta = (
        before.exists
        and scrubbed == before.data
        and after.mode == before.mode
    )
    if only_expected_delta:
        _replace_shared_target_config_if_unchanged(
            path=config_path,
            observed=after,
            data=before.data,
            mode=before.mode,
        )
        if _shared_target_config_snapshot(config_path) != before:
            raise _shared_target_changed_error()
        return

    if not before.exists and not scrubbed.strip():
        if _shared_target_config_snapshot(config_path) != after:
            raise _shared_target_changed_error()
        try:
            config_path.unlink()
            parent_descriptor = os.open(
                config_path.parent,
                os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
            )
            try:
                os.fsync(parent_descriptor)
            finally:
                os.close(parent_descriptor)
        except OSError:
            raise _shared_materialization_error("failed") from None
        if _shared_target_config_snapshot(config_path) != before:
            raise _shared_target_changed_error()
        return

    _replace_shared_target_config_if_unchanged(
        path=config_path,
        observed=after,
        data=scrubbed,
        mode=after.mode,
    )
    raise _shared_target_changed_error()


def _native_add_shared_plugin_preserving_config(
    *,
    runtime: PluginMaintenanceRuntime,
    config_args: list[str],
    identity: SharedPluginDesiredIdentity,
    store_lock_descriptor: int,
) -> None:
    config_path = runtime.home / "config.toml"
    before = _shared_target_config_snapshot(config_path)
    try:
        _native_add_shared_plugin(
            runtime=runtime,
            config_args=config_args,
            identity=identity,
            store_lock_descriptor=store_lock_descriptor,
        )
    except BaseException:
        _restore_native_add_config(
            config_path=config_path,
            selector=identity.requirement.selector,
            before=before,
        )
        raise
    _restore_native_add_config(
        config_path=config_path,
        selector=identity.requirement.selector,
        before=before,
    )


def _native_add_shared_plugin(
    *,
    runtime: PluginMaintenanceRuntime,
    config_args: list[str],
    identity: SharedPluginDesiredIdentity,
    store_lock_descriptor: int,
) -> None:
    try:
        result = _capture_profile_command(
            codex_bin=runtime.codex_bin,
            home=runtime.home,
            args=[
                *config_args,
                "plugin",
                "add",
                identity.requirement.selector,
                "--json",
            ],
            pass_fds=(store_lock_descriptor,),
        )
    except (OSError, SwitchError) as error:
        raise _shared_materialization_error("failed") from error
    if result.returncode != 0:
        raise _shared_materialization_error("failed")


def _validate_shared_materializer_lease(store: Store, descriptor: object) -> int:
    """Bind the private inherited lease to this materializer's exact store."""
    if (
        isinstance(descriptor, bool)
        or not isinstance(descriptor, int)
        or descriptor < 0
    ):
        raise _shared_materialization_error("failed")
    try:
        locked = os.fstat(descriptor)
        current = store.root.lstat()
    except OSError as error:
        raise _shared_materialization_error("failed") from error
    if (
        stat.S_ISLNK(current.st_mode)
        or not stat.S_ISDIR(current.st_mode)
        or not stat.S_ISDIR(locked.st_mode)
        or (current.st_dev, current.st_ino) != (locked.st_dev, locked.st_ino)
    ):
        raise _shared_materialization_error("failed")
    return descriptor


def materialize_shared_plugins(
    *,
    store: Store,
    selection: object,
    source_profile: str,
    target_profile: str,
    desired_plugins: tuple[object, ...],
    generation: int,
    _store_lock_descriptor: object = None,
) -> tuple[dict[str, object], ...]:
    """Materialize one desired generation with the target profile backend.

    This adapter never directly copies, links, deletes, garbage-collects, or
    recreates Plugin cache artifacts, and it never publishes the target config.
    Native backend commands own their installed-version cache lifecycle and may
    replace prior versions. Desired marketplace values are temporary command
    overrides; every returned receipt is rebuilt from the fresh target tree.
    """
    del selection
    store_lock_descriptor = _validate_shared_materializer_lease(
        store,
        _store_lock_descriptor,
    )
    if (
        source_profile == target_profile
        or {source_profile, target_profile} != PRODUCT_PROFILES
    ):
        raise _shared_materialization_error("failed")
    if not isinstance(generation, int) or generation < 1:
        raise _shared_materialization_error("failed")
    identities = tuple(
        identity
        for identity in (
            _normalize_shared_desired_plugin(desired)
            for desired in desired_plugins
        )
        if identity is not None
    )
    if len({identity.requirement.selector for identity in identities}) != len(
        identities
    ):
        raise _shared_materialization_error("unsafe_cache")
    if not identities:
        return ()

    try:
        source_home = profile_home(store, source_profile)
        target_home = profile_home(store, target_profile)
        _source_cache, target_cache = _validate_independent_cache_roots(
            source_home,
            target_home,
        )
    except SwitchError as error:
        if str(error).startswith(SHARED_MATERIALIZATION_ERROR_PREFIX):
            raise
        raise _shared_materialization_error("unsafe_cache") from error

    receipts: dict[str, dict[str, object]] = {}
    pending: list[SharedPluginDesiredIdentity] = []
    for identity in identities:
        if identity.policy != "portable_exact":
            pending.append(identity)
            continue
        if not _safe_cache_key(identity.cache_key):
            pending.append(identity)
            continue
        candidate = (
            target_cache
            / identity.requirement.marketplace
            / identity.requirement.plugin
            / identity.cache_key
        )
        if not candidate.exists():
            pending.append(identity)
            continue
        if candidate.is_symlink() or not candidate.is_dir():
            raise _shared_materialization_error("unsafe_cache")
        _validate_artifact_tree(candidate, target_cache)
        try:
            receipt = _attest_shared_plugin_artifact(
                root=candidate,
                cache_root=target_cache,
                identity=identity,
                require_exact=identity.policy == "portable_exact",
            )
        except SwitchError:
            pending.append(identity)
            continue
        receipts[identity.requirement.selector] = receipt

    if not pending:
        return tuple(
            receipts[identity.requirement.selector] for identity in identities
        )

    try:
        runtime = profile_plugin_runtime(store, target_profile)
    except SwitchError as error:
        raise _shared_materialization_error("failed") from error
    try:
        runtime_home = runtime.home.expanduser().resolve(strict=False)
        expected_home = target_home.expanduser().resolve(strict=False)
    except (OSError, RuntimeError) as error:
        raise _shared_materialization_error("unsafe_cache") from error
    if runtime_home != expected_home:
        raise _shared_materialization_error("unsafe_cache")

    config_args = _shared_marketplace_config_args(identities)
    catalog = _shared_available_catalog(
        runtime=runtime,
        config_args=config_args,
        store_lock_descriptor=store_lock_descriptor,
    )
    for identity in pending:
        entry = catalog.entries.get(identity.requirement.selector)
        if entry is None:
            raise _shared_materialization_error("unavailable")
        if (
            identity.policy == "portable_exact"
            and not _safe_cache_key(entry.version)
        ):
            raise _shared_materialization_error("unsafe_cache")
        if not _catalog_source_is_exact(identity, entry):
            raise _shared_materialization_error("source_mismatch")

    try:
        running_pids = running_target_app_server_pids(store, runtime)
    except (OSError, SwitchError) as error:
        raise _shared_materialization_error("failed") from error
    if running_pids:
        raise _shared_materialization_error("running_process")

    backend_pending: list[SharedPluginDesiredIdentity] = []
    for identity in pending:
        if identity.policy == "backend_managed":
            backend_pending.append(identity)
            continue
        target_key = identity.cache_key
        candidate = (
            target_cache
            / identity.requirement.marketplace
            / identity.requirement.plugin
            / target_key
        )
        needs_add = True
        if candidate.exists():
            if candidate.is_symlink() or not candidate.is_dir():
                raise _shared_materialization_error("unsafe_cache")
            _validate_artifact_tree(candidate, target_cache)
            try:
                current = _attest_shared_plugin_artifact(
                    root=candidate,
                    cache_root=target_cache,
                    identity=identity,
                    require_exact=identity.policy == "portable_exact",
                )
            except SwitchError:
                current = None
            if current is not None:
                needs_add = False
        if needs_add:
            _native_add_shared_plugin_preserving_config(
                runtime=runtime,
                config_args=config_args,
                identity=identity,
                store_lock_descriptor=store_lock_descriptor,
            )

        receipts[identity.requirement.selector] = _attest_shared_plugin_artifact(
            root=candidate,
            cache_root=target_cache,
            identity=identity,
            require_exact=identity.policy == "portable_exact",
        )

    for identity in backend_pending:
        _native_add_shared_plugin_preserving_config(
            runtime=runtime,
            config_args=config_args,
            identity=identity,
            store_lock_descriptor=store_lock_descriptor,
        )

    if backend_pending:
        post_catalog = _shared_available_catalog(
            runtime=runtime,
            config_args=config_args,
            store_lock_descriptor=store_lock_descriptor,
        )
        for identity in backend_pending:
            entry = post_catalog.entries.get(identity.requirement.selector)
            if (
                entry is None
                or not entry.installed_record_seen
                or len(entry.installed_versions) != 1
            ):
                raise _shared_materialization_error("unverified_target")
            target_key = entry.installed_versions[0]
            if not _safe_cache_key(target_key):
                raise _shared_materialization_error("unsafe_cache")
            candidate = (
                target_cache
                / identity.requirement.marketplace
                / identity.requirement.plugin
                / target_key
            )
            receipts[
                identity.requirement.selector
            ] = _attest_backend_managed_target(
                root=candidate,
                cache_root=target_cache,
                identity=identity,
                target_cache_key=target_key,
            )

    return tuple(
        receipts[identity.requirement.selector] for identity in identities
    )


def classify_installed_plugin_cache(
    home: Path,
    requirement: PluginRequirement,
    entry: PluginCatalogEntry,
) -> tuple[str, str]:
    source, problem = inspectable_plugin_source(entry)
    if source is None:
        return "uninspectable", problem
    cache = plugin_cache_path(home, requirement) / entry.version
    if cache.is_symlink() or not cache.is_dir():
        return "stale", "catalog-version cache is missing"
    source_manifest_version = plugin_manifest_version(source, entry.plugin)
    cache_manifest_version = plugin_manifest_version(cache, entry.plugin)
    if cache_manifest_version is None:
        return "stale", "catalog-version cache marker is invalid"
    if source_manifest_version != cache_manifest_version:
        return "uninspectable", "source and cache manifest versions differ"
    try:
        matches = plugin_tree_manifest(source) == plugin_tree_manifest(cache)
    except OSError:
        return "uninspectable", "source or cache tree could not be inspected"
    if matches:
        return "current", ""
    return "stale", "installed cache differs from catalog source"


def running_target_app_server_pids(
    store: Store,
    runtime: PluginMaintenanceRuntime,
) -> list[int]:
    binding = runtime.binding
    if binding is None:
        return []
    observation = collect_store_runtime_observation(store, binding)
    pids: list[int] = []
    for process in observation.processes:
        if getattr(process, "kind", "") != "app-server":
            continue
        if app_server_matches_expected_cli(
            process,
            str(binding.desktop_cli),
        ) or app_server_matches_expected_cli(
            process,
            str(binding.backend_cli),
        ):
            pids.append(int(getattr(process, "pid", 0)))
    return [pid for pid in pids if pid > 0]


def build_plugin_repair_plan(
    *,
    profile: str,
    home: Path,
    requirements: list[PluginRequirement],
    catalog: CatalogResult | None,
    disable_unavailable: bool = False,
) -> PluginRepairPlan:
    missing: list[PluginRequirement] = []
    installed: list[PluginRequirement] = []
    for requirement in requirements:
        if plugin_is_installed(home, requirement):
            installed.append(requirement)
        else:
            missing.append(requirement)

    if catalog is None or not catalog.verified:
        return PluginRepairPlan(
            profile=profile,
            catalog_verified=False,
            conditional_install=tuple(missing),
            installed=tuple(installed),
        )

    catalog_entries = catalog.entries
    available_selectors = set(catalog_entries)
    installable = [
        requirement
        for requirement in missing
        if requirement.selector in available_selectors
    ]
    unavailable = [
        requirement
        for requirement in missing
        if requirement.selector not in available_selectors
    ]
    current: list[PluginRequirement] = []
    stale: list[PluginRequirement] = []
    diagnostics: list[str] = []
    for requirement in installed:
        entry = catalog_entries.get(requirement.selector)
        if entry is None:
            diagnostics.append(
                f"Skipping stale-cache check for {requirement.selector}: "
                "selector is not present in the refreshed plugin catalog"
            )
            continue
        status, detail = classify_installed_plugin_cache(home, requirement, entry)
        if status == "current":
            current.append(requirement)
            diagnostics.append(f"Plugin cache current: {requirement.selector}")
        elif status == "stale":
            stale.append(requirement)
            diagnostics.append(
                f"Stale plugin cache detected: {requirement.selector} ({detail})"
            )
        else:
            diagnostics.append(
                f"Skipping stale-cache check for {requirement.selector}: {detail}"
            )

    return PluginRepairPlan(
        profile=profile,
        catalog_verified=True,
        installed=tuple(installed),
        install=tuple(installable),
        unavailable=tuple(unavailable),
        disable=tuple(unavailable) if disable_unavailable else (),
        refresh=tuple(stale),
        current=tuple(current),
        diagnostics=tuple(diagnostics),
    )


def print_plugin_repair_plan(
    plan: PluginRepairPlan,
    *,
    dry_run: bool,
    disable_unavailable: bool,
) -> None:
    if dry_run:
        if not plan.conditional_install:
            print(f"No missing enabled plugins for {plan.profile}")
        print(
            "Dry run: plugin catalog is not inspected; missing enabled plugins "
            "will only be installed when they appear in the refreshed available catalog."
        )
        for requirement in plan.conditional_install:
            print(f"Dry run: would install if available: {requirement.selector}")
        if disable_unavailable:
            print(
                "Dry run: would disable unavailable enabled plugins only after "
                "a real catalog refresh proves they are unavailable."
            )
        if plan.installed:
            print(
                "Dry run: installed enabled plugin caches are not compared; "
                "inspectable caches would be refreshed only when they differ "
                "from the real refreshed catalog source."
            )
        return

    if not plan.install and not plan.unavailable:
        print(f"No missing enabled plugins for {plan.profile}")
    for requirement in plan.unavailable:
        print(
            f"Skipping unavailable enabled plugin: {requirement.selector} "
            "(not found in available plugin catalog)"
        )
    for diagnostic in plan.diagnostics:
        print(diagnostic)


def apply_plugin_repair_plan(
    plan: PluginRepairPlan,
    *,
    runtime: PluginMaintenanceRuntime,
) -> None:
    if not plan.catalog_verified:
        raise SwitchError(
            f"{plan.profile}: refusing to apply an unverified plugin repair plan"
        )

    if plan.disable:
        for requirement in plan.disable:
            print(f"Disabling unavailable enabled plugin: {requirement.selector}")
        apply_plugin_config_updates(plan.config_updates)
        for update in plan.config_updates:
            print(f"Updated plugin config: {update.path}")

    for requirement in plan.install:
        print(f"Installing plugin: {requirement.selector}")
        run_profile_plugin_command(
            name=plan.profile,
            codex_bin=runtime.codex_bin,
            home=runtime.home,
            args=["add", requirement.selector],
            description=f"install plugin {requirement.selector}",
        )
    for requirement in plan.refresh:
        print(f"Refreshing stale plugin cache: {requirement.selector}")
        run_profile_plugin_command(
            name=plan.profile,
            codex_bin=runtime.codex_bin,
            home=runtime.home,
            args=["add", requirement.selector],
            description=f"refresh stale plugin {requirement.selector}",
        )


def repair_profile_plugins(
    store: Store,
    name: str,
    *,
    dry_run: bool = False,
    disable_unavailable: bool = False,
) -> PluginRepairPlan:
    runtime = profile_plugin_runtime(store, name)
    codex_bin = runtime.codex_bin
    home = runtime.home
    verify_profile_plugin_runtime(
        name=name,
        codex_bin=codex_bin,
        home=home,
        dry_run=dry_run,
    )
    catalog = refresh_profile_plugin_catalogs(
        name=name,
        codex_bin=codex_bin,
        home=home,
        dry_run=dry_run,
    )
    requirements = enabled_plugin_requirements(home / "config.toml")
    plan = build_plugin_repair_plan(
        profile=name,
        home=home,
        requirements=requirements,
        catalog=catalog,
        disable_unavailable=disable_unavailable,
    )
    if dry_run:
        print_plugin_repair_plan(
            plan,
            dry_run=True,
            disable_unavailable=disable_unavailable,
        )
        return plan

    if not plan.catalog_verified:
        status = catalog.status if catalog is not None else "not_run"
        detail = catalog.detail if catalog is not None else "catalog not run"
        raise SwitchError(
            f"{name}: plugin catalog is unverified ({status}): {detail}"
        )
    if catalog.stderr.strip():
        print(
            f"Plugin catalog for {name}: verified with stderr diagnostics."
        )
    print_plugin_repair_plan(
        plan,
        dry_run=False,
        disable_unavailable=disable_unavailable,
    )
    if plan.refresh:
        running_pids = running_target_app_server_pids(store, runtime)
        if running_pids:
            selectors = ", ".join(
                requirement.selector for requirement in plan.refresh
            )
            pid_text = ", ".join(str(pid) for pid in running_pids)
            raise SwitchError(
                f"{name}: target profile {name} app-server is running "
                f"(pid {pid_text}); refusing to hot-replace stale plugin "
                f"cache(s): {selectors}. Quit ChatGPT completely, rerun "
                f"codex-switch repair-plugins {name}, then reopen ChatGPT."
            )

    if plan.disable:
        config_updates = build_plugin_config_updates(
            store,
            name,
            home,
            list(plan.disable),
        )
        plan = replace(plan, config_updates=config_updates)
    apply_plugin_repair_plan(plan, runtime=runtime)
    return plan


def cmd_repair_plugins(args) -> None:
    repair_profile_plugins(
        make_store(args),
        args.name,
        dry_run=args.dry_run,
        disable_unavailable=args.disable_unavailable,
    )
