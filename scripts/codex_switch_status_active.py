from __future__ import annotations

from codex_switch_constants import SwitchError
from codex_switch_io import read_json
from codex_switch_paths import profile_app_cli_path
from codex_switch_runtime_binding import (
    RuntimeBindingError,
    manifest_uses_canonical_binding,
    resolve_store_runtime_binding,
)
from codex_switch_selection import ProfileSelection, active_profile_selection
from codex_switch_store import Store


def _canonical_binding(store: Store, profile: str, manifest: dict) -> object | None:
    if profile not in {"internal", "openai-official", "official"}:
        return None
    if not manifest_uses_canonical_binding(profile, manifest):
        return None
    return resolve_store_runtime_binding(
        store,
        profile,
        manifest=manifest,
    )


def print_active_profile_status(store: Store) -> ProfileSelection | None:
    if not store.active_path.exists():
        print("Active profile: <none recorded>")
        return None
    try:
        active = read_json(store.active_path)
        if not isinstance(active, dict):
            raise SwitchError("active.selection.invalid: active record must be an object")
        selection = active_profile_selection(active)
    except SwitchError as exc:
        print(f"Active profile: <invalid: {exc}>")
        return None

    print(f"Active profile: {selection.cli_profile} ({active.get('switched_at')})")
    print(f"CLI profile: {selection.cli_profile}")
    print(f"App profile: {selection.app_profile}")
    if active.get("config_mode"):
        print(f"Config mode: {active.get('config_mode')}")
    if active.get("home_mode"):
        print(f"Home mode: {active.get('home_mode')}")
    if active.get("codex_home"):
        print(f"Active CODEX_HOME: {active.get('codex_home')}")
    if active.get("backup_id"):
        print(f"Last backup: {active.get('backup_id')}")
    if active.get("shared_sync_source") and active.get("shared_sync_target"):
        print(
            "Shared sync: "
            f"{active.get('shared_sync_source')} -> {active.get('shared_sync_target')}"
        )
    if active.get("shared_config_base"):
        print(f"Shared config base: {active.get('shared_config_base')}")
    try:
        cli_manifest = store.load_manifest(selection.cli_profile)
        app_manifest = (
            cli_manifest
            if selection.app_profile == selection.cli_profile
            else store.load_manifest(selection.app_profile)
        )
        print(f"Active configured CLI: {cli_manifest.get('codex_bin', '')}")
        print(f"Active configured App CLI: {profile_app_cli_path(app_manifest)}")
        cli_binding = _canonical_binding(
            store,
            selection.cli_profile,
            cli_manifest,
        )
        app_binding = (
            cli_binding
            if selection.app_profile == selection.cli_profile
            else _canonical_binding(store, selection.app_profile, app_manifest)
        )
        if cli_binding is not None:
            print(f"Expected CLI binding: {cli_binding.shell_cli}")
        if app_binding is not None:
            print(f"Expected App binding: {app_binding.desktop_cli}")
        for surface, binding in (("CLI", cli_binding), ("App", app_binding)):
            if binding is None:
                continue
            for finding in binding.findings:
                if finding.severity in {"error", "warning"}:
                    print(f"{surface} runtime binding finding: {finding.code}")
    except (SwitchError, RuntimeBindingError) as exc:
        print(f"Active profile manifest: <unavailable: {exc}>")
    return selection
