## Context

The internal product profile is correctly bound to its own binary, Azure
provider, model, endpoint, and auth, but those allowed identity differences do
not prove behavioral compatibility with the current ChatGPT Desktop backend.
The canonical Runtime Binding currently reports:

- ChatGPT bundled reference: `codex-cli 0.146.0-alpha.3.1` at
  `/Applications/ChatGPT.app/Contents/Resources/codex`.
- Internal backend: `codex-cli 0.144.6` at `/Users/cY/.local/bin/codex`.
- Generated experimental schemas: 347 official documents and 337 internal
  documents.
- Official-only methods: `app/installed`, `app/read`, `environment/status`,
  `thread/searchOccurrences`, `thread/environment/connected`, and
  `thread/environment/disconnected`.
- Feature drift includes official-only `skill_search` and several
  under-development features, plus stage/default differences for
  `enable_fanout`, `item_ids`, `memories`, and `multi_agent_v2`.

The configured internal catalog entry for `gpt-5.6-sol` preserves the intended
Azure model contract but omits official `multi_agent_version = "v2"` and
`tool_mode = "code_mode"`. A retained isolated probe proved that the current
internal backend accepts a catalog copy whose only semantic change is
`multi_agent_version = "v2"`. The first v2 thread failed with:

`agents.max_threads cannot be set when features.multi_agent_v2 is enabled`

After removing only that stale assignment from the isolated config, the same
backend completed both `parity-ok` and a real subagent result
`parity-subagent-ok`. This proves the v2 overlay path, but it does not prove that
`tool_mode`, every feature difference, or every official-only method is safe to
project.

The existing architecture already has three relevant deep modules:

- Runtime Binding owns executable, launcher, process, and Desktop-host intent.
- Protocol Adapter owns exact direction/method/path message transformations.
- Capability Receipt owns generated-schema and config-write capability
  evidence for one internal backend.

Parity policy must not be added to any of those modules. It needs its own
provider-bound evidence, classification, overlay, and promotion contract.

`update-internal` also has a separate atomicity defect. The environment helper
moves the bound binary aside, installs into the bound path, and removes the old
backup after only executable/version checks. The later app-server compatibility
smoke therefore runs after the last-known-good backup has already been retired.
Parity promotion must close that gap instead of layering another post-update
check onto the current sequence.

## Skill Routing Ledger

- request kind: compatibility, integration, migration, error-handling, and
  update-safety change
- workflow mode: Full OpenSpec
- capability-research: used; current Runtime Binding, both local CLI versions,
  isolated feature lists, generated schemas, official model cache, internal
  source catalog, retained v2 behavior probe, and update/rebind source were
  inspected on 2026-07-26
- decision-resolution: used; the local ChatGPT bundled CLI is the reference,
  parity policy is independent, and unknown drift fails closed
- decision-grilling: skipped; local evidence resolves the remaining
  classification and atomicity choices without a product question
- implementation-planning: used through DevFlow/OpenSpec and the AI-native
  Target State, Completion Contract, Capability Slices, and Execution Ledger
- architecture-guidance: used; parity is a separate deep module with one small
  preparation/evaluation interface
- domain-language-modeling: skipped; the explicit reference, inventory,
  finding, receipt, overlay, and synchronization-queue vocabulary is sufficient
  without a separate bounded-context model
- openspec-routing: required and used
- Open Questions: none

## Goals / Non-Goals

**Goals:**

- Compare the current verified ChatGPT bundled CLI with an internal candidate
  using deterministic version, feature, protocol, model-metadata, and behavior
  inventories.
- Preserve exactly five allowed identity differences: internal binary, model,
  endpoint, provider, and auth.
- Make core or unclassified non-whitelisted drift unhealthy while retaining
  known optional drift in a deterministic report and synchronization queue.
- Produce a provider-bound parity receipt and a managed model-catalog overlay
  without mutating the configured source catalog.
- Enable internal multi-agent v2 only after schema and real behavior evidence
  pass, with no silent v1 fallback.
- Promote manifest, launcher, capability receipt, parity receipt, overlay, and
  exact config changes as one crash-recoverable runtime bundle.
- Stage internal binary updates beside the bound binary and preserve
  last-known-good until parity promotion and post-promotion verification pass.
