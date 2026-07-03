from __future__ import annotations

import shutil

from codex_switch_io import run_quiet
from codex_switch_paths import equivalent_paths
from codex_switch_store import Store


def codex_version(path: str) -> str:
    code, output = run_quiet([path, "--version"])
    return output if code == 0 else "<unavailable>"


def print_codex_version(label: str, path: str) -> None:
    print(f"{label}: {codex_version(path)}")


def print_shell_codex_status(store: Store) -> None:
    current = shutil.which("codex") or "<not found>"
    print(f"PATH codex: {current}")
    if current != "<not found>":
        print_codex_version("PATH codex version", current)

    shim = store.bin_dir / "codex"
    print(f"Switch shim: {shim if shim.exists() else '<missing>'}")
    if shim.exists():
        print_codex_version("Shim codex version", str(shim))
        if current == "<not found>":
            print("PATH codex alignment: mismatch (codex not found on PATH)")
            print('PATH codex remediation: eval "$(codex-switch shim-env)"')
        elif equivalent_paths(current, str(shim)):
            print("PATH codex alignment: ok")
        else:
            print(
                "PATH codex alignment: mismatch "
                f"(expected switch shim {shim})"
            )
            print('PATH codex remediation: eval "$(codex-switch shim-env)"')
    else:
        print("PATH codex alignment: unavailable (switch shim missing)")
