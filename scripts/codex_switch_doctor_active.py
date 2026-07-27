from __future__ import annotations

from pathlib import Path

from codex_switch_constants import APP_CLI_ENV, SwitchError
from codex_switch_io import read_json
from codex_switch_launch import read_launch_agent_cli_path
from codex_switch_paths import detect_current_app_cli_path, equivalent_paths, profile_app_cli_path
from codex_switch_plugins import plugin_materialization_problems
from codex_switch_running_app import (
    attestation_problem_messages,
    collect_store_runtime_observation,
    running_desktop_problems,
)
from codex_switch_runtime_binding import (
    RuntimeBinding,
    RuntimeBindingError,
    RuntimeObservation,
    manifest_uses_canonical_binding,
    resolve_store_runtime_binding,
)
from codex_switch_store import Store


def active_app_cli_observation(
    store: Store,
    runtime_observation: RuntimeObservation | None = None,
) -> tuple[str, str]:
    if runtime_observation is not None:
        if runtime_observation.launch_agent_cli:
            return (f"LaunchAgent {APP_CLI_ENV}", runtime_observation.launch_agent_cli)
        if runtime_observation.gui_app_cli:
            return (f"GUI {APP_CLI_ENV}", runtime_observation.gui_app_cli)
        return ("", "")
    launch_agent_cli = read_launch_agent_cli_path(store.launch_agent_path)
    if launch_agent_cli:
        return (f"LaunchAgent {APP_CLI_ENV}", launch_agent_cli)
    current_app_cli = detect_current_app_cli_path()
    if current_app_cli:
        return (f"GUI {APP_CLI_ENV}", current_app_cli)
    return ("", "")


def active_profile_problems(
    store: Store,
    *,
    runtime_binding: RuntimeBinding | None = None,
    runtime_observation: RuntimeObservation | None = None,
) -> list[str]:
    if not store.active_path.exists():
        return []
    active = read_json(store.active_path)
    active_profile = active.get("profile")
    if not isinstance(active_profile, str):
        return []
    try:
        active_manifest = store.load_manifest(active_profile)
    except SwitchError as exc:
        return [str(exc)]

    binding = runtime_binding
    if (
        binding is None
        and active_profile in {"internal", "openai-official", "official"}
        and manifest_uses_canonical_binding(active_profile, active_manifest)
    ):
        try:
            binding = resolve_store_runtime_binding(
                store,
                active_profile,
                manifest=active_manifest,
                active_record=active,
            )
        except RuntimeBindingError as exc:
            return [f"{exc.code}: {exc}"]
    observation = runtime_observation
    if observation is None and binding is not None:
        observation = collect_store_runtime_observation(store, binding)
    expected_app_cli = (
        str(binding.desktop_cli)
        if binding is not None
        else profile_app_cli_path(active_manifest)
    )
    observed_label, current_app_cli = active_app_cli_observation(store, observation)
    problems: list[str] = []
    codex_home = active.get("codex_home")
    if isinstance(codex_home, str) and not store.profile_dir(active_profile).exists():
        problems.append(f"active profile {active_profile}: profile directory is missing")
    if isinstance(codex_home, str):
        if not Path(codex_home).expanduser().exists():
            problems.append(f"active profile {active_profile}: CODEX_HOME is missing: {codex_home}")
    backup_id = active.get("backup_id")
    if isinstance(backup_id, str) and not (store.backups_dir / backup_id / "backup.json").exists():
        problems.append(f"active profile {active_profile}: backup is missing: {backup_id}")
    if binding is not None and observation is not None:
        problems.extend(attestation_problem_messages(binding, observation))
    else:
        if (
            expected_app_cli
            and current_app_cli
            and not equivalent_paths(current_app_cli, expected_app_cli)
        ):
            problems.append(
                f"active profile {active_profile}: {observed_label} is "
                f"{current_app_cli}, expected {expected_app_cli}"
            )
        problems.extend(running_desktop_problems(store, active_profile, expected_app_cli))
    problems.extend(plugin_materialization_problems(store, active_profile))
    return problems