- Make verify, Doctor, reports, packaging, and an explicitly authorized live
  Desktop Subagent acceptance consume the same parity evidence.

**Non-Goals:**

- Rebinding internal to the official bundle binary.
- Changing the configured internal model, endpoint, provider, auth, or
  credential material.
- Emulating unsupported Apps, remote-environment, thread-search, skill-search,
  or tool-mode behavior without capability evidence.
- Treating a network release, PATH binary, or cached upstream version as the
  official Desktop reference.
- Adding a production dependency or a general JSON Schema compatibility
  framework.
- Automatically restarting ChatGPT, running a live update, publishing a
  release, committing, pushing, archiving, or deleting retained probe evidence.

## Target State

One parity preparation call resolves the current official reference and one
internal candidate, generates deterministic inventories, applies the fixed
classification policy, creates an exact managed overlay and internal config
projection, runs bounded probes, and returns a bundle plus a provider-bound
receipt. Runtime rebind and internal update promote that complete bundle or
leave the previous healthy runtime effective. Diagnostics load the same
receipt, reject stale or foreign state, and expose optional work without
claiming that it is core parity.

### Task 8.3 Repair Target State

Preparation produces a coverage decision for every incompatible protocol
method before it can claim health. Each decision binds the exact direction,
method, official and internal normalized method-schema SHA-256 values,
incompatibility reason codes, one disposition, and the proof required by that
disposition:

- `native_equivalent`: the comparator proves semantic equality after canonical
  normalization; no adapter rule is claimed.
- `adapter_transformed`: one structured Protocol Adapter rule names the exact
  method and transformed paths/variants, and its rule digest is bound.
- `optional_extension`: one parity-owned exact schema-pair rule names the
  excluded extension and deterministic queue identifier; observed use
  escalates it to core.
- `uncovered`: the candidate is unhealthy and no probe or promotion begins.

The existing global adapter digest remains a whole-rule-set freshness check,
but it is never sufficient coverage evidence on its own. A parity receipt can
be healthy only after all core feature and protocol decisions have final
evidence and no `uncovered` record remains.

The final implementation receipt uses schema version 2. Version-1 receipts do
not migrate in place: they are stale/unsupported evidence and require the
existing staged parity repair route to regenerate a complete candidate.

Receipt-v2 also binds one versioned official Desktop acceptance trace. The
trace owns the exact observed protocol methods, core features, item-ID
dependencies, and observed optional extensions used by both policy passes.
Preparation passes that object directly to eligibility and final policy, then
serializes the same canonical object into the receipt. A changed or malformed
trace is stale evidence; callers cannot combine it with independent observed
sets to construct a different policy view.

### Current Thirteen-Finding Closure Matrix

| Current error | Exact planned disposition | Required proof |
|---|---|---|
| feature `multi_agent_v2` | provisional core, then satisfied | internal effective v2, exact overlay/config projection, and passed `typed_subagent_v2` probe |
| feature `item_ids` | core dependency satisfied only for the observed resume path; remaining metadata drift queued | method-scoped `thread/resume` ID/opaque-reasoning adapter rule plus no other observed core dependency |
| client `thread/resume` | adapter transform plus optional `input_audio` extension | exact rule digest and exact schema-pair optional record |
| client `thread/realtime/start` | common method remains core; v3/handoff/initial-item additions are optional-unless-observed | exact schema pair and extension identifier |
| client `turn/start` | common method remains core; `localAudio`/`audio` additions are optional-unless-observed | exact schema pair and extension identifier |
| client `turn/steer` | common method remains core; `localAudio`/`audio` additions are optional-unless-observed | exact schema pair and extension identifier |
| server requests `item/commandExecution/requestApproval`, `item/permissions/requestApproval` | native semantic equivalence | canonical equality of `anyOf(null,string)` and `type:[null,string]` |
| server notifications `item/autoApprovalReview/started`, `item/autoApprovalReview/completed` | native semantic equivalence | the same canonical nullable-union proof |
| client `account/login/start` | Bedrock variant optional-unless-observed under the fixed non-internal provider/auth boundary | exact schema pair and extension identifier |
| client `externalAgentConfig/import` | memory/provider/migration additions optional-unless-observed | exact schema pair, existing optional external-agent-memory policy, and extension identifier |
| client `plugin/share/updateTargets` | `LISTED` discoverability optional-unless-observed | exact schema pair and extension identifier |

