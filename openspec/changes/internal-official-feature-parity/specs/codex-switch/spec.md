## ADDED Requirements

### Requirement: Verified official parity reference
The system SHALL use the current verified ChatGPT Desktop bundled CLI as the
official parity reference and SHALL preserve internal binary, model, endpoint,
provider, and auth as the complete allowed-difference whitelist.

#### Scenario: Current ChatGPT bundle is authoritative
- **WHEN** the canonical Runtime Binding resolves a verified current ChatGPT
  Desktop host
- **THEN** parity fingerprints that host's bundle identity, bundle version,
  bundled CLI path, CLI version, and binary digest
- **AND** uses that bundled CLI for official schema, feature, and behavior
  evidence.

#### Scenario: PATH and network latest are not reference authority
- **WHEN** PATH, cached release metadata, or a network release points to a
  different Codex binary or version
- **THEN** parity does not replace the verified ChatGPT bundled reference with
  that observation.

#### Scenario: Official reference change invalidates prior evidence
- **WHEN** the verified bundle identity, bundle version, bundled binary digest,
  schema digest, or feature-inventory digest differs from a stored receipt
- **THEN** the stored receipt is stale
- **AND** internal health requires a new parity preparation.

#### Scenario: Non-whitelisted identity difference is classified
- **WHEN** official and internal differ outside binary, model, endpoint,
  provider, or auth identity
- **THEN** the difference is classified as core, optional, or unclassified
- **AND** it is not silently accepted as another allowed identity difference.

### Requirement: Deterministic parity inventory
The system SHALL create deterministic official and internal inventories for CLI
versions, features, protocol methods and shapes, active-model metadata, and
bounded behavior probes.

#### Scenario: Feature inventory separates default and effective state
- **WHEN** a feature is present in either CLI
- **THEN** the inventory records its name, stage, isolated default state, and
  relevant effective internal state
- **AND** configuration overrides are not mistaken for CLI defaults.

#### Scenario: Protocol inventory includes direction and transitive shape
- **WHEN** generated app-server schemas are compared
- **THEN** every client request, client notification, server request, and
  server notification is recorded with its direction and method-scoped
  transitive schema shape
- **AND** documentation-only text and object ordering do not create semantic
  drift.

#### Scenario: Identical inputs produce identical inventory bytes
- **WHEN** official and internal fingerprints, schemas, features, model
  metadata, policy version, and probe results are unchanged
- **THEN** canonical inventory and receipt payloads are byte-identical.

#### Scenario: Unsupported schema construct fails closed
- **WHEN** a core method closure contains a schema construct the compatibility
  evaluator cannot classify
- **THEN** parity emits an unclassified unhealthy finding
- **AND** does not infer compatibility from a raw digest or partial traversal.

#### Scenario: Inventory persistence excludes sensitive material
- **WHEN** parity records provider-bound evidence
- **THEN** it persists no credential value, credential digest, authorization
  header, query secret, raw config, raw prompt, or unbounded process output.

#### Scenario: Equivalent nullable schema spellings normalize identically
- **WHEN** one method schema represents the same nullable scalar with
  `anyOf` null/string branches and the other uses a `type` array
- **THEN** normalization produces the same semantic form
- **AND** parity does not claim an adapter transform for that difference.

### Requirement: Direction-aware core protocol parity
The system SHALL require direction-aware compatibility for the supported core
Desktop coding protocol and SHALL accept an incompatibility only when an exact
capability-proven Protocol Adapter rule covers it.

#### Scenario: Official core request must be accepted internally
- **WHEN** the official Desktop can send a baseline initialize, config, model,
  collaboration, thread, turn, tool, approval, or completion request shape
- **THEN** the internal backend or an exact request adapter accepts that core
  shape without losing required semantics.

#### Scenario: Internal core response must satisfy Desktop
- **WHEN** the internal backend emits a baseline response or notification
- **THEN** the native or exactly adapted message satisfies the official
  Desktop's required core shape.

#### Scenario: Proven adapter covers native drift
- **WHEN** a core native schema difference is covered by the Protocol Adapter
- **THEN** the parity receipt binds the adapter rule-set digest and the
  capability evidence that selects the exact rule
- **AND** a missing, stale, broader, or unproven transform remains unhealthy.

