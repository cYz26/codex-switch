## ADDED Requirements

### Requirement: Independent CLI and Desktop profile selection

The system SHALL allow the managed shell CLI and ChatGPT Desktop to use
different product profiles without treating the resulting state as drift.

#### Scenario: Internal CLI with official Desktop

- **WHEN** the user switches the CLI profile to `internal` with the App profile
  explicitly set to `official`
- **THEN** the shell shim executes the internal profile's configured binary
  with the internal profile home
- **AND** ChatGPT Desktop is bound to the verified official bundled binary with
  the official profile home
- **AND** the persisted active state identifies `internal` as the CLI profile
  and `openai-official` as the App profile.

#### Scenario: Existing synchronized switches remain unchanged

- **WHEN** the user switches to `internal` or `official` without an explicit
  App-profile override
- **THEN** the CLI and App profiles both select the requested profile
- **AND** existing one-key command behavior remains compatible.

#### Scenario: Unsupported split is rejected

- **WHEN** a user requests a split other than internal CLI with official App
- **THEN** the command fails before mutating profile homes, the shell shim,
  Desktop binding, or active state
- **AND** the error identifies the supported split.

#### Scenario: Explicit App selection cannot be skipped

- **WHEN** a user combines an App-profile override with an option that skips
  Desktop binding
- **THEN** the command rejects the contradictory request before mutation.

#### Scenario: Dry run reports both targets

- **WHEN** the user previews internal CLI with official App
- **THEN** the plan identifies the separate CLI and App profiles, homes, and
  binary bindings
- **AND** no profile, shell, Desktop, process, or active-state mutation occurs.

### Requirement: Compatible active selection state

The system SHALL persist independent profile identities additively and SHALL
remain compatible with valid active records written by earlier releases.

#### Scenario: New split state is explicit

- **WHEN** a split-profile switch commits
- **THEN** the active record contains explicit `cli_profile` and `app_profile`
  identities
- **AND** the legacy `profile` field remains equal to the CLI profile.

#### Scenario: Legacy state resolves as synchronized

- **WHEN** a valid earlier active record contains `profile` but no independent
  profile fields
- **THEN** readers treat both CLI and App as that legacy profile
- **AND** status, Doctor, and verify do not require an immediate migration.

#### Scenario: Partial or contradictory state fails closed

- **WHEN** an active record contains only one independent profile field or its
  legacy `profile` conflicts with `cli_profile`
- **THEN** status exposes the invalid state
- **AND** Doctor and verify report a stable error rather than guessing a
  profile identity.

### Requirement: Atomic split-profile switching

The system SHALL apply independent CLI and Desktop targets within the existing
recoverable switch transaction.

#### Scenario: Complete split switch commits together

- **WHEN** validation of the internal CLI target and official App target passes
- **THEN** profile-home preparation, shell shim, Desktop binding, and the active
  selection commit as one recoverable operation
- **AND** the active record is written only after all earlier effects succeed.

#### Scenario: Desktop binding failure rolls back the split switch

- **WHEN** the official Desktop binding fails after an internal shell shim has
  been staged or written
- **THEN** the transaction restores the prior shim, Desktop binding, profile
  state, and active record
- **AND** no split state is reported as committed.

#### Scenario: Target drift aborts before commit

- **WHEN** either selected manifest, binary, home, or Desktop binding input
  changes after planning
- **THEN** the transaction fails closed or rolls back according to the existing
  journal contract
- **AND** it does not silently substitute the other profile's target.

### Requirement: Split-aware diagnostics and verification

The system SHALL diagnose and verify each active surface against its selected
profile.

#### Scenario: Status reports separate ownership

- **WHEN** internal CLI with official App is active
- **THEN** status reports the CLI profile, CLI home, configured internal binary,
  shim resolution, App profile, official bundled binary, LaunchAgent binding,
  and running App/app-server paths separately.

#### Scenario: Doctor accepts a healthy split

