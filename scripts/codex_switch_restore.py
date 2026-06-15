from __future__ import annotations

import argparse
import hashlib
import os
import shutil
import stat
from pathlib import Path
from typing import Any

from codex_switch_constants import SwitchError
from codex_switch_io import ensure_private_dir, now_stamp, read_json, write_json
from codex_switch_store import Store, make_store


def backup_id(operation: str, from_profile: str | None, to_profile: str | None) -> str:
    left = from_profile or "none"
    right = to_profile or "none"
    return f"{now_stamp()}-{operation}-{left}-to-{right}"


def path_exists(path: Path) -> bool:
    return path.exists() or path.is_symlink()


def file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def path_state(path: Path) -> dict[str, Any]:
    if not path_exists(path):
        return {"kind": "missing", "path": str(path)}
    info = path.lstat()
    state: dict[str, Any] = {
        "path": str(path),
        "mode": stat.S_IMODE(info.st_mode),
        "mtime": info.st_mtime,
    }
    if path.is_symlink():
        state["kind"] = "symlink"
        state["symlink_target"] = os.readlink(path)
    elif path.is_file():
        state["kind"] = "file"
        state["sha256"] = file_sha256(path)
    elif path.is_dir():
        state["kind"] = "directory"
    else:
        state["kind"] = "other"
    return state


def copy_path_to_backup(path: Path, backup_path: Path, state: dict[str, Any]) -> str | None:
    if state["kind"] not in {"file", "directory"}:
        return None
    ensure_private_dir(backup_path.parent)
    if state["kind"] == "file":
        shutil.copy2(path, backup_path)
    else:
        shutil.copytree(path, backup_path, symlinks=True)
    return backup_path.name


def create_switch_backup(
    store: Store,
    operation: str,
    from_profile: str | None,
    to_profile: str,
    paths: list[Path],
) -> Path:
    ensure_private_dir(store.backups_dir)
    candidate = backup_id(operation, from_profile, to_profile)
    backup_dir = store.backups_dir / candidate
    suffix = 1
    while backup_dir.exists():
        suffix += 1
        backup_dir = store.backups_dir / f"{candidate}-{suffix}"
    ensure_private_dir(backup_dir)

    entries: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, raw_path in enumerate(paths):
        path = raw_path.expanduser()
        key = str(path)
        if key in seen:
            continue
        seen.add(key)
        state = path_state(path)
        entry = {
            "path": str(path),
            "pre_state": state,
        }
        backup_rel = copy_path_to_backup(path, backup_dir / f"{index}-{path.name}", state)
        if backup_rel:
            entry["backup_rel"] = backup_rel
        entries.append(entry)

    write_json(
        backup_dir / "backup.json",
        {
            "id": backup_dir.name,
            "operation": operation,
            "from_profile": from_profile,
            "to_profile": to_profile,
            "created_at": now_stamp(),
            "tool": "codex-switch",
            "entries": entries,
        },
    )
    return backup_dir


def finalize_backup(backup_dir: Path) -> None:
    manifest = read_json(backup_dir / "backup.json")
    for entry in manifest.get("entries", []):
        entry["post_state"] = path_state(Path(entry["path"]))
    manifest["finalized_at"] = now_stamp()
    write_json(backup_dir / "backup.json", manifest)


def states_match(current: dict[str, Any], expected: dict[str, Any]) -> bool:
    if current.get("kind") != expected.get("kind"):
        return False
    kind = current.get("kind")
    if kind == "file":
        return current.get("sha256") == expected.get("sha256")
    if kind == "symlink":
        return current.get("symlink_target") == expected.get("symlink_target")
    return True


def remove_existing(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.is_dir():
        shutil.rmtree(path)


def restore_entry(backup_dir: Path, entry: dict[str, Any]) -> None:
    target = Path(entry["path"])
    pre_state = entry["pre_state"]
    if path_exists(target):
        remove_existing(target)
    kind = pre_state["kind"]
    if kind == "missing":
        return
    ensure_private_dir(target.parent)
    if kind == "symlink":
        target.symlink_to(pre_state["symlink_target"])
    elif kind == "file":
        backup_rel = entry.get("backup_rel")
        if not backup_rel:
            raise SwitchError(f"Backup entry is missing file payload: {target}")
        shutil.copy2(backup_dir / backup_rel, target)
    elif kind == "directory":
        backup_rel = entry.get("backup_rel")
        if not backup_rel:
            raise SwitchError(f"Backup entry is missing directory payload: {target}")
        shutil.copytree(backup_dir / backup_rel, target, symlinks=True)
    if "mode" in pre_state and path_exists(target) and not target.is_symlink():
        target.chmod(int(pre_state["mode"]))


def restore_backup(store: Store, backup_id_value: str, dry_run: bool, apply: bool, force: bool) -> None:
    backup_dir = store.backups_dir / backup_id_value
    if not backup_dir.exists():
        raise SwitchError(f"Backup not found: {backup_id_value}")
    manifest = read_json(backup_dir / "backup.json")
    print(f"{'Dry run: ' if dry_run else ''}restore backup {backup_id_value}")
    for entry in manifest.get("entries", []):
        print(f"- restore {entry['path']}")
    if dry_run:
        return
    if not apply:
        raise SwitchError("restore requires --dry-run or --apply")

    if not force:
        for entry in manifest.get("entries", []):
            expected = entry.get("post_state")
            if not expected:
                raise SwitchError(
                    f"Backup has no post-switch state for {entry['path']}; re-run with --force."
                )
            current = path_state(Path(entry["path"]))
            if not states_match(current, expected):
                raise SwitchError(
                    f"Current path changed since backup was finalized: {entry['path']}. "
                    "Use --force to restore anyway."
                )

    for entry in reversed(manifest.get("entries", [])):
        restore_entry(backup_dir, entry)
    print(f"Restored backup {backup_id_value}")


def cmd_restore(args: argparse.Namespace) -> None:
    restore_backup(
        store=make_store(args),
        backup_id_value=args.backup_id,
        dry_run=args.dry_run,
        apply=args.apply,
        force=args.force,
    )
