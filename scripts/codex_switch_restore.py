from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from codex_switch_constants import SwitchError
from codex_switch_io import ensure_private_dir, now_stamp, read_json, write_json
from codex_switch_store import Store, make_store


@dataclass(frozen=True)
class RestoreManifestEntry:
    path: str
    before_state: Mapping[str, Any]
    committed_after_state: Mapping[str, Any]
    payload: str | None
    created_parent_paths: tuple[str, ...] = tuple()


@dataclass(frozen=True)
class RestoreManifest:
    backup_id: str
    schema_version: int
    lifecycle: str
    operation: str
    profile: str
    entries: tuple[RestoreManifestEntry, ...]


def _read_v1_manifest(backup_dir: Path, manifest: Mapping[str, Any]) -> RestoreManifest:
    raw_entries = manifest.get("entries")
    if not isinstance(raw_entries, list):
        raise SwitchError(
            f"Backup {backup_dir.name} has no supported entries manifest."
        )
    if not raw_entries:
        raise SwitchError(f"Backup {backup_dir.name} has no entries to restore.")
    entries: list[RestoreManifestEntry] = []
    for index, raw_entry in enumerate(raw_entries):
        if not isinstance(raw_entry, dict):
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} must be an object."
            )
        path = raw_entry.get("path")
        before_state = raw_entry.get("pre_state")
        committed_after_state = raw_entry.get("post_state")
        payload = raw_entry.get("backup_rel")
        if not isinstance(path, str) or not path:
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} has no destination path."
            )
        if not isinstance(before_state, dict) or not isinstance(
            committed_after_state, dict
        ):
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} lacks v1 state attestations."
            )
        if payload is not None and not isinstance(payload, str):
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} has an invalid payload path."
            )
        entries.append(
            RestoreManifestEntry(
                path=path,
                before_state=dict(before_state),
                committed_after_state=dict(committed_after_state),
                payload=payload,
                created_parent_paths=tuple(),
            )
        )
    operation = manifest.get("operation")
    profile = manifest.get("to_profile")
    return RestoreManifest(
        backup_id=backup_dir.name,
        schema_version=1,
        lifecycle="committed",
        operation=operation if isinstance(operation, str) else "switch",
        profile=profile if isinstance(profile, str) else "restore",
        entries=tuple(entries),
    )


def _read_v2_manifest(backup_dir: Path, manifest: Mapping[str, Any]) -> RestoreManifest:
    lifecycle = manifest.get("lifecycle")
    if lifecycle not in {"prepared", "committed", "rolled_back", "rollback_failed"}:
        raise SwitchError(
            f"Backup {backup_dir.name} has an invalid schema-v2 lifecycle: {lifecycle!r}"
        )
    raw_entries = manifest.get("entries")
    if not isinstance(raw_entries, list):
        raise SwitchError(f"Backup {backup_dir.name} has no schema-v2 entries list.")
    if not raw_entries:
        raise SwitchError(f"Backup {backup_dir.name} has no entries to restore.")
    entries: list[RestoreManifestEntry] = []
    for index, raw_entry in enumerate(raw_entries):
        if not isinstance(raw_entry, dict):
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} must be an object."
            )
        path = raw_entry.get("path")
        before_state = raw_entry.get("before_state")
        committed_after_state = raw_entry.get("committed_after_state")
        payload = raw_entry.get("payload")
        raw_created_parent_paths = raw_entry.get("created_parent_paths", [])
        if not isinstance(path, str) or not path:
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} has no destination path."
            )
        if not isinstance(before_state, dict) or not isinstance(
            committed_after_state, dict
        ):
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} lacks schema-v2 state attestations."
            )
        if payload is not None and not isinstance(payload, str):
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} has an invalid payload path."
            )
        if not isinstance(raw_created_parent_paths, list) or not all(
            isinstance(path, str) and path
            for path in raw_created_parent_paths
        ):
            raise SwitchError(
                f"Backup {backup_dir.name} entry {index} has an invalid "
                "created-parent journal."
            )
        entries.append(
            RestoreManifestEntry(
                path=path,
                before_state=dict(before_state),
                committed_after_state=dict(committed_after_state),
                payload=payload,
                created_parent_paths=tuple(raw_created_parent_paths),
            )
        )
    operation = manifest.get("operation")
    profile = manifest.get("to_profile")
    return RestoreManifest(
        backup_id=backup_dir.name,
        schema_version=2,
        lifecycle=lifecycle,
        operation=operation if isinstance(operation, str) else "switch",
        profile=profile if isinstance(profile, str) else "restore",
        entries=tuple(entries),
    )


