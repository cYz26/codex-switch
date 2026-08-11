## ADDED Requirements

### Requirement: Explicit generic Home support ownership

The system SHALL project generic support entries between managed profile Homes
only through a versioned allowlist containing global `AGENTS.md`, `prompts`,
`rules`, and personal standalone `skills` surfaces. Plugin selectors and
configured Skills SHALL continue to use the canonical shared-capability layer,
and physical plugin caches SHALL remain profile-local.

#### Scenario: Supported user-authored entries are shared

- **WHEN** a shared-mode switch observes an allowlisted support entry
- **THEN** the planned target uses the existing safe file, directory-link, or
  directory-copy semantics for that entry
- **AND** the transaction records and verifies that selected source and target.

#### Scenario: Unknown and runtime-owned entries are ignored

- **WHEN** a source Home contains an unknown top-level entry, runtime state,
  generated output, log, backup, cache, or Desktop atomic-write artifact
- **THEN** the switch does not plan, copy, link, hash as shared content, or
  report mutation progress for that entry
- **AND** an existing same-named target remains untouched.

#### Scenario: Desktop temporary naming variants remain private

- **WHEN** Desktop leaves `.codex-global-state.json` temporary or backup files
  using timestamped or otherwise variable suffixes
- **THEN** no such artifact is selected by generic Home support sharing
- **AND** only the separately allowlisted Desktop settings projection may read
  the canonical `.codex-global-state.json` file.

### Requirement: Bounded frozen-input validation

The system SHALL preserve recoverable compare-and-swap transaction safety
without recursively re-attesting every unchanged source tree before and after
each unrelated mutation effect.

#### Scenario: Deep validation work does not multiply by effect count

- **WHEN** a switch contains one or more allowlisted directory sources and
  multiple mutation effects
- **THEN** recursive content attestation for an unchanged source is bounded by
  planning, its relevant shared action, and final commit proof
- **AND** adding unrelated effects does not add another full traversal of every
  frozen directory for each journal checkpoint.

#### Scenario: Current shared source drift fails before its action

- **WHEN** a selected shared file or copied directory changes after planning
  but before or during its own shared action
- **THEN** the transaction rejects that action or rolls it back
- **AND** does not commit a target assembled from mixed source generations.

#### Scenario: Final commit retains complete CAS protection

- **WHEN** any required frozen input changes before the active record and
  backup commit point
- **THEN** one complete commit-time proof detects the drift
- **AND** the transaction restores all begun effects according to the existing
  journal contract.

### Requirement: Effect-derived App preservation and stopped rebind

The system SHALL derive whether a supported internal-CLI/official-App split
preserves or rebinds the App surface from the current attested official
binding. It SHALL require a stopped App only when the plan includes an
App-owned mutation.

#### Scenario: Running official App is preserved

- **WHEN** the App and app-server are running on the healthy canonical official
  binding and the user applies the supported split
- **THEN** the split commits the internal CLI Home, shim, shared capabilities,
  independent internal Plugin cache, and explicit active selection
- **AND** does not write the LaunchAgent, GUI environment, App wrapper, official
  Home, or any running App process state.

#### Scenario: CLI-only split excludes Desktop settings projection

- **WHEN** the supported split selects the App-preserving path
- **THEN** the canonical official `.codex-global-state.json` and any internal
  Desktop global-state target are absent from the frozen and mutation plans
- **AND** only generic allowlisted support plus the generationed Plugin/Skill
  desired state needed by the internal CLI is synchronized.

#### Scenario: Running App blocks a required rebind

- **WHEN** the App surface does not match the canonical official binding and a
  Desktop or app-server process is running
- **THEN** the command fails before backup with a stable instruction to quit
  the App and keep it closed until the rebind completes
- **AND** creates no journal, profile, shell, App binding, or active-selection
  mutation.

#### Scenario: Unreadable rebind process inventory fails closed

- **WHEN** an App rebind is required and the live process inventory cannot be
  read or classified safely
- **THEN** the split fails before backup and mutation
- **AND** does not treat an unreadable inventory as proof that the App stopped.

#### Scenario: Preview reports the derived App action

- **WHEN** the user previews a supported split
- **THEN** the command reports the planned CLI/App targets and whether the App
  action is `preserve` or `rebind`
- **AND** reports the stopped-App requirement only for `rebind`
- **AND** performs no process, backup, profile, or binding mutation.

#### Scenario: Stopped App permits a required rebind

- **WHEN** the App surface needs the canonical official binding and the live
  Desktop and app-server process set is provably stopped
- **THEN** the transaction applies the existing recoverable Desktop effects
- **AND** commits CLI and App ownership together only after final CAS proof.

#### Scenario: App starts during a required rebind

- **WHEN** stopped-App preflight succeeds for a required rebind but the App
  starts or rewrites a frozen input during mutation
- **THEN** the existing CAS and journal detect the late drift and roll back
- **AND** no partial split state is reported as committed.

### Requirement: Counted shared-sync progress

The system SHALL expose deterministic progress for the shared-support portion
of a switch without exposing file contents or weakening failure handling.

#### Scenario: Shared entries report ordered progress

- **WHEN** a switch applies multiple allowlisted shared entries
- **THEN** output identifies the current ordinal, total selected entries, and
  support entry name in deterministic order
- **AND** each reported item corresponds to one planned shared-support effect.

#### Scenario: Progress stops at the failing effect

- **WHEN** validation or mutation fails during a shared-support effect
- **THEN** no later item is reported as applied
- **AND** ordinary failure and rollback output remains authoritative.