The matrix is exhaustive for the saved diagnostic. It is not a prefix,
method-name-only, reason-code-only, or future-version allowlist. Any additional
method, changed schema pair, changed adapter rule, unsupported comparator
construct, or newly observed optional extension is unhealthy.

### Task 8.3 Research Evidence Ledger

- `authoritative_current`: the verified ChatGPT bundle remains
  `/Applications/ChatGPT.app/Contents/Resources/codex` at
  `codex-cli 0.146.0-alpha.3.1`. The current active profile and running
  app-server are official, so the prior internal pid/config snapshot is
  historical RED evidence, not a reusable live preflight.
- `local_scan`: the saved official/internal generated-schema bundles, parity
  diagnostic, comparator, policy, receipt, probes, Protocol Adapter, adapter
  tests, and task-8.3 transaction evidence were inspected. The eleven failing
  method pairs reduce to realtime-v3/handoff additions, resume/turn audio
  variants, four equivalent nullable-string spellings, Bedrock login,
  external-agent memory/provider/migration fields, and listed sharing.
- `comparison`: the current adapter already performs exact resume-history ID
  and opaque-reasoning normalization, but its digest payload does not identify
  that transform. The current policy evaluates before probes and receives no
  method-scoped evidence.
- `assumptions`: the internal candidate binary and schema may change before
  implementation or live retry. Every execution boundary therefore regenerates
  and revalidates fingerprints; no stored digest authorizes a changed pair.
- `recommendation`: use structured adapter-rule evidence, parity-owned exact
  schema-pair dispositions, semantic normalization, two-pass evaluation, and
  receipt-v2. Do not emulate unsupported extension semantics or weaken unknown
  drift.

### Preparation Ordering

Task 8.3 replaces the current single pre-probe health decision with two
fail-closed passes:

1. Capture and normalize current official/internal inventories and build exact
   method coverage.
2. Run a pre-probe eligibility evaluation. Unknown/uncovered drift stops here;
   only core evidence explicitly marked provisional may proceed.
3. Run the existing bounded core and typed-v2 probes against candidate-only
   artifacts.
4. Require exactly one successful `core_protocol` result and one successful
   `typed_subagent_v2` result, revalidate all mutable fingerprints, and execute
   the final policy evaluation with method coverage and probe results.
5. Construct receipt-v2 bytes only from that final evaluation. Promotion
   remains owned by the existing transaction after preparation returns healthy.

This ordering does not let probes override unknown drift. It only allows a
declared provisional capability such as `multi_agent_v2` to acquire the
evidence the Completion Contract already requires.

### Alternatives Rejected for Task 8.3

- Full emulation/down-conversion of realtime v3, audio, Bedrock login, external
  migration, and listed sharing was rejected because those semantics are not
  proven on the fixed internal provider and would expand the product target.
- Whole-method warning suppression or a digest-pair allowlist was rejected
  because it proves neither message transformation nor semantic equivalence.
- Expanding the live probe to invoke all eleven incompatible methods was
  rejected because several methods have provider, permission, sharing, or
  media effects and a passing example cannot prove the complete schema
  contract.

## Decisions

### Decision 1: The verified ChatGPT bundle is the official reference

Parity resolves the official side through the existing canonical Runtime
Binding and accepts only the current verified ChatGPT Desktop host. The
reference fingerprint includes bundle identifier and version, bundled CLI
path, CLI version, binary digest, generated-schema digest, and feature-inventory
digest. PATH, network latest, cached release metadata, and an internal profile
alias are observations only.

The internal fingerprint includes the canonical backend path, version and
digest, active model slug, provider identifier, wire API, a digest of the
configured endpoint, auth source kind without credential values, capability
receipt digest, source-catalog path/digest, and relevant config digests. A
change to either fingerprint invalidates reuse.

Alternative A was comparing version strings only. It was rejected because
different builds can share protocol behavior and a newer string can still lack
required metadata. Alternative B was using the latest upstream release. It was
rejected because ChatGPT Desktop communicates with its bundled CLI, not an
arbitrary network artifact.

### Decision 2: Build direction-aware inventories and classify drift explicitly

The parity module normalizes:

- CLI semantic version and binary digest.
- Feature name, stage, isolated default state, and effective internal state.
- Client request, client notification, server request, and server notification
  methods.
