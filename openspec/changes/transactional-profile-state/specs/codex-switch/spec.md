## ADDED Requirements

### Requirement: Transactional profile mutation
The system SHALL build and validate one immutable mutation plan for every supported official/internal profile switch before changing any destination, and SHALL either commit the entire plan or restore the complete pre-operation state.

#### Scenario: Snapshot mode preserves independent homes
- **WHEN** the user switches `internal` with snapshot config mode
- **THEN** the snapshot is applied inside the internal profile home
- **AND** the official live home config and auth are not used as the internal destination.

#### Scenario: Dry-run rejects an invalid required binding
- **WHEN** a target profile has a missing, relative, nonexistent, directory, or non-executable required binding
- **THEN** dry-run fails during plan construction
- **AND** no backup or destination mutation occurs.

#### Scenario: Late Desktop binding failure rolls back the switch
- **WHEN** an injected Desktop binding or launchctl step fails after earlier mutations have applied
- **THEN** all applied profile, home, config, auth, shim, plist, environment, and active-record changes are restored
- **AND** the operation returns failure with rollback evidence.

### Requirement: Profile-local runtime state isolation
The system SHALL exclude known profile-local runtime state from shared-support and backup planning before recursive filesystem capture, and SHALL NOT weaken fail-closed handling for unknown special filesystem objects.

#### Scenario: Official dry-run ignores known runtime socket directories
- **WHEN** the internal source home and existing official target home contain live Unix sockets beneath `ipc` and `mcp-oauth-locks` and the user dry-runs a shared switch to official
- **THEN** planning succeeds without recursively capturing, sharing, backing up, copying, or mutating either runtime directory
- **AND** the dry-run creates no backup or destination mutation.

#### Scenario: Unknown special object still fails closed
- **WHEN** a shared-support candidate outside the known runtime exclusions contains an unsupported socket, FIFO, device, or other special filesystem object
- **THEN** transaction planning fails before backup publication or mutation
- **AND** the object is not silently skipped or copied.

### Requirement: Versioned switch backup and restore
The system SHALL use one explicit backup schema for every supported switch path and SHALL preflight the complete restore before removing or replacing any current target.

#### Scenario: Every switch backup is restorable by the current schema
- **WHEN** shared or snapshot switching creates a backup
- **THEN** the manifest records a supported schema version and ordered entries
- **AND** restore consumes that same representation.

#### Scenario: Legacy manifest is rejected explicitly
- **WHEN** restore receives a legacy manifest containing only the unsupported `files` representation
- **THEN** restore fails before mutation with compatibility and manual-recovery guidance
- **AND** it does not report success.

#### Scenario: V1 compatibility is evidence-bounded
- **WHEN** restore receives an unversioned `entries` manifest
- **THEN** sufficiently attested file, symlink, and missing entries may use the v1 adapter
- **AND** any directory entry without recursive attestation is rejected even when `--force` is supplied.

#### Scenario: Missing or corrupt payload causes zero mutations
- **WHEN** any recorded backup payload is missing, escapes the backup directory, or fails its recorded digest
- **THEN** restore fails during preflight
- **AND** every current target remains byte-for-byte and mode-for-mode unchanged.

#### Scenario: Recursive directory conflict blocks non-force restore
- **WHEN** a file, symlink, mode, or descendant entry inside a post-switch directory differs from the committed after-state
- **THEN** restore without `--force` refuses the entire plan before mutation
- **AND** restore with explicit `--force` may apply the validated backup.

#### Scenario: Restore creates a rollback backup
- **WHEN** a validated historical restore is applied
- **THEN** the current state is first captured in a new schema-v2 safety backup
- **AND** any failure rolls back through that backup while a successful restore remains reversible.

### Requirement: Atomic managed profile capture
The system SHALL validate and stage the complete managed profile file set before replacing an existing profile.

#### Scenario: Required auth failure preserves the previous profile
- **WHEN** overwrite capture has valid config but required source auth is missing
- **THEN** capture fails
- **AND** the previous config, auth, and manifest remain unchanged.

#### Scenario: Allowed missing auth clears stale credentials
- **WHEN** overwrite capture allows missing auth and the source has no `auth.json`
- **THEN** the replacement profile contains the validated config and manifest
- **AND** any prior destination `auth.json` is absent
- **AND** non-managed profile artifacts remain preserved.

#### Scenario: Invalid TOML preserves the previous profile
- **WHEN** the staged capture config is invalid TOML
- **THEN** capture fails before replacing the profile directory
- **AND** no partial managed-file update remains.

### Requirement: Serialized profile store mutation
The system SHALL serialize switch, capture, and restore operations with one store-scoped interprocess lock held from the initial canonical read through backup finalization.

