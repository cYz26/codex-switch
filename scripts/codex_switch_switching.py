from __future__ import annotations

import argparse
import sys

from codex_switch_config import (
    build_base_config_text,
    build_profile_v2_config_text,
    config_uses_file_auth,
    merge_preserved_shared_config_blocks,
)
from codex_switch_backup import backup_live_files
from codex_switch_core import (
    CONFIG_MODE_SHARED,
    Store,
    SwitchError,
    atomic_write,
    copy_file_atomic,
    ensure_private_dir,
    make_store,
    profile_app_cli_path,
    validate_toml,
    write_json,
)
from codex_switch_launch import write_app_cli_launch_agent
from codex_switch_plan import resolve_base_config_path, switch_plan_actions
from codex_switch_record import active_record
from codex_switch_shim import write_codex_shim


def switch_profile(
    store: Store,
    name: str,
    dry_run: bool,
    clear_missing_auth: bool,
    config_mode: str,
    shared_config_base: str | None,
    skip_shim: bool,
    skip_app_cli: bool,
    skip_launchctl: bool,
) -> None:
    manifest = store.load_manifest(name)
    profile_dir = store.profile_dir(name)
    config_path = profile_dir / "config.toml"
    auth_path = profile_dir / "auth.json"
    app_cli_path = profile_app_cli_path(manifest)

    if not config_path.exists():
        raise SwitchError(f"Profile is missing config.toml: {config_path}")
    validate_toml(config_path)
    base_config_path = resolve_base_config_path(store, config_mode, shared_config_base)
    live_config_text = build_base_config_text(base_config_path)
    profile_config_text = build_profile_v2_config_text(name, config_path)
    live_config_path = store.live_codex_home / "config.toml"
    if live_config_path.exists():
        live_config_text = merge_preserved_shared_config_blocks(
            live_config_text,
            live_config_path.read_text(),
        )
    uses_file_auth = config_uses_file_auth(profile_config_text)
    writes_auth = auth_path.exists() and uses_file_auth
    removes_auth = not uses_file_auth

    if uses_file_auth and not auth_path.exists() and not clear_missing_auth:
        print(
            "Warning: profile has no auth.json; live auth.json will be preserved. "
            "Use --clear-missing-auth to remove live auth.json.",
            file=sys.stderr,
        )

    actions = switch_plan_actions(
        store=store,
        name=name,
        manifest=manifest,
        config_path=config_path,
        auth_path=auth_path,
        app_cli_path=app_cli_path,
        writes_auth=writes_auth,
        removes_auth=removes_auth,
        config_mode=config_mode,
        shared_config_base=shared_config_base,
        clear_missing_auth=clear_missing_auth,
        skip_shim=skip_shim,
        skip_app_cli=skip_app_cli,
        skip_launchctl=skip_launchctl,
    )
    if dry_run:
        print(f"Dry run: switch to profile {name}")
        for action in actions:
            print(f"- {action}")
        return

    store.ensure()
    backup_dir = backup_live_files(store, name)
    ensure_private_dir(store.live_codex_home)
    atomic_write(store.live_codex_home / "config.toml", live_config_text.encode(), mode=0o600)
    atomic_write(
        store.live_codex_home / f"{name}.config.toml",
        profile_config_text.encode(),
        mode=0o600,
    )
    if writes_auth:
        copy_file_atomic(auth_path, store.live_codex_home / "auth.json", mode=0o600)
    elif clear_missing_auth or removes_auth:
        target = store.live_codex_home / "auth.json"
        if target.exists():
            target.unlink()

    shim_path = None
    if not skip_shim:
        shim_path = write_codex_shim(store, str(manifest.get("codex_bin", "")))

    launch_agent_path = None
    if not skip_app_cli:
        launch_agent_path = write_app_cli_launch_agent(
            store,
            app_cli_path,
            skip_launchctl=skip_launchctl,
        )

    write_json(
        store.active_path,
        active_record(
            name=name,
            live_codex_home=store.live_codex_home,
            config_mode=config_mode,
            base_config_path=base_config_path,
            backup_dir=backup_dir,
            shim_path=shim_path,
            app_cli_path=app_cli_path,
            launch_agent_path=launch_agent_path,
        ),
    )
    print(f"Switched to profile {name}")
    print(f"Backup: {backup_dir}")
    if shim_path:
        print(f"Shim: {shim_path}")
    if launch_agent_path:
        print(f"App CLI: {app_cli_path}")
        print(f"LaunchAgent: {launch_agent_path}")


def cmd_switch(args: argparse.Namespace) -> None:
    switch_profile(
        store=make_store(args),
        name=args.name,
        dry_run=args.dry_run,
        clear_missing_auth=args.clear_missing_auth,
        config_mode=args.config_mode,
        shared_config_base=args.shared_config_base,
        skip_shim=args.skip_shim,
        skip_app_cli=args.skip_app_cli,
        skip_launchctl=args.skip_launchctl,
    )