- Method-scoped transitive JSON Schema shape with documentation-only fields
  removed and deterministic ordering.
- Active-model behavior metadata.
- Bounded behavior-probe outcomes.

Protocol compatibility is direction-aware. For client-to-server traffic, the
internal backend must accept the core request shape that the official Desktop
can send. For server-to-client traffic, the internal response or notification
must satisfy the official Desktop's core required shape. Additive optional
fields are not automatically core failures. A core incompatibility is healthy
only when an exact Protocol Adapter rule is already capability-proven and its
rule-set digest is bound into the parity receipt.

The initial policy is:

| Surface | Classification | Reason |
|---|---|---|
| Baseline initialize, config, model, collaboration, thread, turn, item, tool, approval, and completion protocol closures | core | Required for the supported internal Desktop coding path |
| `multi_agent_v2` plus active-model `multi_agent_version` | core | Directly selects the targeted Subagent contract and has real backend evidence |
| Exact v2 typed-role spawn, child metadata, and completion behavior | core | User-visible target behavior |
| `app/installed`, `app/read` | optional-unless-observed | Apps extension is not part of the supported core acceptance trace |
| `environment/status`, connected/disconnected notifications | optional-unless-observed | Remote-environment extension is outside the local internal core trace |
| `thread/searchOccurrences` | optional-unless-observed | Search extension is not required to execute or inspect a coding task |
| `skill_search` | optional-unless-observed | Official stable feature is absent internally, but no current core Desktop trace depends on it |
| `code_mode_buffered_exec`, `executor_capability_discovery`, `external_agent_memory_import`, `mcp_2026_07_28` | optional | Official-only and under development |
| Stage/default drift for `enable_fanout`, `item_ids`, and `memories` | optional while behavior-compatible | Current schemas/probes retain the core behavior; a missing core item id or observed dependency escalates to core |
| Active-model `tool_mode` | optional pending provider evidence | It is model/provider-sensitive and has no safe Azure behavior proof |

An `optional-unless-observed` surface becomes core for that reference when the
official Desktop core acceptance trace invokes or requires it. Any new drift
without an explicit policy entry is `unclassified` and unhealthy. This prevents
a newly added official feature or method from silently entering the optional
queue.

Alternative A was declaring every raw schema or stage difference core. It was
rejected because documentation and additive optional changes would make every
version skew unusable. Alternative B was allowing every unknown difference as
optional. It was rejected because new Desktop dependencies would false-pass.

### Decision 3: Add one independent deep Parity module

Create `scripts/codex_switch_parity.py`. Its external interface remains small:

```python
@dataclass(frozen=True)
class ParityCandidate:
    official_binding: RuntimeBinding
    internal_binding: RuntimeBinding
    internal_manifest: Mapping[str, object]
    capability_receipt: CapabilityReceiptArtifact
    source_config: ConfigInputs

@dataclass(frozen=True)
class ParityBundle:
    receipt: ParityReceipt
    receipt_payload: bytes
    overlay_payload: bytes
    config_projection: ConfigProjection
    findings: tuple[ParityFinding, ...]
    synchronization_queue: tuple[ParityQueueItem, ...]

def prepare_parity_bundle(
    candidate: ParityCandidate,
    *,
    work_root: Path,
    timeouts: ParityTimeouts,
) -> ParityBundle: ...

def verify_parity_bundle(
    candidate: ParityCandidate,
    *,
    receipt_path: Path,
    overlay_path: Path,
) -> ParityReport: ...
```

Schema generation, feature-list execution, method-closure normalization,
catalog copying, probe orchestration, sanitization, and finding classification
stay behind this interface. Injectable command and probe runners are internal
test seams, not additional caller-facing policy.

Runtime Binding continues to answer "what should run." Protocol Adapter
continues to answer "how is one proven message transformed." Capability Receipt
continues to answer "what does this backend schema/config-write path support."
Parity answers "does this provider-bound internal runtime satisfy the current
official core contract, and what exact artifacts prove it."

### Decision 4: Store a profile-local overlay and provider-bound receipt

Managed parity artifacts live under the internal profile control directory:

- `profiles/internal/parity/receipt.json`
- `profiles/internal/parity/model-catalog.json`

