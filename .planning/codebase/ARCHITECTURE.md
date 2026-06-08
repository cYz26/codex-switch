# Architecture

Brownfield map for `codex-switch`.

## Purpose

`codex-switch` is a project-agnostic workstation CLI for managing local Codex profiles, auth/config snapshots, shell shim binding, Codex Desktop `CODEX_CLI_PATH`, and internal Codex CLI updates.

## Entry Points

- `scripts/codex-switch` is the public Bash wrapper. It provides one-key commands such as `internal`, `official`, `check-update`, `update-internal`, `env`, `install`, and `version`, then delegates profile operations to the Python CLI.
- `scripts/codex_profile_switch.py` is the Python argparse entrypoint for `init`, `capture`, `switch`, `list`, `status`, `doctor`, `shim-env`, `login`, `set-bin`, and `set-app-bin`.
- `install.sh` installs the release payload under `~/.local/share/codex-switch/current` and links `~/.local/bin/codex-switch`.
- `scripts/package-release.sh` builds the distributable tree and tarball under `dist/`.

## Core Modules

- `codex_switch_core.py` defines shared constants, paths, atomic writes, JSON/TOML validation helpers, and `Store` creation.
- `codex_switch_store.py` manages profile store paths and manifest loading.
- `codex_switch_capture.py`, `codex_switch_lifecycle.py`, and `codex_switch_switching.py` implement profile capture, initialization, and switching.
- `codex_switch_config.py`, `codex_switch_toml_scan.py`, `codex_switch_toml_edit.py`, and `codex_switch_toml_validate.py` manage shared/profile TOML transformations.
- `codex_switch_app_wrapper.py`, `codex_switch_launch.py`, and `codex_switch_shim.py` manage Desktop app wrappers, LaunchAgents, and shell shim updates.
- `codex_switch_doctor*.py`, `codex_switch_status*.py`, and `codex_switch_running_app.py` provide health checks and diagnostics.
- `codex_switch_bindings.py`, `codex_switch_plan.py`, `codex_switch_record.py`, `codex_switch_backup.py`, and `codex_switch_io.py` support command binding, switch plan output, active records, backup, and IO helpers.

## Test Surface

- `scripts/test_codex_profile_switch.py` is the main regression suite. It creates isolated temporary stores and fake Codex binaries, then verifies profile initialization, switching, Desktop app CLI bindings, config migration, doctor/status behavior, and wrapper behavior.

## Release Assets

- `README.md`, `SKILL.md`, `VERSION`, `agents/`, `evals/`, and `scripts/` are copied into the release package by `scripts/package-release.sh`.
- `dist/` is generated output, not source-of-truth project logic.
