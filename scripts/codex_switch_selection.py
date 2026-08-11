from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Mapping

from codex_switch_constants import SwitchError


_PROFILE_ALIASES = {
    "internal": "internal",
    "i": "internal",
    "official": "openai-official",
    "openai": "openai-official",
    "openai-official": "openai-official",
    "o": "openai-official",
}
_SUPPORTED_SPLIT = ("internal", "openai-official")


@dataclass(frozen=True)
class ProfileSelection:
    cli_profile: str
    app_profile: str
    app_profile_explicit: bool = False

    @property
    def is_split(self) -> bool:
        return self.cli_profile != self.app_profile


@dataclass(frozen=True)
class ActiveProfileSelectionSnapshot:
    record: Mapping[str, object] | None
    selection: ProfileSelection | None
    problem: str | None
    payload: bytes | None


def normalize_profile_identity(value: object, *, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise SwitchError(f"{label}.missing: profile identity is required")
    stripped = value.strip()
    return _PROFILE_ALIASES.get(stripped.lower(), stripped)


def _validate_pair(selection: ProfileSelection, *, code: str) -> ProfileSelection:
    if selection.is_split and (
        selection.cli_profile,
        selection.app_profile,
    ) != _SUPPORTED_SPLIT:
        raise SwitchError(
            f"{code}: unsupported CLI/App profile selection "
            f"{selection.cli_profile}/{selection.app_profile}; supported split: "
            f"{_SUPPORTED_SPLIT[0]}/{_SUPPORTED_SPLIT[1]}"
        )
    return selection


def requested_profile_selection(
    cli_profile: object,
    app_profile: object | None,
    *,
    skip_app_cli: bool = False,
) -> ProfileSelection:
    normalized_cli = normalize_profile_identity(cli_profile, label="selection.cli")
    app_profile_explicit = app_profile is not None
    if app_profile_explicit and skip_app_cli:
        raise SwitchError(
            "selection.app_skip_conflict: --app-profile cannot be combined with "
            "--skip-app-cli"
        )
    normalized_app = (
        normalize_profile_identity(app_profile, label="selection.app")
        if app_profile_explicit
        else normalized_cli
    )
    return _validate_pair(
        ProfileSelection(
            cli_profile=normalized_cli,
            app_profile=normalized_app,
            app_profile_explicit=app_profile_explicit,
        ),
        code="selection.unsupported",
    )


def active_profile_selection(active: Mapping[str, object]) -> ProfileSelection:
    legacy_profile = normalize_profile_identity(
        active.get("profile"),
        label="active.selection.profile",
    )
    has_cli = "cli_profile" in active
    has_app = "app_profile" in active
    if not has_cli and not has_app:
        return ProfileSelection(
            cli_profile=legacy_profile,
            app_profile=legacy_profile,
        )
    if has_cli != has_app:
        raise SwitchError(
            "active.selection.partial: cli_profile and app_profile must be recorded together"
        )
    cli_profile = normalize_profile_identity(
        active.get("cli_profile"),
        label="active.selection.cli",
    )
    app_profile = normalize_profile_identity(
        active.get("app_profile"),
        label="active.selection.app",
    )
    if legacy_profile != cli_profile:
        raise SwitchError(
            "active.selection.cli_conflict: profile must match cli_profile"
        )
    return _validate_pair(
        ProfileSelection(
            cli_profile=cli_profile,
            app_profile=app_profile,
        ),
        code="active.selection.unsupported",
    )


def active_profile_fields(selection: ProfileSelection) -> dict[str, str]:
    return {
        "profile": selection.cli_profile,
        "cli_profile": selection.cli_profile,
        "app_profile": selection.app_profile,
    }


def read_active_profile_selection_snapshot(
    active_path: Path,
    *,
    fallback_cli_profile: str | None = None,
) -> ActiveProfileSelectionSnapshot:
    try:
        payload = active_path.read_bytes()
    except FileNotFoundError:
        fallback = (
            ProfileSelection(
                cli_profile=fallback_cli_profile,
                app_profile=fallback_cli_profile,
            )
            if fallback_cli_profile is not None
            else None
        )
        return ActiveProfileSelectionSnapshot(
            record=None,
            selection=fallback,
            problem=None,
            payload=None,
        )
    except OSError as exc:
        return ActiveProfileSelectionSnapshot(
            record=None,
            selection=None,
            problem=f"Active profile record cannot be read: {active_path}: {exc}",
            payload=None,
        )
    try:
        active = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return ActiveProfileSelectionSnapshot(
            record=None,
            selection=None,
            problem=f"Invalid JSON: {active_path}: {exc}",
            payload=payload,
        )
    if not isinstance(active, dict):
        return ActiveProfileSelectionSnapshot(
            record=None,
            selection=None,
            problem="active.selection.invalid: active record must be an object",
            payload=payload,
        )
    try:
        selection = active_profile_selection(active)
    except SwitchError as exc:
        return ActiveProfileSelectionSnapshot(
            record=active,
            selection=None,
            problem=str(exc),
            payload=payload,
        )
    return ActiveProfileSelectionSnapshot(
        record=active,
        selection=selection,
        problem=None,
        payload=payload,
    )


def require_active_profile_selection_payload(
    active_path: Path,
    expected_payload: bytes | None,
) -> None:
    try:
        observed_payload = active_path.read_bytes()
    except FileNotFoundError:
        observed_payload = None
    except OSError as exc:
        raise SwitchError(
            "active.selection.changed_before_repair: active record cannot be "
            f"revalidated: {active_path}: {exc}"
        ) from exc
    if observed_payload != expected_payload:
        raise SwitchError(
            "active.selection.changed_before_repair: active record changed "
            "after verification began"
        )