- **WHEN** the shell shim resolves the selected internal CLI/home and Desktop
  resolves the selected official bundle/home
- **THEN** Doctor treats the split as healthy
- **AND** it does not require the internal managed Desktop launcher to be the
  live App binding.

#### Scenario: Doctor detects per-surface drift

- **WHEN** either the shell shim drifts from the internal selection or Desktop
  drifts from the official selection
- **THEN** Doctor identifies the affected surface and expected profile/path
- **AND** drift on one surface does not rewrite the other surface.

#### Scenario: Verification uses the selected execution surfaces

- **WHEN** verification runs for an active internal-CLI/official-App selection
- **THEN** CLI/runtime/exec checks use the internal binary and internal home
- **AND** App-server checks and live Desktop attestation use the official
  bundled binary and official home
- **AND** parity checks for the internal shell generation remain read-only and
  independent of the live official App binding.

### Requirement: Split-aware one-key workflow and distribution

The one-key wrapper and packaged release SHALL preserve the independent
selection contract.

#### Scenario: Wrapper routes preparation to the CLI profile

- **WHEN** `codex-switch internal --app-profile official` runs
- **THEN** internal update checks and internal profile/plugin preparation target
  the CLI profile
- **AND** post-switch verification and result output retain the official App
  selection.

#### Scenario: Concise split preset preserves normal update behavior

- **WHEN** the user runs `codex-switch split`
- **THEN** the wrapper selects the same internal CLI and official App pairing
  as `codex-switch internal --app-profile official`
- **AND** codex-switch self-update plus internal update detection and promotion
  retain their existing behavior
- **AND** switch, Plugin repair, verify, Doctor, status, and result reporting
  retain the existing one-key workflow.

#### Scenario: Concise split preset cannot be retargeted

- **WHEN** the user supplies `--app-profile` to `codex-switch split`
- **THEN** the wrapper rejects the override before self-update, planning, or
  mutation
- **AND** directs the user to the explicit profile command for another target.

#### Scenario: Keep-version split freezes both update layers

- **WHEN** the user runs `codex-switch split --keep-version`
- **THEN** the wrapper performs neither codex-switch self-update nor internal
  update detection or promotion
- **AND** it still plans and applies the supported split and runs Plugin repair,
  verify, Doctor, status, and result reporting normally
- **AND** `--keep-version` is rejected for commands other than `split`.

#### Scenario: Concise split preview is side-effect free

- **WHEN** the user runs `codex-switch split --dry-run` or
  `codex-switch split --keep-version --dry-run`
- **THEN** the wrapper previews the internal CLI and official App targets
- **AND** no profile, shell, Desktop, process, Plugin, verification, Doctor, or
  active-state mutation occurs.

#### Scenario: Packaged command retains split support

- **WHEN** a release bundle is built from a source tree containing this change
- **THEN** every required independent-selection module and updated operator
  instruction is present
- **AND** the packaged wrapper can parse and preview both the explicit and
  concise split commands without importing files from the source checkout.

#### Scenario: Promotion preserves the immediately prior release generation

- **WHEN** installation promotes a package containing this change over
  `current` and `rollback` releases written by the immediately prior manifest
  generation
- **THEN** promotion accepts only the exact enumerated historical required-path
  set for that generation and preserves the prior release bytes as rollback
- **AND** an unknown, reordered, partial, or extended required-path set still
  fails closed before changing `current` or `rollback`.

#### Scenario: Failed release upload residue is recovered exactly

- **WHEN** a required release asset is absent from the uploaded asset set but
  the explicit GitHub release-asset inventory contains one same-name,
  zero-byte asset in `starter` state
- **THEN** reconciliation rechecks the remote tag identity, deletes only that
  exact asset ID, and reads the release inventory back before upload
- **AND** if that readback reports the Release missing, reconciliation
  rechecks tag identity, creates one draft Release for the verified tag, and
  requires an existing, empty, draft readback before upload
- **AND** when multiple canonical starter records exist, each deletion is
  followed by readback and no remaining asset ID from a vanished Release is
  reused
