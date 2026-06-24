from __future__ import annotations

import argparse
import sys
from pathlib import Path

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
from codex_switch_app_wrapper import (
    managed_profile_app_cli_path,
    maybe_refresh_profile_app_wrapper,
)
from codex_switch_home_sync import (
    build_internal_home_config,
    build_official_home_config_from_internal,
    refresh_profile_canonical_config,
    remove_stale_runtime_links,
    shared_support_targets,
    stale_runtime_links,
    sync_shared_support,
)
from codex_switch_home_select import (
    IndependentHomes,
    resolve_independent_homes,
    write_home_binding_updates,
)
from codex_switch_launch import write_app_cli_launch_agent
from codex_switch_plan import resolve_base_config_path, switch_plan_actions
from codex_switch_record import active_record
from codex_switch_restore import create_switch_backup, finalize_backup
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
    if name in {"internal", "openai-official"} and config_mode == CONFIG_MODE_SHARED:
        switch_independent_profile(
            store=store,
            name=name,
            dry_run=dry_run,
            clear_missing_auth=clear_missing_auth,
            skip_shim=skip_shim,
            skip_app_cli=skip_app_cli,
            skip_launchctl=skip_launchctl,
        )
        return

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
        app_cli_path = maybe_refresh_profile_app_wrapper(
            store=store,
            name=name,
            manifest=manifest,
            app_cli_path=app_cli_path,
            switch_scripts=Path(__file__).resolve().parent,
        )
        launch_agent_path = write_app_cli_launch_agent(
            store,
            app_cli_path,
            skip_launchctl=skip_launchctl,
        )

    write_json(
        store.active_path,
        active_record(
            name=name,
            codex_home=store.live_codex_home,
            config_mode=config_mode,
            base_config_path=base_config_path,
            backup_dir=backup_dir,
            shim_path=shim_path,
            shell_cli_path=str(manifest.get("codex_bin", "")) or None,
            app_cli_path=app_cli_path,
            launch_agent_path=launch_agent_path,
            home_mode="legacy",
        ),
    )
    print(f"Switched to profile {name}")
    print(f"Backup: {backup_dir}")
    if shim_path:
        print(f"Shim: {shim_path}")
    if launch_agent_path:
        print(f"App CLI: {app_cli_path}")
        print(f"LaunchAgent: {launch_agent_path}")


def read_active_record(store: Store) -> dict:
    if not store.active_path.exists():
        return {}
    try:
        import json

        active = store.active_path.read_text()
        value = json.loads(active)
        return value if isinstance(value, dict) else {}
    except Exception:
        return {}


def read_active_profile_home(store: Store) -> tuple[str | None, Path | None]:
    active = read_active_record(store)
    value = active.get("profile")
    profile = value if isinstance(value, str) else None
    raw_home = active.get("codex_home") or active.get("live_codex_home")
    if isinstance(raw_home, str) and raw_home:
        return profile, Path(raw_home).expanduser()
    return profile, None


def read_active_profile(store: Store) -> str | None:
    active = read_active_record(store)
    value = active.get("profile")
    return value if isinstance(value, str) else None


def official_auth_restore_path(store: Store, official_home: Path) -> Path | None:
    official_auth = official_home / "auth.json"
    profile_auth = store.profile_dir("openai-official") / "auth.json"
    if not official_auth.exists() and profile_auth.exists():
        return official_auth
    return None


def independent_switch_paths(
    store: Store,
    name: str,
    homes: IndependentHomes,
    skip_shim: bool,
    skip_app_cli: bool,
) -> tuple[Path, Path, list[Path], list[str]]:
    official_home = homes.official.path
    internal_home = homes.internal.path
    shim_path = store.bin_dir / "codex"
    backup_paths: list[Path] = [
        store.active_path,
        store.manifest_path("internal"),
        store.manifest_path("openai-official"),
    ]
    actions: list[str] = []

    if name == "internal":
        backup_paths.extend(
            [
                internal_home / "config.toml",
                internal_home / "internal.config.toml",
                internal_home / "auth.json",
                store.profile_dir("internal") / "config.toml",
                *shared_support_targets(official_home, internal_home),
                *stale_runtime_links(internal_home, official_home),
            ]
        )
        actions.extend(
            [
                f"sync shared state from {official_home} to {internal_home}",
                f"write managed internal config: {internal_home / 'config.toml'}",
                f"remove managed internal auth: {internal_home / 'auth.json'}",
            ]
        )
    else:
        backup_paths.extend(
            [
                official_home / "config.toml",
                official_home / "openai-official.config.toml",
                store.profile_dir("openai-official") / "config.toml",
                *shared_support_targets(internal_home, official_home),
            ]
        )
        restored_auth = official_auth_restore_path(store, official_home)
        if restored_auth:
            backup_paths.append(restored_auth)
            actions.append(f"restore legacy official auth into {restored_auth}")
        actions.append(f"sync shared state from {internal_home} to {official_home}")

    if not skip_shim:
        backup_paths.append(shim_path)
        actions.append(f"update shell shim: {shim_path}")
    if not skip_app_cli:
        backup_paths.append(store.launch_agent_path)
        if name == "internal":
            backup_paths.append(managed_profile_app_cli_path(store, "internal"))
        actions.append(f"update Codex Desktop binding: {store.launch_agent_path}")
    return official_home, internal_home, backup_paths, actions