#### Scenario: Method coverage is exact and receipt-bound
- **WHEN** an incompatible method is evaluated
- **THEN** its coverage record binds direction, method, official/internal
  normalized method-schema digests, incompatibility reasons, disposition, and
  every required adapter rule digest
- **AND** a global rule-set digest, method prefix, reason code, or schema-pair
  allowlist alone cannot satisfy core compatibility.

#### Scenario: Adapter evidence names only actual transforms
- **WHEN** a coverage record uses `adapter_transformed`
- **THEN** the Protocol Adapter exposes a structured rule consumed by the
  production transform for that exact direction and method
- **AND** parity rejects a rule whose method, path/variant contract, capability
  predicate, or digest differs.

#### Scenario: Exact optional extension remains fail-closed
- **WHEN** a known schema pair differs only by a recorded realtime, media,
  provider-login, external-agent-import, or plugin-sharing extension outside
  the supported core coding path
- **THEN** parity records its exact extension identifier in the optional queue
- **AND** a changed schema pair or observed use escalates it to an unhealthy
  core or unclassified finding.

#### Scenario: Saved task-8.3 failure closes atomically
- **GIVEN** the retained candidate comparison contains two core-feature, eight
  core-protocol, and three unclassified-protocol errors
- **WHEN** exact coverage, overlay/config evidence, and required probe results
  are evaluated
- **THEN** all thirteen errors are resolved in one final policy result
- **AND** removing any required proof restores an unhealthy stable finding
- **AND** no subset-only GREEN can satisfy task 8.3.

#### Scenario: Additive optional field is not an automatic core failure
- **WHEN** one side adds an optional field that does not invalidate the
  direction-specific core contract
- **THEN** parity records the semantic difference without marking the runtime
  unhealthy solely because raw schemas differ.

#### Scenario: Known official-only extensions enter the queue
- **WHEN** `app/installed`, `app/read`, `environment/status`,
  `thread/searchOccurrences`, `thread/environment/connected`, or
  `thread/environment/disconnected` is absent internally and absent from the
  official core acceptance trace
- **THEN** parity records a deterministic optional synchronization item.

#### Scenario: Observed optional extension escalates to core
- **WHEN** the official core acceptance trace invokes or requires a method
  classified optional-unless-observed
- **THEN** that reference classifies the missing or incompatible method as core
- **AND** internal health fails until it is natively compatible or exactly
  adapted.

### Requirement: Explicit feature and model-metadata classification
The system SHALL apply an explicit versioned policy to feature and active-model
metadata drift, with multi-agent v2 as core and unknown drift as unhealthy.

#### Scenario: Multi-agent v2 is core
- **WHEN** the official active-model contract selects
  `multi_agent_version = "v2"`
- **THEN** the internal candidate must expose proven v2 feature, catalog, and
  behavior evidence
- **AND** a missing or v1 result is unhealthy.

#### Scenario: Multi-agent v2 requires final post-probe evaluation
- **WHEN** inventory metadata differs but the candidate projects v2 through
  the exact managed overlay and config
- **THEN** pre-probe evaluation may mark only that named core capability
  provisional
- **AND** final health requires the bounded typed-v2 probe to pass under the
  same revalidated fingerprints.

#### Scenario: Known metadata-only drift remains visible
- **WHEN** `enable_fanout`, `item_ids`, or `memories` differs only in stage or
  isolated default metadata while the core behavior probe remains compatible
- **THEN** parity records optional drift
- **AND** a later missing core behavior escalates the affected feature to core.

#### Scenario: Item IDs require exact observed-path coverage
- **WHEN** `item_ids` effective state differs for the current candidate
- **THEN** parity accepts the observed Desktop resume dependency only when the
  exact `thread/resume.params.history` path is proven by either current
  direction-aware native compatibility for `client_request:thread/resume` or
  the exact adapter that removes top-level item IDs and only non-portable
  opaque reasoning references while preserving all other semantics
- **AND** native compatibility requires both current method schemas and
  `compatible=true`; absence of a method-coverage record alone is not proof
- **AND** an incompatible resume method without accepted exact adapter
  coverage remains unhealthy
- **AND** another observed item-ID dependency remains unhealthy until separately
  proven.

#### Scenario: Skill search absence is queued
- **WHEN** official stable `skill_search` is enabled and the internal CLI does
  not expose it, but the core acceptance trace does not depend on it