- **AND** it uploads and hashes the canonical asset without `--clobber`
- **AND** uploaded, non-zero, duplicate-name, or unknown-state assets are not
  deleted or overwritten and instead fail closed when they conflict
- **AND** failed creation, missing or non-draft recreated state, non-empty
  recreated state, or tag movement fails closed before later mutation.

### Requirement: Canonical shared Plugin and Skill desired state

For the supported internal-CLI/official-App split, the system SHALL own one
secret-safe, generationed desired-state projection for Plugin selectors,
non-secret marketplace descriptors, and standalone Skill configuration while
keeping each runtime config and cache independently owned.

#### Scenario: Official App bootstraps the first desired generation

- **WHEN** the supported split has no existing shared-capability state
- **THEN** the official App projection is the explicit bootstrap authority
- **AND** the first generation contains no model, provider, auth, credential,
  MCP/App connector, session, history, permission, process, or cache data
- **AND** bootstrap does not share either physical plugin cache.

#### Scenario: Single-side and identical changes advance safely

- **WHEN** one side changes from its last-applied baseline, or both sides make
  the same semantic change
- **THEN** one new desired generation records that complete projection
- **AND** authoritative disable and removal are not revived from an older
  snapshot.

#### Scenario: Divergent changes fail closed

- **WHEN** official and internal projections diverge from the same baseline in
  different ways
- **THEN** reconcile reports a stable conflict
- **AND** canonical state, both configs, both caches, and both receipts remain
  unchanged.

#### Scenario: Unstable source observation fails closed

- **WHEN** either source config or source artifact changes during planning
- **THEN** reconcile retries only within its bounded stable-read contract or
  reports `source_changed_during_plan`
- **AND** it does not commit a mixed generation.

### Requirement: App changes are ready before functional internal CLI execution

The managed internal shell SHALL reconcile and independently materialize the
current shared generation after Runtime Binding validation and before a
functional backend command executes.

#### Scenario: App adds or enables a Plugin

- **WHEN** the official App adds or enables a Plugin or contributed Skill
- **AND** the user starts the next functional managed internal CLI invocation
- **THEN** internal config receives the desired selector before backend launch
- **AND** the internal backend materializes a compatible artifact inside the
  internal cache rather than linking or using the official cache
- **AND** the contributed Skill is discoverable from that internal artifact.

#### Scenario: App updates a Plugin without changing its selector

- **WHEN** the official artifact identity changes while its selector remains
  enabled
- **THEN** the next functional internal invocation detects the source identity
  change rather than accepting any old installed version
- **AND** `portable_exact` artifacts match source/version/tree identity while
  `backend_managed` artifacts record the target backend's compatible identity.

#### Scenario: Older installed version does not override an exact portable source

- **WHEN** the target backend reports a selector at an older installed version
- **AND** its safely resolved marketplace source manifest and tree exactly
  match the newer desired `portable_exact` identity
- **THEN** preflight treats the reported version as target state rather than
  source-version authority
- **AND** the target backend may update the selector, after which the new
  independent target artifact must exactly attest before backend execution
- **AND** the stale artifact is never selected as source authority or directly
  copied, linked, deleted, or recreated by `codex-switch`; whether it remains
  after native update is owned by the target backend.

#### Scenario: Portable source mismatch is distinct from unsafe cache

- **WHEN** a safely contained marketplace source does not match the desired
  `portable_exact` manifest version or tree identity
- **THEN** preflight blocks with a stable source-mismatch finding rather than
  reporting cache corruption
- **AND** `unsafe_cache` remains reserved for unsafe paths, links, file kinds,
  cache identities, or traversal.

#### Scenario: Backend-managed source and target versions are independent

- **WHEN** the target catalog reports an installed `backend_managed` selector
  at an older internal version
- **AND** that record resolves the exact current desired marketplace source
  manifest and tree
- **THEN** preflight treats the reported version only as internal target state
  rather than source-version authority
