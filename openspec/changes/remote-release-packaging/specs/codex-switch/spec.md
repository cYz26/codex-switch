# Specification Delta: Remote Release Packaging

## ADDED Requirements

### Requirement: Release packaging and source archive fallback

The system SHALL provide a reproducible remote release packaging path and a
source archive fallback for installing or running `codex-switch` when a release
bundle asset is unavailable.

#### Scenario: Tag workflow uploads release assets

- GIVEN a `v*` tag is pushed to GitHub
- WHEN the release workflow runs successfully
- THEN it builds the release bundle from the tagged source
- AND uploads `install.sh`, `run.sh`, and `codex-switch.tar.gz` as release
  assets for that tag.

#### Scenario: Installer falls back to source archive

- GIVEN the configured release bundle URL cannot be downloaded or validated
- AND a valid source archive fallback is available
- WHEN the user invokes `install.sh`
- THEN the installer stages a valid `codex-switch` implementation from the
  source archive
- AND creates the public `codex-switch` PATH symlink to that implementation.

#### Scenario: Remote runner falls back to source archive

- GIVEN the configured release bundle URL cannot be downloaded or validated
- AND a valid source archive fallback is available
- WHEN the user invokes `run.sh` with command arguments
- THEN the runner stages a valid `codex-switch` implementation from the source
  archive
- AND executes the requested command
- AND does not create or update the public `codex-switch` PATH symlink.

#### Scenario: Local self-update falls back to source archive

- GIVEN a release-installed local wrapper is eligible for self-update
- AND the configured release bundle URL cannot be downloaded or validated
- AND a valid source archive fallback is available
- WHEN the user invokes an ordinary local `codex-switch` command
- THEN the wrapper syncs from the source archive fallback
- AND re-execs the original command once against the synced wrapper.
