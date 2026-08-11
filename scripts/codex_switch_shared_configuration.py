from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import stat
import sys
import urllib.parse
from collections.abc import Callable, Mapping, Sequence
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any

from codex_switch_config_document import ConfigDocument
from codex_switch_constants import SwitchError
from codex_switch_io import atomic_write, read_json, run_quiet, write_json
from codex_switch_selection import ProfileSelection, active_profile_selection
from codex_switch_store import Store, make_store

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - Python < 3.11 fallback
    tomllib = None  # type: ignore[assignment]


SHARED_CONFIGURATION_SCHEMA = 1
SHARED_CONFIGURATION_DIRECTORY = "shared-configuration"
OFFICIAL_PROFILE = "openai-official"
INTERNAL_PROFILE = "internal"
SUPPORTED_SELECTION = (INTERNAL_PROFILE, OFFICIAL_PROFILE)
SHARED_TABLE_ROOTS = frozenset({"marketplaces", "plugins"})
MARKETPLACE_IGNORED_FIELDS = frozenset({"last_updated"})
MARKETPLACE_SAFE_FIELDS = frozenset(
    {
        "source",
        "source_type",
        "last_revision",
        "ref",
        "sparse_paths",
    }
)
MARKETPLACE_SOURCE_SAFE_FIELDS = frozenset(
    {"source", "source_type", "path", "url", "ref", "revision"}
)
SECRET_FIELD_RE = re.compile(
    r"(?:^|[_-])(token|secret|password|passwd|credential|api[_-]?key|"
    r"access[_-]?key|private[_-]?key|client[_-]?secret|authorization|bearer|auth)"
    r"(?:$|[_-])",
    re.IGNORECASE,
)
FINDING_CODE_RE = re.compile(r"shared_configuration(?:\.[a-z0-9_]+)+")
BARE_TOML_KEY_RE = re.compile(r"^[A-Za-z0-9_-]+$")
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
PENDING_COMMIT_NAME = "pending-commit.json"
PENDING_COMMIT_SCHEMA = 1
PENDING_MATERIALIZATION_NAME = "pending-materialization.json"
PENDING_MATERIALIZATION_SCHEMA = 1


@dataclass(frozen=True)
class SharedConfigurationFinding:
    code: str
    severity: str
    message: str


@dataclass(frozen=True)
class SharedDesiredPlugin:
    selector: str
    enabled: bool
    policy: str
    marketplace: str
    plugin: str
    marketplace_config: Mapping[str, Any]
    cache_key: str = ""
    manifest_version: str = ""
    tree_sha256: str = ""
    skill_roots: tuple[str, ...] = ()
    source_artifact: str = ""
    source_identity_sha256: str = ""


@dataclass(frozen=True)
class SharedPluginMaterialization:
    selector: str
    policy: str
    cache_key: str
    manifest_version: str
    tree_sha256: str
    skill_roots: tuple[str, ...] = ()


@dataclass(frozen=True)
class SharedConfigurationReceipt:
    status: str
    generation_before: int
    generation_after: int
    cli_ready: bool
    pending_target: str | None = None
    materializations: tuple[SharedPluginMaterialization, ...] = ()
    findings: tuple[SharedConfigurationFinding, ...] = ()
    source_profile: str | None = None
    target_profile: str | None = None
    actions: tuple[str, ...] = ()

    @property
    def generation(self) -> int:
        return self.generation_after


def _default_read_stable(path: Path) -> str:
    for _attempt in range(3):
        try:
            before = path.stat()
            text = path.read_text()
            after = path.stat()
        except FileNotFoundError:
            return ""
        if (
            before.st_dev,
            before.st_ino,
            before.st_size,
            before.st_mtime_ns,
        ) == (
            after.st_dev,
            after.st_ino,
            after.st_size,
            after.st_mtime_ns,
        ):
            return text
    raise SwitchError("shared_configuration.source_changed_during_plan")


def _default_app_is_running(store: Store, selection: ProfileSelection) -> bool:
    try:
        from codex_switch_plugins import (
            profile_plugin_runtime,
            running_target_app_server_pids,
        )

        code, output = run_quiet(["/bin/ps", "-axo", "pid=,ppid=,args="])
        if code != 0:
            return True
        process_reader = globals().get("running_codex_processes")
        if process_reader is None:
            from codex_switch_running_app import running_codex_processes as process_reader
        processes = process_reader(process_output=output)
        if any(
            getattr(process, "kind", "") in {"desktop", "app-server"}
            for process in processes
        ):
            return True
        runtime = profile_plugin_runtime(store, selection.app_profile)
        return bool(running_target_app_server_pids(store, runtime))
    except Exception:
        # A stopped-App apply must be proved; an unreadable runtime is not proof.
        return True


def _default_materialize_plugins(**kwargs: Any) -> tuple[dict[str, object], ...]:
    from codex_switch_plugins import materialize_shared_plugins

    return materialize_shared_plugins(**kwargs)


def _default_before_commit(**_kwargs: Any) -> None:
    return None


def _default_commit_checkpoint(**_kwargs: Any) -> None:
    return None


def _default_progress(_message: str) -> None:
    return None


def _stderr_progress(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


@dataclass(frozen=True)
class SharedConfigurationAdapters:
    read_stable: Callable[[Path], str] = _default_read_stable
    app_is_running: Callable[[Store, ProfileSelection], bool] = _default_app_is_running
    materialize_plugins: Callable[..., Sequence[object]] = _default_materialize_plugins
    before_commit: Callable[..., None] = _default_before_commit
    commit_checkpoint: Callable[..., None] = _default_commit_checkpoint
    progress: Callable[[str], None] = _default_progress


def _report_progress(adapters: object, message: str) -> None:
    callback = getattr(adapters, "progress", _default_progress)
    callback(message)


def _app_running(
    adapters: object,
    store: Store,
    selection: ProfileSelection,
) -> bool:
    callback = getattr(adapters, "app_is_running", _default_app_is_running)
    try:
        return bool(callback(store, selection))
    except Exception:
        return True


@dataclass(frozen=True)
class _HomeObservation:
    profile: str
    home: Path
    raw_text: str
    raw_sha256: str
    projection: dict[str, Any]
    projection_sha256: str
    desired_plugins: tuple[SharedDesiredPlugin, ...]
    observation_sha256: str
    config_kind: str
    config_mode: int


@dataclass(frozen=True)
class _ConfigSnapshot:
    kind: str
    payload: bytes
    mode: int

    @property
    def sha256(self) -> str:
        return _sha256_bytes(self.payload)


@dataclass(frozen=True)
class _ReconcilePlan:
    status: str
    generation_before: int
    generation_after: int
    source_profile: str | None
    target_profile: str | None
    source_observation: _HomeObservation | None
    target_observation: _HomeObservation | None
    projection: dict[str, Any] | None
    desired_plugins: tuple[SharedDesiredPlugin, ...]
    pending_target: str | None
    bootstrap: bool = False
    link_personal_skills: bool = False
    findings: tuple[SharedConfigurationFinding, ...] = ()
    actions: tuple[str, ...] = ()


class _ProjectionError(Exception):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code
        self.message = message


class _OfficialAppApplyPending(Exception):
    pass


def _finding(code: str, message: str, *, severity: str = "error") -> SharedConfigurationFinding:
    return SharedConfigurationFinding(code=code, severity=severity, message=message)


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _canonical_json(value: object) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        separators=(",", ":"),
        sort_keys=True,
    ).encode()


def _semantic_sha256(value: object) -> str:
    return _sha256_bytes(_canonical_json(value))