The directory is mode `0700`; files are regular, non-symlinked, and mode
`0600`. The internal manifest records both paths and payload digests, the parity
policy version, and the official-reference digest.

The canonical JSON receipt contains:

- Official and internal fingerprints.
- Feature and protocol inventory digests.
- Capability-receipt and Protocol Adapter rule-set digests.
- Source-catalog path and digest.
- Overlay path, digest, and exact JSON-pointer change set.
- Relevant source/profile/runtime config digests.
- Bounded sanitized probe result codes and evidence digests.
- Sorted stable findings and synchronization-queue entries.
- Overall health and policy version.

It contains no credential value, credential digest, authorization header, query
secret, raw config, raw prompt, raw model output, or unbounded stderr/stdout.
Optional queue entries are sorted by category, identifier, and finding code so
identical inputs produce identical receipt bytes.

Alternative A was extending the capability receipt. It was rejected because
schema/config-write evidence has a smaller lifecycle and should not acquire
official-reference, provider, overlay, or policy ownership. Alternative B was
storing artifacts beside the launcher. It was rejected because the overlay and
provider-bound evidence belong to the profile and must survive launcher
regeneration as explicit manifest-owned state.

### Decision 5: Project only proven metadata and exact internal config changes

The configured source catalog is opened and digested without mutation. The
overlay is built from a deep structured copy. The active model slug must match
exactly one model object. When the source field is absent, the post-copy
semantic diff must contain exactly one added path,
`/models/<active-index>/multi_agent_version = "v2"`. When the source already
contains `"v2"`, the semantic diff must be empty.

Every other object, array, field, and value is preserved. The overlay never
adds or changes `tool_mode`, model/provider/API fields, reasoning settings,
instructions, modalities, or visibility. A missing model, duplicate slug,
unsupported source shape, source identity change, or broader diff blocks
promotion.

The internal profile-specific config projection:

- Points `model_catalog_json` to the managed overlay.
- Sets `features.multi_agent_v2 = true`.
- Preserves all unrelated profile-specific settings.

The authoritative config source that contributes `[agents].max_threads` is
edited with the existing Config Document machinery. Only that exact scalar
assignment is removed, and only after the isolated v2 probe passes. Duplicate,
non-scalar, syntactically ambiguous, concurrently changed, or multiply sourced
assignments block promotion. The section and unrelated agent settings remain.
If internal is active, the derived managed-home config is regenerated and
included in the same promotion bundle.

There is no fallback to v1. Missing/stale evidence, a failed v2 probe, or an
ambiguous config migration leaves the previous runtime effective and reports a
stable unhealthy finding.

Alternative A was editing the source catalog in place. It was rejected because
it destroys provenance and can overwrite provider-owned updates. Alternative B
was injecting untracked `-c` arguments only in the Desktop launcher. It was
rejected because shell and Desktop behavior would diverge and the stale
`agents.max_threads` source would remain.

### Decision 6: Promote all parity-sensitive runtime files through one journal

Generalize `commit_runtime_binding_pair()` into a compatibility-preserving
`commit_runtime_binding_bundle()`. Runtime rebind marker schema v3 contains an
ordered, exact allowlist of target paths and old/new states for:

- Internal manifest.
- Managed launcher.
- Capability receipt.
- Parity receipt.
- Managed catalog overlay.
- Internal profile config.
- The authoritative shared config only when the exact stale assignment is
  removed.
- Derived internal runtime config when the managed home is materialized.

Marker schemas v1 and v2 remain recoverable. Schema v3 rejects duplicate,
parent/child-overlapping, unexpected, symlinked, directory, or foreign targets.
Small text artifacts retain embedded old/new payloads and digests. Promotion
writes inactive overlay/receipts first, then config sources and derived config,
then launcher, and manifest last. A durable `prepared` marker rolls back;
`committed` rolls forward. Recovery accepts only the exact old or new state for
every target and fails closed on foreign bytes.

This is a multi-file recoverable transaction, not a claim that the filesystem
offers one atomic rename for all targets. Its contract is deterministic
convergence after interruption while never accepting a mixed foreign state.

Alternative A was chaining independent atomic writes. It was rejected because
a crash could bind a new launcher to an old overlay or mark a receipt active
before the required config migration. Alternative B was putting parity repair
inside the general profile-switch journal. It was rejected because runtime
rebind has a smaller exact write set and already owns launcher/manifest
promotion.

