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
    command = [str(codex_bin), *args]
    if dry_run:
        print("Dry run:", " ".join(command))
        return ProfileCommandResult(stdout="", stderr="", returncode=0)
    env = dict(os.environ)
    env["CODEX_HOME"] = str(home)
    result = subprocess.run(
        command,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env,
    )
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


def plugin_catalog_entry(value: dict[str, Any]) -> PluginCatalogEntry | None:
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
    return PluginCatalogEntry(
        selector=requirement.selector,
        plugin=requirement.plugin,
        marketplace=requirement.marketplace,
        version=version,
        source_path=source_path,
    )


def collect_available_plugin_catalog(
    value: Any,
    entries: dict[str, PluginCatalogEntry],
) -> None:
    if isinstance(value, list):
        for item in value:
            collect_available_plugin_catalog(item, entries)
        return
    if not isinstance(value, dict):
        return

    entry = plugin_catalog_entry(value)
    if entry is not None:
        previous = entries.get(entry.selector)
        if previous is None:
            entries[entry.selector] = entry
        else:
            entries[entry.selector] = PluginCatalogEntry(
                selector=entry.selector,
                plugin=entry.plugin,
                marketplace=entry.marketplace,
                version=entry.version or previous.version,
                source_path=entry.source_path or previous.source_path,
            )

    for key in ("installed", "available", "plugins", "items", "data"):
        collect_available_plugin_catalog(value.get(key), entries)


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