- **THEN** parity records an optional-unless-observed synchronization item
- **AND** does not emulate the feature.

#### Scenario: Official-only under-development features are queued
- **WHEN** `code_mode_buffered_exec`, `executor_capability_discovery`,
  `external_agent_memory_import`, or `mcp_2026_07_28` is absent internally
- **THEN** parity records optional drift without projecting the feature.

#### Scenario: Tool mode is not inferred
- **WHEN** the official model metadata contains `tool_mode` and the internal
  provider model does not
- **THEN** parity records optional pending-provider evidence
- **AND** the managed overlay does not add or change `tool_mode`.

#### Scenario: New feature drift fails closed
- **WHEN** a feature difference has no explicit policy entry
- **THEN** parity emits an unclassified unhealthy finding
- **AND** does not place it into the optional queue by default.

### Requirement: Provider-bound parity receipt
The system SHALL persist one canonical parity receipt that binds the official
reference, internal runtime, capability evidence, adapter policy, source
catalog, overlay, config projection, probe results, findings, and
synchronization queue.

#### Scenario: Healthy receipt binds complete evidence
- **WHEN** every core and classification check passes
- **THEN** the receipt records official and internal fingerprints, inventory
  digests, capability-receipt digest, adapter rule-set digest, catalog and
  config digests, overlay digest, bounded probe result codes, findings, queue,
  policy version, exact method-coverage records, the versioned official
  Desktop acceptance trace, and healthy status.
- **AND** the receipt contains exactly one passed `core_protocol` result and
  one passed `typed_subagent_v2` result.

#### Scenario: Acceptance trace is one receipt-bound policy input
- **WHEN** parity evaluates eligibility and final health
- **THEN** both passes consume the same canonical versioned acceptance trace
- **AND** the final receipt binds that exact trace
- **AND** a changed, malformed, or independently conflicting observed set is
  rejected rather than merged.

#### Scenario: Legacy receipt cannot imply method coverage
- **WHEN** a schema-version-1 receipt has no exact method-coverage records
- **THEN** diagnostics reject it as stale or unsupported
- **AND** only the staged parity preparation route may generate a complete
  schema-version-2 replacement.

#### Scenario: Receipt is profile-local and manifest-owned
- **WHEN** parity artifacts are promoted
- **THEN** the receipt is a mode-`0600` regular non-symlinked file under
  `profiles/internal/parity/`
- **AND** the internal manifest records its path, payload digest, policy
  version, and official-reference digest.

#### Scenario: Missing or malformed receipt is unhealthy
- **WHEN** the manifest receipt path is missing, symlinked, not regular,
  malformed, oversized, digest-mismatched, or schema-unsupported
- **THEN** status, Doctor, and verify report stable unhealthy findings.

#### Scenario: Provider or runtime change makes receipt stale
- **WHEN** internal binary, active model, provider id, wire API, endpoint
  digest, auth source kind, capability receipt, source catalog, overlay,
  relevant config, or adapter rules differ from the receipt
- **THEN** the receipt is stale
- **AND** read-only diagnostics do not repair or reuse it.

#### Scenario: Optional queue is deterministic
- **WHEN** optional findings are present
- **THEN** the receipt sorts synchronization items by category, identifier, and
  finding code
- **AND** optional drift does not change healthy status unless its policy
  escalates it to core.

### Requirement: Source-preserving managed model overlay
The system SHALL create a managed internal model-catalog overlay from a deep
structured copy of the configured source catalog and SHALL never mutate the
source catalog.

#### Scenario: Missing v2 field is the only overlay change
- **WHEN** exactly one active-model entry matches the configured model slug and
  its `multi_agent_version` field is absent
- **THEN** the overlay adds only
  `/models/<active-index>/multi_agent_version = "v2"`
- **AND** every other field and value remains semantically equal to the source.

#### Scenario: Existing v2 field requires no semantic change
- **WHEN** the unique active-model entry already contains
  `multi_agent_version = "v2"`
- **THEN** the overlay has no semantic difference from the source
- **AND** its receipt still binds source and overlay digests.

#### Scenario: Source catalog remains byte-unchanged
- **WHEN** overlay preparation, promotion, verification, rollback, or update
  completes or fails
- **THEN** the configured source catalog bytes and mode are unchanged.