### Decision 7: Stage internal updates beside the bound binary

`update-internal` becomes prepare-then-promote:

1. Resolve the bound internal binary and intended semantic version.
2. Run the trusted team installer with `CODEX_INSTALL_DIR` set to a private
   sibling staging directory instead of the bound directory.
3. Validate the candidate executable, version, mode, code signature where
   applicable, generated schema, capability receipt, parity inventory, overlay,
   config projection, and bounded behavior probes.
4. Acquire the store mutation lock and revalidate binary, config, source
   catalog, official reference, and manifest fingerprints.
5. Write a durable promotion marker that includes the runtime bundle plus an
   executable-swap entry containing exact bound/candidate/backup paths, modes,
   and digests. Binary bytes are not embedded in JSON.
6. Rename the old binary to its fixed sibling backup, promote the candidate to
   the bound path, promote the runtime bundle, mark committed, and run the
   post-promotion binding/parity handshake.
7. Retire the old backup only after the handshake succeeds.

Recovery accepts only the expected old/new binary digests and exact sibling
paths. A `prepared` marker restores the old binary and old runtime bundle; a
`committed` marker converges to the new pair. A failed probe or parity check
never replaces the bound binary. `--dry-run` prints the candidate, artifact,
probe, and promotion plan without installer, profile, or filesystem mutation.

`set-bin internal <external-path>` uses the same parity preparation and runtime
bundle but does not move or copy the externally owned backend.

Alternative A was retaining the current in-place installer and delaying backup
deletion. It was rejected because the bound path is still unavailable or
partially replaced while the installer and parity probes run. Alternative B was
copying a large binary into the text journal. It was rejected because sibling
rename state with digest validation is smaller and recoverable.

### Decision 8: Diagnostics and packaging consume, but do not recreate, policy

Internal rebind and update are the only write paths that prepare/promote parity
artifacts. Normal status, Doctor, and verify load and validate the manifest,
receipt, overlay, capability receipt, current official reference, current
internal backend, and config digests.

- Missing, stale, malformed, core-drift, probe-failed, or unclassified evidence
  is unhealthy with stable finding codes.
- Optional drift remains visible and is emitted as the receipt's deterministic
  synchronization queue.
- Read-only verification never repairs, rewrites, downloads, or reclassifies.
- Explicit repair routes back through the same staged rebind preparation.
- Release packaging includes the parity module and validates that all generated
  launchers/imports resolve inside the immutable payload.

The official release advisory remains separate. It can recommend a newer
official stable release but cannot replace the current bundled-reference
fingerprint.

### Decision 9: Desktop acceptance proves typed Subagent behavior and ownership

Automated tests use fake binaries and isolated real-binary probes. Final live
acceptance is a separate Human Gate because it requires a full ChatGPT restart
and a real internal task.

After authorization, acceptance:

1. Confirms ChatGPT main-process identity and `CODEX_CLI_PATH`.
2. Confirms the managed launcher, proxy parent, exact internal backend child,
   capability receipt, parity receipt, overlay, and active config digests.
3. Starts a fresh Desktop task that explicitly requests an `explorer` role with
   a bounded instruction to return `parity-subagent-ok`.
4. Confirms the parent emits a spawn item, the child thread source is
   `thread_spawn`, `agentRole` is `explorer`, and the child exposes a non-empty
   task-oriented title/description rather than relying only on a random
   nickname.
5. Confirms the child and parent completion markers and re-attests the same
   proxy/backend/receipt/overlay ownership after completion.

A successful generic turn, an untyped child, a v1 nickname-only result, a
completion marker from the parent alone, or an unattested backend cannot satisfy
this gate.

## Completion Contract

- The official reference is the verified current ChatGPT bundled CLI and is
  digest-bound.
- Every observed difference is fixed-whitelist, core, optional, or
  unclassified; unclassified never passes.
- Every core protocol path is native-compatible or covered by one exact
  capability-proven Protocol Adapter rule.
- The managed overlay changes only active-model `multi_agent_version` to `v2`
  and preserves the source catalog.
- Internal v2 config projection and exact stale-assignment migration are
  transactional and have no v1 fallback.
- Rebind interruption converges manifest, launcher, both receipts, overlay, and
  config to all-old or all-new state.