- **AND** a changed generation reconciles the selector through the internal
  backend even when an older target cache is inspectable
- **AND** `codex-switch` neither copies nor links the current official source
  artifact and never directly deletes an internal target artifact.

#### Scenario: Backend-managed reconcile requires fresh target proof

- **WHEN** native target-backend add or update returns success for one or more
  `backend_managed` selectors
- **THEN** preflight obtains one fresh target catalog after those operations
- **AND** each selector must be uniquely reported installed with a safe target
  cache key
- **AND** the independent target cache at that key must have a matching selector
  manifest with a non-empty version, inspectable tree, and contained Skill roots
  before any materialization receipt commits
- **AND** a revision-like target cache key may differ from the manifest version,
  with both identities recorded in the receipt
- **AND** the pre-call catalog record or current source tree cannot substitute
  for this post-call target proof.

#### Scenario: Native backend owns installed cache lifecycle

- **WHEN** a changed generation invokes the target backend's native Plugin
  add or update operation
- **THEN** that backend may replace or remove its own prior installed cache
  versions according to its native lifecycle
- **AND** `codex-switch` does not directly copy, link, delete, garbage-collect,
  or recreate those cache artifacts
- **AND** only the fresh post-call catalog and target attestation can authorize
  the resulting materialization receipt.

#### Scenario: Backend-managed target proof fails precisely

- **WHEN** the fresh catalog does not report the selector installed or its
  target cache/manifest/version cannot be proved after native reconciliation
- **THEN** functional backend execution remains blocked with
  `shared_configuration.materialization.unverified_target`
- **AND** an invalid catalog command/schema remains
  `shared_configuration.materialization.unverified_catalog`
- **AND** unsafe paths, links, traversal, or file kinds remain
  `shared_configuration.materialization.unsafe_cache`
- **AND** last-known-good config and canonical receipts are preserved while
  any cache artifact left by the backend remains untrusted until a later fresh
  attestation.

#### Scenario: Installed catalog identity wins deterministically

- **WHEN** one verified target catalog exposes the same selector through both
  installed and available collections
- **THEN** target version and installed status come from the installed record
- **AND** collection ordering cannot replace installed target state with an
  available-only record.

#### Scenario: App disables or removes a Plugin or Skill

- **WHEN** the official desired projection disables or removes an identity
- **THEN** the next functional internal invocation removes that usage from the
  internal rendered config before execution
- **AND** `codex-switch` invokes no plugin-remove and performs no direct cache
  deletion; this usage change does not promise retention of versions otherwise
  managed by the native backend.

#### Scenario: Materialization cannot be proved

- **WHEN** a selector is unavailable, catalog output is unverified, an exact
  artifact or path is unsafe, or a target cache replacement would affect a
  running target process
- **THEN** the functional backend is not executed
- **AND** last-known-good config/canonical receipts are preserved
- **AND** a stable finding identifies the required repair boundary.

#### Scenario: Unchanged invocation takes the fast path

- **WHEN** desired generation, rendered projection, personal-Skill ownership,
  and internal materialization receipt all match
- **THEN** preflight performs no config write, marketplace refresh, network
  command, install, or cache replacement
- **AND** executes the backend once.

#### Scenario: Non-current functional preflight exposes progress

- **WHEN** a functional managed internal CLI invocation must inspect or
  materialize a non-current shared generation
- **THEN** it emits flushed progress to stderr before potentially slow source
  attestation and target materialization phases
- **AND** progress output does not mutate state, weaken failure handling, or
  change help/version behavior.

#### Scenario: Stored receipt no longer matches the target cache

- **WHEN** a previously committed target artifact, manifest, tree, or
  contributed-Skill root is missing, corrupt, moved, or escapes its cache
- **THEN** status/verify do not report the generation CLI-ready
- **AND** a functional preflight repairs through the target backend or blocks
  before backend execution without trusting the stored receipt alone.

#### Scenario: Multiple present versions do not erase active source identity

