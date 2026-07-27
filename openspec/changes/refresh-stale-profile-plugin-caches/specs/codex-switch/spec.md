## ADDED Requirements

### Requirement: Deterministic target-profile plugin cache refresh

The system SHALL run plugin catalog and cache maintenance against the selected
profile runtime and SHALL reinstall an enabled plugin only when it is missing
and available or when an inspectable local source proves its installed cache is
stale.

#### Scenario: Repair uses the canonical target runtime

- **WHEN** the user runs `codex-switch repair-plugins <profile>` for a supported
  product profile
- **THEN** codex-switch resolves the profile's canonical backend CLI and
  profile `CODEX_HOME`
- **AND** it verifies that CLI through `--version`
- **AND** every marketplace, catalog, and plugin-add command uses that same CLI
  and explicit `CODEX_HOME`, without depending on a ChatGPT restart.

#### Scenario: Stale same-version local cache is refreshed

- **WHEN** an enabled installed plugin appears in the refreshed catalog with an
  inspectable local source and safe version
- **AND** the source tree differs from the cache tree for that catalog version
- **THEN** codex-switch reports the cache as stale
- **AND** invokes `codex plugin add <selector>` exactly once for that selector.

#### Scenario: Current local cache is a no-op

- **WHEN** an enabled installed plugin's inspectable source tree matches the
  cache tree for the catalog version
- **THEN** codex-switch does not invoke `codex plugin add` for that selector.

#### Scenario: Runtime residue does not create false drift

- **WHEN** source and cache payloads are equal but differ only by `.git`,
  `__pycache__`, Python bytecode, `.DS_Store`, or standard tool-cache residue
- **THEN** codex-switch treats the installed cache as current.

#### Scenario: Missing available plugin compatibility is preserved

- **WHEN** an enabled plugin has no installed cache and appears in the refreshed
  available catalog
- **THEN** codex-switch invokes `codex plugin add <selector>` once.

#### Scenario: Unavailable enabled plugin compatibility is preserved

- **WHEN** an enabled plugin has no installed cache and does not appear in the
  refreshed available catalog
- **THEN** codex-switch does not invoke `codex plugin add`
- **AND** preserves the existing skip or explicit
  `--disable-unavailable` behavior.

#### Scenario: Uninspectable source is skipped truthfully

- **WHEN** an enabled installed plugin has no safe catalog version or no
  absolute existing local source with matching plugin manifest
- **THEN** codex-switch skips stale-cache comparison and reinstall for that
  selector
- **AND** reports that the source is uninspectable.

#### Scenario: Dry-run does not claim stale refresh

- **WHEN** the user runs `codex-switch repair-plugins <profile> --dry-run`
- **THEN** codex-switch prints the runtime, marketplace, catalog, and
  conditional comparison actions that would run
- **AND** does not print a concrete `codex plugin add` command for missing or
  stale selectors that have not been verified against a real refreshed
  catalog.

#### Scenario: Running target app-server blocks stale replacement

- **WHEN** an inspectable enabled cache is stale
- **AND** a running app-server matches the target profile's canonical
  Desktop/backend chain
- **THEN** codex-switch does not invoke `codex plugin add` for the stale
  selector
- **AND** fails the repair step with instructions to quit ChatGPT, rerun plugin
  repair, and reopen the App.

#### Scenario: One-key switch refreshes before diagnostics

- **WHEN** a one-key `codex-switch internal` or `codex-switch official` command
  completes its profile switch without `--skip-plugin-repair`
- **THEN** codex-switch performs deterministic target-profile plugin repair
  before target verification and Doctor.

#### Scenario: Global cache refresh does not migrate projects

- **WHEN** plugin repair refreshes a target profile cache
- **THEN** codex-switch does not rewrite project-local DevFlow/OpenSpec
  configuration, generated guidance, or skill links.