- Internal update does not replace or retire last-known-good before candidate
  parity and post-promotion handshake pass.
- Status, Doctor, verify, reports, and packaged runtime agree on receipt health
  and stable finding codes.
- Focused parity, protocol, runtime, transaction, profile, verify, and
  update/release tests pass on Python 3.9 and 3.12 where the existing suites
  require both.
- Strict OpenSpec, workflow, shell, AST/import, package, diff, and live Desktop
  acceptance evidence are recorded before completion.

## Critical Path

Reference fingerprint and inventories -> direction-aware classification ->
managed overlay/config projection -> provider-bound receipt and probes ->
recoverable runtime bundle -> staged internal update -> diagnostics/package
integration -> explicitly authorized Desktop Subagent acceptance.

## Incidental Finding Budget

One bounded RED/GREEN guard may cover a newly observed drift inside an already
classified core method closure. A new method/feature, broader overlay field,
provider/model/auth change, public CLI change, new dependency, or additional
live effect is `BLOCKED_AWAITING_HUMAN`.

The retained v2 probe directory contains a copied runtime config with
credential-bearing provider settings. This planning change does not delete or
rewrite retained evidence. New probes must construct minimal credential-free
persisted configs, keep transient credential transport out of receipts/logs,
and sanitize bounded output. Cleanup of existing retained evidence remains a
separate explicit authorization.

Known optional drift is `DEFER_AND_CONTINUE` only through the synchronization
queue. It is never silently emulated or promoted to the Critical Path.

## Risks / Trade-offs

- [The bundled alpha reference can change with a Desktop update] -> bind every
  receipt to bundle and binary digests and require regeneration after change.
- [JSON Schema compatibility is more complex than raw equality] -> limit the
  comparator to the generated draft and supported direction/method closures;
  unknown constructs fail closed.
- [Optional-unless-observed can become required] -> record the acceptance trace
  and automatically escalate a surface that appears in it.
- [Removing `agents.max_threads` changes an old tuning value] -> remove only the
  exact incompatible assignment after v2 proof and preserve rollback bytes in
  the journal.
- [Source catalog changes after overlay preparation] -> revalidate identity and
  digest under the store lock before promotion.
- [A multi-file journal is not single-syscall atomic] -> use durable marker
  states, exact old/new validation, ordered activation, and deterministic
  recovery.
- [Binary promotion crosses the store and install directory] -> restrict it to
  validated sibling paths and exact digests; foreign state blocks recovery.
- [Live Subagent behavior depends on the provider] -> keep it behind an
  explicit Human Gate and require both behavioral marker and runtime ownership
  evidence.

## Migration Plan

No eager mutation runs merely because the new code is installed. A read-only
verify against an old internal manifest reports missing parity evidence and the
explicit rebind remediation.

The next authorized internal rebind or update prepares the overlay, parity
receipt, profile config projection, exact stale config migration, launcher, and
capability receipt in isolation. If internal is active, it also stages the
derived runtime config. The generalized bundle promotes them together.

An interrupted schema-v3 bundle is recovered before any later switch, rebind,
update, or repair. Existing schema-v1/v2 rebind markers retain their current
recovery behavior.

Rollback restores the old binary when update owns it and restores every old
text artifact from the journal. The configured source catalog is never a
rollback target because parity never modifies it.

## Continuation Policy

- Current boundary: planning only; stop for user review after strict OpenSpec
  and workflow validation.
- Execution policy after approval: `auto-until-terminal`.
- Canonical execution source: this change's `tasks.md`.
- Select only the next dependency-ready parity task after its predecessor's
  RED/GREEN evidence and main-agent review pass.
- Genuine Human Gates: broader classification/overlay policy, public CLI
  expansion, provider/model/endpoint/auth change, dependency addition, live
  internal update, ChatGPT restart/Desktop task, destructive cleanup, release,
  commit, push, and archive.
- Ordinary successful items continue with `CONTINUE_NEXT_ITEM`; unexpected
  production-contract failure uses `BLOCKED_AWAITING_HUMAN`; optional findings
  use `DEFER_AND_CONTINUE`; bounded in-scope guards use
  `CONTINUE_WITH_MINIMAL_GUARD`; completed change validation uses
  `VERIFY_ACTIVE_CHANGE`; terminal completion uses `COMPLETE`.

## Open Questions

None.
