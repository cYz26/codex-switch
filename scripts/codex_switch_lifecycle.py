from __future__ import annotations

import argparse

from codex_switch_capture import capture_profile
from codex_switch_constants import MANAGED_FILES
from codex_switch_io import atomic_write, ensure_private_dir, now_stamp, read_json, write_json
from codex_switch_paths import (
    resolve_codex_bin,
    resolve_official_app_cli_path,
    resolve_official_codex_bin,
)
from codex_switch_store import make_store


def default_official_config() -> str:
    return """# Managed by codex_profile_switch.py.
# OpenAI official Codex auth profile.
# Run:
#   CODEX_HOME="$HOME/.codex-switch/profiles/openai-official" codex login

cli_auth_credentials_store = "file"
"""


def cmd_init(args: argparse.Namespace) -> None:
    store = make_store(args)
    store.ensure()

    official_dir = store.profile_dir("openai-official")
    ensure_private_dir(official_dir)
    manifest_path = official_dir / "manifest.json"
    official_app_cli_path = resolve_official_app_cli_path(
        args.app_cli_path,
        fallback=resolve_codex_bin(args.codex_bin),
    )
    official_codex_bin = resolve_official_codex_bin(args.codex_bin, official_app_cli_path)
    if not manifest_path.exists():
        write_json(
            manifest_path,
            {
                "name": "openai-official",
                "description": "OpenAI official Codex profile; auth is stored locally in auth.json.",
                "codex_bin": official_codex_bin,
                "app_cli_path": official_app_cli_path,
                "app_cli_binding": "launchagent",
                "created_at": now_stamp(),
                "managed_files": list(MANAGED_FILES),
            },
        )
    else:
        manifest = read_json(manifest_path)
        changed = False
        if "app_cli_path" not in manifest and official_app_cli_path:
            manifest["app_cli_path"] = official_app_cli_path
            changed = True
        if "codex_bin" not in manifest and official_codex_bin:
            manifest["codex_bin"] = official_codex_bin
            changed = True
        if "app_cli_binding" not in manifest:
            manifest["app_cli_binding"] = "launchagent"
            changed = True
        if changed:
            manifest["updated_at"] = now_stamp()
            write_json(manifest_path, manifest)
    config_path = official_dir / "config.toml"
    if not config_path.exists():
        atomic_write(config_path, default_official_config().encode(), mode=0o600)

    if args.capture_current:
        captured_codex_bin = resolve_codex_bin(args.codex_bin)
        capture_profile(
            store=store,
            name=args.capture_current,
            source_home=store.live_codex_home,
            codex_bin=captured_codex_bin,
            app_cli_path=captured_codex_bin,
            allow_missing_auth=True,
            overwrite=args.overwrite_capture,
        )

    print(f"Initialized Codex switch store: {store.root}")
    print(f"Shim directory: {store.bin_dir}")
