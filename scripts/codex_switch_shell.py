from __future__ import annotations

import os
from pathlib import Path

from codex_switch_io import atomic_write
from codex_switch_store import Store


BEGIN_MARKER = "# >>> codex-switch shell cli >>>"
END_MARKER = "# <<< codex-switch shell cli <<<"


def truthy(value: str | None) -> bool:
    return value in {"1", "true", "TRUE", "yes", "YES", "on", "ON"}


def shell_bootstrap_skipped() -> bool:
    return truthy(os.environ.get("CODEX_SWITCH_SKIP_SHELL_BOOTSTRAP"))


def shell_cli_bootstrap_path() -> Path | None:
    if shell_bootstrap_skipped():
        return None
    override = os.environ.get("CODEX_SWITCH_SHELL_PROFILE")
    if override:
        return Path(os.path.expandvars(override)).expanduser()

    home = Path.home()
    shell_name = Path(os.environ.get("SHELL", "")).name
    if shell_name == "zsh":
        return home / ".zshrc"
    if shell_name == "bash":
        return home / ".bashrc"
    return home / ".profile"


def shell_double_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"').replace("$", "\\$")


def shell_cli_bootstrap_block(store: Store) -> str:
    bin_dir = shell_double_quote(str(store.bin_dir))
    return (
        f"{BEGIN_MARKER}\n"
        "# Keep bare `codex` aligned with the active codex-switch profile.\n"
        'case ":$PATH:" in\n'
        f'  *":{bin_dir}:"*) ;;\n'
        f'  *) export PATH="{bin_dir}:$PATH" ;;\n'
        "esac\n"
        "hash -r 2>/dev/null || true\n"
        f"{END_MARKER}\n"
    )


def replace_managed_block(text: str, block: str) -> str:
    start = text.find(BEGIN_MARKER)
    end = text.find(END_MARKER)
    if start != -1 and end != -1 and start < end:
        end += len(END_MARKER)
        prefix = text[:start].rstrip("\n")
        suffix = text[end:].lstrip("\n")
        parts = [part for part in (prefix, block.rstrip("\n"), suffix.rstrip("\n")) if part]
        return "\n".join(parts) + "\n"

    if not text:
        return block
    return text.rstrip("\n") + "\n\n" + block


def ensure_shell_cli_bootstrap(store: Store) -> Path | None:
    path = shell_cli_bootstrap_path()
    if path is None:
        return None

    text = path.read_text() if path.exists() else ""
    next_text = replace_managed_block(text, shell_cli_bootstrap_block(store))
    if next_text == text:
        return path

    mode = path.stat().st_mode & 0o777 if path.exists() else 0o644
    atomic_write(path, next_text.encode(), mode=mode)
    return path
