from __future__ import annotations

import shutil

from codex_switch_io import run_quiet
from codex_switch_store import Store


def print_codex_version(label: str, path: str) -> None:
    code, output = run_quiet([path, "--version"])
    print(f"{label}: {output if code == 0 else '<unavailable>'}")


def print_shell_codex_status(store: Store) -> None:
    current = shutil.which("codex") or "<not found>"
    print(f"PATH codex: {current}")
    if current != "<not found>":
        print_codex_version("PATH codex version", current)

    shim = store.bin_dir / "codex"
    print(f"Switch shim: {shim if shim.exists() else '<missing>'}")
    if shim.exists():
        print_codex_version("Shim codex version", str(shim))
