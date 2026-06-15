# Specification Delta: codex-switch

## ADDED Requirements

### Requirement: Independent official and internal homes

The system SHALL activate `official` using the official Codex home and activate
`internal` using a managed independent Codex home.

#### Scenario: Internal activation uses managed home

- GIVEN the official Codex home contains shared configuration and runtime state
- WHEN the user switches to `internal`
- THEN the shell shim exports the managed internal `CODEX_HOME`
- AND Codex Desktop uses a managed internal app wrapper
- AND the official Codex home auth and runtime state are not copied into the
  internal home.

#### Scenario: Official activation uses official home

- GIVEN the internal home contains shared configuration changes
- WHEN the user switches to `official`
- THEN shareable internal state is synced back to the official Codex home
- AND the shell shim and Codex Desktop binding use official paths
- AND internal auth, runtime state, model/provider profile layers, and session
  data are not copied to the official home.

#### Scenario: Bulky support and credential state is excluded from sync plans

- GIVEN a source home contains plugin caches, AgentKB data, computer-use state,
  cache directories, sqlite directories, credential files, model catalogs, or
  version/installation state
- WHEN a switch dry-run or real switch builds the shared support plan
- THEN those paths are not included in the backup plan
- AND those paths are not copied, linked, or otherwise synced into the target
  profile home.

#### Scenario: Shared support symlinks do not self-reference target homes

- GIVEN a shareable support entry in the source home is a symlink that points to
  the target path that would be written during sync
- WHEN a switch syncs shared support into the target home
- THEN the system does not create or preserve a symlink that points to itself
- AND an existing concrete target path is left intact
- AND an existing self-referential target symlink is removed when no safe
  concrete source content can be copied.

#### Scenario: Shared support symlinks pointing into the target home are not copied back

- GIVEN a shareable support entry in the source home is a symlink that points
  inside the target home
- WHEN a switch syncs shared support into the target home
- THEN the system does not copy that symlink into the target home
- AND no symlink loop is created.

#### Scenario: Existing self-referential source symlinks are not propagated

- GIVEN a shareable support entry in the source home is already a
  self-referential symlink
- WHEN a switch syncs shared support into the target home
- THEN the system does not copy that symlink into the target home
- AND an existing target self-referential symlink for that entry is removed.

### Requirement: Backup gate before mutations

The system SHALL create a restorable backup before any non-dry-run profile
activation mutates Codex homes, shell shim, LaunchAgent, or active state.

#### Scenario: Backup succeeds before mutation

- GIVEN switching to a target profile will write, delete, replace, link, or
  unlink paths
- WHEN the user runs a non-dry-run switch
- THEN the system creates a backup directory under the store backups directory
- AND `backup.json` records the operation, source profile, target profile,
  affected paths, path type, symlink target, sha256 when applicable, file mode,
  mtime, and tool version
- AND writes only proceed after all backup entries are recorded successfully.

#### Scenario: Backup failure aborts switch

- GIVEN at least one planned backup entry cannot be captured
- WHEN the user runs a non-dry-run switch
- THEN the switch fails before any planned mutation is applied
- AND the official home, internal home, shell shim, LaunchAgent, and active
  record remain unchanged.

#### Scenario: Dry-run shows backup and mutation plans

- GIVEN a switch is run with `--dry-run`
- WHEN the plan is printed
- THEN it includes the paths that would be backed up
- AND it includes the paths that would be mutated
- AND no files are written.

### Requirement: Runtime config merge with canonical fallback

The system SHALL build the target home `config.toml` from shared settings plus
the target profile's last valid runtime profile settings, using the canonical
profile config only as fallback.

#### Scenario: Target runtime profile settings are preferred

- GIVEN the target profile has a valid runtime `config.toml`
- AND its canonical profile config contains older profile-specific settings
- WHEN the user switches to that target profile
- THEN the generated runtime config preserves profile-specific settings from
  the target runtime config
- AND shared settings are merged from the source home
- AND the canonical profile config is refreshed from the validated generated
  runtime config without copying shared settings into the canonical profile
  config.

#### Scenario: Removed profile settings are not resurrected

- GIVEN the target profile runtime `config.toml` no longer contains an optional
  profile-specific setting such as `personality` or `model_provider`
- AND the canonical profile config still contains an older value for that
  setting
- WHEN the canonical profile config is refreshed from the runtime config
- THEN the older optional setting is not copied back into the canonical profile
  config
- AND structural auth settings may still be preserved from the canonical
  fallback when absent from runtime config.

#### Scenario: Canonical profile config is used as fallback

- GIVEN the target profile runtime `config.toml` is missing or invalid
- AND the canonical profile config is valid
- WHEN the user switches to that target profile
- THEN the generated runtime config uses profile-specific settings from the
  canonical profile config
- AND shared settings are still merged from the source home.

#### Scenario: Unsupported runtime reasoning effort uses canonical fallback

- GIVEN the target profile runtime `config.toml` is valid TOML
- AND it sets `model_reasoning_effort` to a value unsupported by the configured
  model catalog for the selected model