#### Scenario: Concurrent mutation receives busy result
- **WHEN** one process holds the store mutation lock and a second process attempts a switch, capture, or restore
- **THEN** the second process fails with a precise busy result
- **AND** it creates no backup and changes no destination.

#### Scenario: Malformed active record fails closed
- **WHEN** an existing `active.json` cannot be parsed or does not satisfy its required object schema
- **THEN** transaction planning fails before mutation
- **AND** active-home collision protection is not bypassed.

### Requirement: Bound pending-transaction evidence
The system SHALL publish bound and durable pending evidence for every newly armed supported switch or restore, SHALL classify all unresolved evidence under the store lock before any mutation dispatch, and SHALL retire a marker only after validating a complete authoritative terminal result.

#### Scenario: Prepared evidence is durable before mutation intent
- **WHEN** a supported switch or restore reaches its first destination or Desktop effect
- **THEN** its backup payload tree, prepared journal, backups parent, and store-root marker are already durable
- **AND** the marker and journal bind the same operation, backup ID, transaction ID, marker name, and prepared-journal digest.

#### Scenario: Every mutation route uses one recovery gate
- **WHEN** switch, capture, restore, `init --capture-current`, or the preserved custom route begins
- **THEN** marker-bearing transactions, markerless legacy switches, marker-required missing-marker journals, pre-marker restores, and capture journals are classified before the first write
- **AND** corrupt, ambiguous, rollback-failed, or multiple unresolved evidence blocks the operation without changing store bytes.

#### Scenario: Missing marker is interpreted by journal provenance
- **WHEN** a marker-required journal has no marker
- **THEN** an effect-free journal may be closed as never started
- **AND** any begun switch or restore remains blocked rather than being recovered as a markerless legacy transaction.

#### Scenario: Legacy markerless evidence remains bounded
- **WHEN** a structurally valid legacy prepared switch has no marker
- **THEN** it may use the legacy recovery adapter before any new mutation
- **AND** a pre-marker restore in `prepared` or `rollback_failed` state blocks every mutation because it has no safe legacy recovery contract.

#### Scenario: Verified independent rollback evidence survives manifest corruption
- **WHEN** rollback was completely verified, the marker remains, and `backup.json` later becomes unreadable
- **THEN** only a `failure.json` whose operation, IDs, marker name, and prepared-journal digest match the trusted marker may prove `rolled_back`
- **AND** every incomplete, mismatched, unknown, or rollback-failed record remains blocked.

#### Scenario: Terminal marker cleanup is retryable and visible
- **WHEN** a committed, rolled-back, or recovered terminal manifest is durable but marker unlink or parent sync fails
- **THEN** the terminal outcome is not reversed and outcome-specific retained-marker guidance reaches the caller
- **AND** the next applying route, including the custom route, validates and retires the terminal marker before its first write.

### Requirement: Immutable identity-bound mutation plan
The system SHALL freeze each planning input at the read that produces dependent payloads and SHALL bind every filesystem effect to an expected predecessor, approved directory route, staged artifact, and produced object identity.

#### Scenario: Read-to-freeze changes cannot be adopted
- **WHEN** a manifest, active record, config, auth file, plugin snapshot, shell input, Desktop global state, shared-support entry set, stale-link source, wrapper, binding, or composite-builder input changes after its planning read
- **THEN** the transaction rejects the stale plan before the first dependent action
- **AND** it does not overwrite the newer source or target state.

#### Scenario: No-op Desktop global-state merge does not claim ownership
- **GIVEN** the Desktop global-state source settings merge is byte-identical to
  the target
- **WHEN** the running Desktop App updates the target while later switch effects
  execute
- **THEN** the switch preserves the App-owned update and does not fail or roll
  back because of that path
- **AND** the target is absent from the mutation journal, backup set, rollback
  set, and retained frozen inputs
- **AND** a merge that would change bytes remains a staged, identity-bound,
  fail-closed transaction effect.

#### Scenario: Exact legacy no-op rollback evidence is safely recoverable
- **GIVEN** a marker-bound pre-fix switch is `rollback_failed` only because its
  final Desktop global-state effect claimed a byte-identical target
- **WHEN** the effect has no staged artifact and its before, planned, observed,
  frozen commit, and produced identity evidence all prove no mutation
- **AND** any preceding filesystem effect has a valid route and manifest entry
  whose before, planned, and observed states strictly prove a byte-identical
  no-op
- **THEN** recovery preserves later externally owned state at every proven
  no-op path, rolls back every remaining attested real change, records the
  released ownership, and retires the marker
- **AND** a real planned change or any trigger, route, entry, state, identity,
  ordering, profile, or failure-evidence mismatch remains under the normal
  fail-closed recovery contract.

#### Scenario: Replacement installs the recorded staged artifact
- **WHEN** a replacement effect is applied
- **THEN** the exact pre-journaled staged object is installed through the already-validated parent descriptor
- **AND** the applied checkpoint verifies its produced device/inode identity as well as content state.

