## ADDED Requirements

### Requirement: Profile update checks include an upstream stable advisory
The system SHALL compare the selected profile CLI version with the latest stable
release published by `openai/codex` during normal profile update checks.

#### Scenario: Internal switch shows stable comparison
- **WHEN** a one-key internal switch runs update checking successfully
- **THEN** output identifies the current internal CLI version
- **AND** output identifies the latest `openai/codex` stable version
- **AND** output classifies the internal CLI as behind, matching, or ahead.

#### Scenario: Official update check shows stable comparison
- **WHEN** the official profile update check runs
- **THEN** output retains ChatGPT.app update ownership
- **AND** output compares the bundled official CLI with the latest upstream
  stable release.

### Requirement: Stable and prerelease channels remain distinct
The system SHALL use the latest non-prerelease `openai/codex` release as the
default baseline and SHALL NOT present a prerelease as the stable target.

#### Scenario: Stable redirect is accepted
- **WHEN** the official latest-release endpoint resolves to a valid
  `rust-v<stable-semver>` tag
- **THEN** that semantic version is used as the advisory baseline.

#### Scenario: Prerelease tag is rejected as a stable baseline
- **WHEN** the resolved tag contains a semantic-version prerelease component
- **THEN** the stable comparison is reported unavailable
- **AND** no prerelease is presented as the stable target.

#### Scenario: Current prerelease is ahead of stable
- **WHEN** the selected CLI is a valid prerelease whose semantic version orders
  after the latest stable baseline
- **THEN** output classifies it as ahead of stable
- **AND** output does not recommend replacing or installing it.

### Requirement: Upstream advisory is bounded and non-blocking
The system SHALL bound upstream lookup work and SHALL preserve the existing
switch/update outcome when advisory evidence is unavailable.

#### Scenario: Network lookup fails
- **WHEN** GitHub lookup fails, times out, or returns no usable redirect tag
- **THEN** output reports the official stable comparison as unavailable
- **AND** an otherwise valid profile switch continues.

#### Scenario: Version parsing fails
- **WHEN** the selected CLI output or upstream tag lacks a valid semantic version
- **THEN** output reports the comparison as unavailable
- **AND** the advisory does not convert the update check into a failure.

#### Scenario: Update checking is explicitly skipped
- **WHEN** the user selects `--skip-update-check`
- **THEN** neither the profile-specific update check nor the upstream advisory
  performs network work.

### Requirement: Advisory cannot control internal installation
The upstream comparison SHALL be informational only and SHALL NOT select an
internal install target, invoke the internal update helper, or mutate profile
state.

#### Scenario: Internal is behind upstream stable
- **WHEN** the internal CLI is older than the upstream stable baseline but the
  internal release channel reports no update
- **THEN** output reports the internal CLI as behind upstream stable
- **AND** the internal update helper is not invoked because of that comparison.

#### Scenario: Advisory completes
- **WHEN** any upstream comparison outcome is produced
- **THEN** no profile manifest, config, active record, backup, or cached release
  metadata is written by the advisory.
