# Specification Delta: codex-switch

## ADDED Requirements

### Requirement: Self-update status output

The system SHALL print concise status messages when a release-installed
`codex-switch` wrapper performs a self-update check.

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

#### Scenario: Skipped checks remain quiet

- GIVEN the user passes `--skip-self-update`
- WHEN the user invokes a local `codex-switch` command
- THEN no self-update status message is printed.