def _clone_json(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def _profile_home(store: Store, profile: str) -> Path:
    if profile == OFFICIAL_PROFILE:
        return store.official_codex_home
    if profile == INTERNAL_PROFILE:
        if store.internal_codex_home is not None:
            return store.internal_codex_home
        return store.managed_home(INTERNAL_PROFILE)
    manifest = store.load_manifest(profile)
    raw = manifest.get("codex_home")
    if isinstance(raw, str) and raw:
        return Path(raw).expanduser()
    return store.managed_home(profile)


def _config_path(store: Store, profile: str) -> Path:
    return _profile_home(store, profile) / "config.toml"


def _shared_root(store: Store) -> Path:
    return store.root / SHARED_CONFIGURATION_DIRECTORY


def _state_path(store: Store) -> Path:
    return _shared_root(store) / "state.json"


def _generation_path(store: Store, generation: int) -> Path:
    return _shared_root(store) / "generations" / f"{generation:020d}.toml"


def _pending_commit_path(store: Store) -> Path:
    return _shared_root(store) / PENDING_COMMIT_NAME


def _pending_materialization_path(store: Store) -> Path:
    return _shared_root(store) / PENDING_MATERIALIZATION_NAME


def _real_private_directory_exists(path: Path, *, unsafe_code: str) -> bool:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return False
    except OSError as error:
        raise SwitchError(unsafe_code) from error
    if (
        stat.S_ISLNK(metadata.st_mode)
        or not stat.S_ISDIR(metadata.st_mode)
        or stat.S_IMODE(metadata.st_mode) & 0o077
    ):
        raise SwitchError(unsafe_code)
    return True


def _validate_shared_storage(store: Store) -> None:
    code = "shared_configuration.state_integrity"
    if not _real_private_directory_exists(store.root, unsafe_code=code):
        return
    shared_root = _shared_root(store)
    if not _real_private_directory_exists(shared_root, unsafe_code=code):
        return
    _real_private_directory_exists(shared_root / "generations", unsafe_code=code)


def _json_payload(value: Mapping[str, Any]) -> bytes:
    return json.dumps(value, indent=2, sort_keys=True).encode() + b"\n"


def _path_snapshot(path: Path, *, unsafe_code: str) -> _ConfigSnapshot:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return _ConfigSnapshot(kind="missing", payload=b"", mode=0o600)
    except OSError as error:
        raise SwitchError(unsafe_code) from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise SwitchError(unsafe_code)
    try:
        payload = path.read_bytes()
    except OSError as error:
        raise SwitchError(unsafe_code) from error
    return _ConfigSnapshot(
        kind="regular",
        payload=payload,
        mode=stat.S_IMODE(metadata.st_mode),
    )


def _config_snapshot(path: Path) -> _ConfigSnapshot:
    return _path_snapshot(
        path,
        unsafe_code="shared_configuration.target_config_unsafe",
    )


def _valid_sha256(value: object) -> bool:
    return isinstance(value, str) and SHA256_RE.fullmatch(value) is not None


def _validate_persisted_projection(projection: object) -> dict[str, Any]:
    if not isinstance(projection, Mapping):
        raise SwitchError("shared_configuration.state_schema")
    if set(projection) != {"marketplaces", "plugins", "skills"}:
        raise SwitchError("shared_configuration.state_schema")
    marketplaces = projection.get("marketplaces")
    plugins = projection.get("plugins")
    skills = projection.get("skills")
    if (
        not isinstance(marketplaces, Mapping)
        or not isinstance(plugins, Mapping)
        or not isinstance(skills, list)
    ):
        raise SwitchError("shared_configuration.state_schema")
    normalized_marketplaces: dict[str, Any] = {}
    try:
        for raw_name, raw_value in sorted(
            marketplaces.items(), key=lambda item: str(item[0])
        ):
            if not isinstance(raw_name, str) or not isinstance(raw_value, Mapping):
                raise SwitchError("shared_configuration.state_schema")
            normalized_marketplaces[raw_name] = _validate_secret_free_mapping(
                raw_value,
                allowed=MARKETPLACE_SAFE_FIELDS,
            )
    except _ProjectionError as error:
        raise SwitchError("shared_configuration.state_integrity") from error
    normalized_plugins: dict[str, dict[str, bool]] = {}
    for selector, raw_value in sorted(plugins.items(), key=lambda item: str(item[0])):
        if (
            not isinstance(selector, str)
            or _selector_parts(selector) is None
            or not isinstance(raw_value, Mapping)
            or set(raw_value) != {"enabled"}
            or not isinstance(raw_value.get("enabled"), bool)
        ):
            raise SwitchError("shared_configuration.state_schema")
        normalized_plugins[selector] = {"enabled": bool(raw_value["enabled"])}
    normalized_skills: list[dict[str, Any]] = []
    for raw_skill in skills:
        if (
            not isinstance(raw_skill, Mapping)
            or set(raw_skill) != {"owner", "path", "enabled"}
            or raw_skill.get("owner") not in {"external", "plugin-cache"}
            or not isinstance(raw_skill.get("path"), str)
            or not isinstance(raw_skill.get("enabled"), bool)
        ):
            raise SwitchError("shared_configuration.state_schema")
        owner = str(raw_skill["owner"])
        path = str(raw_skill["path"])
        if owner == "plugin-cache":
            relative = Path(path)
            if relative.is_absolute() or ".." in relative.parts or len(relative.parts) < 3:
                raise SwitchError("shared_configuration.state_integrity")
        normalized_skills.append(
            {"owner": owner, "path": path, "enabled": bool(raw_skill["enabled"])}
        )
    normalized_skills.sort(
        key=lambda value: (value["owner"], value["path"], value["enabled"])
    )
    normalized = {
        "marketplaces": normalized_marketplaces,
        "plugins": normalized_plugins,
        "skills": normalized_skills,
    }
    if _canonical_json(normalized) != _canonical_json(projection):
        raise SwitchError("shared_configuration.state_integrity")
    return normalized


def _load_state(store: Store) -> dict[str, Any] | None:
    _validate_shared_storage(store)
    path = _state_path(store)
    if not path.exists() and not path.is_symlink():
        return None
    snapshot = _path_snapshot(
        path,
        unsafe_code="shared_configuration.state_integrity",
    )
    try:
        state = json.loads(snapshot.payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SwitchError("shared_configuration.state_integrity") from error
    if not isinstance(state, dict):
        raise SwitchError("shared_configuration.state_schema")
    if state.get("schema_version") != SHARED_CONFIGURATION_SCHEMA:
        raise SwitchError("shared_configuration.state_schema")
    generation = state.get("generation")
    projection = state.get("projection")
    baselines = state.get("baselines")
    projection_sha256 = state.get("projection_sha256")
    producer_profile = state.get("producer_profile")
    pending_target = state.get("pending_target")
    materializations = state.get("materializations")
    if (
        not isinstance(generation, int)
        or generation < 1
        or not isinstance(projection, dict)
        or not isinstance(baselines, dict)
        or not _valid_sha256(projection_sha256)
        or producer_profile not in {OFFICIAL_PROFILE, INTERNAL_PROFILE}
        or pending_target not in {None, OFFICIAL_PROFILE}
        or not isinstance(materializations, Mapping)
    ):
        raise SwitchError("shared_configuration.state_schema")
    normalized_projection = _validate_persisted_projection(projection)
    if _semantic_sha256(normalized_projection) != projection_sha256:
        raise SwitchError("shared_configuration.state_integrity")
    if set(baselines) != {OFFICIAL_PROFILE, INTERNAL_PROFILE}:
        raise SwitchError("shared_configuration.state_schema")
    for profile in (OFFICIAL_PROFILE, INTERNAL_PROFILE):
        baseline = baselines.get(profile)
        if (
            not isinstance(baseline, Mapping)
            or set(baseline) != {"observation_sha256", "projection_sha256"}
            or not _valid_sha256(baseline.get("observation_sha256"))
            or not _valid_sha256(baseline.get("projection_sha256"))
            or (
                profile != pending_target
                and baseline.get("projection_sha256") != projection_sha256
            )
        ):
            raise SwitchError("shared_configuration.state_integrity")
    if not set(materializations).issubset({OFFICIAL_PROFILE, INTERNAL_PROFILE}):
        raise SwitchError("shared_configuration.state_schema")
    enabled_selectors = {
        selector
        for selector, value in normalized_projection["plugins"].items()
        if value.get("enabled", True)
    }
    for raw_receipts in materializations.values():
        if not isinstance(raw_receipts, list):
            raise SwitchError("shared_configuration.state_schema")
        try:
            receipts = tuple(_normalize_materialization(item) for item in raw_receipts)
        except SwitchError as error:
            raise SwitchError("shared_configuration.state_integrity") from error
        if (
            len({receipt.selector for receipt in receipts}) != len(receipts)
            or any(not _valid_sha256(receipt.tree_sha256) for receipt in receipts)
            or any(receipt.selector not in enabled_selectors for receipt in receipts)
        ):
            raise SwitchError("shared_configuration.state_integrity")
    generation_path = _generation_path(store, generation)
    generation_snapshot = _path_snapshot(
        generation_path,
        unsafe_code="shared_configuration.generation_integrity",
    )
    if generation_snapshot.kind != "regular":
        raise SwitchError("shared_configuration.generation_integrity")
    expected_generation = _render_generation_projection(normalized_projection).encode()
    if generation_snapshot.payload != expected_generation:
        raise SwitchError("shared_configuration.generation_integrity")
    if snapshot.sha256 != _sha256_bytes(_json_payload(state)):
        # read_json and the byte snapshot must describe the same complete object.
        raise SwitchError("shared_configuration.state_integrity")
    return state


def _toml_parser() -> Any:
    if tomllib is None:
        raise SwitchError("Python 3.11+ with tomllib is required")
    return tomllib


def _validate_secret_free_value(value: object) -> None:
    if isinstance(value, Mapping):
        for nested in value.values():
            _validate_secret_free_value(nested)
        return
    if isinstance(value, list):
        for nested in value:
            _validate_secret_free_value(nested)
        return
    if not isinstance(value, str) or "://" not in value:
        return
    try:
        parsed = urllib.parse.urlsplit(value)
    except ValueError as error:
        raise _ProjectionError(
            "shared_configuration.secret_value",
            "Credential-bearing marketplace source values cannot enter shared state.",
        ) from error
    if not parsed.scheme:
        return
    try:
        has_userinfo = parsed.username is not None or parsed.password is not None
        query_keys = tuple(
            key for key, _item in urllib.parse.parse_qsl(parsed.query, keep_blank_values=True)
        )
    except ValueError as error:
        raise _ProjectionError(
            "shared_configuration.secret_value",
            "Credential-bearing marketplace source values cannot enter shared state.",
        ) from error
    if has_userinfo or parsed.fragment or any(SECRET_FIELD_RE.search(key) for key in query_keys):
        raise _ProjectionError(
            "shared_configuration.secret_value",
            "Credential-bearing marketplace source values cannot enter shared state.",
        )


def _validate_secret_free_mapping(
    value: Mapping[str, Any],
    *,
    allowed: frozenset[str],
    nested_source: bool = False,
) -> dict[str, Any]:
    sanitized: dict[str, Any] = {}
    for raw_key, raw_value in value.items():
        key = str(raw_key)
        if key in MARKETPLACE_IGNORED_FIELDS:
            continue
        if SECRET_FIELD_RE.search(key):
            raise _ProjectionError(
                "shared_configuration.secret_field",
                "Credential-like marketplace fields cannot enter shared state.",
            )
        if key not in allowed:
            raise _ProjectionError(
                "shared_configuration.marketplace_schema",
                f"Unsupported shared marketplace field: {key}",
            )
        if isinstance(raw_value, Mapping):
            if key != "source" or nested_source:
                raise _ProjectionError(
                    "shared_configuration.marketplace_schema",
                    f"Unsupported nested marketplace field: {key}",
                )
            sanitized[key] = _validate_secret_free_mapping(
                raw_value,
                allowed=MARKETPLACE_SOURCE_SAFE_FIELDS,
                nested_source=True,
            )
            continue
        if isinstance(raw_value, list):
            if not all(isinstance(item, (str, int, bool)) for item in raw_value):
                raise _ProjectionError(
                    "shared_configuration.marketplace_schema",
                    f"Unsupported marketplace list value: {key}",
                )
            sanitized[key] = list(raw_value)
            _validate_secret_free_value(sanitized[key])
            continue
        if not isinstance(raw_value, (str, int, bool)):
            raise _ProjectionError(
                "shared_configuration.marketplace_schema",
                f"Unsupported marketplace value: {key}",
            )
        _validate_secret_free_value(raw_value)
        sanitized[key] = raw_value
    return sanitized


def _normalize_skill_path(
    path: str,
    home: Path,
    *,
    allowed_missing_plugin_paths: frozenset[str] = frozenset(),
) -> tuple[str, str]:
    candidate = Path(path).expanduser()
    cache = home / "plugins" / "cache"
    if candidate.is_absolute():
        lexical_relative: Path | None = None
        try:
            lexical_relative = candidate.relative_to(cache)
        except ValueError:
            pass
        if lexical_relative is not None and ".." in lexical_relative.parts:
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill paths must remain inside one attested artifact.",
            )
        if cache.is_symlink() or not cache.is_dir():
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill cache root is unavailable or unsafe.",
            )
        try:
            resolved_cache = cache.resolve(strict=True)
        except (OSError, RuntimeError):
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill cache root cannot be resolved.",
            ) from None
        resolved_lexical = lexical_relative
        if resolved_lexical is None:
            try:
                resolved_lexical = candidate.relative_to(resolved_cache)
            except ValueError:
                pass
        try:
            resolved_candidate = candidate.resolve(strict=True)
        except (OSError, RuntimeError):
            if resolved_lexical is None:
                return "external", str(candidate)
            if (
                ".." not in resolved_lexical.parts
                and len(resolved_lexical.parts) >= 3
                and resolved_lexical.as_posix() in allowed_missing_plugin_paths
            ):
                return "plugin-cache", resolved_lexical.as_posix()
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill path escapes or cannot be resolved inside its artifact.",
            ) from None
        try:
            relative = resolved_candidate.relative_to(resolved_cache)
        except ValueError:
            if lexical_relative is None:
                return "external", str(candidate)
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill path escapes its cache root.",
            ) from None
        if ".." in relative.parts or len(relative.parts) < 3:
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill path has an unsafe normalized identity.",
            )
        artifact = resolved_cache.joinpath(*relative.parts[:3])
        try:
            resolved_artifact = artifact.resolve(strict=True)
            resolved_artifact.relative_to(resolved_cache)
            resolved_candidate.relative_to(resolved_artifact)
        except (OSError, RuntimeError, ValueError):
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill path escapes or cannot be resolved inside its artifact.",
            ) from None
        if not (resolved_candidate.is_dir() or resolved_candidate.is_file()):
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill path has an unsupported file kind.",
            )
        normalized = relative
        if ".." in normalized.parts or len(normalized.parts) < 3:
            raise _ProjectionError(
                "shared_configuration.materialization.unsafe_cache",
                "Plugin Skill path has an unsafe normalized identity.",
            )
        return "plugin-cache", normalized.as_posix()
    return "external", path


def _project_config(
    text: str,
    home: Path,
    *,
    label: str,
    allowed_missing_plugin_paths: frozenset[str] = frozenset(),
) -> dict[str, Any]:
    try:
        parsed = _toml_parser().loads(text or "")
    except Exception as exc:
        raise _ProjectionError(
            "shared_configuration.invalid_config",
            f"Invalid TOML in {label}: {exc}",
        ) from exc
    if not isinstance(parsed, dict):
        raise _ProjectionError(
            "shared_configuration.invalid_config",
            f"Config root is not a table: {label}",
        )

    raw_marketplaces = parsed.get("marketplaces", {})
    if raw_marketplaces is None:
        raw_marketplaces = {}
    if not isinstance(raw_marketplaces, Mapping):
        raise _ProjectionError(
            "shared_configuration.marketplace_schema",
            "marketplaces must be a table",
        )
    marketplaces: dict[str, Any] = {}
    for raw_name, raw_value in sorted(raw_marketplaces.items(), key=lambda item: str(item[0])):
        if not isinstance(raw_value, Mapping):
            raise _ProjectionError(
                "shared_configuration.marketplace_schema",
                f"Marketplace {raw_name} must be a table",
            )
        marketplaces[str(raw_name)] = _validate_secret_free_mapping(
            raw_value,
            allowed=MARKETPLACE_SAFE_FIELDS,
        )

    raw_plugins = parsed.get("plugins", {})
    if raw_plugins is None:
        raw_plugins = {}
    if not isinstance(raw_plugins, Mapping):
        raise _ProjectionError(
            "shared_configuration.plugin_schema",
            "plugins must be a table",
        )
    plugins: dict[str, dict[str, bool]] = {}
    for raw_selector, raw_value in sorted(raw_plugins.items(), key=lambda item: str(item[0])):
        if not isinstance(raw_value, Mapping):
            raise _ProjectionError(
                "shared_configuration.plugin_schema",
                f"Plugin {raw_selector} must be a table",
            )
        unexpected = set(str(key) for key in raw_value) - {"enabled"}
        if unexpected:
            if any(SECRET_FIELD_RE.search(key) for key in unexpected):
                raise _ProjectionError(
                    "shared_configuration.secret_field",
                    "Credential-like plugin fields cannot enter shared state.",
                )
            raise _ProjectionError(
                "shared_configuration.plugin_schema",
                f"Unsupported plugin fields: {', '.join(sorted(unexpected))}",
            )
        enabled = raw_value.get("enabled", True)
        if not isinstance(enabled, bool):
            raise _ProjectionError(
                "shared_configuration.plugin_schema",
                f"Plugin enabled must be boolean: {raw_selector}",
            )
        plugins[str(raw_selector)] = {"enabled": enabled}

    skills_table = parsed.get("skills", {})
    if skills_table is None:
        skills_table = {}
    if not isinstance(skills_table, Mapping):
        raise _ProjectionError(
            "shared_configuration.skill_schema",
            "skills must be a table",
        )
    raw_skills = skills_table.get("config", [])
    if raw_skills is None:
        raw_skills = []
    if not isinstance(raw_skills, list):
        raise _ProjectionError(
            "shared_configuration.skill_schema",
            "skills.config must be an array of tables",
        )
    skills: list[dict[str, Any]] = []
    for index, raw_skill in enumerate(raw_skills):
        if not isinstance(raw_skill, Mapping):
            raise _ProjectionError(
                "shared_configuration.skill_schema",
                f"skills.config[{index}] must be a table",
            )
        unexpected = set(str(key) for key in raw_skill) - {"path", "enabled"}
        if unexpected:
            raise _ProjectionError(
                "shared_configuration.skill_schema",
                f"Unsupported skills.config fields: {', '.join(sorted(unexpected))}",
            )
        raw_path = raw_skill.get("path")
        enabled = raw_skill.get("enabled", True)
        if not isinstance(raw_path, str) or not isinstance(enabled, bool):
            raise _ProjectionError(
                "shared_configuration.skill_schema",
                f"skills.config[{index}] requires string path and boolean enabled",
            )
        owner, normalized_path = _normalize_skill_path(
            raw_path,
            home,
            allowed_missing_plugin_paths=allowed_missing_plugin_paths,
        )
        skills.append(
            {"owner": owner, "path": normalized_path, "enabled": enabled}
        )
    skills.sort(key=lambda value: (value["owner"], value["path"], value["enabled"]))
    return {
        "marketplaces": marketplaces,
        "plugins": plugins,
        "skills": skills,
    }


