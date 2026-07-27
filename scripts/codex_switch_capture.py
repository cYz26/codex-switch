from __future__ import annotations

import argparse
from pathlib import Path

from codex_switch_constants import SwitchError
from codex_switch_paths import (
    resolve_codex_bin,
    resolve_internal_codex_bin,
    resolve_path,
)
from codex_switch_store import Store, make_store
from codex_switch_runtime_binding import (
    internal_managed_launcher_path,
)
from codex_switch_transaction import (
    LockedStoreMutation,
    TransactionReceipt,
    TransactionRequest,
    execute_transaction,
)


def capture_profile(
    store: Store,
    name: str,
    source_home: Path,
    codex_bin: str,
    app_cli_path: str,
    allow_missing_auth: bool,
    overwrite: bool,
    locked_store: LockedStoreMutation | None = None,
) -> TransactionReceipt:
    if name == "internal":
        codex_bin = resolve_internal_codex_bin(codex_bin)
        app_cli_path = str(internal_managed_launcher_path(store))
    request = TransactionRequest(
        operation="capture",
        profile=name,
        options={
            "source_home": source_home,
            "codex_bin": codex_bin,
            "app_cli_path": app_cli_path,
            "allow_missing_auth": allow_missing_auth,
            "overwrite": overwrite,
        },
    )
    receipt = (
        locked_store.execute_transaction(request)
        if locked_store is not None
        else execute_transaction(store, request)
    )
    if receipt.outcome != "committed":
        outcome_lines = (
            receipt.preview_lines[1:]
            if len(receipt.preview_lines) > 1
            else receipt.preview_lines
        )
        detail = "; ".join(outcome_lines) if outcome_lines else receipt.outcome
        raise SwitchError(f"Capture transaction did not commit: {detail}")
    for line in receipt.preview_lines:
        print(line)
    return receipt


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