- **WHEN** a selector has multiple present cache versions and no configured
  path or other deterministic attested identity selects one
- **THEN** reconciliation reports an ambiguous materialization finding
- **AND** never silently changes a local `portable_exact` policy to
  `backend_managed`.

#### Scenario: Informational invocation remains read-only

- **WHEN** the managed shim is invoked only for `--help` or `--version`
- **THEN** it does not reconcile, install, write a receipt, or change a link
- **AND** preserves existing backend execution semantics.

### Requirement: CLI-originated changes have an explicit safe App apply boundary

The system SHALL capture Plugin/Skill changes left by a previous internal CLI
session at the next preflight and SHALL not overwrite an active official App.

#### Scenario: Running App receives a pending apply

- **WHEN** the internal projection changed from its baseline and the official
  App or app-server is running
- **THEN** canonical state records `pending_app_apply`
- **AND** the official App config and cache remain unchanged.

#### Scenario: Explicit stopped-App sync applies pending state

- **WHEN** the App is stopped and the user applies `sync-shared`
- **THEN** the pending projection is rendered to the official config only
  after required official materialization verifies
- **AND** the App receipt advances to the committed generation.

#### Scenario: Stopped-App and target identity are re-proved at commit

- **WHEN** process enumeration is unreadable, a Desktop/app-server appears, or
  target config changes after planning/materialization
- **THEN** explicit sync performs no shared target write
- **AND** preserves the pending generation with a stable stopped/CAS finding.

#### Scenario: Sync preview is side-effect free

- **WHEN** the user runs `sync-shared --dry-run`
- **THEN** the plan reports source, target, generation, pending/conflict, and
  materialization actions
- **AND** performs no config, cache, state, process, or network mutation.

### Requirement: Skill ownership and cache separation are explicit

The system SHALL distinguish personal standalone Skills, plugin-contributed
Skills, and project-local Skills.

#### Scenario: Personal Skills use one validated canonical root

- **WHEN** the internal Skills entry is absent
- **THEN** reconcile may create one validated non-circular link to the official
  personal Skills root
- **AND** a real directory, foreign link, dangling link, or self-link fails
  with migration guidance rather than being replaced.

#### Scenario: Plugin-owned Skill paths render for the target home

- **WHEN** desired Skill configuration refers to an artifact under the source
  profile plugin cache
- **THEN** the target projection refers to the corresponding target-cache
  artifact
- **AND** no target config retains an absolute source-cache path.

#### Scenario: Plugin-owned Skill path cannot escape either cache

- **WHEN** a configured Plugin Skill contains `..`, traverses a symlink, or
  resolves outside the attested source artifact or target cache
- **THEN** reconciliation fails closed before config/state publication
- **AND** no escaped path is persisted into a generation or rendered config.

#### Scenario: Project-local Skills remain repository-owned

- **WHEN** both surfaces open the same project worktree
- **THEN** project-local `.agents/skills` remains shared through that worktree
- **AND** profile reconciliation neither copies nor migrates it.

### Requirement: Shared capability health has one diagnostic authority

Status, Doctor, and verify SHALL consume the same read-only shared-capability
report.

#### Scenario: Diagnostics agree on generation health

- **WHEN** shared state is current, pending, conflicting, missing, unsafe, or
  incompletely materialized
- **THEN** status, Doctor, and verify report the same generation and stable
  finding codes
- **AND** diagnostic and verify modes never repair or install implicitly.

### Requirement: Shared projection publication is crash recoverable

The system SHALL publish a prepared recovery journal before the first shared
config/link/generation/state effect and SHALL treat atomic `state.json`
publication as the only commit point.

#### Scenario: Interruption before committed state is recovered

- **WHEN** execution stops after any prepared config, link, or generation effect
  but before committed state publication
- **THEN** the next apply under the store lock restores the recorded predecessor
  or blocks on foreign drift before planning new work
- **AND** an orphan immutable generation is retained/skipped rather than causing
  a permanent collision.