def _selector_parts(selector: str) -> tuple[str, str] | None:
    if "@" not in selector:
        return None
    plugin, marketplace = selector.rsplit("@", 1)
    if not plugin or not marketplace:
        return None
    return plugin, marketplace


def _artifact_from_skill_paths(
    projection: Mapping[str, Any],
    *,
    plugin: str,
    marketplace: str,
    cache_root: Path,
) -> Path | None:
    for skill in projection.get("skills", []):
        if not isinstance(skill, Mapping) or skill.get("owner") != "plugin-cache":
            continue
        relative = Path(str(skill.get("path", "")))
        parts = relative.parts
        if len(parts) < 3 or parts[0] != marketplace or parts[1] != plugin:
            continue
        return cache_root / parts[0] / parts[1] / parts[2]
    return None


def _valid_plugin_manifest(root: Path, plugin: str) -> tuple[str, Mapping[str, Any]] | None:
    manifest_path = root / ".codex-plugin" / "plugin.json"
    if manifest_path.is_symlink() or not manifest_path.is_file():
        return None
    try:
        manifest_path.resolve(strict=True).relative_to(root.resolve(strict=True))
        value = json.loads(manifest_path.read_text())
    except (OSError, RuntimeError, ValueError, UnicodeDecodeError, json.JSONDecodeError):
        return None
    if not isinstance(value, dict) or value.get("name") != plugin:
        return None
    version = value.get("version")
    if not isinstance(version, str) or not version:
        return None
    return version, value


def _find_plugin_artifact(
    home: Path,
    projection: Mapping[str, Any],
    *,
    selector: str,
    retained: SharedPluginMaterialization | None = None,
) -> tuple[Path, str, Mapping[str, Any]] | None:
    parts = _selector_parts(selector)
    if parts is None:
        return None
    plugin, marketplace = parts
    cache_root = home / "plugins" / "cache"
    selected = _artifact_from_skill_paths(
        projection,
        plugin=plugin,
        marketplace=marketplace,
        cache_root=cache_root,
    )
    if selected is not None:
        manifest = _valid_plugin_manifest(selected, plugin)
        if manifest is not None:
            return selected, manifest[0], manifest[1]
    versions_root = cache_root / marketplace / plugin
    if versions_root.is_symlink() or not versions_root.is_dir():
        return None
    candidates: list[tuple[Path, str, Mapping[str, Any]]] = []
    try:
        children = sorted(versions_root.iterdir(), key=lambda value: value.name)
    except OSError:
        return None
    for child in children:
        if child.is_symlink() or not child.is_dir():
            continue
        manifest = _valid_plugin_manifest(child, plugin)
        if manifest is not None:
            candidates.append((child, manifest[0], manifest[1]))
    if selected is not None and candidates:
        raise _ProjectionError(
            "shared_configuration.materialization.unsafe_cache",
            f"Configured Plugin Skill does not select an attested artifact: {selector}",
        )
    if len(candidates) == 1:
        return candidates[0]
    if len(candidates) > 1 and retained is not None:
        retained_key = Path(retained.cache_key).name
        for candidate in candidates:
            if candidate[0].name == retained_key:
                return candidate
    if len(candidates) > 1:
        raise _ProjectionError(
            "shared_configuration.materialization.ambiguous_cache",
            f"Multiple retained Plugin versions have no attested active identity: {selector}",
        )
    return None


def _plugin_tree_sha256(root: Path) -> str:
    from codex_switch_plugins import plugin_tree_sha256

    return plugin_tree_sha256(root)


def _marketplace_policy(marketplace: str, config: Mapping[str, Any], artifact: Path | None) -> str:
    if marketplace.startswith("openai-"):
        return "backend_managed"
    raw_source = config.get("source")
    source_kind = config.get("source_type")
    if isinstance(raw_source, Mapping):
        source_kind = raw_source.get("source", raw_source.get("source_type", source_kind))
    if artifact is not None and str(source_kind or "").lower() in {
        "local",
        "git",
        "github",
    }:
        return "portable_exact"
    return "backend_managed"


def _manifest_skill_roots(root: Path, manifest: Mapping[str, Any]) -> tuple[str, ...]:
    declared = manifest.get("skills", "./skills/")
    values: list[str] = []
    if isinstance(declared, str):
        values.append(declared)
    elif isinstance(declared, list):
        values.extend(value for value in declared if isinstance(value, str))
    roots: set[str] = set()
    for value in values:
        candidate = root / value
        if not candidate.exists() or candidate.is_symlink():
            continue
        if candidate.is_file() and candidate.name == "SKILL.md":
            roots.add(str(candidate.parent))
            continue
        if candidate.is_dir():
            if (candidate / "SKILL.md").is_file():
                roots.add(str(candidate))
            try:
                roots.update(
                    str(path.parent)
                    for path in candidate.rglob("SKILL.md")
                    if path.is_file() and not path.is_symlink()
                )
            except OSError:
                continue
    return tuple(sorted(roots))


def _desired_plugins(
    home: Path,
    projection: Mapping[str, Any],
    *,
    profile_receipts: Sequence[SharedPluginMaterialization] = (),
    policy_receipts: Sequence[SharedPluginMaterialization] = (),
) -> tuple[SharedDesiredPlugin, ...]:
    marketplaces = projection.get("marketplaces", {})
    retained_by_selector = {receipt.selector: receipt for receipt in profile_receipts}
    policy_by_selector: dict[str, str] = {}
    for receipt in policy_receipts:
        current = policy_by_selector.get(receipt.selector)
        if current != "portable_exact" or receipt.policy == "portable_exact":
            policy_by_selector[receipt.selector] = receipt.policy
    for receipt in profile_receipts:
        policy_by_selector[receipt.selector] = receipt.policy
    desired: list[SharedDesiredPlugin] = []
    for selector, raw_plugin in sorted(projection.get("plugins", {}).items()):
        enabled = bool(raw_plugin.get("enabled", True))
        parts = _selector_parts(selector)
        if parts is None:
            raise _ProjectionError(
                "shared_configuration.plugin_schema",
                f"Invalid plugin selector: {selector}",
            )
        plugin, marketplace = parts
        marketplace_config = marketplaces.get(marketplace, {})
        if not isinstance(marketplace_config, Mapping):
            marketplace_config = {}
        artifact_entry = _find_plugin_artifact(
            home,
            projection,
            selector=selector,
            retained=retained_by_selector.get(selector),
        )
        artifact: Path | None = artifact_entry[0] if artifact_entry else None
        policy = _marketplace_policy(marketplace, marketplace_config, artifact)
        policy = policy_by_selector.get(selector, policy)
        cache_key = ""
        manifest_version = ""
        tree_sha256 = ""
        skill_roots: tuple[str, ...] = ()
        if artifact_entry is not None:
            artifact, manifest_version, manifest = artifact_entry
            cache_key = artifact.name
            try:
                tree_sha256 = _plugin_tree_sha256(artifact)
            except (OSError, SwitchError):
                raise _ProjectionError(
                    "shared_configuration.materialization.unsafe_cache",
                    f"Plugin artifact cannot be attested: {selector}",
                ) from None
            skill_roots = _manifest_skill_roots(artifact, manifest)
        source_identity_sha256 = _semantic_sha256(
            {
                "selector": selector,
                "marketplace": marketplace_config,
                "cache_key": cache_key,
                "manifest_version": manifest_version,
                "tree_sha256": tree_sha256,
            }
        )
        desired.append(
            SharedDesiredPlugin(
                selector=selector,
                enabled=enabled,
                policy=policy,
                marketplace=marketplace,
                plugin=plugin,
                marketplace_config=_clone_json(dict(marketplace_config)),
                cache_key=cache_key,
                manifest_version=manifest_version,
                tree_sha256=tree_sha256,
                skill_roots=skill_roots,
                source_artifact=str(artifact) if artifact is not None else "",
                source_identity_sha256=source_identity_sha256,
            )
        )
    return tuple(desired)


def _state_receipts(
    state: Mapping[str, Any] | None,
    profile: str | None = None,
) -> tuple[SharedPluginMaterialization, ...]:
    if state is None:
        return ()
    if profile is not None:
        return _stored_materializations(state, profile)
    receipts: list[SharedPluginMaterialization] = []
    for name in (OFFICIAL_PROFILE, INTERNAL_PROFILE):
        receipts.extend(_stored_materializations(state, name))
    return tuple(receipts)


def _observation_from_text(
    store: Store,
    profile: str,
    raw: str,
    *,
    config_kind: str,
    config_mode: int,
    state: Mapping[str, Any] | None,
) -> _HomeObservation:
    home = _profile_home(store, profile)
    allowed_missing_paths: frozenset[str] = frozenset()
    if _state_receipts(state, profile) and isinstance(
        state.get("projection") if state is not None else None,
        Mapping,
    ):
        allowed_missing_paths = frozenset(
            str(skill.get("path"))
            for skill in state["projection"].get("skills", [])
            if isinstance(skill, Mapping) and skill.get("owner") == "plugin-cache"
        )
    projection = _project_config(
        raw,
        home,
        label=str(home / "config.toml"),
        allowed_missing_plugin_paths=allowed_missing_paths,
    )
    desired = _desired_plugins(
        home,
        projection,
        profile_receipts=_state_receipts(state, profile),
        policy_receipts=_state_receipts(state),
    )
    identity = [
        {
            "selector": item.selector,
            "enabled": item.enabled,
            "policy": item.policy,
            "cache_key": item.cache_key,
            "manifest_version": item.manifest_version,
            "tree_sha256": item.tree_sha256,
            "source_identity_sha256": item.source_identity_sha256,
        }
        for item in desired
    ]
    return _HomeObservation(
        profile=profile,
        home=home,
        raw_text=raw,
        raw_sha256=_sha256_bytes(raw.encode()),
        projection=projection,
        projection_sha256=_semantic_sha256(projection),
        desired_plugins=desired,
        observation_sha256=_semantic_sha256(
            {"projection": projection, "plugin_identities": identity}
        ),
        config_kind=config_kind,
        config_mode=config_mode,
    )


def _observe_home(
    store: Store,
    profile: str,
    adapters: object,
    state: Mapping[str, Any] | None = None,
) -> _HomeObservation:
    home = _profile_home(store, profile)
    path = home / "config.toml"
    reader = getattr(adapters, "read_stable", _default_read_stable)
    before = _config_snapshot(path)
    try:
        raw = reader(path)
    except FileNotFoundError:
        raw = ""
    if not isinstance(raw, str):
        raise _ProjectionError(
            "shared_configuration.invalid_config",
            f"Stable config reader returned non-text for {path}",
        )
    after = _config_snapshot(path)
    if before != after or raw.encode() != before.payload:
        raise SwitchError("shared_configuration.source_changed_during_plan")
    return _observation_from_text(
        store,
        profile,
        raw,
        config_kind=before.kind,
        config_mode=before.mode,
        state=state,
    )


def _baseline_hash(state: Mapping[str, Any], profile: str) -> str:
    baselines = state.get("baselines", {})
    if not isinstance(baselines, Mapping):
        return ""
    value = baselines.get(profile, {})
    if not isinstance(value, Mapping):
        return ""
    raw = value.get("observation_sha256")
    return str(raw) if isinstance(raw, str) else ""


def _baseline_projection_hash(state: Mapping[str, Any], profile: str) -> str:
    baselines = state.get("baselines", {})
    if not isinstance(baselines, Mapping):
        return ""
    value = baselines.get(profile, {})
    if not isinstance(value, Mapping):
        return ""
    raw = value.get("projection_sha256")
    return str(raw) if isinstance(raw, str) else ""


def _same_semantic_change(left: _HomeObservation, right: _HomeObservation) -> bool:
    if left.projection_sha256 != right.projection_sha256:
        return False
    left_exact = {
        item.selector: (item.cache_key, item.manifest_version, item.tree_sha256)
        for item in left.desired_plugins
        if item.enabled and item.policy == "portable_exact"
    }
    right_exact = {
        item.selector: (item.cache_key, item.manifest_version, item.tree_sha256)
        for item in right.desired_plugins
        if item.enabled and item.policy == "portable_exact"
    }
    return left_exact == right_exact


def _validate_supported_selection(selection: ProfileSelection) -> None:
    if (selection.cli_profile, selection.app_profile) != SUPPORTED_SELECTION:
        raise SwitchError(
            "shared_configuration.unsupported_selection: expected internal CLI and official App"
        )


def _validate_personal_skills(
    store: Store,
) -> tuple[bool, SharedConfigurationFinding | None]:
    official = _profile_home(store, OFFICIAL_PROFILE) / "skills"
    internal = _profile_home(store, INTERNAL_PROFILE) / "skills"
    if not official.exists():
        return False, None
    if official.is_symlink() or not official.is_dir():
        return False, _finding(
            "shared_configuration.personal_skills.unsafe_source",
            "The official personal Skills root must be a real directory.",
        )
    if not internal.exists() and not internal.is_symlink():
        return True, None
    if not internal.is_symlink():
        return False, _finding(
            "shared_configuration.personal_skills.real_directory",
            "The internal Skills entry is independently owned and was preserved.",
        )
    raw_target = os.readlink(internal)
    if raw_target in {"skills", "./skills"}:
        return False, _finding(
            "shared_configuration.personal_skills.self_link",
            "The internal Skills link is self-referential.",
        )
    try:
        resolved_internal = internal.resolve(strict=True)
    except RuntimeError:
        return False, _finding(
            "shared_configuration.personal_skills.self_link",
            "The internal Skills link is circular.",
        )
    except OSError:
        return False, _finding(
            "shared_configuration.personal_skills.dangling_link",
            "The internal Skills link is dangling.",
        )
    if resolved_internal != official.resolve(strict=True):
        return False, _finding(
            "shared_configuration.personal_skills.foreign_link",
            "The internal Skills link points at a foreign root.",
        )
    return False, None


