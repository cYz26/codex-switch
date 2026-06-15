from __future__ import annotations

from pathlib import Path

from codex_switch_constants import SwitchError
from codex_switch_io import atomic_write
from codex_switch_store import Store


def write_codex_shim(store: Store, codex_bin: str, codex_home: Path | None = None) -> Path:
    if not codex_bin:
        raise SwitchError("Profile manifest has no codex_bin. Capture or edit the profile first.")
    bin_path = Path(codex_bin).expanduser()
    if not bin_path.exists():
        raise SwitchError(f"codex_bin does not exist: {bin_path}")

    shim_path = store.bin_dir / "codex"
    home = codex_home or store.live_codex_home
    script = f"""#!/usr/bin/env sh
export CODEX_HOME="{home}"
exec "{bin_path}" "$@"
"""
    atomic_write(shim_path, script.encode(), mode=0o755)
    return shim_path
