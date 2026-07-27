from __future__ import annotations

import argparse
import os
import stat
from pathlib import Path

from codex_switch_capture import capture_profile
from codex_switch_constants import MANAGED_FILES, SwitchError
from codex_switch_io import atomic_write, ensure_private_dir, now_stamp, read_json, write_json
from codex_switch_paths import (
    resolve_codex_bin,
    resolve_path,
)
from codex_switch_store import make_store
from codex_switch_runtime_binding import (
    discover_desktop_hosts,
    resolve_store_runtime_binding,
)


def default_official_config() -> str:
    return """# Managed by codex_profile_switch.py.
# OpenAI official Codex auth profile.
# Run:
#   CODEX_HOME="$HOME/.codex-switch/profiles/openai-official" codex login

cli_auth_credentials_store = "file"
"""


def _snapshot_init_file(path: Path) -> dict[str, object]:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"kind": "missing"}
    if stat.S_ISREG(info.st_mode):
        return {
            "kind": "file",
            "mode": stat.S_IMODE(info.st_mode),
            "payload": path.read_bytes(),
        }
    if stat.S_ISLNK(info.st_mode):
        return {"kind": "symlink", "target": os.readlink(path)}
    return {"kind": "other"}


def _snapshot_init_directory(path: Path) -> dict[str, object]:
    try:
        info = path.lstat()
    except FileNotFoundError:
        return {"kind": "missing"}
    if stat.S_ISDIR(info.st_mode) and not stat.S_ISLNK(info.st_mode):
        return {
            "kind": "directory",
            "mode": stat.S_IMODE(info.st_mode),
        }
    return {"kind": "other"}


def _restore_init_file(path: Path, snapshot: dict[str, object]) -> None:
    kind = snapshot.get("kind")
    try:
        current = path.lstat()
    except FileNotFoundError:
        current = None
    if kind == "missing":
        if current is None:
            return
        if stat.S_ISDIR(current.st_mode) and not stat.S_ISLNK(current.st_mode):
            raise SwitchError(f"Init rollback refuses to remove directory: {path}")
        path.unlink()
        return
    if kind == "other":
        return
    if current is not None:
        if stat.S_ISDIR(current.st_mode) and not stat.S_ISLNK(current.st_mode):
            raise SwitchError(f"Init rollback target became a directory: {path}")
        path.unlink()
    if kind == "file":
        payload = snapshot.get("payload")
        mode = snapshot.get("mode")
        if not isinstance(payload, bytes) or type(mode) is not int:
            raise SwitchError(f"Init rollback file snapshot is invalid: {path}")
        atomic_write(path, payload, mode=mode)
        return
    if kind == "symlink":
        target = snapshot.get("target")
        if not isinstance(target, str):
            raise SwitchError(f"Init rollback symlink snapshot is invalid: {path}")
        path.symlink_to(target)
        return
    raise SwitchError(f"Init rollback file kind is invalid: {path}")


def _restore_init_state(
    directory_snapshots: tuple[tuple[Path, dict[str, object]], ...],
    file_snapshots: tuple[tuple[Path, dict[str, object]], ...],
) -> None:
    rollback_errors: list[str] = []
    for path, snapshot in reversed(file_snapshots):
        try:
            _restore_init_file(path, snapshot)
        except Exception as error:
            rollback_errors.append(str(error))
    for path, snapshot in reversed(directory_snapshots):
        try:
            kind = snapshot.get("kind")
            if kind == "missing":
                try:
                    path.rmdir()
                except FileNotFoundError:
                    pass
                continue
            if kind == "directory":
                info = path.lstat()
                if stat.S_ISLNK(info.st_mode) or not stat.S_ISDIR(info.st_mode):
                    raise SwitchError(
                        f"Init rollback directory identity changed: {path}"
                    )
                mode = snapshot.get("mode")
                if type(mode) is not int:
                    raise SwitchError(
                        f"Init rollback directory mode is invalid: {path}"
                    )
                path.chmod(mode)
        except Exception as error:
            rollback_errors.append(str(error))
    if rollback_errors:
        raise SwitchError("Init rollback failed: " + "; ".join(rollback_errors))


def cmd_init(args: argparse.Namespace) -> None:
    store = make_store(args)
    from codex_switch_transaction import locked_store_mutation

    with locked_store_mutation(
        store,
        operation="init",
        create_if_missing=True,
    ) as locked_store:
        official_dir = store.profile_dir("openai-official")
        manifest_path = official_dir / "manifest.json"
        config_path = official_dir / "config.toml"
        directory_snapshots = tuple(
            (path, _snapshot_init_directory(path))
            for path in (
                store.root,
                store.profiles_dir,
                store.backups_dir,
                store.bin_dir,
                store.homes_dir,
                official_dir,
            )
        )
        if locked_store.root_created:
            directory_snapshots = (
                (store.root, {"kind": "missing"}),
                *directory_snapshots[1:],
            )
        file_snapshots = tuple(
            (path, _snapshot_init_file(path))
            for path in (manifest_path, config_path)
        )
        try:
            store.ensure()
            ensure_private_dir(official_dir)
            if args.app_cli_path or args.codex_bin:
                explicit_codex_bin = (
                    resolve_codex_bin(args.codex_bin) if args.codex_bin else ""
                )
                official_app_cli_path = (
                    resolve_path(args.app_cli_path) or explicit_codex_bin
                )
                official_codex_bin = explicit_codex_bin or official_app_cli_path
            else:
                inventory = getattr(args, "desktop_inventory", None)
                if inventory is None:
                    inventory = discover_desktop_hosts()
                official_binding = resolve_store_runtime_binding(
                    store,
                    "openai-official",
                    manifest={},
                    inventory=inventory,
                )
                official_app_cli_path = str(official_binding.desktop_cli)
                official_codex_bin = str(official_binding.shell_cli)
            if not manifest_path.exists():
                write_json(
                    manifest_path,
                    {
                        "name": "openai-official",
                        "description": "OpenAI official Codex profile; auth is stored locally in auth.json.",
                        "codex_bin": official_codex_bin,
                        "app_cli_path": official_app_cli_path,
                        "app_cli_binding": "launchagent",
                        "runtime_binding": (
                            "canonical"
                            if not args.app_cli_path and not args.codex_bin
                            else "explicit-compatibility"
                        ),
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
                if "runtime_binding" not in manifest:
                    manifest["runtime_binding"] = (
                        "canonical"
                        if not args.app_cli_path and not args.codex_bin
                        else "explicit-compatibility"
                    )
                    changed = True
                if changed:
                    manifest["updated_at"] = now_stamp()
                    write_json(manifest_path, manifest)
            if not config_path.exists():
                atomic_write(
                    config_path,
                    default_official_config().encode(),
                    mode=0o600,
                )

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
                    locked_store=locked_store,
                )
        except Exception as init_error:
            try:
                _restore_init_state(directory_snapshots, file_snapshots)
            except Exception as rollback_error:
                raise SwitchError(
                    f"Init failed: {init_error}; {rollback_error}"
                ) from init_error
            raise

        print(f"Initialized Codex switch store: {store.root}")
        print(f"Shim directory: {store.bin_dir}")
