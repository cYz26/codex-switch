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