#### Scenario: Ambiguous active model blocks overlay
- **WHEN** the catalog shape is unsupported or zero or multiple entries match
  the active model slug
- **THEN** overlay preparation fails with a stable unhealthy finding
- **AND** no runtime artifact is promoted.

#### Scenario: Broader overlay mutation is rejected
- **WHEN** an overlay changes `tool_mode`, model/provider/API fields, reasoning
  settings, instructions, modalities, visibility, another model, or any other
  non-approved path
- **THEN** parity rejects the overlay before promotion.

#### Scenario: Source changes during preparation
- **WHEN** the source catalog identity or digest changes between read,
  probing, and locked promotion
- **THEN** the candidate is stale
- **AND** the previous runtime remains effective.

### Requirement: Proven internal v2 config projection
The system SHALL project multi-agent v2 through internal profile config and
SHALL remove only the exact incompatible `agents.max_threads` assignment after
the isolated v2 probe succeeds.

#### Scenario: Internal profile selects overlay and v2
- **WHEN** a parity candidate is prepared
- **THEN** its internal profile config points `model_catalog_json` to the
  managed overlay and sets `features.multi_agent_v2 = true`
- **AND** unrelated profile settings remain unchanged.

#### Scenario: Exact stale assignment is removed
- **GIVEN** the isolated candidate proves v2 schema and behavior
- **WHEN** one authoritative scalar `[agents].max_threads` assignment supplies
  the internal runtime
- **THEN** the projected config removes only that assignment
- **AND** preserves the section, comments where structurally possible, and all
  unrelated agent settings.

#### Scenario: Ambiguous max-threads config blocks promotion
- **WHEN** `agents.max_threads` is duplicated, non-scalar, syntactically
  ambiguous, multiply sourced, concurrently changed, or not attributable to an
  authoritative config input
- **THEN** parity reports an unhealthy config-migration finding
- **AND** promotes neither v2 config nor overlay.

#### Scenario: Active managed home is updated in the same bundle
- **WHEN** internal is active and its derived managed-home config is
  materialized
- **THEN** the regenerated runtime config is included in the same recoverable
  runtime bundle as its source config, overlay, receipts, launcher, and
  manifest.

#### Scenario: Failed v2 evidence has no v1 fallback
- **WHEN** schema generation, feature proof, config projection, Azure behavior,
  typed-role spawn, or completion evidence fails or is unknown
- **THEN** the candidate is unhealthy
- **AND** the system does not silently remove v2 metadata, select v1, or report
  the candidate promoted.

### Requirement: Isolated bounded parity probes
The system SHALL run bounded isolated probes that prove the candidate's core
schema, configuration, and v2 behavior without persisting sensitive runtime
material.

#### Scenario: Probe uses candidate artifacts
- **WHEN** parity probes an internal candidate
- **THEN** the probe uses the candidate binary, staged overlay, projected
  config, and candidate capability receipt
- **AND** does not read promoted parity artifacts as proof of the candidate.

#### Scenario: Eligibility and final policy are separate
- **WHEN** inventory contains a named provisional core capability and no
  unknown or uncovered drift
- **THEN** pre-probe eligibility permits only the bounded required probes
- **AND** final policy consumes their results before receipt construction
- **AND** all mutable binary, schema, config, catalog, capability, and adapter
  fingerprints are revalidated after the probes
- **AND** an unknown or uncovered drift stops before any probe.

#### Scenario: Typed-role subagent probe completes
- **WHEN** the candidate's isolated v2 probe explicitly requests an
  `explorer` child to return `parity-subagent-ok`
- **THEN** the child uses the v2 contract and returns the exact marker
- **AND** the parent completes without a v1 fallback.

#### Scenario: Probe output is bounded and sanitized
- **WHEN** a probe writes stdout, stderr, headers, config-derived diagnostics,
  or model output
- **THEN** retained evidence contains only bounded sanitized status and digest
  data
- **AND** no credential-bearing config or raw secret is persisted.

#### Scenario: Probe timeout or malformed output fails
- **WHEN** a probe times out, exits unexpectedly, returns malformed JSON,
  omits a required response, or exceeds its output bound
- **THEN** the probe process group is terminated
- **AND** parity records a stable unhealthy result.

