# Specification Delta: Local Command Self Update

## ADDED Requirements

### Requirement: Local command implementation self-update

The system SHALL provide a bounded self-update check for persistent local
`codex-switch` commands installed from a release bundle.

#### Scenario: Eligible release install syncs before command execution

- GIVEN the local wrapper is running from the configured release implementation
  directory
- AND the self-update interval has elapsed
- AND the configured release bundle contains executable `scripts/codex-switch`
- WHEN the user invokes a local `codex-switch` command
- THEN the wrapper syncs the stable implementation directory from the release
  bundle
- AND re-execs the original command once against the synced wrapper.

#### Scenario: Source checkout does not self-modify

- GIVEN the wrapper is running from a source checkout outside the configured
  release implementation directory
- WHEN the user invokes a local `codex-switch` command
- THEN the wrapper does not rewrite the source checkout.

#### Scenario: Self-update can be skipped

- GIVEN the user sets `CODEX_SWITCH_SKIP_SELF_UPDATE=1`
- OR passes the global `--skip-self-update` option
- WHEN the user invokes a local `codex-switch` command
- THEN the wrapper skips the self-update check and runs the requested command
  with the current implementation.

#### Scenario: Remote runner skips redundant self-update

- GIVEN `run.sh` has already downloaded or copied a release bundle into the
  stable implementation directory
- WHEN it dispatches the bundled wrapper
- THEN the wrapper self-update check is disabled for that invocation.

#### Scenario: Sync failures do not block ordinary commands

- GIVEN the wrapper is eligible for self-update
- AND the release bundle cannot be fetched or validated
- WHEN the user invokes an ordinary local command
- THEN the wrapper warns about the failed self-update
- AND continues with the currently installed implementation.
