## ADDED Requirements

### Requirement: Split-mode internal updates are CLI-scoped

The system SHALL treat the internal runtime selected by `codex-switch split`
as a shell CLI runtime and SHALL NOT require that a staged internal candidate
be compatible with Codex App before promoting it.

#### Scenario: Healthy CLI candidate is promoted

- **GIVEN** `codex-switch split` selects internal for CLI and the official
  bundle for Codex App
- **AND** the ordered update check selects a newer internal candidate
- **WHEN** the candidate passes the bounded CLI validation and exact-version
  postcondition
- **THEN** the candidate replaces the bound internal CLI atomically
- **AND** the internal manifest records the promoted CLI generation identity
- **AND** that generation is recorded as unverified for internal App use.

#### Scenario: CLI postcondition fails

- **GIVEN** a staged internal candidate is being promoted for split-mode CLI
  use
- **WHEN** its CLI validation or exact-version postcondition fails after the
  prepared transaction begins
- **THEN** the prior bound internal binary and prior manifest are restored
- **AND** no partially promoted generation is reported as healthy.

#### Scenario: Official App may remain running

- **GIVEN** Codex App is using the official bundled runtime and is currently
  running
- **WHEN** split mode promotes an internal CLI candidate
- **THEN** the promotion does not require Codex App to exit
- **AND** it does not modify the official App binary, App binding, LaunchAgent,
  App global state, Desktop wrapper, or App parity artifacts.

#### Scenario: Preserved App has no restart guidance

- **GIVEN** a successful split apply reports `App action: preserve`
- **WHEN** the wrapper prints its final result
- **THEN** it does not instruct the user to restart ChatGPT or Codex App
- **AND** a successful apply that reports `App action: rebind` retains explicit
  guidance to open or restart the App.

#### Scenario: Keep-version retains the bound CLI

- **GIVEN** a newer internal candidate is available
- **WHEN** the user runs `codex-switch split --keep-version`
- **THEN** the internal update check and promotion remain skipped
- **AND** the existing internal CLI generation is retained.

### Requirement: CLI-only generations execute independently of App parity

The system SHALL validate and execute an explicitly promoted CLI-only internal
generation without treating stale or unsupported internal-App protocol parity
as a CLI health failure.

#### Scenario: Shell invocation uses the promoted CLI generation

- **GIVEN** the internal manifest records a CLI-only generation whose binary
  digest and version match the bound internal executable
- **WHEN** the managed internal shell entrypoint runs an informational or
  functional CLI command
- **THEN** it executes that bound internal executable with the internal CLI
  home
- **AND** it does not require the prior App capability, proxy, overlay, or
  parity generation to match that executable.

#### Scenario: CLI generation identity drifts

- **GIVEN** the internal manifest records a CLI-only generation
- **WHEN** the bound executable no longer matches the recorded generation
  identity
- **THEN** the managed internal shell entrypoint fails closed before executing
  the drifted binary.

#### Scenario: Production-sized CLI generation is validated

- **GIVEN** a valid CLI-only internal generation whose executable is larger
  than the bounded text-artifact limit but within the executable safety bound
- **WHEN** the managed internal shell validates the generation
- **THEN** it computes the complete executable digest with a stable streaming
  read
- **AND** it does not buffer the complete executable in memory
- **AND** it does not reject the executable solely because it exceeds a config
  or receipt artifact limit.

#### Scenario: CLI executable exceeds its independent safety bound

- **GIVEN** a CLI-only manifest selects a backend larger than the supported
  executable safety bound
- **WHEN** managed generation validation begins
- **THEN** validation fails before reading or executing that backend
- **AND** the error identifies the CLI backend size contract.

#### Scenario: Functional CLI preflight remains enforced

- **GIVEN** a valid CLI-only internal generation
- **WHEN** a functional internal CLI command is invoked
- **THEN** the existing shared Plugin and Skill configuration preflight still
  completes before backend execution
- **AND** informational version or help invocations retain their existing
  read-only behavior.

#### Scenario: Promotion and final verification attest the managed generation

- **GIVEN** a CLI-only candidate's raw executable can answer `--version`
- **WHEN** its managed generation metadata, home, identity, or freshly rendered
  internal shell entrypoint is invalid
- **THEN** the prepared promotion postcondition restores the prior binary and
  manifest when the defect exists before commit
- **AND** final split runtime smoke invokes the managed shell path rather than
  the raw backend
- **AND** the split command cannot report success while the operator-facing
  `codex` entrypoint is unusable.

#### Scenario: Apply progress remains visible while the switch is running

- **GIVEN** split apply emits a progress line and then remains busy
- **WHEN** the wrapper filters output to capture the App action
- **THEN** the progress line is observable before the switch process exits
- **AND** this guarantee applies to the Python producer as well as the stream
  filter.

### Requirement: App readiness is surface-specific and fail-closed

The system SHALL apply internal Desktop parity only when Codex App is selected
to use internal, and SHALL reject an unverified internal App generation before
any App mutation.

#### Scenario: Split diagnostics do not require internal App parity

- **GIVEN** the active selection is internal CLI plus official App
- **WHEN** verify, Doctor, or status evaluates the selection
- **THEN** internal App parity is reported as not applicable
- **AND** stale or unsupported internal-App parity does not make internal CLI
  verification unhealthy
- **AND** App checks use the independently owned official bundle and home.

#### Scenario: Diagnostics observe one active selection generation

- **GIVEN** verify or Doctor begins from one valid active CLI/App selection
- **WHEN** it resolves runtime bindings, shared configuration, App parity, and
  active-state health
- **THEN** every result in that invocation uses the same selection snapshot
- **AND** a concurrent switch cannot make the invocation mix owners from two
  active-record generations
- **AND** a requested parity repair fails before full-rebind preparation or
  mutation when the active record changed after that snapshot.

#### Scenario: Unverified internal App selection is rejected

- **GIVEN** the internal manifest records that its current backend generation
  is unverified for App use
- **WHEN** a dry-run or apply requests internal as the App profile
- **THEN** the request fails with a stable readiness error before transaction
  planning commits any App, LaunchAgent, global-state, active-record, or home
  mutation.

#### Scenario: Full parity promotion clears the CLI-only restriction

- **GIVEN** an internal generation was previously promoted for CLI-only use
- **WHEN** an explicit full internal-App rebind later completes its existing
  capability, parity, proxy, and App-server verification contract
- **THEN** the CLI-only App-readiness restriction is removed as part of that
  full atomic generation commit.

#### Scenario: Legacy full-parity manifests remain compatible

- **GIVEN** an internal manifest predates CLI-only readiness metadata
- **WHEN** internal App is selected
- **THEN** the existing full parity and runtime-generation validation contract
  remains authoritative.
