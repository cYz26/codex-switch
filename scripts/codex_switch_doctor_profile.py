from __future__ import annotations

from pathlib import Path

from codex_switch_constants import SwitchError
from codex_switch_paths import equivalent_paths, profile_app_cli_path
from codex_switch_app_wrapper import managed_profile_app_cli_path
from codex_switch_runtime_binding import (
    RuntimeBindingError,
    manifest_uses_canonical_binding,
    resolve_store_runtime_binding,
)
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
    binding = None
    if name in {"internal", "openai-official", "official"}:
        try:
            if manifest_uses_canonical_binding(name, manifest):
                binding = resolve_store_runtime_binding(
                    store,
                    name,
                    manifest=manifest,
                )
        except RuntimeBindingError as exc:
            problems.append(f"{exc.code}: {exc}")
    if binding is not None:
        problems.extend(
            f"{finding.code}: {finding.message}"
            for finding in binding.findings
            if finding.severity in {"error", "warning"}
            and finding.code.startswith("binding.")
        )
    codex_bin = (
        str(binding.shell_cli)
        if binding is not None
        else str(manifest.get("codex_bin", ""))
    )
    if not codex_bin:
        problems.append(f"{name}: missing codex_bin")
    elif not Path(codex_bin).expanduser().exists():
        problems.append(f"{name}: codex_bin does not exist: {codex_bin}")
    app_cli_path = (
        str(binding.desktop_cli)
        if binding is not None
        else profile_app_cli_path(manifest)
    )
    if not app_cli_path:
        problems.append(f"{name}: missing app_cli_path")
    elif (
        name == "internal"
        and equivalent_paths(
            app_cli_path,
            str(managed_profile_app_cli_path(store, "internal")),
        )
    ):
        # The managed launcher is deterministically rendered by the first
        # internal switch; an inactive freshly captured profile may not have it yet.
        pass
    elif not Path(app_cli_path).expanduser().exists():
        problems.append(f"{name}: app_cli_path does not exist: {app_cli_path}")
    return problems