def _cache_root_problem(store: Store) -> SharedConfigurationFinding | None:
    official = _profile_home(store, OFFICIAL_PROFILE) / "plugins" / "cache"
    internal = _profile_home(store, INTERNAL_PROFILE) / "plugins" / "cache"
    for home, root in (
        (_profile_home(store, OFFICIAL_PROFILE), official),
        (_profile_home(store, INTERNAL_PROFILE), internal),
    ):
        plugins = home / "plugins"
        if plugins.is_symlink() or root.is_symlink():
            return _finding(
                "shared_configuration.cache_not_independent",
                "Plugin cache roots must be independent real directories.",
            )
        if root.exists() and not root.is_dir():
            return _finding(
                "shared_configuration.cache_not_independent",
                "Plugin cache root has an unsafe file kind.",
            )
    if official.exists() and internal.exists():
        try:
            if official.resolve(strict=True) == internal.resolve(strict=True):
                return _finding(
                    "shared_configuration.cache_not_independent",
                    "Official and internal plugin caches resolve to the same root.",
                )
        except OSError:
            return _finding(
                "shared_configuration.cache_not_independent",
                "Plugin cache roots cannot be safely resolved.",
            )
    return None


def _receipt(
    *,
    status: str,
    before: int,
    after: int,
    cli_ready: bool,
    pending_target: str | None = None,
    materializations: Sequence[SharedPluginMaterialization] = (),
    findings: Sequence[SharedConfigurationFinding] = (),
    source_profile: str | None = None,
    target_profile: str | None = None,
    actions: Sequence[str] = (),
) -> SharedConfigurationReceipt:
    return SharedConfigurationReceipt(
        status=status,
        generation_before=before,
        generation_after=after,
        cli_ready=cli_ready,
        pending_target=pending_target,
        materializations=tuple(materializations),
        findings=tuple(findings),
        source_profile=source_profile,
        target_profile=target_profile,
        actions=tuple(actions),
    )


def _blocked_receipt(
    generation: int,
    finding: SharedConfigurationFinding,
    *,
    source_profile: str | None = None,
    target_profile: str | None = None,
) -> SharedConfigurationReceipt:
    return _receipt(
        status="blocked",
        before=generation,
        after=generation,
        cli_ready=False,
        findings=(finding,),
        source_profile=source_profile,
        target_profile=target_profile,
    )


def _plan_reconcile(
    store: Store,
    selection: ProfileSelection,
    *,
    boundary: str,
    adapters: object,
) -> _ReconcilePlan | SharedConfigurationReceipt:
    _validate_supported_selection(selection)
    state = _load_state(store)
    generation = int(state.get("generation", 0)) if state is not None else 0

    link_personal, skills_problem = _validate_personal_skills(store)
    if skills_problem is not None:
        return _blocked_receipt(generation, skills_problem)
    cache_problem = _cache_root_problem(store)
    if cache_problem is not None:
        return _blocked_receipt(generation, cache_problem)

    try:
        official = _observe_home(store, OFFICIAL_PROFILE, adapters, state)
        internal = _observe_home(store, INTERNAL_PROFILE, adapters, state)
    except _ProjectionError as error:
        return _blocked_receipt(generation, _finding(error.code, error.message))
    except SwitchError as error:
        code = _code_from_error(error, "shared_configuration.source_changed_during_plan")
        return _blocked_receipt(generation, _finding(code, str(error)))

    if state is None:
        findings: tuple[SharedConfigurationFinding, ...] = ()
        if not official.desired_plugins or any(
            item.enabled and not item.tree_sha256 for item in official.desired_plugins
        ):
            findings = (
                _finding(
                    "shared_configuration.bootstrap",
                    "Official App configuration is seeding the first shared generation.",
                    severity="info",
                ),
            )
        return _ReconcilePlan(
            status="apply",
            generation_before=0,
            generation_after=1,
            source_profile=OFFICIAL_PROFILE,
            target_profile=INTERNAL_PROFILE,
            source_observation=official,
            target_observation=internal,
            projection=official.projection,
            desired_plugins=official.desired_plugins,
            pending_target=None,
            bootstrap=True,
            link_personal_skills=link_personal,
            findings=findings,
            actions=("bootstrap", "materialize:internal", "render:internal"),
        )

    pending_target = state.get("pending_target")
    official_changed = official.observation_sha256 != _baseline_hash(state, OFFICIAL_PROFILE)
    internal_changed = internal.observation_sha256 != _baseline_hash(state, INTERNAL_PROFILE)
    if (
        not pending_target
        and not official_changed
        and internal_changed
        and internal.projection_sha256
        == _baseline_projection_hash(state, INTERNAL_PROFILE)
    ):
        try:
            _validate_materializations(
                store,
                INTERNAL_PROFILE,
                internal.desired_plugins,
                _stored_materializations(state, INTERNAL_PROFILE),
            )
        except SwitchError:
            return _ReconcilePlan(
                status="repair",
                generation_before=generation,
                generation_after=generation,
                source_profile=OFFICIAL_PROFILE,
                target_profile=INTERNAL_PROFILE,
                source_observation=official,
                target_observation=internal,
                projection=_clone_json(state["projection"]),
                desired_plugins=official.desired_plugins,
                pending_target=None,
                link_personal_skills=link_personal,
                actions=("repair:internal", "materialize:internal", "render:internal"),
            )
    if pending_target:
        if official_changed or internal_changed:
            return _receipt(
                status="conflict",
                before=generation,
                after=generation,
                cli_ready=False,
                findings=(
                    _finding(
                        "shared_configuration.conflict",
                        "A profile changed while an App apply was pending.",
                    ),
                ),
            )
        if boundary != "explicit-sync":
            try:
                materializations = _validate_materializations(
                    store,
                    INTERNAL_PROFILE,
                    internal.desired_plugins,
                    _stored_materializations(state, INTERNAL_PROFILE),
                )
            except SwitchError as error:
                return _blocked_receipt(
                    generation,
                    _finding(
                        _code_from_error(
                            error,
                            "shared_configuration.materialization.unsafe_cache",
                        ),
                        str(error),
                    ),
                )
            return _receipt(
                status="pending",
                before=generation,
                after=generation,
                cli_ready=True,
                pending_target=str(pending_target),
                materializations=materializations,
                findings=(
                    _finding(
                        "shared_configuration.pending_app_apply",
                        "Shared configuration is waiting for a stopped-App apply.",
                        severity="warning",
                    ),
                ),
                source_profile=INTERNAL_PROFILE,
                target_profile=OFFICIAL_PROFILE,
            )
        app_running = _app_running(adapters, store, selection)
        if app_running:
            return _receipt(
                status="pending",
                before=generation,
                after=generation,
                cli_ready=True,
                pending_target=OFFICIAL_PROFILE,
                findings=(
                    _finding(
                        "shared_configuration.pending_app_apply",
                        "Quit the official App before applying shared configuration.",
                        severity="warning",
                    ),
                ),
                source_profile=INTERNAL_PROFILE,
                target_profile=OFFICIAL_PROFILE,
            )
        projection = _clone_json(state["projection"])
        return _ReconcilePlan(
            status="apply",
            generation_before=generation,
            generation_after=generation,
            source_profile=INTERNAL_PROFILE,
            target_profile=OFFICIAL_PROFILE,
            source_observation=internal,
            target_observation=official,
            projection=projection,
            desired_plugins=internal.desired_plugins,
            pending_target=None,
            link_personal_skills=link_personal,
            actions=("materialize:openai-official", "render:openai-official"),
        )

    if not official_changed and not internal_changed and not link_personal:
        try:
            stored = _validate_materializations(
                store,
                INTERNAL_PROFILE,
                internal.desired_plugins,
                _stored_materializations(state, INTERNAL_PROFILE),
            )
        except SwitchError:
            return _ReconcilePlan(
                status="repair",
                generation_before=generation,
                generation_after=generation,
                source_profile=OFFICIAL_PROFILE,
                target_profile=INTERNAL_PROFILE,
                source_observation=official,
                target_observation=internal,
                projection=_clone_json(state["projection"]),
                desired_plugins=official.desired_plugins,
                pending_target=None,
                link_personal_skills=False,
                actions=("repair:internal", "materialize:internal", "render:internal"),
            )
        return _receipt(
            status="current",
            before=generation,
            after=generation,
            cli_ready=True,
            materializations=stored,
        )
    if official_changed and internal_changed and not _same_semantic_change(official, internal):
        return _receipt(
            status="conflict",
            before=generation,
            after=generation,
            cli_ready=False,
            findings=(
                _finding(
                    "shared_configuration.conflict",
                    "Official App and internal CLI changed from the same baseline.",
                ),
            ),
        )

    if official_changed or (official_changed and internal_changed):
        source = official
        source_profile = OFFICIAL_PROFILE
        target_profile = INTERNAL_PROFILE
        pending_after = None
    elif internal_changed:
        source = internal
        source_profile = INTERNAL_PROFILE
        if boundary == "explicit-sync" and not _app_running(
            adapters, store, selection
        ):
            target_profile = OFFICIAL_PROFILE
            pending_after = None
        else:
            target_profile = INTERNAL_PROFILE
            pending_after = OFFICIAL_PROFILE
    else:
        # Only the personal Skills link is missing from an otherwise current state.
        source = official
        source_profile = OFFICIAL_PROFILE
        target_profile = INTERNAL_PROFILE
        pending_after = None

    return _ReconcilePlan(
        status="apply",
        generation_before=generation,
        generation_after=(generation + 1 if official_changed or internal_changed else generation),
        source_profile=source_profile,
        target_profile=target_profile,
        source_observation=source,
        target_observation=(
            internal if target_profile == INTERNAL_PROFILE else official
        ),
        projection=source.projection,
        desired_plugins=source.desired_plugins,
        pending_target=pending_after,
        link_personal_skills=link_personal,
        actions=(
            f"materialize:{target_profile}",
            f"render:{target_profile}" if target_profile != source_profile else "capture:internal",
        ),
    )


def _stored_materializations(
    state: Mapping[str, Any], profile: str
) -> tuple[SharedPluginMaterialization, ...]:
    by_profile = state.get("materializations", {})
    if not isinstance(by_profile, Mapping):
        return ()
    raw = by_profile.get(profile, [])
    if not isinstance(raw, list):
        return ()
    receipts: list[SharedPluginMaterialization] = []
    for item in raw:
        try:
            receipts.append(_normalize_materialization(item))
        except SwitchError:
            return ()
    return tuple(receipts)


def _code_from_error(error: BaseException, fallback: str) -> str:
    match = FINDING_CODE_RE.search(str(error))
    return match.group(0) if match else fallback


def _normalize_materialization(value: object) -> SharedPluginMaterialization:
    def field_value(name: str, default: object = "") -> object:
        if isinstance(value, Mapping):
            return value.get(name, default)
        return getattr(value, name, default)

    roots = field_value("skill_roots", ())
    if not isinstance(roots, (tuple, list)):
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    receipt = SharedPluginMaterialization(
        selector=str(field_value("selector")),
        policy=str(field_value("policy")),
        cache_key=str(field_value("cache_key")),
        manifest_version=str(field_value("manifest_version")),
        tree_sha256=str(field_value("tree_sha256")),
        skill_roots=tuple(str(root) for root in roots),
    )
    if (
        not receipt.selector
        or _selector_parts(receipt.selector) is None
        or receipt.policy not in {"portable_exact", "backend_managed"}
        or not receipt.cache_key
        or not receipt.manifest_version
        or not receipt.tree_sha256
        or Path(receipt.cache_key).is_absolute()
        or ".." in Path(receipt.cache_key).parts
        or len(set(receipt.skill_roots)) != len(receipt.skill_roots)
        or any(
            not root
            or not Path(root).is_absolute()
            or ".." in Path(root).parts
            for root in receipt.skill_roots
        )
    ):
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    return receipt


def _receipt_artifact(
    cache_root: Path,
    receipt: SharedPluginMaterialization,
) -> tuple[Path, str, str]:
    parts = _selector_parts(receipt.selector)
    if parts is None:
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    plugin, marketplace = parts
    key = Path(receipt.cache_key)
    if len(key.parts) >= 3 and key.parts[:2] == (marketplace, plugin):
        artifact = cache_root / key
    elif len(key.parts) == 1:
        artifact = cache_root / marketplace / plugin / key
    else:
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    return artifact, plugin, marketplace


