from __future__ import annotations

from pathlib import Path

from codex_switch_constants import APP_CLI_ENV, SwitchError
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
from codex_switch_selection import (
    ActiveProfileSelectionSnapshot,
    read_active_profile_selection_snapshot,
)
from codex_switch_shim import render_codex_shim_payload
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
    snapshot: ActiveProfileSelectionSnapshot | None = None,
) -> list[str]:
    active_snapshot = snapshot or read_active_profile_selection_snapshot(
        store.active_path
    )
    if active_snapshot.record is None and active_snapshot.problem is None:
        return []
    if active_snapshot.problem is not None:
        return [active_snapshot.problem]
    active = active_snapshot.record
    selection = active_snapshot.selection
    if active is None or selection is None:
        return ["active.selection.invalid: active selection is unavailable"]
    try:
        cli_manifest = store.load_manifest(selection.cli_profile)
        app_manifest = (
            cli_manifest
            if selection.app_profile == selection.cli_profile
            else store.load_manifest(selection.app_profile)
        )
    except SwitchError as exc:
        return [str(exc)]

    cli_binding: RuntimeBinding | None = None
    if (
        selection.cli_profile in {"internal", "openai-official", "official"}
        and manifest_uses_canonical_binding(selection.cli_profile, cli_manifest)
    ):
        try:
            cli_binding = resolve_store_runtime_binding(
                store,
                selection.cli_profile,
                manifest=cli_manifest,
            )
        except RuntimeBindingError as exc:
            return [f"{exc.code}: {exc}"]
    binding = runtime_binding
    if (
        binding is None
        and selection.app_profile in {"internal", "openai-official", "official"}
        and manifest_uses_canonical_binding(selection.app_profile, app_manifest)
    ):
        try:
            binding = (
                cli_binding
                if selection.app_profile == selection.cli_profile
                else resolve_store_runtime_binding(
                    store,
                    selection.app_profile,
                    manifest=app_manifest,
                )
            )
        except RuntimeBindingError as exc:
            return [f"{exc.code}: {exc}"]
    observation = runtime_observation
    if observation is None and binding is not None:
        observation = collect_store_runtime_observation(store, binding)
    expected_app_cli = (
        str(binding.desktop_cli)
        if binding is not None
        else profile_app_cli_path(app_manifest)
    )
    observed_label, current_app_cli = active_app_cli_observation(store, observation)
    problems: list[str] = []
    codex_home = active.get("codex_home")
    if isinstance(codex_home, str) and not store.profile_dir(
        selection.cli_profile
    ).exists():
        problems.append(
            f"active CLI profile {selection.cli_profile}: profile directory is missing"
        )
    if isinstance(codex_home, str):
        if not Path(codex_home).expanduser().exists():
            problems.append(
                f"active CLI profile {selection.cli_profile}: "
                f"CODEX_HOME is missing: {codex_home}"
            )
    backup_id = active.get("backup_id")
    if isinstance(backup_id, str) and not (store.backups_dir / backup_id / "backup.json").exists():
        problems.append(
            f"active CLI profile {selection.cli_profile}: backup is missing: {backup_id}"
        )
    if cli_binding is not None:
        expected_cli_home = cli_binding.codex_home
        if isinstance(codex_home, str) and not equivalent_paths(
            codex_home,
            str(expected_cli_home),
        ):
            problems.append(
                f"active CLI profile {selection.cli_profile}: recorded CODEX_HOME is "
                f"{codex_home}, expected {expected_cli_home}"
            )
        active_shell_cli = active.get("shell_cli_path")
        if isinstance(active_shell_cli, str) and not equivalent_paths(
            active_shell_cli,
            str(cli_binding.shell_cli),
        ):
            problems.append(
                f"active CLI profile {selection.cli_profile}: recorded shell CLI is "
                f"{active_shell_cli}, expected {cli_binding.shell_cli}"
            )
        raw_shim = active.get("shim_path") or active.get("shim")
        if isinstance(raw_shim, str) and raw_shim:
            shim_path = Path(raw_shim).expanduser()
            expected_shim = render_codex_shim_payload(
                store,
                str(cli_binding.shell_cli),
                expected_cli_home,
                profile_name=selection.cli_profile,
            )
            try:
                shim_matches = (
                    shim_path.is_file()
                    and not shim_path.is_symlink()
                    and shim_path.read_bytes() == expected_shim
                )
            except OSError:
                shim_matches = False
            if not shim_matches:
                problems.append(
                    f"active CLI profile {selection.cli_profile}: switch shim mismatch: "
                    f"{shim_path}"
                )
    if binding is not None and observation is not None:
        problems.extend(attestation_problem_messages(binding, observation))
    else:
        if (
            expected_app_cli
            and current_app_cli
            and not equivalent_paths(current_app_cli, expected_app_cli)
        ):
            problems.append(
                f"active App profile {selection.app_profile}: {observed_label} is "
                f"{current_app_cli}, expected {expected_app_cli}"
            )
        problems.extend(
            running_desktop_problems(
                store,
                selection.app_profile,
                expected_app_cli,
            )
        )
    problems.extend(plugin_materialization_problems(store, selection.cli_profile))
    return problems