#### Scenario: Candidate changes during probe
- **WHEN** the official reference, candidate binary, capability receipt,
  source catalog, or relevant config changes during probing
- **THEN** parity rejects the evidence as stale.

### Requirement: Crash-recoverable runtime parity bundle
The system SHALL promote all parity-sensitive internal runtime files through
one exact, durable, crash-recoverable runtime rebind journal.

#### Scenario: Complete bundle is promoted together
- **WHEN** a verified internal rebind is committed
- **THEN** manifest, launcher, capability receipt, parity receipt, overlay,
  internal profile config, any exact authoritative config edit, and any active
  derived runtime config converge to the complete new bundle
- **AND** manifest activation occurs last.

#### Scenario: Prepared interruption rolls back
- **WHEN** a process stops after a schema-v3 marker is durable but before the
  marker is committed
- **THEN** recovery restores every target to its recorded old state
- **AND** removes the marker only after all old states are verified.

#### Scenario: Committed interruption rolls forward
- **WHEN** a process stops after the schema-v3 marker is committed
- **THEN** recovery converges every target to its recorded new state
- **AND** removes the marker only after all new states are verified.

#### Scenario: Foreign target state fails closed
- **WHEN** any target matches neither its recorded old nor new identity
- **THEN** recovery stops with a foreign-state finding
- **AND** does not overwrite or delete the foreign bytes.

#### Scenario: Bundle target set is exact
- **WHEN** a bundle contains a duplicate, unexpected, parent/child-overlapping,
  symlinked, directory, or out-of-policy target
- **THEN** commit fails before the marker or any target write.

#### Scenario: Legacy rebind markers remain recoverable
- **WHEN** recovery encounters an existing schema-v1 or schema-v2 runtime
  rebind marker
- **THEN** it applies the established legacy manifest/launcher/receipt
  recovery contract
- **AND** does not reinterpret the marker as a schema-v3 bundle.

### Requirement: Fail-safe staged internal binary update
The system SHALL install an internal update into a private sibling candidate,
prove full parity before replacing the bound binary, and retain
last-known-good until the post-promotion handshake succeeds.

#### Scenario: Installer targets a sibling candidate
- **WHEN** `update-internal` prepares a real update
- **THEN** the trusted installer writes into a validated private sibling
  staging directory
- **AND** the bound internal binary remains executable during installation and
  candidate probing.

#### Scenario: Installer ambient state is hermetic
- **WHEN** the trusted installer runs for a sibling candidate
- **THEN** it receives a private mode-0700 `HOME` and `CODEX_HOME`
- **AND** the validated candidate is first in the installer child `PATH`
- **AND** the live shell profile, live Codex config, active record, manifest,
  wrapper, bound binary, and runtime bundle remain unchanged.

#### Scenario: Installer scratch is removed on every supported exit
- **WHEN** the installer succeeds, fails, receives `HUP`, `INT`, or `TERM`
- **THEN** cleanup removes only the exact private installer root
- **AND** no generated config, shell profile, credential-bearing scratch byte,
  or scratch path remains.

#### Scenario: Candidate parity precedes bound replacement
- **WHEN** the staged binary has the intended version
- **THEN** executable, mode, code-signature where applicable, generated schema,
  capability receipt, parity inventory, overlay, config projection, and
  behavior probes all pass before the bound path is replaced.

#### Scenario: Candidate failure preserves last-known-good
- **WHEN** installer, version, schema, receipt, overlay, config, probe, or parity
  preparation fails
- **THEN** the bound binary and active runtime bundle remain unchanged
- **AND** live shell/config/profile state remains byte-for-byte unchanged
- **AND** any retained candidate is absent from the live shell PATH
- **AND** update returns nonzero without reporting success.

#### Scenario: Binary and runtime bundle recover together
- **WHEN** promotion is interrupted around the old-to-backup or
  candidate-to-bound renames
- **THEN** recovery validates exact sibling paths and old/new binary digests
- **AND** converges the binary and runtime parity bundle to the same old or new
  generation.

#### Scenario: Foreign binary state fails closed
- **WHEN** bound, candidate, or backup binary identity matches neither the
  recorded old nor new promotion state
- **THEN** recovery stops without deleting or replacing the foreign binary.

