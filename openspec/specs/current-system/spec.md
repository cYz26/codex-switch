# Current System Specification

## Purpose

Document the verified baseline behavior for `codex-switch`, a local workstation
CLI that switches Codex CLI and Codex Desktop profiles while preserving shared
non-auth configuration.

## Requirements

### Requirement: Profile store lifecycle

The system SHALL manage a profile store under `~/.codex-switch` by default.

#### Scenario: Initialize and capture profiles

- **WHEN** a user initializes the profile store
- **THEN** the system can create the official profile
- **AND** it can capture an existing `CODEX_HOME` as a named profile.

### Requirement: Profile switching

The system SHALL switch the live Codex home between stored profiles with dry-run
support.

#### Scenario: Switch profile safely

- **WHEN** a user switches to a stored profile
- **THEN** the system backs up live files
- **AND** rewrites the live Codex configuration for the target profile
- **AND** updates the shell Codex shim when requested
- **AND** persists Codex Desktop `CODEX_CLI_PATH` through a LaunchAgent when
  requested.

### Requirement: Shared and profile-specific configuration separation

The system SHALL keep shared workstation configuration separate from
profile-specific model and auth configuration.

#### Scenario: Preserve shared configuration

- **WHEN** profile switching writes the live `config.toml`
- **THEN** plugin marketplaces, enabled plugins, skill config, hook trust state,
  projects, MCP servers, UI preferences, feature flags, and other non-auth
  shared settings remain in the shared base config
- **AND** profile-specific model/auth settings are written separately to
  `<profile>.config.toml`.

### Requirement: Operational commands

The shell wrapper SHALL expose one-key profile commands and maintenance
commands.

#### Scenario: Inspect and maintain profile bindings

- **WHEN** a user invokes the shell wrapper
- **THEN** it supports internal and official one-key profile commands
- **AND** supports internal Codex CLI update checks
- **AND** supports environment helper commands
- **AND** supports installer linking
- **AND** supports raw pass-through to the Python CLI.

### Requirement: Release package

The repository SHALL package release artifacts from source files.

#### Scenario: Build release archive

- **WHEN** the release packaging script runs
- **THEN** it includes the README, skill metadata, version, agents, evals, and
  scripts needed to install and run `codex-switch`.

## Key Capabilities

- Initialize a profile store and official profile.
- Capture an existing `CODEX_HOME` as a named profile.
- Switch between stored profiles with dry-run support.
- Bind shell Codex and Codex Desktop app CLI paths per profile.
- Run login inside an isolated profile.
- Print active profile, shell resolution, app CLI binding, and doctor diagnostics.
- Package release artifacts from source files.

## Verification Commands

- `python3 scripts/test_codex_profile_switch.py`
- `bash -n scripts/codex-switch`
- `bash -n scripts/codex_env_setup`
- `bash -n install.sh`
- Python syntax compile over `scripts/*.py`
- `git diff --check`

## Source Areas

- Shell wrapper and installer: `scripts/codex-switch`, `install.sh`, `scripts/codex_env_setup`, `scripts/package-release.sh`.
- Python CLI entrypoint: `scripts/codex_profile_switch.py`.
- Profile store, config, switching, app wrapper, LaunchAgent, shim, status, and doctor modules: `scripts/codex_switch_*.py`.
- Regression tests: `scripts/test_codex_profile_switch.py`.
- Release metadata and assets: `README.md`, `SKILL.md`, `VERSION`, `agents/`, `evals/`.
