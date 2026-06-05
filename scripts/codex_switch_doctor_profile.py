from __future__ import annotations

from pathlib import Path

from codex_switch_constants import SwitchError
from codex_switch_paths import profile_app_cli_path
from codex_switch_store import Store
from codex_switch_toml_validate import validate_toml


def profile_health_problems(store: Store, name: str) -> list[str]:
    manifest = store.load_manifest(name)
    profile_dir = store.profile_dir(name)
    config_path = profile_dir / "config.toml"
    problems: list[str] = []
    if not config_path.exists():
        problems.append(f"{name}: missing config.toml")
    else:
        try:
            validate_toml(config_path)
        except SwitchError as exc:
            problems.append(str(exc))
    codex_bin = str(manifest.get("codex_bin", ""))
    if not codex_bin:
        problems.append(f"{name}: missing codex_bin")
    elif not Path(codex_bin).expanduser().exists():
        problems.append(f"{name}: codex_bin does not exist: {codex_bin}")
    app_cli_path = profile_app_cli_path(manifest)
    if not app_cli_path:
        problems.append(f"{name}: missing app_cli_path")
    elif not Path(app_cli_path).expanduser().exists():
        problems.append(f"{name}: app_cli_path does not exist: {app_cli_path}")
    return problems
