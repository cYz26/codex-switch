# codex-switch Specification

## Purpose

Define the runtime-state isolation contract for `codex-switch` managed Codex
Desktop profile app homes.
## Requirements
### Requirement: Profile Desktop runtime state isolation

The internal Codex Desktop wrapper SHALL keep response/session runtime state
profile-local instead of symlinking it from the live shared `CODEX_HOME`.

#### Scenario: Existing live state symlinks are removed

- GIVEN the internal profile app home contains generated symlinks for runtime
  state paths that target live `CODEX_HOME`
- WHEN the internal Desktop wrapper starts
- THEN those stale symlinks are removed before Codex launches
- AND no live `auth.json` is copied into the app home.

#### Scenario: Future runtime state links are not created

- GIVEN live `CODEX_HOME` contains session, history, log, temporary, browser, or
  sqlite runtime state
- WHEN the internal Desktop wrapper prepares the profile app home
- THEN those runtime state entries are not symlinked into the profile app home
- AND stable non-auth support assets may still be shared.

#### Scenario: Shared config overlay is preserved

- GIVEN Codex Desktop writes non-auth shared configuration into the profile app
  home
- WHEN the internal Desktop wrapper starts again
- THEN non-auth shared configuration is folded back into live shared
  `config.toml`
- AND profile-specific model/auth configuration remains in the generated app
  home config.

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
