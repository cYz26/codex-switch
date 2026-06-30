# Specification Delta: codex-switch

## ADDED Requirements

### Requirement: Target profile switch verification

The system SHALL provide target-profile verification that can be run directly
from the `codex-switch` CLI and from one-key profile switches.

#### Scenario: Standalone verification detects official provider contamination

- GIVEN `openai-official` is the active profile
- AND the official runtime `config.toml` contains `model_provider`
- WHEN the user runs `codex-switch verify openai-official`
- THEN verification fails
- AND the output explains that official runtime config contains provider
  settings that should not seed the official profile.

#### Scenario: Standalone verification can refresh plugin support snapshots

- GIVEN the active profile runtime `config.toml` contains marketplace, plugin,
  skill, or hook trust settings
- AND the profile-local plugin support snapshot is missing
- WHEN the user runs `codex-switch verify <profile> --repair=safe`
- THEN verification refreshes the profile-local plugin support snapshot from
  the runtime config
- AND verification passes when no other problems remain.

#### Scenario: Standalone verification reports missing plugin support snapshots

- GIVEN the active profile runtime `config.toml` contains marketplace, plugin,
  skill, or hook trust settings
- AND the profile-local plugin support snapshot is missing
- WHEN the user runs `codex-switch verify <profile>` without repair
- THEN verification fails
- AND the output identifies the missing plugin support snapshot path.

#### Scenario: One-key switches verify before doctor

- GIVEN a one-key `codex-switch internal` or `codex-switch official` command
  completes the profile switch and plugin repair
- WHEN the post-switch flow continues
- THEN codex-switch runs target-profile verification before doctor
- AND the final result summary includes verification status.

#### Scenario: Verification can be skipped for diagnostic switches

- GIVEN a one-key `codex-switch internal` or `codex-switch official` command
  includes `--skip-verify`
- WHEN the post-switch flow continues
- THEN codex-switch does not run target-profile verification
- AND doctor/status behavior remains unchanged.

#### Scenario: Runtime smoke uses target profile environment

- GIVEN the requested profile has a configured `codex_bin`
- AND the requested profile has a resolved `CODEX_HOME`
- WHEN the user runs `codex-switch verify <profile> --runtime-smoke`
- THEN verification runs the profile `codex_bin --version` with `CODEX_HOME`
  set to that profile home
- AND verification runs `codex plugin list --json` with that same
  `CODEX_HOME`
- AND any smoke failure is reported as a verification problem.

#### Scenario: Exec smoke is explicit

- GIVEN the user wants a model-backed Codex runtime smoke
- WHEN the user runs `codex-switch verify <profile> --exec-smoke <prompt>`
- THEN verification runs `codex exec --json <prompt>` with `CODEX_HOME` set to
  the profile home
- AND no exec smoke runs unless that option is explicitly provided.

#### Scenario: Verification reports can be written

- GIVEN the user runs `codex-switch verify <profile> --report`
- WHEN verification completes
- THEN codex-switch writes a JSON verification report under the profile store
- AND the report records the profile, result, problems, repair mode, and smoke
  options used.