def print_independent_dry_run(
    name: str,
    homes: IndependentHomes,
    backup_paths: list[Path],
    actions: list[str],
) -> None:
    print(f"Dry run: switch to profile {name}")
    print("Home plan:")
    print(f"- internal: {homes.internal.path} ({homes.internal.mode})")
    print(f"- openai-official: {homes.official.path} ({homes.official.mode})")
    for profile in homes.manifest_updates:
        print(f"- update profile home binding: {profile}")
    print("Backup plan:")
    for path in backup_paths:
        print(f"- {path}")
    print("Mutation plan:")
    for action in actions:
        print(f"- {action}")

def switch_independent_profile(
    store: Store,
    name: str,
    dry_run: bool,
    clear_missing_auth: bool,
    skip_shim: bool,
    skip_app_cli: bool,
    skip_launchctl: bool,
) -> None:
    del clear_missing_auth
    manifest = store.load_manifest(name)
    internal_manifest = store.load_manifest("internal")
    official_manifest = store.load_manifest("openai-official")
    active_profile, active_home = read_active_profile_home(store)
    homes = resolve_independent_homes(
        store,
        internal_manifest=internal_manifest,
        official_manifest=official_manifest,
        target_profile=name,
        dry_run=dry_run,
        active_profile=active_profile,
        active_home=active_home,
    )
    profile_dir = store.profile_dir(name)
    config_path = profile_dir / "config.toml"
    if not config_path.exists():
        raise SwitchError(f"Profile is missing config.toml: {config_path}")
    validate_toml(config_path)

    official_home, internal_home, backup_paths, actions = independent_switch_paths(
        store=store,
        name=name,
        homes=homes,
        skip_shim=skip_shim,
        skip_app_cli=skip_app_cli,
    )
    if dry_run:
        print_independent_dry_run(name, homes, backup_paths, actions)
        return

    store.ensure()
    from_profile = active_profile
    print("Creating switch backup...")
    backup_dir = create_switch_backup(
        store=store,
        operation="switch",
        from_profile=from_profile,
        to_profile=name,
        paths=backup_paths,
    )
    print(f"Backup captured: {backup_dir}")
    print("Applying switch mutations...")
    write_home_binding_updates(store, homes)

    codex_bin = str(manifest.get("codex_bin", ""))
    if name == "internal":
        target_home = internal_home
        home_mode = homes.internal.mode
        ensure_private_dir(target_home)
        sync_shared_support(official_home, target_home, prefer_link=True)
        remove_stale_runtime_links(target_home, official_home)
        shared_source_home = official_home
        if (
            not (shared_source_home / "config.toml").exists()
            and (target_home / "config.toml").exists()
        ):
            shared_source_home = target_home
        atomic_write(
            target_home / "config.toml",
            build_internal_home_config(
                shared_source_home,
                name,
                target_home / "config.toml",
                config_path,
            ).encode(),
            mode=0o600,
        )
        profile_config_text = refresh_profile_canonical_config(
            name,
            target_home / "config.toml",
            config_path,
        )
        atomic_write(
            target_home / f"{name}.config.toml",
            profile_config_text.encode(),
            mode=0o600,
        )
        auth_path = target_home / "auth.json"
        if auth_path.exists():
            auth_path.unlink()
        app_cli_path = str(managed_profile_app_cli_path(store, name))
        sync_source = official_home
        sync_target = target_home
    else:
        target_home = official_home
        home_mode = homes.official.mode
        merged_config = build_official_home_config_from_internal(
            official_home,
            internal_home,
            config_path,
        )
        if merged_config is not None:
            atomic_write(official_home / "config.toml", merged_config.encode(), mode=0o600)
            profile_config_text = refresh_profile_canonical_config(
                name,
                official_home / "config.toml",
                config_path,
            )
            atomic_write(
                official_home / f"{name}.config.toml",
                profile_config_text.encode(),
                mode=0o600,
            )
        sync_shared_support(internal_home, official_home, prefer_link=False)
        restored_auth = official_auth_restore_path(store, official_home)
        if restored_auth:
            copy_file_atomic(store.profile_dir(name) / "auth.json", restored_auth, mode=0o600)
        app_cli_path = profile_app_cli_path(manifest)
        sync_source = internal_home
        sync_target = official_home

    shim_path = None
    if not skip_shim:
        shim_path = write_codex_shim(store, codex_bin, codex_home=target_home)

    launch_agent_path = None
    if not skip_app_cli:
        if name == "internal":
            app_cli_path = maybe_refresh_profile_app_wrapper(
                store=store,
                name=name,
                manifest=manifest,
                app_cli_path=app_cli_path,
                switch_scripts=Path(__file__).resolve().parent,
            )
        launch_agent_path = write_app_cli_launch_agent(
            store,
            app_cli_path,
            skip_launchctl=skip_launchctl,
        )

    write_json(
        store.active_path,
        active_record(
            name=name,
            codex_home=target_home,
            config_mode=CONFIG_MODE_SHARED,
            base_config_path=official_home / "config.toml",
            backup_dir=backup_dir,
            shim_path=shim_path,
            shell_cli_path=codex_bin,
            app_cli_path=app_cli_path,
            launch_agent_path=launch_agent_path,
            home_mode=home_mode,
            shared_sync_source=sync_source,
            shared_sync_target=sync_target,
        ),
    )
    finalize_backup(backup_dir)
    print(f"Switched to profile {name}")
    print(f"Backup: {backup_dir}")
    print(f"CODEX_HOME: {target_home}")
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
