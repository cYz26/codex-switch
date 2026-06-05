from __future__ import annotations

from codex_switch_paths import equivalent_paths, profile_app_cli_path
from codex_switch_store import Store


def desktop_switching_problems(store: Store) -> list[str]:
    profile_names = set(store.list_profiles())
    if not {"internal", "openai-official"}.issubset(profile_names):
        return []
    internal_manifest = store.load_manifest("internal")
    official_manifest = store.load_manifest("openai-official")
    internal_cli = str(internal_manifest.get("codex_bin", ""))
    official_cli = str(official_manifest.get("codex_bin", ""))
    internal_app = profile_app_cli_path(internal_manifest)
    official_app = profile_app_cli_path(official_manifest)
    if (
        internal_cli
        and official_cli
        and internal_app
        and official_app
        and not equivalent_paths(internal_cli, official_cli)
        and equivalent_paths(internal_app, official_app)
    ):
        return [
            "internal and openai-official use different codex_bin values but "
            "the same app_cli_path; Desktop switching would not change the "
            "underlying codex binary"
        ]
    return []
