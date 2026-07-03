# Specification Delta: codex-switch

## ADDED Requirements

### Requirement: Internal Desktop app-server request compatibility

The system SHALL keep using the internal profile's configured Codex binary and
SHALL route internal Desktop app-server launches through the generated app
proxy before forwarding them to an older internal app-server backend. The proxy
SHALL normalize known newer Desktop request shapes before forwarding them.

#### Scenario: Desktop app-server flags still enter the compatibility proxy

- GIVEN internal mode is configured with a generated Desktop app wrapper
- AND the Desktop app launches `app-server` with an app-server flag other than
  `--stdio`
- WHEN the generated wrapper handles the launch
- THEN it runs the configured internal binary through the app proxy
- AND non-app-server CLI commands still run the configured internal binary
  directly.

#### Scenario: Namespace dynamic tools are compatible with older internal backends

- GIVEN internal mode is configured with an older Codex backend that accepts
  flat dynamic tool specs requiring top-level `inputSchema`
- AND Codex Desktop sends a `thread/start` request containing a namespace
  dynamic tool spec
- WHEN the app proxy forwards the request to the backend
- THEN the namespace spec is converted to one or more flat function tool specs
- AND each converted tool includes the original namespace name
- AND no namespace dynamic tool spec is forwarded to the older backend.

#### Scenario: Canonical dynamic tools are preserved for namespace-capable internal backends

- GIVEN internal mode is configured with an internal backend that accepts
  canonical namespace dynamic tool specs
- AND Codex Desktop sends a `thread/start` request containing a canonical
  namespace dynamic tool spec and a canonical function dynamic tool spec
- WHEN the app proxy forwards the request to the backend
- THEN the dynamic tool specs remain in canonical format
- AND no mixed canonical and legacy dynamic tool array is forwarded.

#### Scenario: Unsupported plugin marketplace kinds are filtered

- GIVEN internal mode is configured with an older Codex backend that does not
  accept the `created-by-me-remote` plugin marketplace kind
- AND Codex Desktop sends a `plugin/list` request containing
  `created-by-me-remote`
- WHEN the app proxy forwards the request to the backend
- THEN the unsupported marketplace kind is removed
- AND supported marketplace kinds in the same request are preserved.

#### Scenario: Internal binary binding is preserved

- GIVEN the internal profile manifest has a configured `codex_bin`
- WHEN internal Desktop mode is repaired for app-server protocol compatibility
- THEN the internal profile continues to launch that configured binary through
  the generated app proxy
- AND it is not rebound to the Codex Desktop App bundle.

#### Scenario: Post-update app-server startup smoke catches early backend exits

- GIVEN a one-key internal switch auto-updated the internal profile backend
- WHEN post-switch verification runs
- THEN verification starts the target profile `codex_bin app-server` with the
  target profile `CODEX_HOME`
- AND it sends a Desktop-like initialization and `plugin/list` request
- AND it fails verification if the app-server exits non-zero during the startup
  settle window.

#### Scenario: Plugin list auth errors are not app-server startup crashes

- GIVEN the app-server startup smoke receives a JSON-RPC response or error for
  the `plugin/list` request
- AND the app-server remains running during the startup settle window
- WHEN verification evaluates the smoke
- THEN the smoke is considered healthy even if the response reports missing
  ChatGPT or remote plugin catalog authentication.

#### Scenario: App-server startup smoke can be requested explicitly

- GIVEN a user wants to verify a rebound or manually upgraded internal backend
- WHEN they run `codex-switch verify internal --app-server-smoke`
- THEN verification performs the app-server startup smoke against the internal
  profile runtime
- AND ordinary verification without `--app-server-smoke` keeps the previous
  local checks unchanged.

### Requirement: Internal known-bad release pinning

The system SHALL prevent one-key internal switches from automatically upgrading
to a known-bad internal Codex CLI release, and SHALL resume normal latest
auto-update once the latest internal release is no longer blocked.

#### Scenario: Healthy fallback is kept while latest is blocked

- GIVEN the internal profile `codex_bin` reports `codex-cli 0.142.4`
- AND the latest internal release resolves to `internal-rust-v0.142.5`
- WHEN the user runs `codex-switch internal`
- THEN the update check reports that `0.142.5` is blocked
- AND no internal installer command is run
- AND the switch continues with the existing `0.142.4` profile binary.

#### Scenario: Blocked current binary is replaced with pinned fallback

- GIVEN the internal profile `codex_bin` reports `codex-cli 0.142.5`
- AND the latest internal release resolves to `internal-rust-v0.142.5`
- WHEN the user runs `codex-switch internal`
- THEN the update check reports that `0.142.5` is blocked
- AND the automatic internal update runs with `--version 0.142.4`
- AND the installer is scoped to the current internal profile binary directory.

#### Scenario: Successor latest resumes ordinary auto-update

- GIVEN the internal profile `codex_bin` reports `codex-cli 0.142.4`
- AND the latest internal release resolves to a version after blocked
  `0.142.5`
- WHEN the user runs `codex-switch internal`
- THEN the automatic internal update runs without the `0.142.4` fallback pin.

### Requirement: Active shell Codex CLI alignment is visible

The system SHALL report whether bare `codex` in the current shell resolves to
the codex-switch shim for the active profile, and SHALL provide a shell command
that aligns PATH ordering when it does not.

#### Scenario: Status reports shell PATH drift

- GIVEN a profile switch wrote the codex-switch shim
- AND the current shell resolves bare `codex` to a different executable first
- WHEN the user runs `codex-switch status`
- THEN status reports the resolved PATH executable
- AND status reports the codex-switch shim path
- AND status reports the alignment as a mismatch
- AND status prints `eval "$(codex-switch shim-env)"` as the remediation.

#### Scenario: Shim environment clears shell command cache

- WHEN the user runs `codex-switch shim-env`
- THEN the output prepends the codex-switch shim directory to PATH
- AND the output clears the shell command lookup cache when the shell supports
  it.

#### Scenario: Profile switch installs shell bootstrap

- GIVEN a profile switch updates the codex-switch command-line shim
- AND the user's shell startup file has unrelated content
- WHEN the switch is applied
- THEN codex-switch preserves the unrelated content
- AND installs a marker-managed block that prepends the active store `bin`
  directory to PATH
- AND the block clears the shell command lookup cache when the shell supports
  it.

#### Scenario: Shell bootstrap remains idempotent across switches

- GIVEN a shell startup file already contains the codex-switch managed block
- WHEN the user switches profiles again
- THEN codex-switch replaces the existing managed block
- AND it does not duplicate the block.

#### Scenario: Shell bootstrap can be skipped explicitly

- GIVEN the environment variable `CODEX_SWITCH_SKIP_SHELL_BOOTSTRAP` is truthy
- WHEN the user switches profiles
- THEN codex-switch updates the profile shim and App binding as requested
- AND does not create or mutate a shell startup file.
