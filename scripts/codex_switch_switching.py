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
    maybe_refresh_profile_app_wrapper,
)
from codex_switch_launch import write_app_cli_launch_agent
from codex_switch_plan import resolve_base_config_path, switch_plan_actions
from codex_switch_record import active_record
from codex_switch_restore import finalize_backup
from codex_switch_shim import write_codex_shim
from codex_switch_shell import ensure_shell_cli_bootstrap, shell_cli_bootstrap_path
from codex_switch_runtime_binding import (
    DesktopInventory,
    manifest_uses_canonical_binding,
    resolve_store_runtime_binding,
)


def _switch_profile_unlocked(
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
    if name in {"internal", "openai-official"}:
        from codex_switch_transaction import TransactionRequest, execute_transaction

        manifest = store.load_manifest(name)
        canonical_app_cli_path = None
        if name == "internal":
            binding = resolve_store_runtime_binding(
                store,
                name,
                manifest=manifest,
                inventory=DesktopInventory(current=None),
            )
            canonical_app_cli_path = str(binding.desktop_cli)
        elif manifest_uses_canonical_binding(name, manifest):
            binding = resolve_store_runtime_binding(store, name, manifest=manifest)
            canonical_app_cli_path = str(binding.desktop_cli)
        progress_callback = print if config_mode == CONFIG_MODE_SHARED else None
        transaction_options = {
            "config_mode": config_mode,
            "shared_config_base": shared_config_base,
            "clear_missing_auth": clear_missing_auth,
            "skip_shim": skip_shim,
            "skip_app_cli": skip_app_cli,
            "skip_launchctl": skip_launchctl,
            "progress_callback": progress_callback,
        }
        if canonical_app_cli_path is not None:
            transaction_options["canonical_app_cli_path"] = canonical_app_cli_path
        receipt = execute_transaction(
            store,
            TransactionRequest(
                operation="switch",
                profile=name,
                options=transaction_options,
            ),
            dry_run=dry_run,
        )
        if dry_run:
            for index, line in enumerate(receipt.preview_lines):
                print(f"Dry run: {line}" if index == 0 else line)
            return
        if receipt.outcome == "rolled_back":
            detail = receipt.preview_lines[-2] if len(receipt.preview_lines) >= 2 else ""
            raise SwitchError(
                "Switch failed and was rolled back; "
                f"backup: {receipt.backup_id}; {detail}"
            )
        if receipt.outcome == "rollback_failed":
            raise SwitchError(
                "Switch failed and rollback failed; "
                f"backup: {receipt.backup_id}"
            )
        if receipt.outcome != "committed" or receipt.backup_id is None:
            raise SwitchError(f"Switch ended with unexpected outcome: {receipt.outcome}")

        active = read_active_record(store)
        backup_dir = store.backups_dir / receipt.backup_id
        print(f"Switched to profile {name}")
        print(f"Backup: {backup_dir}")
        if config_mode == CONFIG_MODE_SHARED:
            print(f"CODEX_HOME: {active.get('codex_home')}")
        shim_path = active.get("shim_path")
        if shim_path:
            print(f"Shim: {shim_path}")
        shell_bootstrap = shell_cli_bootstrap_path()
        if not skip_shim and shell_bootstrap is not None:
            print(f"Shell CLI bootstrap: {shell_bootstrap}")
        launch_agent_path = active.get("launch_agent_path")
        if launch_agent_path:
            print(f"App CLI: {active.get('app_cli_path')}")
            print(f"LaunchAgent: {launch_agent_path}")
        for line in receipt.guidance_lines:
            print(line)
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
    shell_bootstrap_path = None
    if not skip_shim:
        shim_path = write_codex_shim(
            store,
            str(manifest.get("codex_bin", "")),
            profile_name=name,
            switch_scripts=Path(__file__).resolve().parent,
        )
        shell_bootstrap_path = ensure_shell_cli_bootstrap(store)

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
    finalize_backup(backup_dir)
    print(f"Switched to profile {name}")
    print(f"Backup: {backup_dir}")
    if shim_path:
        print(f"Shim: {shim_path}")
    if shell_bootstrap_path:
        print(f"Shell CLI bootstrap: {shell_bootstrap_path}")
    if launch_agent_path:
        print(f"App CLI: {app_cli_path}")
        print(f"LaunchAgent: {launch_agent_path}")


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
    if name in {"internal", "openai-official"}:
        _switch_profile_unlocked(
            store,
            name,
            dry_run,
            clear_missing_auth,
            config_mode,
            shared_config_base,
            skip_shim,
            skip_app_cli,
            skip_launchctl,
        )
        return

    from codex_switch_transaction import custom_switch_mutation_gate

    with custom_switch_mutation_gate(store, dry_run=dry_run):
        _switch_profile_unlocked(
            store,
            name,
            dry_run,
            clear_missing_auth,
            config_mode,
            shared_config_base,
            skip_shim,
            skip_app_cli,
            skip_launchctl,
        )


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
