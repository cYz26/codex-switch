# Specification Delta: codex-switch

## MODIFIED Requirements

### Requirement: Local command implementation self-update

The system SHALL check for self-updates on every ordinary persistent local
`codex-switch` command installed from a release bundle.

#### Scenario: Eligible release install syncs before command execution

- GIVEN the local wrapper is running from the configured release implementation
  directory
- AND the configured release bundle contains executable `scripts/codex-switch`
- WHEN the user invokes a local `codex-switch` command
- THEN the wrapper checks the stable implementation directory against the
  release bundle
- AND syncs from the release bundle when the release bundle version is newer
- AND re-execs the original command once against the synced wrapper.

#### Scenario: Source checkout does not self-modify

- GIVEN the wrapper is running from a source checkout outside the configured
  release implementation directory
- WHEN the user invokes a local `codex-switch` command
- THEN the wrapper does not rewrite the source checkout.

#### Scenario: Older release bundle does not replace current implementation

- GIVEN the wrapper is running from the configured release implementation
  directory
- AND the installed implementation has a version newer than the configured
  release bundle
- WHEN the user invokes a local `codex-switch` command
- THEN the wrapper reports the current implementation as up to date
- AND the installed implementation remains unchanged.

#### Scenario: Formal release replaces same-core development build

- GIVEN the wrapper is running from the configured release implementation
  directory
- AND the installed implementation is a prerelease build such as `0.1.13-dev`
- AND the configured release bundle version is the corresponding formal release
  such as `0.1.13`
- WHEN the user invokes a local `codex-switch` command
- THEN the wrapper syncs from the formal release bundle
- AND re-execs the original command once against the synced wrapper.

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

#### Scenario: Same-version check reports current status

- GIVEN a release-installed wrapper is eligible for self-update
- AND the configured release bundle has the same version as the installed
  bundle
- WHEN the user invokes a local `codex-switch` command
- THEN stderr reports that self-update is checking the latest release
- AND stderr reports that the implementation is already up to date.

#### Scenario: Sync-needed check reports version transition

- GIVEN a release-installed wrapper is eligible for self-update
- AND the configured release bundle has a newer version than the installed
  bundle
- WHEN the user invokes a local `codex-switch` command
- THEN stderr reports that self-update is checking the latest release
- AND stderr reports the synced implementation version transition.

#### Scenario: Repeated invocations check every time

- GIVEN a release-installed wrapper is eligible for self-update
- AND the configured release bundle has the same version as the installed
  bundle
- WHEN the user invokes a local `codex-switch` command twice in sequence
- THEN each invocation reports that self-update is checking the latest release.

#### Scenario: Skipped checks remain quiet

- GIVEN the user passes `--skip-self-update`
- WHEN the user invokes a local `codex-switch` command
- THEN no self-update status message is printed.
