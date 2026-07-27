#!/usr/bin/env python3

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from codex_switch_constants import SwitchError
from codex_switch_runtime_binding import (
    DesktopInventory,
    discover_desktop_hosts,
    manifest_uses_canonical_binding,
    resolve_store_runtime_binding,
)
from codex_switch_update_policy import (
    extract_semantic_version,
    parse_semantic_version,
)


@dataclass(frozen=True)
class OfficialStableComparison:
    outcome: str
    current_version: Optional[str]
    stable_version: Optional[str]
    current_is_prerelease: bool
    reason: str


def resolve_profile_advisory_cli(
    store: object,
    profile: str,
    *,
    inventory: DesktopInventory | None = None,
) -> Path:
    normalized = (
        "openai-official" if profile == "official" else profile
    )
    manifest = getattr(store, "load_manifest")(normalized)
    if normalized in {"internal", "openai-official"}:
        selected_inventory = inventory or discover_desktop_hosts()
        if manifest_uses_canonical_binding(
            normalized,
            manifest,
            selected_inventory,
        ):
            return resolve_store_runtime_binding(
                store,
                normalized,
                manifest=manifest,
                inventory=selected_inventory,
            ).backend_cli
    raw_codex_bin = manifest.get("codex_bin")
    if not isinstance(raw_codex_bin, str) or not raw_codex_bin.strip():
        raise SwitchError(
            f"{normalized}: missing codex_bin for official release advisory"
        )
    return Path(raw_codex_bin).expanduser()


def _stable_version_from_tag(tag: str) -> Optional[str]:
    normalized = tag.strip()
    if not normalized.startswith("rust-v"):
        return None
    candidate = normalized[len("rust-v") :]
    parsed = parse_semantic_version(candidate)
    if parsed is None or parsed.prerelease:
        return None
    return candidate


def compare_to_official_stable(
    current_output: str,
    stable_tag: str,
) -> OfficialStableComparison:
    current_version = extract_semantic_version(current_output)
    stable_version = _stable_version_from_tag(stable_tag)
    current = parse_semantic_version(current_version)
    stable = parse_semantic_version(stable_version)
    current_is_prerelease = bool(current and current.prerelease)

    if stable is None:
        return OfficialStableComparison(
            outcome="unknown",
            current_version=current_version,
            stable_version=None,
            current_is_prerelease=current_is_prerelease,
            reason="latest upstream tag is not a stable rust-v semantic version",
        )
    if current is None:
        return OfficialStableComparison(
            outcome="unknown",
            current_version=None,
            stable_version=stable_version,
            current_is_prerelease=False,
            reason="selected profile CLI version is not parseable",
        )
    if current < stable:
        outcome = "behind"
        reason = "selected profile CLI is older than upstream stable"
    elif current > stable:
        outcome = "ahead"
        reason = "selected profile CLI is newer than upstream stable"
    else:
        outcome = "matches"
        reason = "selected profile CLI matches upstream stable"
    return OfficialStableComparison(
        outcome=outcome,
        current_version=current_version,
        stable_version=stable_version,
        current_is_prerelease=current_is_prerelease,
        reason=reason,
    )