def _attest_materialization(
    cache_root: Path,
    receipt: SharedPluginMaterialization,
) -> SharedPluginMaterialization:
    artifact, plugin, _marketplace = _receipt_artifact(cache_root, receipt)
    try:
        resolved_cache = cache_root.resolve(strict=True)
        if cache_root.is_symlink() or not cache_root.is_dir():
            raise OSError("unsafe cache root")
        if artifact.is_symlink() or not artifact.is_dir():
            raise OSError("unsafe artifact")
        resolved_artifact = artifact.resolve(strict=True)
        resolved_artifact.relative_to(resolved_cache)
    except (OSError, RuntimeError, ValueError):
        raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
    manifest_entry = _valid_plugin_manifest(resolved_artifact, plugin)
    if manifest_entry is None or manifest_entry[0] != receipt.manifest_version:
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    try:
        artifact_paths = tuple(resolved_artifact.rglob("*"))
    except OSError:
        raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
    for path in artifact_paths:
        try:
            metadata = path.lstat()
            if stat.S_ISLNK(metadata.st_mode):
                path.resolve(strict=True).relative_to(resolved_artifact)
            elif not (stat.S_ISDIR(metadata.st_mode) or stat.S_ISREG(metadata.st_mode)):
                raise OSError("unsupported artifact file kind")
        except (OSError, RuntimeError, ValueError):
            raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
    supplied_skill_files: set[Path] = set()
    for raw_root in receipt.skill_roots:
        root = Path(raw_root)
        try:
            resolved = root.resolve(strict=True)
            resolved.relative_to(resolved_cache)
            resolved.relative_to(resolved_artifact)
        except (OSError, RuntimeError, ValueError):
            raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
        if not resolved.is_dir():
            raise SwitchError("shared_configuration.materialization.unsafe_cache")
        try:
            root_skill_files = {
                path.resolve(strict=True)
                for path in (
                    (resolved / "SKILL.md"),
                    *resolved.rglob("SKILL.md"),
                )
                if path.is_file() and not path.is_symlink()
            }
            for skill_file in root_skill_files:
                skill_file.relative_to(resolved_artifact)
        except (OSError, RuntimeError, ValueError):
            raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
        if not root_skill_files:
            raise SwitchError("shared_configuration.materialization.unsafe_cache")
        supplied_skill_files.update(root_skill_files)
    declared_roots = {
        Path(root).resolve(strict=True)
        for root in _manifest_skill_roots(resolved_artifact, manifest_entry[1])
    }
    try:
        declared_skill_files = {
            (root / "SKILL.md").resolve(strict=True) for root in declared_roots
        }
    except (OSError, RuntimeError):
        raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
    if supplied_skill_files != declared_skill_files:
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    actual_roots = tuple(
        str(artifact / root.relative_to(resolved_artifact))
        for root in sorted(declared_roots, key=lambda value: str(value))
    )
    try:
        tree_sha256 = _plugin_tree_sha256(resolved_artifact)
    except (OSError, SwitchError):
        raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
    if tree_sha256 != receipt.tree_sha256:
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    return SharedPluginMaterialization(
        selector=receipt.selector,
        policy=receipt.policy,
        cache_key=receipt.cache_key,
        manifest_version=receipt.manifest_version,
        tree_sha256=tree_sha256,
        skill_roots=actual_roots,
    )


def _validate_materializations(
    store: Store,
    target_profile: str,
    desired: Sequence[SharedDesiredPlugin],
    raw_receipts: Sequence[object],
) -> tuple[SharedPluginMaterialization, ...]:
    enabled = {item.selector: item for item in desired if item.enabled}
    normalized = tuple(_normalize_materialization(value) for value in raw_receipts)
    if {item.selector for item in normalized} != set(enabled) or len(normalized) != len(enabled):
        raise SwitchError("shared_configuration.materialization.failed")
    cache_root = _profile_home(store, target_profile) / "plugins" / "cache"
    other_profile = OFFICIAL_PROFILE if target_profile == INTERNAL_PROFILE else INTERNAL_PROFILE
    other_cache = _profile_home(store, other_profile) / "plugins" / "cache"
    try:
        resolved_cache = cache_root.resolve(strict=False)
        resolved_other = other_cache.resolve(strict=False)
    except (OSError, RuntimeError):
        raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
    if resolved_cache == resolved_other:
        raise SwitchError("shared_configuration.cache_not_independent")
    attested: list[SharedPluginMaterialization] = []
    for receipt in normalized:
        expected = enabled[receipt.selector]
        if receipt.policy != expected.policy:
            raise SwitchError("shared_configuration.materialization.unsafe_cache")
        actual = _attest_materialization(cache_root, receipt)
        if expected.policy == "portable_exact" and (
            actual.cache_key != expected.cache_key
            or actual.manifest_version != expected.manifest_version
            or actual.tree_sha256 != expected.tree_sha256
        ):
            raise SwitchError("shared_configuration.materialization.unsafe_cache")
        attested.append(actual)
    return tuple(attested)


def _local_materializations(
    store: Store,
    profile: str,
    desired: Sequence[SharedDesiredPlugin],
) -> tuple[SharedPluginMaterialization, ...]:
    cache_root = _profile_home(store, profile) / "plugins" / "cache"
    state = _load_state(store)
    retained = {
        receipt.selector: receipt
        for receipt in (
            _stored_materializations(state, profile) if state is not None else ()
        )
    }
    receipts: list[SharedPluginMaterialization] = []
    for item in desired:
        if not item.enabled:
            continue
        if not item.source_artifact or not item.cache_key or not item.manifest_version:
            previous = retained.get(item.selector)
            if previous is None or previous.policy != item.policy:
                raise SwitchError("shared_configuration.materialization.unavailable")
            receipts.append(previous)
            continue
        artifact = Path(item.source_artifact)
        try:
            artifact.resolve(strict=True).relative_to(cache_root.resolve(strict=False))
        except (OSError, RuntimeError, ValueError):
            raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
        receipts.append(
            SharedPluginMaterialization(
                selector=item.selector,
                policy=item.policy,
                cache_key=item.cache_key,
                manifest_version=item.manifest_version,
                tree_sha256=item.tree_sha256,
                skill_roots=item.skill_roots,
            )
        )
    return _validate_materializations(store, profile, desired, receipts)


def _materialize_plan(
    store: Store,
    selection: ProfileSelection,
    plan: _ReconcilePlan,
    adapters: object,
    *,
    store_lock_descriptor: int,
) -> tuple[SharedPluginMaterialization, ...]:
    enabled = tuple(item for item in plan.desired_plugins if item.enabled)
    if not enabled:
        return ()
    if plan.source_profile == plan.target_profile:
        return _local_materializations(store, str(plan.target_profile), enabled)
    target_config = _config_path(store, str(plan.target_profile))
    planned_before = _ConfigSnapshot(
        kind=plan.target_observation.config_kind,
        payload=plan.target_observation.raw_text.encode(),
        mode=plan.target_observation.config_mode,
    )
    before = _config_snapshot(target_config)
    if before != planned_before:
        raise SwitchError("shared_configuration.target_changed_during_plan")
    if plan.target_profile == OFFICIAL_PROFILE and _app_running(
        adapters, store, selection
    ):
        raise _OfficialAppApplyPending()
    selectors = tuple(sorted({item.selector for item in enabled}))
    _write_pending_materialization(
        store,
        source_profile=str(plan.source_profile),
        target_profile=str(plan.target_profile),
        target_path=target_config,
        before=before,
        selectors=selectors,
    )
    plugin_label = "Plugin" if len(enabled) == 1 else "Plugins"
    _report_progress(
        adapters,
        "Shared configuration: materializing "
        f"{len(enabled)} {plugin_label} for {plan.target_profile}...",
    )
    materializer = getattr(adapters, "materialize_plugins", _default_materialize_plugins)
    try:
        raw = materializer(
            store=store,
            selection=selection,
            source_profile=plan.source_profile,
            target_profile=plan.target_profile,
            desired_plugins=enabled,
            generation=plan.generation_after,
            _store_lock_descriptor=store_lock_descriptor,
        )
    except Exception:
        _recover_pending_materialization(store)
        raise
    _recover_pending_materialization(store)
    if _config_snapshot(target_config) != before:
        raise SwitchError("shared_configuration.target_changed_during_plan")
    return _validate_materializations(store, str(plan.target_profile), enabled, tuple(raw))


def _target_skill_path(
    skill: Mapping[str, Any],
    target_home: Path,
    receipts: Mapping[str, SharedPluginMaterialization],
) -> str:
    if skill.get("owner") != "plugin-cache":
        return str(skill.get("path", ""))
    relative = Path(str(skill.get("path", "")))
    parts = relative.parts
    if relative.is_absolute() or ".." in parts or len(parts) < 3:
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    marketplace, plugin, source_key = parts[:3]
    selector = f"{plugin}@{marketplace}"
    receipt = receipts.get(selector)
    if receipt is None:
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    cache_root = target_home / "plugins" / "cache"
    base, _plugin, _marketplace = _receipt_artifact(cache_root, receipt)
    target = base.joinpath(*parts[3:])
    try:
        resolved_cache = cache_root.resolve(strict=True)
        resolved_base = base.resolve(strict=True)
        resolved_target = target.resolve(strict=True)
        resolved_base.relative_to(resolved_cache)
        resolved_target.relative_to(resolved_base)
    except (OSError, RuntimeError, ValueError):
        raise SwitchError("shared_configuration.materialization.unsafe_cache") from None
    if not (resolved_target.is_dir() or resolved_target.is_file()):
        raise SwitchError("shared_configuration.materialization.unsafe_cache")
    return str(resolved_target)


def _runtime_projection(
    projection: Mapping[str, Any],
    target_home: Path,
    materializations: Sequence[SharedPluginMaterialization],
) -> dict[str, Any]:
    receipts = {item.selector: item for item in materializations}
    result = _clone_json(projection)
    rendered_skills: list[dict[str, Any]] = []
    for skill in result.get("skills", []):
        rendered_skills.append(
            {
                "path": _target_skill_path(skill, target_home, receipts),
                "enabled": bool(skill.get("enabled", True)),
            }
        )
    result["skills"] = rendered_skills
    return result


def _toml_key(value: str) -> str:
    return value if BARE_TOML_KEY_RE.fullmatch(value) else json.dumps(value, ensure_ascii=False)


def _toml_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, int) and not isinstance(value, bool):
        return str(value)
    if isinstance(value, list):
        return "[" + ", ".join(_toml_value(item) for item in value) + "]"
    if isinstance(value, Mapping):
        return "{ " + ", ".join(
            f"{_toml_key(str(key))} = {_toml_value(item)}"
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        ) + " }"
    raise SwitchError("shared_configuration.marketplace_schema")


def _render_runtime_projection(projection: Mapping[str, Any]) -> str:
    lines: list[str] = []
    for marketplace, values in sorted(projection.get("marketplaces", {}).items()):
        lines.append(f"[marketplaces.{_toml_key(str(marketplace))}]")
        for key, value in sorted(values.items()):
            lines.append(f"{_toml_key(str(key))} = {_toml_value(value)}")
        lines.append("")
    for selector, values in sorted(projection.get("plugins", {}).items()):
        lines.append(f"[plugins.{_toml_key(str(selector))}]")
        lines.append(f"enabled = {'true' if values.get('enabled', True) else 'false'}")
        lines.append("")
    for skill in projection.get("skills", []):
        lines.append("[[skills.config]]")
        lines.append(f"path = {_toml_value(str(skill['path']))}")
        lines.append(f"enabled = {'true' if skill.get('enabled', True) else 'false'}")
        lines.append("")
    return "\n".join(lines).rstrip() + ("\n" if lines else "")