- AND the canonical profile config has a supported `model_reasoning_effort`
- WHEN the user switches to that target profile
- THEN the generated runtime config uses the supported canonical profile
  reasoning effort
- AND the unsupported runtime value is not written back to the canonical
  profile config.

#### Scenario: Internal Desktop model alias keeps supported reasoning efforts

- GIVEN an internal profile uses a versioned deployment model such as
  `gpt-5.5-2026-04-24`
- AND the configured model catalog supports `low`, `medium`, `high`, and
  `xhigh` reasoning efforts for that deployment
- WHEN Codex Desktop talks to the managed internal app CLI through
  `app-server --stdio`
- THEN the managed app wrapper exposes a Desktop-compatible model alias such
  as `gpt-5.5` with only the catalog-supported reasoning efforts
- AND backend thread or conversation payloads exposed to Desktop use the same
  Desktop-compatible model alias
- AND requests or config writes that select the Desktop alias are translated
  back to the versioned deployment model before reaching the backend
- AND the managed profile and runtime config files continue to store the
  versioned deployment model.

#### Scenario: Runtime config includes managed section comments

- GIVEN a switch generates a target runtime `config.toml`
- WHEN the file is written
- THEN it remains valid TOML
- AND it includes managed comments identifying shared settings
- AND it includes managed comments identifying profile-specific settings.

#### Scenario: Internal Desktop wrapper preserves official profile settings

- GIVEN the official home runtime `config.toml` contains profile-specific
  settings such as `model` or `personality`
- AND the internal Desktop wrapper has an internal app home config with shared
  settings to fold back
- WHEN the internal Desktop wrapper starts Codex
- THEN shared settings from the internal app home are folded into the official
  home
- AND official profile-specific settings remain in the official home.

### Requirement: Profile home selection and adoption

The system SHALL support explicit and interactive Codex home selection for
independent profiles while preventing `internal` and `openai-official` from
sharing the same home.

#### Scenario: Internal adopts existing Codex home

- GIVEN the existing official Codex home has long-lived internal runtime state
- WHEN the user switches to `internal` with that path selected as the internal
  Codex home
- THEN `internal` uses the selected existing home
- AND `openai-official` is assigned a distinct managed home when it would
  otherwise collide
- AND both profile home bindings are persisted in their profile manifests
- AND historical runtime state remains in the adopted internal home.

#### Scenario: Identical explicit homes are corrected interactively

- GIVEN the user explicitly assigns the same path to `internal` and
  `openai-official`
- AND the switch runs in an interactive terminal
- WHEN a switch is planned or applied
- THEN the system prompts the user to choose a different home for one profile
- AND the switch continues only after the selected homes are distinct.

#### Scenario: Identical non-interactive homes are rejected

- GIVEN the user explicitly assigns the same path to `internal` and
  `openai-official`
- AND no interactive prompt is available
- WHEN a switch is planned or applied
- THEN the switch fails before mutation
- AND the error explains that independent profiles cannot share one Codex home.

#### Scenario: Interactive selection offers defaults and custom path

- GIVEN a profile has no persisted Codex home binding
- AND no home path was specified on the command line
- WHEN the user switches in an interactive terminal
- THEN the system offers at least the existing `~/.codex` path, the managed
  `~/.codex-switch/homes/<profile>` path, and a custom path choice
- AND it prompts for the target profile before the other independent profile
- AND `openai-official` recommends the official home, defaulting to `~/.codex`
- AND `internal` recommends the managed internal home, defaulting to
  `~/.codex-switch/homes/internal`
- AND the recommended path is listed first and marked as recommended
- AND it refuses a selection that would make both independent profiles use the
  same home.

#### Scenario: Persisted home bindings require user confirmation

- GIVEN a profile manifest contains a persisted Codex home binding
- AND the binding has not been confirmed by an explicit option or prior prompt
- WHEN the user switches in an interactive terminal
- THEN the system prompts the user to confirm or change that profile's Codex
  home
- AND the selected binding is persisted with a confirmation marker.

#### Scenario: Target profile cannot reuse the active profile home

- GIVEN the current active profile records a Codex home
- AND the user switches to a different target profile
- WHEN the target profile resolves to the same Codex home as the active profile
- THEN an interactive switch prompts for a different target-profile home
- AND a non-interactive real switch fails before mutation
- AND dry-run remains read-only and does not prompt.

### Requirement: Restore from switch backup

The system SHALL restore previously backed up switch state through an explicit
restore command.

#### Scenario: Restore dry-run is read-only

- GIVEN a backup exists
- WHEN the user runs `codex-switch restore <backup-id> --dry-run`
- THEN the system prints the paths that would be restored
- AND no target file is changed.

#### Scenario: Restore apply restores original state

- GIVEN a backup exists from a completed switch
- WHEN the user runs `codex-switch restore <backup-id> --apply`
- THEN regular files, directories, missing-path markers, symlinks, permissions,
  the shell shim, LaunchAgent, and active record are restored according to the
  backup manifest.

#### Scenario: Restore refuses unrelated current changes

- GIVEN a backup records the post-switch state of a path
- AND the current path no longer matches that post-switch state
- WHEN the user runs restore without `--force`
- THEN the restore fails before overwriting that path.
