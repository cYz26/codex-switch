from __future__ import annotations

import argparse
import os
import subprocess
import tempfile
from pathlib import Path

from codex_switch_config import config_uses_file_auth
from codex_switch_core import (
    SwitchError,
    atomic_write,
    copy_file_atomic,
    ensure_private_dir,
    make_store,
    now_stamp,
    resolve_codex_bin,
    resolve_path,
    write_json,
)
from codex_switch_launch import validate_executable_path


def login_config_uses_file_auth(config_path: Path) -> bool:
    if not config_path.exists():
        return False
    return config_uses_file_auth(config_path.read_text())


def run_file_auth_login(
    command: list[str],
    base_env: dict[str, str],
    profile_dir: Path,
) -> int:
    ensure_private_dir(profile_dir)
    with tempfile.TemporaryDirectory(prefix="codex-switch-login-") as tmp:
        login_home = Path(tmp)
        atomic_write(
            login_home / "config.toml",
            b'cli_auth_credentials_store = "file"\n',
            mode=0o600,
        )
        env = dict(base_env)
        env["CODEX_HOME"] = str(login_home)
        result = subprocess.call(command, env=env)
        if result != 0:
            return result
        auth_path = login_home / "auth.json"
        if not auth_path.exists():
            raise SwitchError(f"Login completed but did not create auth.json in {login_home}.")
        copy_file_atomic(auth_path, profile_dir / "auth.json", mode=0o600)
    return 0


def cmd_login(args: argparse.Namespace) -> None:
    store = make_store(args)
    manifest = store.load_manifest(args.name)
    codex_bin = str(manifest.get("codex_bin", ""))
    if args.codex_bin:
        codex_bin = resolve_codex_bin(args.codex_bin)
    if not codex_bin:
        raise SwitchError("No codex_bin configured for this profile.")
    profile_dir = store.profile_dir(args.name)
    env = os.environ.copy()
    env["CODEX_HOME"] = str(profile_dir)
    command = [codex_bin, "login"]
    if args.with_api_key:
        command.append("--with-api-key")
    print(f"Running login for {args.name} with CODEX_HOME={profile_dir}")
    if login_config_uses_file_auth(profile_dir / "config.toml"):
        print("File auth profile detected; using a clean temporary CODEX_HOME for Codex login.")
        raise SystemExit(run_file_auth_login(command, env, profile_dir))
    raise SystemExit(subprocess.call(command, env=env))


def cmd_set_bin(args: argparse.Namespace) -> None:
    store = make_store(args)
    manifest = store.load_manifest(args.name)
    codex_bin = resolve_codex_bin(args.codex_bin)
    if not codex_bin:
        raise SwitchError("No codex binary path provided and none found on PATH.")
    bin_path = Path(codex_bin).expanduser()
    if not bin_path.exists():
        raise SwitchError(f"codex_bin does not exist: {bin_path}")

    manifest["codex_bin"] = str(bin_path)
    if not args.preserve_app_cli:
        manifest["app_cli_path"] = str(bin_path)
        manifest["app_cli_binding"] = "launchagent"
    manifest["updated_at"] = now_stamp()
    write_json(store.manifest_path(args.name), manifest)
    print(f"Updated {args.name} codex_bin: {bin_path}")
    if not args.preserve_app_cli:
        print(f"Updated {args.name} app_cli_path: {bin_path}")


def cmd_set_app_bin(args: argparse.Namespace) -> None:
    store = make_store(args)
    manifest = store.load_manifest(args.name)
    app_cli_path = resolve_path(args.app_cli_path)
    bin_path = validate_executable_path(app_cli_path, "app_cli_path")

    manifest["app_cli_path"] = str(bin_path)
    manifest["app_cli_binding"] = "launchagent"
    manifest["updated_at"] = now_stamp()
    write_json(store.manifest_path(args.name), manifest)
    print(f"Updated {args.name} app_cli_path: {bin_path}")


def cmd_shim_env(args: argparse.Namespace) -> None:
    store = make_store(args)
    print(f'export PATH="{store.bin_dir}:$PATH"')
    print("hash -r 2>/dev/null || true")