#### Scenario: Identity change before applied checkpoint is not accepted
- **WHEN** the live result is replaced by a byte-identical but differently identified object before the applied checkpoint
- **THEN** the transaction retains recovery evidence and does not record that effect as applied.

#### Scenario: Repeated effects on one destination form a chain
- **WHEN** two planned effects target the same canonical destination
- **THEN** the second expected predecessor equals the first planned terminal state
- **AND** recovery validates each persisted intermediate identity without comparing all historical identities to the final live object.

#### Scenario: Directory effects use the same identity contract
- **WHEN** a transaction creates, changes, or removes a directory or nested home chain
- **THEN** intent, predecessor identity, route, planned state, observed identity, and durability are journaled
- **AND** later unrelated replacement or non-empty state is preserved rather than deleted.

#### Scenario: Attested lexical symlink ancestor remains compatible
- **WHEN** an approved historical path has a lexical symlink ancestor whose identity and target remain unchanged
- **THEN** descriptor-relative planning and apply may continue through the attested route
- **AND** any changed identity or target is rejected before mutation.

### Requirement: Complete durable recovery
The system SHALL validate the entire switch or restore recovery plan before its first recovery write and SHALL make each recovery effect durable before publishing terminal evidence.

#### Scenario: Later invalid recovery evidence causes zero earlier writes
- **WHEN** any later payload, allowlist destination, route identity, staged identity, produced identity, directory ensure state, Desktop state, or active state is invalid
- **THEN** recovery fails during read-only simulation
- **AND** no earlier target has been materialized, removed, or reconciled.

#### Scenario: Switch rollback is durable before terminal publication
- **WHEN** switch apply fails or an interrupted switch is recovered
- **THEN** every reversed file, tree, link, removal, chmod, Desktop, active, and directory effect reaches its durability boundary
- **AND** only then are lifecycle and switch-journal terminal states atomically published and the marker retired.

#### Scenario: Restore parent cleanup is recoverable
- **WHEN** restore removes a transaction-created original parent directory
- **THEN** cleanup intent, identity, planned missing state, observed result, and parent sync are journaled before later effects
- **AND** catchable failure or a second interruption recreates the exact prior directory and mode idempotently.

#### Scenario: Desktop already restored is idempotent
- **WHEN** an earlier recovery reconciled Desktop state but stopped before terminal publication
- **THEN** the next recovery recognizes the persisted complete `desktop_before` state
- **AND** it completes without replaying an incompatible reverse effect.

#### Scenario: Terminal reread requires complete marker-bound evidence
- **WHEN** a terminal-manifest adapter raises after writing data
- **THEN** the transaction accepts an on-disk commit only if the full schema, entries, payloads, authority, IDs, digest, effect chain, and terminal states validate against the retained marker
- **AND** an incomplete or unbound committed object does not cause marker cleanup or a committed receipt.

### Requirement: Lock-owned init capture and custom compatibility
The system SHALL keep initial managed-file writes and capture under the same store lock and recovery gate, while preserving the custom route only as a locked compatibility path that never arms supported transaction evidence.

#### Scenario: Busy or pending init capture is byte-identical
- **WHEN** `init --capture-current` encounters a held lock or unresolved transaction evidence
- **THEN** no official manifest, config, capture directory, backup, marker, shim, or active state is created or changed
- **AND** the command returns the same precise busy or pending guidance as the transaction layer.

#### Scenario: Successful init capture avoids nested locking
- **WHEN** `init --capture-current` proceeds
- **THEN** one outer lock owns classification, init writes, and an already-locked capture dispatch
- **AND** successful output remains capture receipt followed by the existing init and shim lines.

#### Scenario: Custom apply shares the gate without claiming the protocol
- **WHEN** the preserved custom route applies
- **THEN** it holds the common store lock, blocks unresolved supported or capture evidence, and retires valid terminal markers before its first write
- **AND** it never creates a supported transaction marker or journal.

### Requirement: Strict restore metadata and authority
The system SHALL validate every recorded state field and manifest-bound restore root before creating a safety backup, and `--force` SHALL NOT bypass metadata, payload, path, identity, or authority validation.

#### Scenario: Empty and malformed state metadata is rejected uniformly
- **WHEN** a v1 or v2 manifest has no entries, an inconsistent directory entry count, or any file/directory/symlink/missing state mode that is boolean, negative, or above `0o7777`
- **THEN** restore fails before creating a safety backup even with `--force`
- **AND** valid special permission bits through `0o7777` remain supported.

#### Scenario: Both supported adopted homes are evidence-bounded
- **WHEN** an official or internal manifest binds an adopted home
- **THEN** the home is allowed only when absolute, canonical, and outside the backup tree
- **AND** a valid switch backup is immediately restorable while preserving an existing home mode.
