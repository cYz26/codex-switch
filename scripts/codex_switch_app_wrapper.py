from __future__ import annotations

import shlex
from pathlib import Path

from codex_switch_core import SwitchError, atomic_write
from codex_switch_store import Store


def managed_profile_app_cli_path(store: Store, name: str) -> Path:
    return store.bin_dir / f"codex-{name}-app"


def should_refresh_profile_app_wrapper(store: Store, name: str, app_cli_path: str) -> bool:
    path = Path(app_cli_path).expanduser()
    if not path.is_absolute():
        return False
    if path == managed_profile_app_cli_path(store, name):
        return True
    return name == "internal" and path == store.bin_dir / "codex-internal-app"


def profile_app_home(store: Store, name: str) -> Path:
    try:
        manifest = store.load_manifest(name)
    except Exception:
        manifest = {}
    raw_home = manifest.get("codex_home")
    if raw_home:
        return Path(str(raw_home)).expanduser()
    return store.managed_home(name)


def write_profile_app_wrapper(
    store: Store,
    name: str,
    app_cli_path: str,
    codex_bin: str,
    switch_scripts: Path,
) -> str:
    if not codex_bin:
        raise SwitchError("Profile manifest has no codex_bin. Capture or edit the profile first.")
    bin_path = Path(codex_bin).expanduser()
    if not bin_path.exists():
        raise SwitchError(f"codex_bin does not exist: {bin_path}")
    wrapper_path = Path(app_cli_path).expanduser()
    if not wrapper_path.is_absolute():
        raise SwitchError(f"app_cli_path must be an absolute path: {app_cli_path}")

    app_home = profile_app_home(store, name)
    script = f"""#!/usr/bin/env sh
set -eu

LIVE_CODEX_HOME={shlex.quote(str(store.live_codex_home))}
APP_CODEX_HOME={shlex.quote(str(app_home))}
CODEX_BIN={shlex.quote(str(bin_path))}
SWITCH_SCRIPTS={shlex.quote(str(switch_scripts))}
PROFILE_NAME={shlex.quote(name)}
PROFILE_CONFIG={shlex.quote(str(store.profile_dir(name) / "config.toml"))}

umask 077
mkdir -p "$APP_CODEX_HOME"

is_runtime_state_name() {{
  case "$1" in
    sessions|session_index.jsonl|history.jsonl|archived_sessions|log|tmp|.tmp)
      return 0
      ;;
    process_manager|node_repl|shell_snapshots|browser|ambient-suggestions)
      return 0
      ;;
    *.sqlite|*.sqlite-shm|*.sqlite-wal|*.sqlite.corrupt.*)
      return 0
      ;;
    *.sqlite-shm.corrupt.*|*.sqlite-wal.corrupt.*)
      return 0
      ;;
  esac
  return 1
}}

is_non_shareable_home_entry_name() {{
  case "$1" in
    .codex-global-state.json|.codex-global-state.json.bak|.credentials.json)
      return 0
      ;;
    agent-kb|automations|cache|computer-use|plugins|secrets|sqlite)
      return 0
      ;;
    chrome-native-hosts-v2.json|chrome-native-hosts.json|installation_id)
      return 0
      ;;
    model-catalogs|models_cache.json|pets|update-backups|vendor_imports|version.json)
      return 0
      ;;
  esac
  return 1
}}

remove_live_state_symlink() {{
  target="$APP_CODEX_HOME/$1"
  if [ -L "$target" ]; then
    link_target="$(readlink "$target" || true)"
    case "$link_target" in
      "$LIVE_CODEX_HOME"/*)
        rm -f "$target"
        ;;
    esac
  fi
}}

find "$APP_CODEX_HOME" -mindepth 1 -maxdepth 1 | while IFS= read -r path; do
  name="$(basename "$path")"
  if is_runtime_state_name "$name"; then
    remove_live_state_symlink "$name"
  fi
  if is_non_shareable_home_entry_name "$name"; then
    remove_live_state_symlink "$name"
  fi
done

find "$LIVE_CODEX_HOME" -mindepth 1 -maxdepth 1 | while IFS= read -r path; do
  name="$(basename "$path")"
  case "$name" in
    config.toml|auth.json|*.config.toml)
      continue
      ;;
  esac
  if is_runtime_state_name "$name"; then
    remove_live_state_symlink "$name"
    continue
  fi
  if is_non_shareable_home_entry_name "$name"; then
    remove_live_state_symlink "$name"
    continue
  fi
  target="$APP_CODEX_HOME/$name"
  if [ ! -e "$target" ] && [ ! -L "$target" ]; then
    ln -s "$path" "$target"
  fi
done

PYTHONPATH="$SWITCH_SCRIPTS" python3 - \\
  "$LIVE_CODEX_HOME/config.toml" \\
  "$PROFILE_CONFIG" \\
  "$APP_CODEX_HOME/config.toml" \\
  "$PROFILE_NAME" <<'PY'
import sys
from pathlib import Path

from codex_switch_config import (
    merge_shared_config_overlay,
)
from codex_switch_core import atomic_write
from codex_switch_home_sync import (
    build_internal_home_config,
    plugin_support_snapshot_name,
    refresh_profile_plugin_support_snapshot,
)

base = Path(sys.argv[1])
profile = Path(sys.argv[2])
target = Path(sys.argv[3])
profile_name = sys.argv[4]
if target.exists():
    shared_text = merge_shared_config_overlay(
        base.read_text(),
        target.read_text(),
    )
    atomic_write(base, shared_text.encode(), mode=0o600)
atomic_write(
    target,
    build_internal_home_config(base.parent, profile_name, target, profile).encode(),
    mode=0o600,
)
refresh_profile_plugin_support_snapshot(
    profile_name,
    target,
    [
        target.parent / plugin_support_snapshot_name(profile_name),
        profile.parent / plugin_support_snapshot_name(profile_name),
    ],
)
PY
rm -f "$APP_CODEX_HOME/auth.json"

export CODEX_HOME="$APP_CODEX_HOME"
if [ "${{1:-}}" = "app-server" ]; then
  exec env PYTHONPATH="$SWITCH_SCRIPTS" python3 \\
    "$SWITCH_SCRIPTS/codex_switch_app_proxy.py" \\
    "$CODEX_BIN" \\
    "$APP_CODEX_HOME/config.toml" \\
    "$@"
fi
exec "$CODEX_BIN" "$@"
"""
    atomic_write(wrapper_path, script.encode(), mode=0o755)
    return str(wrapper_path)


def maybe_refresh_profile_app_wrapper(
    store: Store,
    name: str,
    manifest: dict[str, object],
    app_cli_path: str,
    switch_scripts: Path,
) -> str:
    if not should_refresh_profile_app_wrapper(store, name, app_cli_path):
        return app_cli_path
    return write_profile_app_wrapper(
        store=store,
        name=name,
        app_cli_path=app_cli_path,
        codex_bin=str(manifest.get("codex_bin") or ""),
        switch_scripts=switch_scripts,
    )
