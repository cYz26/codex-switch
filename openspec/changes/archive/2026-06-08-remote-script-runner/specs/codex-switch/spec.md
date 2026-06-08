# Specification Delta: Remote Script Runner

## ADDED Requirements

### Requirement: Remote script invocation

The system SHALL provide a standalone remote runner that can execute
`codex-switch` commands from a release URL without requiring a pre-existing PATH
install.

#### Scenario: Execute command from release tarball

- GIVEN a valid `codex-switch.tar.gz` release bundle
- WHEN the user invokes the remote runner with command arguments
- THEN the runner installs the bundle into a stable local implementation
  directory
- AND executes `scripts/codex-switch` with the original arguments.

#### Scenario: No public symlink is installed

- GIVEN the user invokes the remote runner
- WHEN the runner prepares the local implementation directory
- THEN it does not create or update the public `codex-switch` PATH symlink.

#### Scenario: Release asset is emitted

- GIVEN release packaging is run
- WHEN the package script completes
- THEN `dist/run.sh` exists for upload as a direct remote execution script.