def read_restore_manifest(backup_dir: Path) -> RestoreManifest:
    if not backup_dir.is_dir():
        raise SwitchError(f"Backup not found: {backup_dir.name}")
    manifest_path = backup_dir / "backup.json"
    if not manifest_path.is_file():
        raise SwitchError(f"Backup manifest not found: {backup_dir.name}")
    manifest = read_json(manifest_path)
    if not isinstance(manifest, dict):
        raise SwitchError(f"Backup manifest must be an object: {backup_dir.name}")
    schema_version = manifest.get("schema_version")
    if schema_version is None:
        if "files" in manifest:
            raise SwitchError(
                f"Backup {backup_dir.name} uses an unsupported legacy v0 files "
                "manifest with no attested destinations; preserve the backup for "
                "manual recovery."
            )
        return _read_v1_manifest(backup_dir, manifest)
    if type(schema_version) is int and schema_version == 2:
        return _read_v2_manifest(backup_dir, manifest)
    raise SwitchError(
        f"Unsupported backup schema version for {backup_dir.name}: "
        f"{schema_version!r}"
    )


def backup_id(operation: str, from_profile: str | None, to_profile: str | None) -> str:
    left = from_profile or "none"
    right = to_profile or "none"
    return f"{now_stamp()}-{operation}-{left}-to-{right}"


def path_state(path: Path) -> dict[str, Any]:
    from codex_switch_transaction import capture_path_state

    return capture_path_state(path)