#### Scenario: Interruption after committed state completes terminal cleanup

- **WHEN** committed state matches the prepared journal but journal cleanup did
  not finish
- **THEN** the next apply recognizes the committed generation and completes
  terminal cleanup without rolling back it.

#### Scenario: Read-only modes expose unfinished recovery

- **WHEN** a prepared journal exists
- **THEN** status, Doctor, verify, and sync preview report a stable recovery
  finding and perform zero recovery writes.

#### Scenario: Backend config mutation is journaled before materialization

- **WHEN** target-backend Plugin materialization can activate a selector in the
  target config before the main shared commit is prepared
- **THEN** reconcile first rechecks target CAS and durably records a private
  materialization intent binding exact target bytes/mode and the bounded
  selector set
- **AND** an official target receives a fail-closed stopped-App proof before
  the backend call or its first possible target-config write
- **AND** the main prepared-commit journal cannot coexist with that intent.

#### Scenario: Interrupted backend activation is selectively recovered

- **WHEN** SIGKILL or power loss leaves a materialization intent and an
  operation-owned selector activation in target config
- **THEN** read-only modes report pending recovery without mutation
- **AND** the next apply under the store lock removes or restores only the
  operation-owned selector delta before planning
- **AND** foreign edits are preserved and block that apply with target drift
- **AND** any cache artifacts left by the interrupted backend remain untrusted;
  their continued presence or later replacement follows the native backend
  lifecycle, and normal target attestation remains mandatory.

#### Scenario: A surviving backend retains the mutation lease

- **WHEN** the reconciling parent is terminated after spawning an external
  target-backend materialization command and that backend remains alive
- **THEN** the backend retains an inherited lease on the exact store mutation
  lock until it exits
- **AND** a concurrent or later apply fails closed without retiring the
  materialization intent or planning new work while that lease remains held
- **AND** after backend exit, the next apply classifies any late target-config
  write through the bounded selector recovery rules before planning.

#### Scenario: Recovery evidence remains local and private

- **WHEN** a prepared transaction records exact target-config bytes needed for
  deterministic rollback
- **THEN** that journal is stored only as a `0600` file beneath private `0700`
  codex-switch store directories and is never projected or copied to the other
  profile
- **AND** canonical state and generation artifacts remain secret-screened
- **AND** terminal committed cleanup or successful rollback removes the
  journal.

### Requirement: Shared marketplace values remain secret-free

The system SHALL screen both marketplace field names and values before storing
the shared projection.

#### Scenario: Credential-bearing source value is rejected

- **WHEN** a URL/source descriptor contains userinfo, a credential-like query
  key, a fragment, or another rejected credential-bearing value
- **THEN** reconciliation blocks before generation/state persistence
- **AND** the rejected value is absent from the shared store.

### Requirement: Managed runtime rendering remains byte-idempotent

The system SHALL render a managed runtime configuration without accumulating
generator-owned whitespace or annotation trivia.

#### Scenario: Reusing the prior managed runtime does not grow blank lines

- **WHEN** unchanged profile and shared configuration inputs are rendered in
  two consecutive passes that both reuse the prior managed runtime as the
  profile seed
- **THEN** the later rendered bytes equal the earlier rendered bytes
- **AND** managed section annotations retain one stable boundary without
  rewriting unrelated user comments or whitespace.

### Requirement: Other configuration surfaces remain classified and gated

The system SHALL document the ownership decision for other known configuration
surfaces and SHALL not infer sharing merely because a key currently survives a
switch-time merge.

#### Scenario: Unreviewed or sensitive surface is excluded

- **WHEN** configuration belongs to credentials/auth, models/providers,
  MCP/apps/connectors, permissions/trust, sessions/history/databases,
  automations, runtime caches, or version-specific experimental capability
- **THEN** it remains profile-local or explicitly deferred according to the
  configuration policy matrix
- **AND** adding it to canonical ownership requires a separate field-level
  compatibility/secret review and approved OpenSpec delta.
