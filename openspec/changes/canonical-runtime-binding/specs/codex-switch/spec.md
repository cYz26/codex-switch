## ADDED Requirements

### Requirement: Canonical runtime binding
The system SHALL derive shell CLI, Desktop launcher, backend CLI, profile home, Desktop host ownership, and proxy requirement from one canonical runtime binding for each supported profile.

#### Scenario: All consumers use manifest intent
- **WHEN** switch, status, Doctor, or verify evaluates a profile
- **THEN** its expected paths come from the same canonical binding derived from the profile manifest and store
- **AND** stale `active.json`, launchctl, or process observations are reported as drift rather than accepted as intent.

#### Scenario: Managed shim is not official bundle evidence
- **WHEN** no verified official Desktop bundle CLI is available and PATH resolves to a codex-switch managed shim
- **THEN** official binding resolution fails closed
- **AND** it does not record the shim as the official backend or Desktop CLI.

### Requirement: ChatGPT Desktop ownership
The system SHALL treat the verified ChatGPT desktop bundle as the current official Codex Desktop host and SHALL treat Codex.app only as a legacy migration observation.

#### Scenario: Current ChatGPT bundle is selected
- **WHEN** `/Applications/ChatGPT.app` has the expected bundle identity and executable bundled CLI
- **THEN** official shell and Desktop CLI resolve to its `Contents/Resources/codex`
- **AND** the main Desktop executable expectation resolves to `Contents/MacOS/ChatGPT`.

#### Scenario: Legacy Codex bundle requires migration
- **WHEN** ChatGPT.app is absent and a legacy Codex.app is observed
- **THEN** official binding does not certify it as the current healthy host
- **AND** reports migration guidance for installing or updating to ChatGPT.app.

#### Scenario: ChatGPT Classic is excluded
- **WHEN** ChatGPT Classic is installed
- **THEN** it is not selected as the Codex Desktop host or backend source.

### Requirement: Managed internal Desktop binding
The system SHALL bind the internal profile's Desktop path to the generated managed launcher/proxy and SHALL track the validated internal backend separately.

#### Scenario: Fresh internal capture is self-consistent
- **WHEN** init or capture creates the internal profile from a valid backend
- **THEN** the effective Desktop binding is the managed internal launcher
- **AND** Doctor, status, verify, and the next normal internal switch expect that same launcher/backend pair.

#### Scenario: Internal discovery symlink resolves to backend identity
- **WHEN** PATH, capture, or rebind supplies a symlink whose final target is a regular executable internal backend
- **THEN** the internal manifest persists the resolved backend path rather than the symlink alias
- **AND** the shim, managed launcher, and capability receipt bind to that same regular file.

#### Scenario: Legacy internal symlink manifest migrates on switch
- **WHEN** a normal internal switch reads a legacy manifest whose `codex_bin` is a symlink to a regular executable
- **THEN** planning hashes and probes the resolved regular backend without weakening receipt no-follow checks
- **AND** a successful transaction commits the canonical backend path together with the refreshed launcher and receipt.

#### Scenario: Rebind promotes launcher and manifest together
- **WHEN** `set-bin internal` receives a valid new backend and the staged compatibility smoke succeeds
- **THEN** the regenerated managed launcher and manifest backend are promoted atomically
- **AND** `app_cli_path` does not bypass the proxy.

#### Scenario: Failed rebind restores the old pair
- **WHEN** validation, launcher generation, or compatibility smoke fails during internal rebind
- **THEN** the previous manifest and managed launcher remain effective
- **AND** the command returns failure without reporting the new backend as active.

### Requirement: Runtime process attestation
The system SHALL recognize app-server commands with supported global options before the subcommand and SHALL attest the expected Desktop host, launcher, proxy, and child backend.

#### Scenario: ChatGPT app-server with global config option is recognized
- **WHEN** the running command contains the bundled `codex`, one or more global options such as `-c key=value`, and then `app-server`
- **THEN** process inventory identifies it as an app-server process
- **AND** compares it with the canonical official binding.

#### Scenario: Stale internal child backend is rejected
- **WHEN** a process uses the expected managed launcher and proxy but its child app-server executable differs from the current internal backend
- **THEN** status, Doctor, and verify report a stale backend mismatch.

#### Scenario: Ambiguous process shape fails closed
- **WHEN** a process command cannot be parsed unambiguously as the expected app-server chain
- **THEN** it is not counted as healthy evidence.

### Requirement: Successful app-server initialization evidence
The system SHALL require a successful app-server initialize result before an app-server smoke can pass.

#### Scenario: Initialize error fails smoke
- **WHEN** the app-server returns a matching initialize response containing an error
- **THEN** app-server smoke fails even if later requests receive responses and the process stays alive.

#### Scenario: Successful initialize allows documented plugin auth error
- **WHEN** initialize returns a matching result and plugin-list later returns an explicitly allowed authentication error
- **THEN** the process may pass compatibility smoke if it remains healthy for the settle window.