def create_switch_backup(
    store: Store,
    operation: str,
    from_profile: str | None,
    to_profile: str,
    paths: list[Path],
    *,
    filesystem_adapter: object | None = None,
    created_parent_paths: Mapping[str, tuple[Path, ...]] | None = None,
) -> Path:
    from codex_switch_transaction import FilesystemAdapter

    adapter = filesystem_adapter or FilesystemAdapter()
    capture_state = getattr(adapter, "capture_state", None)
    copy_material = getattr(adapter, "copy_material", None)
    if not callable(capture_state) or not callable(copy_material):
        raise SwitchError(
            "Backup filesystem_adapter must provide capture_state() and "
            "copy_material()"
        )
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
        state = capture_state(path)
        if not isinstance(state, dict):
            raise SwitchError(f"Backup adapter returned invalid state for {path}")
        entry = {
            "path": str(path),
            "before_state": state,
            "committed_after_state": {},
        }
        entry_created_parents = (created_parent_paths or {}).get(str(path), tuple())
        if entry_created_parents:
            entry["created_parent_paths"] = [
                str(parent) for parent in entry_created_parents
            ]
        kind = state.get("kind")
        if kind in {"file", "directory"}:
            payload_path = backup_dir / "payloads" / f"{index:04d}-{path.name}"
            try:
                copy_material(
                    path,
                    payload_path,
                    kind,
                    phase="switch_backup",
                )
                copied_state = capture_state(payload_path)
            except Exception as copy_error:
                copied_state = {"kind": "unavailable", "error": str(copy_error)}
            if not isinstance(copied_state, dict) or not states_match(
                copied_state,
                state,
            ):
                error = (
                    "Backup payload copy does not match captured state: "
                    f"{path}; backup: {backup_dir.name}"
                )
                write_json(
                    backup_dir / "failure.json",
                    {
                        "schema_version": 2,
                        "lifecycle": "rollback_failed",
                        "id": backup_dir.name,
                        "operation": operation,
                        "from_profile": from_profile,
                        "to_profile": to_profile,
                        "failed_at": now_stamp(),
                        "failed_path": str(path),
                        "expected_state": state,
                        "observed_payload_state": copied_state,
                        "error": error,
                        "entries": entries,
                    },
                )
                raise SwitchError(error)
            entry["payload"] = payload_path.relative_to(backup_dir).as_posix()
        entries.append(entry)

    write_json(
        backup_dir / "backup.json",
        {
            "schema_version": 2,
            "lifecycle": "prepared",
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


def finalize_backup(
    backup_dir: Path,
    *,
    filesystem_adapter: object | None = None,
    terminal_journal_effect_id: int | None = None,
) -> dict[str, Any]:
    capture_state = (
        getattr(filesystem_adapter, "capture_state", None)
        if filesystem_adapter is not None
        else path_state
    )
    write_manifest = (
        getattr(filesystem_adapter, "write_manifest", None)
        if filesystem_adapter is not None
        else None
    )
    if not callable(capture_state) or (
        filesystem_adapter is not None and not callable(write_manifest)
    ):
        raise SwitchError(
            "Backup filesystem_adapter must provide capture_state() and "
            "write_manifest()"
        )
    manifest = read_json(backup_dir / "backup.json")
    schema_version = manifest.get("schema_version")
    if type(schema_version) is int and schema_version == 2:
        if manifest.get("lifecycle") != "prepared":
            raise SwitchError(
                f"Backup {backup_dir.name} is not prepared: "
                f"{manifest.get('lifecycle')!r}"
            )
        entries = manifest.get("entries")
        if not isinstance(entries, list):
            raise SwitchError(f"Backup {backup_dir.name} has no entries list.")
        backup_root = backup_dir.resolve()
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                raise SwitchError(
                    f"Backup {backup_dir.name} entry {index} must be an object."
                )
            before_state = entry.get("before_state")
            if not isinstance(before_state, dict):
                raise SwitchError(
                    f"Backup {backup_dir.name} entry {index} has no before-state."
                )
            kind = before_state.get("kind")
            payload = entry.get("payload")
            if kind in {"file", "directory"}:
                if not isinstance(payload, str) or not payload:
                    raise SwitchError(
                        f"Backup {backup_dir.name} entry {index} has no payload."
                    )
                relative = Path(payload)
                if relative.is_absolute():
                    raise SwitchError(
                        f"Backup {backup_dir.name} payload escapes its directory: "
                        f"{payload}"
                    )
                payload_path = (backup_dir / relative).resolve()
                try:
                    payload_path.relative_to(backup_root)
                except ValueError as exc:
                    raise SwitchError(
                        f"Backup {backup_dir.name} payload escapes its directory: "
                        f"{payload}"
                    ) from exc
                if payload_path == backup_root or not states_match(
                    capture_state(payload_path), before_state
                ):
                    raise SwitchError(
                        f"Backup {backup_dir.name} payload no longer matches "
                        f"captured state: {payload}"
                    )
            elif payload is not None:
                raise SwitchError(
                    f"Backup {backup_dir.name} entry {index} has unexpected payload."
                )
        for entry in entries:
            entry["committed_after_state"] = capture_state(Path(entry["path"]))
        manifest["lifecycle"] = "committed"
        manifest["committed_at"] = now_stamp()
        if terminal_journal_effect_id is not None:
            journal = manifest.get("switch_journal")
            if not isinstance(journal, dict):
                raise SwitchError(
                    f"Backup {backup_dir.name} has no terminal switch journal."
                )
            effects = journal.get("effects")
            if (
                not isinstance(effects, list)
                or terminal_journal_effect_id < 0
                or terminal_journal_effect_id >= len(effects)
                or not isinstance(effects[terminal_journal_effect_id], dict)
            ):
                raise SwitchError(
                    f"Backup {backup_dir.name} has no terminal finalize intent."
                )
            finalize_effect = effects[terminal_journal_effect_id]
            if (
                finalize_effect.get("kind") != "finalize"
                or finalize_effect.get("phase") != "backup_finalize"
                or finalize_effect.get("status") != "intent"
            ):
                raise SwitchError(
                    f"Backup {backup_dir.name} has an invalid finalize intent."
                )
            finalize_effect["observed_after_state"] = {
                "lifecycle": "committed"
            }
            finalize_effect["status"] = "applied"
            journal["state"] = "committed"
    elif schema_version is not None:
        raise SwitchError(
            f"Unsupported backup schema version for {backup_dir.name}: "
            f"{schema_version!r}"
        )
    else:
        for entry in manifest.get("entries", []):
            entry["post_state"] = capture_state(Path(entry["path"]))
        manifest["finalized_at"] = now_stamp()
    if filesystem_adapter is None:
        write_json(backup_dir / "backup.json", manifest)
    else:
        write_manifest(
            backup_dir / "backup.json",
            manifest,
            phase="backup_finalize",
        )
    return manifest


def states_match(current: dict[str, Any], expected: dict[str, Any]) -> bool:
    if current.get("kind") != expected.get("kind"):
        return False
    kind = current.get("kind")
    if kind == "file":
        return (
            current.get("sha256") == expected.get("sha256")
            and current.get("size") == expected.get("size")
            and current.get("mode") == expected.get("mode")
        )
    if kind == "symlink":
        return current.get("symlink_target") == expected.get("symlink_target")
    if kind == "directory":
        return (
            current.get("tree_sha256") == expected.get("tree_sha256")
            and current.get("entry_count") == expected.get("entry_count")
            and current.get("mode") == expected.get("mode")
        )
    return True


def restore_backup(store: Store, backup_id_value: str, dry_run: bool, apply: bool, force: bool) -> None:
    if not apply:
        if not dry_run:
            raise SwitchError("restore requires --dry-run or --apply")

    from codex_switch_transaction import TransactionRequest, execute_transaction

    receipt = execute_transaction(
        store,
        TransactionRequest(
            operation="restore",
            profile="restore",
            options={"backup_id": backup_id_value, "force": force},
        ),
        dry_run=dry_run,
    )
    for index, line in enumerate(receipt.preview_lines):
        if dry_run and index == 0:
            print(f"Dry run: {line}")
        else:
            print(line)
    if dry_run:
        return
    if receipt.outcome == "rolled_back":
        raise SwitchError(
            f"Restore failed and was rolled back; safety backup: {receipt.backup_id}"
        )
    if receipt.outcome == "rollback_failed":
        raise SwitchError(
            f"Restore failed and rollback failed; safety backup: {receipt.backup_id}"
        )
    if receipt.outcome != "committed":
        raise SwitchError(f"Restore ended with unexpected outcome: {receipt.outcome}")
    print(f"Restored backup {backup_id_value}")


def cmd_restore(args: argparse.Namespace) -> None:
    restore_backup(
        store=make_store(args),
        backup_id_value=args.backup_id,
        dry_run=args.dry_run,
        apply=args.apply,
        force=args.force,
    )