def _render_generation_projection(projection: Mapping[str, Any]) -> str:
    lines = [f"schema_version = {SHARED_CONFIGURATION_SCHEMA}", ""]
    for marketplace, values in sorted(projection.get("marketplaces", {}).items()):
        lines.append(f"[marketplaces.{_toml_key(str(marketplace))}]")
        for key, value in sorted(values.items()):
            lines.append(f"{_toml_key(str(key))} = {_toml_value(value)}")
        lines.append("")
    for selector, values in sorted(projection.get("plugins", {}).items()):
        lines.append(f"[plugins.{_toml_key(str(selector))}]")
        lines.append(f"enabled = {'true' if values.get('enabled', True) else 'false'}")
        lines.append("")
    for skill in projection.get("skills", []):
        lines.append("[[skills.config]]")
        lines.append(f"owner = {_toml_value(str(skill['owner']))}")
        lines.append(f"path = {_toml_value(str(skill['path']))}")
        lines.append(f"enabled = {'true' if skill.get('enabled', True) else 'false'}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def _replace_shared_projection(target_text: str, projection_text: str, *, label: str) -> str:
    target = ConfigDocument.parse(target_text, f"{label} target")
    without_shared = target.select(
        include_top_level=lambda _path: True,
        include_table=lambda path, _is_array: not (
            bool(path)
            and (path[0] in SHARED_TABLE_ROOTS or path[:2] == ("skills", "config"))
        ),
        label=f"{label} without shared Plugin/Skill projection",
    )
    desired = ConfigDocument.parse(projection_text, f"{label} desired projection")
    recovered = without_shared.recover_missing_from(
        desired,
        protected_paths=frozenset(),
    )
    if recovered.diagnostics:
        codes = ", ".join(sorted({item.code for item in recovered.diagnostics}))
        raise SwitchError(f"shared_configuration.render_failed: {codes}")
    return recovered.text


def _materialization_json(
    receipts: Sequence[SharedPluginMaterialization],
) -> list[dict[str, Any]]:
    return [
        {
            "selector": item.selector,
            "policy": item.policy,
            "cache_key": item.cache_key,
            "manifest_version": item.manifest_version,
            "tree_sha256": item.tree_sha256,
            "skill_roots": list(item.skill_roots),
        }
        for item in receipts
    ]


def _snapshot_json(snapshot: _ConfigSnapshot) -> dict[str, Any]:
    return {
        "kind": snapshot.kind,
        "payload_base64": base64.b64encode(snapshot.payload).decode(),
        "payload_sha256": snapshot.sha256,
        "mode": snapshot.mode,
    }


def _snapshot_from_json(value: object) -> _ConfigSnapshot:
    if not isinstance(value, Mapping):
        raise SwitchError("shared_configuration.pending_recovery")
    kind = value.get("kind")
    encoded = value.get("payload_base64")
    digest = value.get("payload_sha256")
    mode = value.get("mode")
    if (
        kind not in {"missing", "regular"}
        or not isinstance(encoded, str)
        or not _valid_sha256(digest)
        or not isinstance(mode, int)
        or mode < 0
        or mode > 0o7777
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    try:
        payload = base64.b64decode(encoded.encode(), validate=True)
    except (ValueError, TypeError) as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    snapshot = _ConfigSnapshot(kind=str(kind), payload=payload, mode=mode)
    if snapshot.sha256 != digest or (kind == "missing" and payload):
        raise SwitchError("shared_configuration.pending_recovery")
    return snapshot


def _link_snapshot(path: Path) -> dict[str, Any]:
    try:
        metadata = path.lstat()
    except FileNotFoundError:
        return {"kind": "missing", "target": ""}
    except OSError as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    if not stat.S_ISLNK(metadata.st_mode):
        raise SwitchError("shared_configuration.pending_recovery")
    try:
        target = os.readlink(path)
    except OSError as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    return {"kind": "symlink", "target": target}


def _valid_link_snapshot(value: object) -> bool:
    return bool(
        isinstance(value, Mapping)
        and value.get("kind") in {"missing", "symlink"}
        and isinstance(value.get("target"), str)
        and (value.get("kind") == "symlink" or value.get("target") == "")
    )


def _journal_sha256(value: Mapping[str, Any]) -> str:
    payload = dict(value)
    payload.pop("journal_sha256", None)
    return _semantic_sha256(payload)


def _materialization_intent_sha256(value: Mapping[str, Any]) -> str:
    payload = dict(value)
    payload.pop("intent_sha256", None)
    return _semantic_sha256(payload)


def _ensure_private_durable_directory(path: Path) -> None:
    try:
        path.mkdir(mode=0o700)
    except FileExistsError:
        _real_private_directory_exists(
            path,
            unsafe_code="shared_configuration.pending_recovery",
        )
    except OSError as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    else:
        _fsync_directory(path.parent)


def _write_pending_journal(store: Store, journal: dict[str, Any]) -> None:
    _validate_shared_storage(store)
    shared_root = _shared_root(store)
    _ensure_private_durable_directory(shared_root)
    _ensure_private_durable_directory(shared_root / "generations")
    path = _pending_commit_path(store)
    materialization_path = _pending_materialization_path(store)
    if (
        path.exists()
        or path.is_symlink()
        or materialization_path.exists()
        or materialization_path.is_symlink()
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    journal["journal_sha256"] = _journal_sha256(journal)
    write_json(path, journal)


def _write_pending_materialization(
    store: Store,
    *,
    source_profile: str,
    target_profile: str,
    target_path: Path,
    before: _ConfigSnapshot,
    selectors: tuple[str, ...],
) -> None:
    _validate_shared_storage(store)
    shared_root = _shared_root(store)
    remove_empty_root = not shared_root.exists()
    _ensure_private_durable_directory(shared_root)
    intent_path = _pending_materialization_path(store)
    commit_path = _pending_commit_path(store)
    if (
        intent_path.exists()
        or intent_path.is_symlink()
        or commit_path.exists()
        or commit_path.is_symlink()
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    intent = {
        "schema_version": PENDING_MATERIALIZATION_SCHEMA,
        "source_profile": source_profile,
        "target_profile": target_profile,
        "target": {
            "path": str(target_path),
            "before": _snapshot_json(before),
        },
        "selectors": list(selectors),
        "remove_empty_root": remove_empty_root,
    }
    intent["intent_sha256"] = _materialization_intent_sha256(intent)
    write_json(intent_path, intent)
    if _load_pending_materialization(store) != intent:
        raise SwitchError("shared_configuration.pending_recovery")


def _load_pending_materialization(store: Store) -> dict[str, Any] | None:
    _validate_shared_storage(store)
    path = _pending_materialization_path(store)
    if not path.exists() and not path.is_symlink():
        return None
    commit_path = _pending_commit_path(store)
    if commit_path.exists() or commit_path.is_symlink():
        raise SwitchError("shared_configuration.pending_recovery")
    snapshot = _path_snapshot(
        path,
        unsafe_code="shared_configuration.pending_recovery",
    )
    if snapshot.kind != "regular" or snapshot.mode != 0o600:
        raise SwitchError("shared_configuration.pending_recovery")
    try:
        intent = json.loads(snapshot.payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    if (
        not isinstance(intent, dict)
        or set(intent)
        != {
            "schema_version",
            "source_profile",
            "target_profile",
            "target",
            "selectors",
            "remove_empty_root",
            "intent_sha256",
        }
        or intent.get("schema_version") != PENDING_MATERIALIZATION_SCHEMA
        or intent.get("intent_sha256")
        != _materialization_intent_sha256(intent)
        or intent.get("source_profile") not in SUPPORTED_SELECTION
        or intent.get("target_profile") not in SUPPORTED_SELECTION
        or intent.get("source_profile") == intent.get("target_profile")
        or not isinstance(intent.get("target"), Mapping)
        or set(intent["target"]) != {"path", "before"}
        or not isinstance(intent.get("selectors"), list)
        or not isinstance(intent.get("remove_empty_root"), bool)
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    target_profile = str(intent["target_profile"])
    if intent["target"].get("path") != str(_config_path(store, target_profile)):
        raise SwitchError("shared_configuration.pending_recovery")
    selectors = intent["selectors"]
    if (
        not selectors
        or any(
            not isinstance(selector, str) or _selector_parts(selector) is None
            for selector in selectors
        )
        or selectors != sorted(set(selectors))
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    _snapshot_from_json(intent["target"].get("before"))
    return intent


def _load_pending_journal(store: Store) -> dict[str, Any] | None:
    _validate_shared_storage(store)
    path = _pending_commit_path(store)
    if not path.exists() and not path.is_symlink():
        return None
    snapshot = _path_snapshot(
        path,
        unsafe_code="shared_configuration.pending_recovery",
    )
    try:
        journal = json.loads(snapshot.payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    if (
        not isinstance(journal, dict)
        or journal.get("schema_version") != PENDING_COMMIT_SCHEMA
        or journal.get("journal_sha256") != _journal_sha256(journal)
        or not isinstance(journal.get("source"), Mapping)
        or not isinstance(journal.get("target"), Mapping)
        or not isinstance(journal.get("personal_skills"), Mapping)
        or not isinstance(journal.get("generation"), Mapping)
        or not isinstance(journal.get("expected_state"), Mapping)
        or not _valid_sha256(journal.get("expected_state_sha256"))
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    target = journal["target"]
    source = journal["source"]
    personal = journal["personal_skills"]
    generation = journal["generation"]
    if (
        not isinstance(source.get("path"), str)
        or source.get("kind") not in {"missing", "regular"}
        or not _valid_sha256(source.get("payload_sha256"))
        or not isinstance(source.get("mode"), int)
        or not isinstance(target.get("path"), str)
        or not isinstance(personal.get("path"), str)
        or not _valid_link_snapshot(personal.get("before"))
        or not _valid_link_snapshot(personal.get("after"))
        or not isinstance(generation.get("number"), int)
        or generation.get("number", 0) < 1
        or not isinstance(generation.get("path"), str)
        or not isinstance(generation.get("payload_base64"), str)
        or not _valid_sha256(generation.get("payload_sha256"))
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    _snapshot_from_json(target.get("before"))
    _snapshot_from_json(target.get("after"))
    _snapshot_from_json(journal.get("predecessor_state"))
    expected_payload = _json_payload(dict(journal["expected_state"]))
    if _sha256_bytes(expected_payload) != journal["expected_state_sha256"]:
        raise SwitchError("shared_configuration.pending_recovery")
    try:
        generation_payload = base64.b64decode(
            str(generation["payload_base64"]).encode(),
            validate=True,
        )
    except (ValueError, TypeError) as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    if _sha256_bytes(generation_payload) != generation["payload_sha256"]:
        raise SwitchError("shared_configuration.pending_recovery")
    try:
        projection = _validate_persisted_projection(journal.get("projection"))
        raw_receipts = journal.get("materializations")
        if not isinstance(raw_receipts, list):
            raise SwitchError("shared_configuration.pending_recovery")
        receipts = tuple(_normalize_materialization(item) for item in raw_receipts)
    except SwitchError as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    expected_state = journal["expected_state"]
    if (
        generation_payload != _render_generation_projection(projection).encode()
        or expected_state.get("schema_version") != SHARED_CONFIGURATION_SCHEMA
        or expected_state.get("generation") != generation["number"]
        or expected_state.get("projection") != projection
        or expected_state.get("projection_sha256") != _semantic_sha256(projection)
        or any(not _valid_sha256(receipt.tree_sha256) for receipt in receipts)
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    return journal


def _fsync_directory(path: Path) -> None:
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _durable_unlink(path: Path) -> None:
    path.unlink()
    _fsync_directory(path.parent)


def _retire_materialization_intent(
    store: Store,
    intent: Mapping[str, Any],
) -> None:
    shared_root = _shared_root(store)
    _durable_unlink(_pending_materialization_path(store))
    if not bool(intent.get("remove_empty_root")):
        return
    try:
        shared_root.rmdir()
    except OSError:
        # Another durable shared artifact (or a foreign entry) now owns the
        # directory.  Never remove it recursively or guess at ownership.
        return
    _fsync_directory(shared_root.parent)


def _restore_snapshot(path: Path, snapshot: _ConfigSnapshot) -> None:
    current = _config_snapshot(path)
    if current == snapshot:
        return
    if snapshot.kind == "regular":
        atomic_write(path, snapshot.payload, mode=snapshot.mode)
        return
    if current.kind != "regular":
        raise SwitchError("shared_configuration.pending_recovery")
    _durable_unlink(path)


def _replace_snapshot_if_unchanged(
    path: Path,
    *,
    observed: _ConfigSnapshot,
    replacement: _ConfigSnapshot,
) -> None:
    if _config_snapshot(path) != observed:
        raise SwitchError("shared_configuration.target_changed_during_plan")
    try:
        if replacement.kind == "regular":
            atomic_write(path, replacement.payload, mode=replacement.mode)
        elif observed.kind == "regular":
            _durable_unlink(path)
        else:
            raise SwitchError("shared_configuration.pending_recovery")
    except OSError as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    if _config_snapshot(path) != replacement:
        raise SwitchError("shared_configuration.pending_recovery")


def _recover_pending_materialization(store: Store) -> str | None:
    intent = _load_pending_materialization(store)
    if intent is None:
        return None
    target = intent["target"]
    target_path = Path(str(target["path"]))
    before = _snapshot_from_json(target["before"])
    try:
        current = _config_snapshot(target_path)
    except SwitchError as error:
        raise SwitchError("shared_configuration.pending_recovery") from error
    if current == before:
        _retire_materialization_intent(store, intent)
        return "clean"
    if current.kind != "regular":
        raise SwitchError("shared_configuration.pending_recovery")

    from codex_switch_plugins import _scrub_expected_plugin_activations

    scrub_result = _scrub_expected_plugin_activations(
        before=before.payload if before.kind == "regular" else b"",
        after=current.payload,
        selectors=tuple(str(value) for value in intent["selectors"]),
    )
    if scrub_result is None:
        # A bounded selector changed, but not as an exact native-add
        # activation.  Keep the intent so a later apply cannot guess or erase.
        raise SwitchError("shared_configuration.pending_recovery")
    scrubbed, removed_activation = scrub_result
    if not removed_activation:
        # Foreign-only drift is classified and preserved.  It no longer needs
        # operation recovery, but it must block this apply before planning.
        _retire_materialization_intent(store, intent)
        raise SwitchError("shared_configuration.target_changed_during_plan")

    if (
        before.kind == "regular"
        and scrubbed == before.payload
        and current.mode == before.mode
    ):
        _replace_snapshot_if_unchanged(
            target_path,
            observed=current,
            replacement=before,
        )
        _retire_materialization_intent(store, intent)
        return "restored"
    if before.kind == "missing" and not scrubbed.strip():
        _replace_snapshot_if_unchanged(
            target_path,
            observed=current,
            replacement=before,
        )
        _retire_materialization_intent(store, intent)
        return "restored"

    # The exact operation-owned activation was removed, while foreign bytes
    # and their mode remain.  Publish that selective scrub with target CAS,
    # retire the intent durably, and block the apply on the preserved drift.
    scrubbed_snapshot = _ConfigSnapshot(
        kind="regular",
        payload=scrubbed,
        mode=current.mode,
    )
    _replace_snapshot_if_unchanged(
        target_path,
        observed=current,
        replacement=scrubbed_snapshot,
    )
    _retire_materialization_intent(store, intent)
    raise SwitchError("shared_configuration.target_changed_during_plan")


def _recover_pending_commit(store: Store) -> str | None:
    journal = _load_pending_journal(store)
    if journal is None:
        return None
    allowed_configs = {
        str(_config_path(store, OFFICIAL_PROFILE)),
        str(_config_path(store, INTERNAL_PROFILE)),
    }
    source = journal["source"]
    target = journal["target"]
    personal = journal["personal_skills"]
    generation = journal["generation"]
    if (
        source.get("path") not in allowed_configs
        or target.get("path") not in allowed_configs
        or personal.get("path")
        != str(_profile_home(store, INTERNAL_PROFILE) / "skills")
        or generation.get("path")
        != str(_generation_path(store, int(generation["number"])))
        or journal["expected_state"].get("generation") != generation["number"]
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    expected_state = dict(journal["expected_state"])
    expected_state_payload = _json_payload(expected_state)
    state_path = _state_path(store)
    current_state = _path_snapshot(
        state_path,
        unsafe_code="shared_configuration.pending_recovery",
    )
    if (
        current_state.kind == "regular"
        and current_state.payload == expected_state_payload
        and current_state.sha256 == journal["expected_state_sha256"]
    ):
        _load_state(store)
        _durable_unlink(_pending_commit_path(store))
        return "committed"

    predecessor_state = _snapshot_from_json(journal["predecessor_state"])
    if current_state != predecessor_state:
        raise SwitchError("shared_configuration.pending_recovery")

    target_path = Path(str(target["path"]))
    target_before = _snapshot_from_json(target["before"])
    target_after = _snapshot_from_json(target["after"])
    current_target = _config_snapshot(target_path)
    target_needs_restore = current_target == target_after and current_target != target_before
    if current_target != target_before and current_target != target_after:
        raise SwitchError("shared_configuration.pending_recovery")

    link_path = Path(str(personal["path"]))
    link_before = dict(personal["before"])
    link_after = dict(personal["after"])
    current_link = _link_snapshot(link_path)
    link_needs_restore = current_link == link_after and current_link != link_before
    if link_needs_restore and (
        current_link.get("kind") != "symlink" or link_before.get("kind") != "missing"
    ):
        raise SwitchError("shared_configuration.pending_recovery")
    if current_link != link_before and current_link != link_after:
        raise SwitchError("shared_configuration.pending_recovery")

    # Classify every rollback target before the first recovery write. Foreign
    # drift on either surface must leave all expected transaction effects
    # untouched for operator inspection.
    if target_needs_restore:
        _restore_snapshot(target_path, target_before)
    if link_needs_restore:
        _durable_unlink(link_path)

    _durable_unlink(_pending_commit_path(store))
    return "rolled_back"


def _next_generation(store: Store, requested: int, previous: int) -> int:
    _validate_shared_storage(store)
    if requested <= previous:
        return requested
    generation = requested
    while _generation_path(store, generation).exists() or _generation_path(
        store, generation
    ).is_symlink():
        generation += 1
    return generation


def _checkpoint(adapters: object, phase: str, **kwargs: Any) -> None:
    callback = getattr(adapters, "commit_checkpoint", _default_commit_checkpoint)
    callback(phase=phase, **kwargs)


def _pending_app_receipt(plan: _ReconcilePlan) -> SharedConfigurationReceipt:
    return _receipt(
        status="pending",
        before=plan.generation_before,
        after=plan.generation_before,
        cli_ready=True,
        pending_target=OFFICIAL_PROFILE,
        findings=(
            _finding(
                "shared_configuration.pending_app_apply",
                "Quit the official App before applying shared configuration.",
                severity="warning",
            ),
        ),
        source_profile=plan.source_profile,
        target_profile=plan.target_profile,
    )


def _commit_plan(
    store: Store,
    selection: ProfileSelection,
    plan: _ReconcilePlan,
    adapters: object,
    previous_state: Mapping[str, Any] | None,
    *,
    store_lock_descriptor: int,
) -> SharedConfigurationReceipt:
    assert plan.source_observation is not None
    assert plan.target_observation is not None
    assert plan.projection is not None
    assert plan.source_profile is not None
    assert plan.target_profile is not None

    target_path = _config_path(store, plan.target_profile)
    target_before = _ConfigSnapshot(
        kind=plan.target_observation.config_kind,
        payload=plan.target_observation.raw_text.encode(),
        mode=plan.target_observation.config_mode,
    )
    try:
        materializations = _materialize_plan(
            store,
            selection,
            plan,
            adapters,
            store_lock_descriptor=store_lock_descriptor,
        )
    except _OfficialAppApplyPending:
        return _pending_app_receipt(plan)
    except (OSError, SwitchError) as error:
        code = _code_from_error(error, "shared_configuration.materialization.failed")
        return _blocked_receipt(
            plan.generation_before,
            _finding(code, str(error)),
            source_profile=plan.source_profile,
            target_profile=plan.target_profile,
        )

    callback = getattr(adapters, "before_commit", _default_before_commit)
    try:
        callback(store=store, selection=selection, plan=plan)
    except (OSError, SwitchError) as error:
        code = _code_from_error(error, "shared_configuration.materialization.failed")
        return _blocked_receipt(
            plan.generation_before,
            _finding(code, str(error)),
            source_profile=plan.source_profile,
            target_profile=plan.target_profile,
        )

    try:
        current_source = _observe_home(
            store,
            plan.source_profile,
            adapters,
            previous_state,
        )
    except (_ProjectionError, SwitchError):
        current_source = None
    if (
        current_source is None
        or current_source.raw_sha256 != plan.source_observation.raw_sha256
        or current_source.observation_sha256 != plan.source_observation.observation_sha256
    ):
        return _blocked_receipt(
            plan.generation_before,
            _finding(
                "shared_configuration.source_changed_during_plan",
                "The source configuration or artifact changed before commit.",
            ),
            source_profile=plan.source_profile,
            target_profile=plan.target_profile,
        )

    try:
        if _config_snapshot(target_path) != target_before:
            return _blocked_receipt(
                plan.generation_before,
                _finding(
                    "shared_configuration.target_changed_during_plan",
                    "The target configuration changed after the locked plan.",
                ),
                source_profile=plan.source_profile,
                target_profile=plan.target_profile,
            )
    except SwitchError as error:
        return _blocked_receipt(
            plan.generation_before,
            _finding(_code_from_error(error, "shared_configuration.target_config_unsafe"), str(error)),
            source_profile=plan.source_profile,
            target_profile=plan.target_profile,
        )

    if plan.target_profile == OFFICIAL_PROFILE and _app_running(
        adapters, store, selection
    ):
        return _pending_app_receipt(plan)

    try:
        materializations = _validate_materializations(
            store,
            plan.target_profile,
            plan.desired_plugins,
            materializations,
        )
    except SwitchError as error:
        return _blocked_receipt(
            plan.generation_before,
            _finding(
                _code_from_error(
                    error,
                    "shared_configuration.materialization.unsafe_cache",
                ),
                str(error),
            ),
            source_profile=plan.source_profile,
            target_profile=plan.target_profile,
        )

    internal_skills = _profile_home(store, INTERNAL_PROFILE) / "skills"
    projection = _clone_json(plan.projection)
    target_after = target_before
    try:
        if plan.target_profile != plan.source_profile:
            runtime_projection = _runtime_projection(
                projection,
                _profile_home(store, plan.target_profile),
                materializations,
            )
            rendered = _replace_shared_projection(
                target_before.payload.decode(),
                _render_runtime_projection(runtime_projection),
                label=f"shared configuration {plan.target_profile}",
            )
            rendered_payload = rendered.encode()
            target_after = _ConfigSnapshot(
                kind=(
                    "missing"
                    if target_before.kind == "missing" and not rendered_payload
                    else "regular"
                ),
                payload=rendered_payload,
                mode=target_before.mode,
            )

        materializations_by_profile: dict[str, Any] = {}
        if previous_state is not None and isinstance(
            previous_state.get("materializations"), Mapping
        ):
            materializations_by_profile = _clone_json(previous_state["materializations"])
        enabled_selectors = {
            selector
            for selector, value in projection.get("plugins", {}).items()
            if bool(value.get("enabled", True))
        }
        for profile, raw_receipts in tuple(materializations_by_profile.items()):
            if isinstance(raw_receipts, list):
                materializations_by_profile[profile] = [
                    receipt
                    for receipt in raw_receipts
                    if isinstance(receipt, Mapping)
                    and receipt.get("selector") in enabled_selectors
                ]
        materializations_by_profile[plan.target_profile] = _materialization_json(
            materializations
        )
        prospective_context = {"materializations": materializations_by_profile}
        raw_by_profile: dict[str, tuple[str, str, int]] = {}
        for profile in (OFFICIAL_PROFILE, INTERNAL_PROFILE):
            if profile == plan.target_profile:
                raw_by_profile[profile] = (
                    target_after.payload.decode(),
                    target_after.kind,
                    target_after.mode,
                )
                continue
            observation = _observe_home(
                store,
                profile,
                adapters,
                previous_state,
            )
            raw_by_profile[profile] = (
                observation.raw_text,
                observation.config_kind,
                observation.config_mode,
            )
        observations = {
            profile: _observation_from_text(
                store,
                profile,
                raw_by_profile[profile][0],
                config_kind=raw_by_profile[profile][1],
                config_mode=raw_by_profile[profile][2],
                state=prospective_context,
            )
            for profile in (OFFICIAL_PROFILE, INTERNAL_PROFILE)
        }
        state = {
            "schema_version": SHARED_CONFIGURATION_SCHEMA,
            "generation": plan.generation_after,
            "projection_sha256": _semantic_sha256(projection),
            "projection": projection,
            "producer_profile": plan.source_profile,
            "pending_target": plan.pending_target,
            "baselines": {
                profile: {
                    "observation_sha256": observation.observation_sha256,
                    "projection_sha256": observation.projection_sha256,
                }
                for profile, observation in observations.items()
            },
            "materializations": materializations_by_profile,
        }
        generation_payload = _render_generation_projection(projection).encode()
        generation_path = _generation_path(store, plan.generation_after)
        predecessor_state = _path_snapshot(
            _state_path(store),
            unsafe_code="shared_configuration.state_integrity",
        )
        expected_predecessor = (
            _ConfigSnapshot("missing", b"", 0o600)
            if previous_state is None
            else _ConfigSnapshot(
                "regular",
                _json_payload(previous_state),
                predecessor_state.mode,
            )
        )
        if predecessor_state != expected_predecessor:
            raise SwitchError("shared_configuration.state_changed_during_plan")
        link_before = _link_snapshot(internal_skills)
        link_after = dict(link_before)
        if plan.link_personal_skills:
            if link_before.get("kind") != "missing":
                raise SwitchError("shared_configuration.pending_recovery")
            link_after = {
                "kind": "symlink",
                "target": str(_profile_home(store, OFFICIAL_PROFILE) / "skills"),
            }
        expected_state_payload = _json_payload(state)
        journal = {
            "schema_version": PENDING_COMMIT_SCHEMA,
            "predecessor_state": _snapshot_json(predecessor_state),
            "source": {
                "path": str(_config_path(store, plan.source_profile)),
                "kind": current_source.config_kind,
                "payload_sha256": current_source.raw_sha256,
                "mode": current_source.config_mode,
            },
            "target": {
                "path": str(target_path),
                "before": _snapshot_json(target_before),
                "after": _snapshot_json(target_after),
            },
            "personal_skills": {
                "path": str(internal_skills),
                "before": link_before,
                "after": link_after,
            },
            "projection": projection,
            "materializations": _materialization_json(materializations),
            "generation": {
                "number": plan.generation_after,
                "path": str(generation_path),
                "payload_base64": base64.b64encode(generation_payload).decode(),
                "payload_sha256": _sha256_bytes(generation_payload),
            },
            "expected_state": state,
            "expected_state_sha256": _sha256_bytes(expected_state_payload),
        }
        _write_pending_journal(store, journal)
        _checkpoint(
            adapters,
            "prepared",
            store=store,
            selection=selection,
            plan=plan,
        )

        try:
            prepared_source = _observe_home(
                store,
                plan.source_profile,
                adapters,
                previous_state,
            )
        except (_ProjectionError, SwitchError):
            prepared_source = None
        if (
            prepared_source is None
            or prepared_source.raw_sha256 != plan.source_observation.raw_sha256
            or prepared_source.observation_sha256
            != plan.source_observation.observation_sha256
        ):
            _recover_pending_commit(store)
            return _blocked_receipt(
                plan.generation_before,
                _finding(
                    "shared_configuration.source_changed_during_plan",
                    "The source configuration or artifact changed before publication.",
                ),
                source_profile=plan.source_profile,
                target_profile=plan.target_profile,
            )
        try:
            materializations = _validate_materializations(
                store,
                plan.target_profile,
                plan.desired_plugins,
                materializations,
            )
        except SwitchError as error:
            _recover_pending_commit(store)
            return _blocked_receipt(
                plan.generation_before,
                _finding(
                    _code_from_error(
                        error,
                        "shared_configuration.materialization.unsafe_cache",
                    ),
                    str(error),
                ),
                source_profile=plan.source_profile,
                target_profile=plan.target_profile,
            )
        if _config_snapshot(target_path) != target_before:
            _recover_pending_commit(store)
            return _blocked_receipt(
                plan.generation_before,
                _finding(
                    "shared_configuration.target_changed_during_plan",
                    "The target configuration changed before publication.",
                ),
                source_profile=plan.source_profile,
                target_profile=plan.target_profile,
            )
        if plan.target_profile == OFFICIAL_PROFILE and _app_running(
            adapters, store, selection
        ):
            _recover_pending_commit(store)
            return _pending_app_receipt(plan)

        if target_after != target_before:
            if target_after.kind != "regular":
                raise SwitchError("shared_configuration.target_config_unsafe")
            atomic_write(target_path, target_after.payload, mode=target_after.mode)
        if _config_snapshot(target_path) != target_after:
            raise SwitchError("shared_configuration.target_changed_during_plan")
        _checkpoint(
            adapters,
            "target_config_written",
            store=store,
            selection=selection,
            plan=plan,
        )

        if plan.link_personal_skills:
            internal_skills.symlink_to(
                _profile_home(store, OFFICIAL_PROFILE) / "skills",
                target_is_directory=True,
            )
            _fsync_directory(internal_skills.parent)
        if _link_snapshot(internal_skills) != link_after:
            raise SwitchError("shared_configuration.pending_recovery")
        _checkpoint(
            adapters,
            "personal_skills_link_created",
            store=store,
            selection=selection,
            plan=plan,
        )

        if generation_path.exists() or generation_path.is_symlink():
            if (
                generation_path.is_symlink()
                or not generation_path.is_file()
                or generation_path.read_bytes() != generation_payload
            ):
                raise SwitchError("shared_configuration.generation_collision")
        else:
            atomic_write(generation_path, generation_payload, mode=0o600)
        _checkpoint(
            adapters,
            "generation_published",
            store=store,
            selection=selection,
            plan=plan,
        )

        write_json(_state_path(store), state)
        _checkpoint(
            adapters,
            "state_published",
            store=store,
            selection=selection,
            plan=plan,
        )
        if _state_path(store).read_bytes() != expected_state_payload:
            raise SwitchError("shared_configuration.state_integrity")
        _load_state(store)
        _durable_unlink(_pending_commit_path(store))
    except Exception as error:
        recovery_outcome = None
        if _pending_commit_path(store).exists() or _pending_commit_path(store).is_symlink():
            recovery_outcome = _recover_pending_commit(store)
        if recovery_outcome != "committed":
            if isinstance(error, SwitchError):
                raise
            raise SwitchError("shared_configuration.commit_failed") from error

    status = "pending" if plan.pending_target else "applied"
    findings = list(plan.findings)
    if plan.pending_target:
        findings.append(
            _finding(
                "shared_configuration.pending_app_apply",
                "Shared configuration is waiting for a stopped-App apply.",
                severity="warning",
            )
        )
    return _receipt(
        status=status,
        before=plan.generation_before,
        after=plan.generation_after,
        cli_ready=True,
        pending_target=plan.pending_target,
        materializations=materializations,
        findings=findings,
        source_profile=plan.source_profile,
        target_profile=plan.target_profile,
        actions=plan.actions,
    )


def reconcile_shared_configuration(
    store: Store,
    selection: ProfileSelection,
    *,
    boundary: str = "cli-preflight",
    mode: str = "apply",
    adapters: object | None = None,
) -> SharedConfigurationReceipt:
    if boundary not in {"cli-preflight", "explicit-sync", "verify"}:
        raise SwitchError(f"shared_configuration.invalid_boundary: {boundary}")
    if mode not in {"plan", "apply", "verify"}:
        raise SwitchError(f"shared_configuration.invalid_mode: {mode}")
    selected_adapters = adapters or SharedConfigurationAdapters()
    if mode == "verify" or boundary == "verify":
        return shared_configuration_report(store, selection)

    try:
        _validate_shared_storage(store)
    except SwitchError as error:
        return _blocked_receipt(
            0,
            _finding(
                _code_from_error(error, "shared_configuration.state_integrity"),
                str(error),
            ),
        )
    pending_commit = _pending_commit_path(store)
    pending_materialization = _pending_materialization_path(store)
    if mode == "plan" and (
        pending_commit.exists()
        or pending_commit.is_symlink()
        or pending_materialization.exists()
        or pending_materialization.is_symlink()
    ):
        return _blocked_receipt(
            0,
            _finding(
                "shared_configuration.pending_recovery",
                "Shared configuration has unfinished locked recovery.",
            ),
        )

    planned: _ReconcilePlan | SharedConfigurationReceipt | None = None
    try:
        if not (
            pending_commit.exists()
            or pending_commit.is_symlink()
            or pending_materialization.exists()
            or pending_materialization.is_symlink()
        ):
            planned = _plan_reconcile(
                store,
                selection,
                boundary=boundary,
                adapters=selected_adapters,
            )
    except SwitchError as error:
        generation = 0
        try:
            state = _load_state(store)
            generation = int(state["generation"]) if state is not None else 0
        except SwitchError:
            pass
        return _blocked_receipt(
            generation,
            _finding(_code_from_error(error, "shared_configuration.failed"), str(error)),
        )
    if isinstance(planned, SharedConfigurationReceipt):
        return planned
    if mode == "plan":
        assert planned is not None
        return _receipt(
            status="planned",
            before=planned.generation_before,
            after=planned.generation_after,
            cli_ready=False,
            pending_target=planned.pending_target,
            findings=planned.findings,
            source_profile=planned.source_profile,
            target_profile=planned.target_profile,
            actions=planned.actions,
        )

    # Plan again while holding the existing store-wide cooperative mutation lock.
    from codex_switch_transaction import locked_store_mutation

    try:
        with locked_store_mutation(
            store,
            operation="shared configuration reconcile",
            create_if_missing=False,
        ) as locked:
            locked.revalidate()
            _recover_pending_materialization(store)
            _recover_pending_commit(store)
            previous_state = _load_state(store)
            locked_plan = _plan_reconcile(
                store,
                selection,
                boundary=boundary,
                adapters=selected_adapters,
            )
            if isinstance(locked_plan, SharedConfigurationReceipt):
                return locked_plan
            allocated_generation = _next_generation(
                store,
                locked_plan.generation_after,
                locked_plan.generation_before,
            )
            if allocated_generation != locked_plan.generation_after:
                locked_plan = replace(
                    locked_plan,
                    generation_after=allocated_generation,
                )
            return _commit_plan(
                store,
                selection,
                locked_plan,
                selected_adapters,
                previous_state,
                store_lock_descriptor=(
                    locked._shared_materializer_lease_descriptor(store)
                ),
            )
    except SwitchError as error:
        generation = (
            planned.generation_before
            if isinstance(planned, _ReconcilePlan)
            else 0
        )
        return _blocked_receipt(
            generation,
            _finding(_code_from_error(error, "shared_configuration.failed"), str(error)),
            source_profile=(
                planned.source_profile if isinstance(planned, _ReconcilePlan) else None
            ),
            target_profile=(
                planned.target_profile if isinstance(planned, _ReconcilePlan) else None
            ),
        )


def shared_configuration_report(
    store: Store,
    selection: ProfileSelection,
) -> SharedConfigurationReceipt:
    try:
        _validate_supported_selection(selection)
    except SwitchError as error:
        return _blocked_receipt(
            0,
            _finding(
                _code_from_error(
                    error,
                    "shared_configuration.unsupported_selection",
                ),
                str(error),
            ),
        )
    try:
        _validate_shared_storage(store)
    except SwitchError as error:
        return _blocked_receipt(
            0,
            _finding(
                _code_from_error(error, "shared_configuration.state_integrity"),
                str(error),
            ),
        )
    if (
        _pending_commit_path(store).exists()
        or _pending_commit_path(store).is_symlink()
        or _pending_materialization_path(store).exists()
        or _pending_materialization_path(store).is_symlink()
    ):
        generation = 0
        try:
            current_state = _load_state(store)
            if current_state is not None:
                generation = int(current_state["generation"])
        except SwitchError:
            pass
        return _blocked_receipt(
            generation,
            _finding(
                "shared_configuration.pending_recovery",
                "Shared configuration has unfinished locked recovery.",
            ),
        )
    try:
        state = _load_state(store)
    except SwitchError as error:
        return _blocked_receipt(
            0,
            _finding(_code_from_error(error, "shared_configuration.state_schema"), str(error)),
        )
    generation = int(state["generation"]) if state is not None else 0
    link_personal, skills_problem = _validate_personal_skills(store)
    if skills_problem is not None:
        return _blocked_receipt(generation, skills_problem)
    cache_problem = _cache_root_problem(store)
    if cache_problem is not None:
        return _blocked_receipt(generation, cache_problem)
    if state is None:
        return _receipt(
            status="missing",
            before=0,
            after=0,
            cli_ready=True,
            findings=(
                _finding(
                    "shared_configuration.bootstrap_required",
                    "The next functional internal CLI invocation will bootstrap shared state.",
                    severity="info",
                ),
            ),
        )
    if link_personal:
        return _receipt(
            status="stale",
            before=generation,
            after=generation,
            cli_ready=False,
            findings=(
                _finding(
                    "shared_configuration.personal_skills.link_required",
                    "The internal personal Skills link is missing.",
                    severity="warning",
                ),
            ),
        )
    adapters = SharedConfigurationAdapters()
    try:
        official = _observe_home(store, OFFICIAL_PROFILE, adapters, state)
        internal = _observe_home(store, INTERNAL_PROFILE, adapters, state)
    except _ProjectionError as error:
        return _blocked_receipt(generation, _finding(error.code, error.message))
    except SwitchError as error:
        return _blocked_receipt(
            generation,
            _finding(_code_from_error(error, "shared_configuration.failed"), str(error)),
        )
    official_changed = official.observation_sha256 != _baseline_hash(state, OFFICIAL_PROFILE)
    internal_changed = internal.observation_sha256 != _baseline_hash(state, INTERNAL_PROFILE)
    pending_target = state.get("pending_target")
    try:
        internal_materializations = _validate_materializations(
            store,
            INTERNAL_PROFILE,
            internal.desired_plugins,
            _stored_materializations(state, INTERNAL_PROFILE),
        )
    except SwitchError as error:
        return _blocked_receipt(
            generation,
            _finding(
                _code_from_error(
                    error,
                    "shared_configuration.materialization.unsafe_cache",
                ),
                str(error),
            ),
        )
    if pending_target:
        if official_changed or internal_changed:
            return _receipt(
                status="conflict",
                before=generation,
                after=generation,
                cli_ready=False,
                findings=(
                    _finding(
                        "shared_configuration.conflict",
                        "A profile changed while an App apply was pending.",
                    ),
                ),
            )
        return _receipt(
            status="pending",
            before=generation,
            after=generation,
            cli_ready=True,
            pending_target=str(pending_target),
            materializations=internal_materializations,
            findings=(
                _finding(
                    "shared_configuration.pending_app_apply",
                    "Shared configuration is waiting for a stopped-App apply.",
                    severity="warning",
                ),
            ),
        )
    if not official_changed and not internal_changed:
        return _receipt(
            status="current",
            before=generation,
            after=generation,
            cli_ready=True,
            materializations=internal_materializations,
        )
    if official_changed and internal_changed and not _same_semantic_change(official, internal):
        return _receipt(
            status="conflict",
            before=generation,
            after=generation,
            cli_ready=False,
            findings=(
                _finding(
                    "shared_configuration.conflict",
                    "Official App and internal CLI diverged from the shared baseline.",
                ),
            ),
        )
    return _receipt(
        status="stale",
        before=generation,
        after=generation,
        cli_ready=False,
        findings=(
            _finding(
                "shared_configuration.reconcile_required",
                "A functional internal CLI preflight must reconcile the changed projection.",
                severity="warning",
            ),
        ),
    )


def _official_home_from_store_root(store_root: Path) -> Path:
    manifest = store_root / "profiles" / OFFICIAL_PROFILE / "manifest.json"
    if manifest.exists():
        try:
            raw = read_json(manifest).get("codex_home")
        except SwitchError:
            raw = None
        if isinstance(raw, str) and raw and Path(raw).expanduser().is_absolute():
            return Path(raw).expanduser()
    return Path.home() / ".codex"


def preflight_internal_shared_configuration(
    *,
    store_root: Path,
    internal_home: Path,
    backend_args: Sequence[str] = (),
) -> SharedConfigurationReceipt:
    del backend_args
    active_path = Path(store_root) / "active.json"
    if not active_path.exists():
        raise SwitchError("shared_configuration.active_selection_missing")
    active = read_json(active_path)
    selection = active_profile_selection(active)
    if (selection.cli_profile, selection.app_profile) != SUPPORTED_SELECTION:
        return _receipt(
            status="not_applicable",
            before=0,
            after=0,
            cli_ready=True,
        )
    launch_agent_raw = active.get("launch_agent_path") or active.get("launch_agent")
    launch_agent = (
        Path(str(launch_agent_raw)).expanduser()
        if launch_agent_raw
        else Path.home() / "Library" / "LaunchAgents" / "com.openai.codex.plist"
    )
    store = Store(
        Path(store_root),
        official_codex_home=_official_home_from_store_root(Path(store_root)),
        internal_codex_home=Path(internal_home),
        launch_agent_path=launch_agent,
        launch_agent_label="com.openai.codex",
    )
    adapters = SharedConfigurationAdapters(progress=_stderr_progress)
    _report_progress(
        adapters,
        "Shared configuration: attesting source configuration and Plugin identities...",
    )
    receipt = reconcile_shared_configuration(
        store,
        selection,
        boundary="cli-preflight",
        mode="apply",
        adapters=adapters,
    )
    if not receipt.cli_ready:
        codes = ", ".join(finding.code for finding in receipt.findings) or receipt.status
        raise SwitchError(f"shared_configuration.preflight_blocked: {codes}")
    return receipt


def cmd_sync_shared(args: Any) -> None:
    store = make_store(args)
    if not store.active_path.exists():
        raise SwitchError(f"Active profile state not found: {store.active_path}")
    selection = active_profile_selection(read_json(store.active_path))
    dry_run = bool(getattr(args, "dry_run", False))
    receipt = reconcile_shared_configuration(
        store,
        selection,
        boundary="explicit-sync",
        mode="plan" if dry_run else "apply",
    )
    print(f"Shared configuration source: {receipt.source_profile or 'none'}")
    print(f"Shared configuration target: {receipt.target_profile or 'none'}")
    print(
        "Shared configuration generation: "
        f"{receipt.generation_before} -> {receipt.generation_after}"
    )
    print(f"Shared configuration status: {receipt.status}")
    print(f"Shared configuration pending: {receipt.pending_target or 'none'}")
    print(f"Shared configuration conflict: {'yes' if receipt.status == 'conflict' else 'no'}")
    print(
        "Shared configuration materialization: "
        + (", ".join(receipt.actions) if receipt.actions else "none")
    )
    for finding in receipt.findings:
        print(f"Shared configuration finding: {finding.code} ({finding.severity})")
    if not dry_run and not receipt.cli_ready:
        codes = ", ".join(finding.code for finding in receipt.findings) or receipt.status
        raise SwitchError(f"Shared configuration sync blocked: {codes}")
