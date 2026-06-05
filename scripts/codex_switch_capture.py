from __future__ import annotations

import argparse
from pathlib import Path

from codex_switch_constants import MANAGED_FILES, SwitchError
from codex_switch_io import copy_file_atomic, ensure_private_dir, now_stamp, write_json
from codex_switch_paths import resolve_codex_bin, resolve_path
from codex_switch_store import Store, make_store, validate_profile_name
from codex_switch_toml_validate import validate_toml


def capture_profile(
    store: Store,
    name: str,
    source_home: Path,
    codex_bin: str,
    app_cli_path: str,
    allow_missing_auth: bool,
    overwrite: bool,
) -> None:
    validate_profile_name(name)
    store.ensure()
    profile_dir = store.profile_dir(name)
    if profile_dir.exists() and not overwrite and (profile_dir / "manifest.json").exists():
        raise SwitchError(f"Profile already exists: {name}. Use --overwrite to replace files.")

    ensure_private_dir(profile_dir)
    copied: list[str] = []
    if not (source_home / "config.toml").exists():
        raise SwitchError(
            f"Missing {source_home / 'config.toml'}; cannot capture a switchable profile."
        )

    for file_name in MANAGED_FILES:
        src = source_home / file_name
        dst = profile_dir / file_name
        if src.exists():
            copy_file_atomic(src, dst, mode=0o600)
            copied.append(file_name)
        elif file_name == "auth.json" and not allow_missing_auth:
            raise SwitchError(
                f"Missing {src}. Re-run with --allow-missing-auth when this profile has no auth yet."
            )

    config_path = profile_dir / "config.toml"
    if config_path.exists():
        validate_toml(config_path)

    write_json(
        profile_dir / "manifest.json",
        {
            "name": name,
            "description": f"Captured from {source_home}",
            "codex_bin": codex_bin,
            "app_cli_path": app_cli_path or codex_bin,
            "app_cli_binding": "launchagent",
            "captured_at": now_stamp(),
            "managed_files": list(MANAGED_FILES),
        },
    )
    captured = ", ".join(copied) if copied else "manifest only"
    print(f"Captured profile {name}: {captured}")


def cmd_capture(args: argparse.Namespace) -> None:
    codex_bin = resolve_codex_bin(args.codex_bin)
    app_cli_path = resolve_path(args.app_cli_path) or codex_bin
    capture_profile(
        store=make_store(args),
        name=args.name,
        source_home=args.from_codex_home,
        codex_bin=codex_bin,
        app_cli_path=app_cli_path,
        allow_missing_auth=args.allow_missing_auth,
        overwrite=args.overwrite,
    )