#### Scenario: Backup survives until final handshake
- **WHEN** the new binary and runtime bundle have been promoted
- **THEN** the old binary backup remains until canonical binding attestation,
  app-server smoke, parity receipt verification, and version postcondition all
  pass
- **AND** any failed handshake restores the last-known-good generation.

#### Scenario: Internal update dry-run has zero mutation
- **WHEN** `update-internal --dry-run` is requested
- **THEN** it reports target version, candidate path class, parity checks,
  artifact set, and promotion order
- **AND** invokes no installer and changes no binary, config, receipt, overlay,
  launcher, manifest, or journal.

#### Scenario: Pre-fix installer residue is repaired precisely
- **WHEN** the operator authorizes recovery from confirmed installer-added PATH
  blocks and failed sibling candidates
- **THEN** the system records a private timestamped backup before editing
- **AND** removes or moves only the exact preflight-validated blocks and
  candidates
- **AND** preserves unrelated shell content, config, plugins, user data, and
  recoverable backup bytes.

### Requirement: Unified parity diagnostics and packaging
The system SHALL make status, Doctor, verify, reports, repair routing, and
release packaging consume the same parity receipt and stable finding codes.

#### Scenario: Read-only diagnostics do not repair
- **WHEN** status, Doctor, or `verify --repair=none` observes missing, stale,
  malformed, core-drift, probe-failed, or unclassified parity evidence
- **THEN** it reports the same unhealthy finding codes
- **AND** performs no download, rewrite, rebind, update, or reclassification.

#### Scenario: Optional drift is reported as a queue
- **WHEN** a valid receipt contains optional findings
- **THEN** diagnostics display the deterministic synchronization queue
- **AND** distinguish it from core health failures.

#### Scenario: Explicit repair uses staged rebind
- **WHEN** an authorized repair is requested for stale parity artifacts
- **THEN** repair routes through the same parity preparation and recoverable
  runtime bundle used by internal rebind
- **AND** does not patch receipt or overlay files in place.

#### Scenario: Packaged runtime contains parity implementation
- **WHEN** a release bundle is built and validated
- **THEN** it includes the parity module and every required runtime import
- **AND** generated launchers and wrappers resolve only to files inside the
  immutable payload.

#### Scenario: Official release advisory remains separate
- **WHEN** the network stable-release advisory reports a version different
  from the bundled ChatGPT CLI
- **THEN** parity continues to bind the current bundled reference
- **AND** the advisory does not rewrite parity health or promote an internal
  candidate.

### Requirement: Live Desktop typed-Subagent acceptance
The system SHALL require an explicitly authorized live ChatGPT Desktop
acceptance that proves typed v2 Subagent behavior and complete runtime
ownership before the change is declared complete.

#### Scenario: Live acceptance requires Human Gate
- **WHEN** final acceptance would quit or reopen ChatGPT or create a real
  provider-backed Desktop task
- **THEN** execution stops until the user explicitly authorizes that live
  effect.

#### Scenario: Runtime ownership is attested before task
- **WHEN** live acceptance starts
- **THEN** it verifies ChatGPT main-process identity, GUI `CODEX_CLI_PATH`,
  managed launcher, proxy parent, exact internal backend child, capability
  receipt, parity receipt, overlay, active config, and their expected digests.

#### Scenario: Explicit explorer child is observable
- **WHEN** the fresh Desktop task requests an `explorer` child with a bounded
  instruction to return `parity-subagent-ok`
- **THEN** the parent emits a spawn item
- **AND** the child thread source is `thread_spawn`
- **AND** the child `agentRole` is `explorer`.

#### Scenario: Desktop shows task-oriented child metadata
- **WHEN** the explorer child is created through the proven v2 contract
- **THEN** its Desktop-visible name and description are non-empty and
  task-oriented
- **AND** acceptance does not rely only on a random nickname.

#### Scenario: Child and parent complete under same ownership
- **WHEN** the child returns `parity-subagent-ok`
- **THEN** the parent completes with the expected acceptance marker
- **AND** post-task attestation proves the same launcher, proxy, backend,
  receipt, overlay, and active config generation remained in use.

#### Scenario: Partial smoke cannot pass
- **WHEN** only a generic turn passes, the child is untyped, v1 fallback occurs,
  metadata is nickname-only, only the parent emits a marker, or runtime
  ownership is unattested
- **THEN** live Desktop acceptance fails.
