# Internal Official Feature Parity Implementation Plan

**Goal:** Make the internal profile provably compatible with the current
ChatGPT bundled Codex core contract while preserving only its binary, model,
endpoint, provider, and auth differences.

**Architecture:** A new `codex_switch_parity.py` deep module owns deterministic
official/internal inventories, classification, the provider-bound parity
receipt, managed catalog overlay, config projection, and bounded probes.
Existing Runtime Binding, Protocol Adapter, Capability Receipt, Config
Document, and transaction modules retain their current ownership and expose
only the evidence or promotion seams parity needs.

**Tech Stack:** Python 3.9/3.12 standard library, Bash entrypoints, generated
JSON Schema, TOML through the existing Config Document, `unittest`, macOS
process/bundle inspection, existing release packaging.

## Global Constraints

- The official reference is the verified current ChatGPT bundled CLI, never
  PATH or network latest.
- The fixed allowed differences are internal binary, model, endpoint, provider,
  and auth only.
- The configured source model catalog is read-only.
- The initial managed overlay may add only active-model
  `multi_agent_version = "v2"`; it never adds `tool_mode`.
- Unknown/unclassified drift and failed/unknown v2 evidence are unhealthy.
- There is no silent v1 fallback.
- No production dependency, provider/model/endpoint/auth migration, public
  compatibility expansion, release, commit, push, archive, destructive
  cleanup, retained-probe cleanup, or live App/update effect without its
  explicit Human Gate.
- Production writes are serialized. OpenSpec, root control-plane files,
  verification evidence, package/release metadata, and final integration remain
  main-agent owned.
- Preserve all unrelated worktree changes.

## Layered Validation Budget and Complexity Gate

- Task-local validation runs only the focused regression needed for the current
  acceptance criterion.
- Slice closure, including task 5.10, runs that slice's complete required
  Python 3.12/system-Python 3.9 matrix.
- Integrated and final gates in tasks 7.x and 9.x own full-project
  verification.
- An adjacent task MUST NOT repeat the same complete suite unless related code
  changed after the recorded result, the result was started but not collected,
  or a real failure requires rerunning it.
- Before adding a shared abstraction, another fault axis, or an edge test not
  required by the current acceptance criteria, name the failing acceptance
  criterion it repairs. Otherwise record the observation as
  `DEFER_AND_CONTINUE`; it does not block the current item.

## Target State

Internal rebind and update prepare a deterministic parity bundle against the
current bundled reference, prove core schema/config/v2 behavior, and promote
manifest, launcher, capability receipt, parity receipt, overlay, and exact
config artifacts through one recoverable journal. Read-only diagnostics consume
that evidence and distinguish unhealthy core drift from a deterministic
optional synchronization queue. Final completion includes a real typed-role
Desktop Subagent acceptance after explicit authorization.

## Completion Contract

- Every one of the 75 delta scenarios has a focused regression or an explicit
  live acceptance check.
- Core protocol drift is native-compatible or covered by one exact
  capability-proven adapter rule.
- The saved task-8.3 diagnostic's two core-feature, eight core-protocol, and
  three unclassified-protocol errors close as one RED/GREEN slice. No subset
  can be suppressed or accepted independently.
- Every incompatible method has one exact coverage record; semantic
  equivalence, actual adapter transformation, and optional extension
  classification are distinct dispositions.
- Receipt schema v2 binds exact coverage and final post-probe policy evidence;
  schema-v1 receipts cannot imply coverage.
- The overlay and source catalog pass structural equality outside the single
  approved metadata path.
- Profile v2 projection and exact `agents.max_threads` migration are proven
  before promotion.
- Schema-v3 runtime bundle interruption converges to all-old or all-new state;
  foreign bytes fail closed.
- Internal update preserves the bound binary and last-known-good until parity
  and post-promotion handshake pass.
- Status, Doctor, verify, reports, and packaged runtime share receipt health and
  stable findings.
- Focused and broad Python 3.9/3.12 suites, strict OpenSpec, DevFlow workflow,
  shell, AST/import, package, and diff checks pass.
- The explicitly authorized live Desktop acceptance proves typed `explorer`
  child metadata, child/parent markers, and full launcher/proxy/backend/receipt/
  overlay ownership.

## Acceptance Criteria

- Planning may enter implementation only when OpenSpec reports all artifacts
  complete, strict change/all validation passes, the AI plan lint passes, and
  the design/spec/task review gate is explicitly cleared.
- All 12 requirements and 75 scenarios map to a named automated regression or
  the explicit live Desktop acceptance, with exact evidence recorded before
  the corresponding task is checked.
- The parity module is the only owner of official-reference, classification,
  overlay, and synchronization-queue policy; authority scans find no duplicate
  policy in Runtime Binding, Protocol Adapter, Capability Receipt, or callers.
- The five allowed identity differences remain unchanged, the source catalog is
  byte-preserved, and every unknown or unclassified non-whitelisted drift
  blocks promotion.
- Rebind and update interruption tests prove all-old or all-new runtime state,
  retain last-known-good until the complete handshake succeeds, and reject
  foreign target or binary state.
- Status, Doctor, verify, reports, and the packaged runtime consume the same
  receipt health and stable finding codes without write-on-read repair or
  sensitive evidence retention.
- No install, profile/App mutation, provider-backed probe, ChatGPT restart, or
  live Desktop acceptance occurs before task 8.1 receives explicit approval.

## Critical Path

Reference/inventory -> exact method coverage -> pre-probe eligibility ->
bounded probes -> final policy/receipt -> recoverable bundle -> rebind ->
staged update -> diagnostics/package -> live Desktop acceptance -> final
evidence.

## Incidental Finding Budget

One bounded RED/GREEN guard may cover a newly exposed issue inside an already
classified core method closure and approved write set. A new method or feature,
broader overlay field, public CLI contract, provider/model/auth change,
dependency, destructive cleanup, or additional live effect is
`BLOCKED_AWAITING_HUMAN`. Known optional drift is recorded as
`DEFER_AND_CONTINUE`; it is not implemented during this change.

## Escalation Triggers

- Official or internal binary changes while a task is in progress.
- A generated schema construct cannot be classified directionally.
- A new difference has no explicit policy entry.
- The active model is missing or duplicated in the source catalog.
- Config ownership or `agents.max_threads` source is ambiguous.
- A task needs a path outside its recorded write set.
- A schema-v3 recovery target contains foreign state.
- A staged installer needs to write outside the validated sibling directory.
- Any test would require real provider traffic, live profile mutation, or a
  ChatGPT restart before the Human Gate.

## File Structure

Create:

- `scripts/codex_switch_parity.py`: parity policy, inventory, receipt, overlay,
  probes, and verification interface.
- `scripts/test_codex_parity.py`: focused parity RED/GREEN suite.
- `testdata/parity/retained-v2-probe-redacted.json`: sanitized provider-shaped
  retained probe fixture; excluded from release payloads.
- `.planning/devflow/verification/internal-official-feature-parity.md`: exact
  execution and acceptance evidence.

Modify only as required:

- `scripts/codex_switch_protocol_adapter.py` and
  `scripts/test_codex_protocol_config.py`: deterministic adapter rule-set
  evidence only; no parity policy.
- `testdata/parity/current-method-coverage-redacted.json`: sanitized exact
  task-8.3 method/schema/reason/extension evidence; excluded from release
  payloads.
- `scripts/codex_switch_config_document.py`,
  `scripts/codex_switch_home_sync.py`, and their focused/profile tests: exact
  config projection and active-home derivation.
- `scripts/codex_switch_bindings.py`, `scripts/codex_switch_app_wrapper.py`,
  `scripts/codex_switch_runtime_binding.py`, `scripts/codex_switch_shim.py`,
  and runtime-binding/profile tests: staged parity preparation and one exact
  shell/Desktop generation contract for internal rebind.
- `scripts/codex_switch_transaction.py` and
  `scripts/test_codex_transaction.py`: schema-v3 runtime bundle and binary-swap
  recovery while preserving v1/v2 markers.
- `scripts/codex-switch`, `scripts/codex_env_setup`,
  `scripts/codex_switch_promotion.py`, and
  `scripts/test_codex_update_release.py`: sibling candidate update and
  last-known-good handshake.
- `scripts/codex_switch_verify.py`, Doctor/status modules,
  `scripts/test_codex_verify.py`, and profile tests: shared parity findings and
  synchronization queue.
- `scripts/codex_switch_release_bundle.py`,
  `scripts/codex_switch_promotion.py`, `scripts/package-release.sh`, package
  validation tests, `install.sh`, `run.sh`, `README.md`, and `SKILL.md`:
  packaged runtime, immutable promotion, bootstrap trust anchors, and operator
  contract. The `install.sh`/`run.sh` parity-change ownership is limited to
  hashes that bind the current verified release-bundle and promotion modules.
- This change's OpenSpec artifacts, `TASK_LEDGER.md`, `.planning/STATE.md`, and
  the parity verification record: main-agent control plane.

## 1. Reference, Inventory, and Classification

- [x] 1.1 Add RED `ParityReferenceTests` in
  `scripts/test_codex_parity.py` for verified ChatGPT bundle selection, PATH and
  network-latest rejection, fixed allowed-difference whitelist, and stale
  reference fingerprints.
- [x] 1.2 Run
  `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v` and
  record the expected missing-module/reference failures before implementation.
- [x] 1.3 Create `scripts/codex_switch_parity.py` with immutable
  `OfficialReference`, `InternalFingerprint`, `ParityCandidate`,
  `ParityFinding`, `ParityQueueItem`, `ParityReport`, and policy-version types;
  implement canonical reference/fingerprint validation and make 1.1 GREEN.
- [x] 1.4 Add RED `ParityFeatureInventoryTests` proving isolated defaults are
  distinct from effective config, official/internal-only features are retained,
  ordering is deterministic, malformed output fails closed, and identical
  input produces identical canonical bytes.
- [x] 1.5 Implement bounded feature-list execution and parsing behind an
  injected runner; make 1.4 GREEN without reading or writing live config.
- [x] 1.6 Add RED `ParityProtocolInventoryTests` for all four protocol
  directions, method extraction, transitive local-reference closure,
  documentation-field removal, deterministic ordering, additive optional
  compatibility, required-field/enum incompatibility, reference cycles, and
  unsupported constructs.
- [x] 1.7 Implement method-scoped schema normalization and the direction-aware
  compatibility evaluator; make 1.6 GREEN and keep it private to the parity
  module.
- [x] 1.8 Add RED adapter-evidence tests in
  `scripts/test_codex_protocol_config.py` proving the existing Protocol Adapter
  exposes one deterministic rule-set digest without importing parity policy.
- [x] 1.9 Implement the adapter rule-set digest from the existing exact
  transform tables and bind it into parity input; make 1.8 GREEN.
- [x] 1.10 Add RED `ParityPolicyTests` for core baseline closures,
  `multi_agent_v2`, the six optional-unless-observed methods, `skill_search`,
  known under-development features, stage/default-only drift,
  pending-provider `tool_mode`, observed escalation, and unknown drift.
- [x] 1.11 Implement the explicit versioned classification table, stable
  finding-code families, severity/health rules, and deterministic queue sorting;
  make 1.10 GREEN.
- [x] 1.12 Add and pass serialization tests proving no credential value or
  digest, auth/query header, raw config, raw prompt, raw model output, absolute
  temporary probe path, or unbounded process text enters inventory/receipt
  payloads.
- [x] 1.13 Run the complete parity suite on Python 3.12 and system Python 3.9;
  record exact counts before selecting task 2.

## 2. Provider Receipt and Managed Overlay

- [x] 2.1 Add RED `ParityReceiptTests` for canonical payload bytes, policy
  version, complete fingerprints/digests, mode-`0600` profile-local paths,
  manifest metadata, missing/symlink/non-regular/oversized/malformed receipts,
  digest drift, provider/runtime staleness, and optional queue health.
- [x] 2.2 Implement safe bounded receipt serialization/loading and
  `profiles/internal/parity/{receipt.json,model-catalog.json}` path resolution;
  make 2.1 GREEN without adding receipt preparation to callers.
- [x] 2.3 Add RED `ParityOverlayTests` for unique active-model selection,
  absent-to-v2 single-path addition, already-v2 zero semantic diff, deep
  preservation, source byte/mode preservation, duplicate/missing slug,
  unsupported root, `tool_mode` rejection, broader mutation rejection, and
  source identity/digest races.
- [x] 2.4 Implement no-follow/identity-checked catalog reading, structured deep
  copy, exact JSON-pointer diff validation, canonical overlay bytes, and source/
  overlay digest evidence; make 2.3 GREEN.
- [x] 2.5 Add RED manifest-candidate tests proving parity receipt/overlay paths,
  payload digests, policy version, official-reference digest, source-catalog
  digest, and adapter/capability receipt digests are complete before promotion.
- [x] 2.6 Implement `ParityBundle` and manifest metadata preparation, keeping
  generated artifacts in a private staging root until the transaction task.
- [x] 2.7 Run parity/overlay focused tests under Python 3.9 and 3.12 and use
  structural comparison to prove the fixture source catalogs remain
  byte-identical.

## 3. Config Projection and Bounded Probes

- [x] 3.1 Add RED config-projection tests in
  `scripts/test_codex_parity.py` and
  `scripts/test_codex_config_document.py` for internal-only
  `model_catalog_json`, `features.multi_agent_v2 = true`, unrelated setting
  preservation, exact scalar `[agents].max_threads` removal, retained section/
  sibling keys, and already-clean idempotence.
- [x] 3.2 Add RED ambiguity/TOCTOU tests for duplicate, dotted, non-scalar,
  invalid TOML, multiply sourced, symlinked, and concurrently changed
  `agents.max_threads`; require zero writes and an unhealthy finding.
- [x] 3.3 Extend the Config Document with the smallest exact key-removal/
  projection interface required by 3.1-3.2, reparse every result, and make both
  RED groups GREEN without adding a generic TOML rewrite framework.
- [x] 3.4 Add RED home-sync tests proving the internal profile config and shared
  source produce a derived managed-home config with overlay/v2 and without
  stale max threads, while official/shared source bytes and unrelated profile
  settings remain correct.
- [x] 3.5 Integrate parity config projection with the existing canonical home
  sync and produce a staged active-runtime config payload when internal is
  materialized; make 3.4 GREEN without committing it.
- [x] 3.6 Add RED `ParityProbeTests` for candidate-only artifacts,
  initialize/core-method ordering, typed `explorer` v2 marker, no v1 fallback,
  timeout, malformed/missing responses, early exit, oversized output, process-
  group termination, stale candidate inputs, and bounded sanitizer behavior.
- [x] 3.7 Implement injected bounded probe orchestration using the existing
  structured smoke/sanitizer primitives; persist only status codes and evidence
  digests and make 3.6 GREEN.
- [x] 3.8 Add a retained-probe regression fixture that contains redacted
  provider structure but no credential material; prove the new probe path never
  copies a live credential-bearing config into retained evidence.
- [x] 3.9 Run parity, Config Document, home-sync/profile focused, and verify
  sanitizer suites on Python 3.9 and 3.12 before selecting task 4.

## 4. Recoverable Runtime Bundle and Internal Rebind

- [x] 4.1 Add RED schema-v3 journal tests in
  `scripts/test_codex_transaction.py` for the exact manifest, launcher,
  capability receipt, parity receipt, overlay, profile config, optional shared
  config, and optional active runtime config target set.
- [x] 4.2 Add RED target-safety tests for duplicate, unexpected, parent/child-
  overlapping, symlinked, directory, missing-required, mode-invalid, digest-
  invalid, oversized embedded payload, and foreign old/new states before any
  marker or target write.
- [x] 4.3 Generalize `commit_runtime_binding_pair()` to
  `commit_runtime_binding_bundle()` with typed text-artifact entries, exact
  allowlist validation, deterministic activation order, manifest-last
  semantics, and a schema-v3 marker; retain the old function as a compatibility
  adapter until all callers/tests migrate.
- [x] 4.4 Add a fault-injection RED/GREEN matrix at marker write, each inactive
  artifact, config source, derived config, launcher, manifest, committed marker,
  and marker retirement; prove prepared rollback and committed roll-forward
  converge every target.
- [x] 4.5 Add and pass legacy schema-v1/v2 marker fixtures proving their
  established recovery behavior remains byte-compatible and is never
  reinterpreted as schema v3.
- [x] 4.6 Add RED internal `set-bin` tests in
  `scripts/test_codex_runtime_binding.py` and
  `scripts/test_codex_profile_switch.py` proving parity preparation precedes
  launcher smoke, failed/unknown/core/unclassified evidence promotes nothing,
  the source catalog remains unchanged, and successful staging supplies the
  complete bundle.
- [x] 4.7 Integrate `prepare_parity_bundle()` into
  `scripts/codex_switch_bindings.py`, pass parity/overlay/config metadata into
  the generated launcher/manifest as required, and commit only through the
  schema-v3 bundle after existing child-backend attestation passes.
- [x] 4.8 Add RED launcher/shell equivalence tests proving both internal
  Desktop and shell execution consume the same projected managed-home config,
  overlay, v2 contract, and receipt generation; reject an old launcher/new
  manifest or new launcher/old overlay mix.
- [x] 4.9 Remove the compatibility adapter only after `rg` proves every current
  runtime-rebind caller and test uses the bundle interface; retain marker
  schema-v1/v2 recovery functions.
- [x] 4.10 Run parity, runtime binding, transaction, Protocol Adapter, and
  profile suites serially on Python 3.9 and 3.12; review the integrated diff
  before selecting task 5.

## 5. Staged Internal Binary Update

- [x] 5.1 Add RED update tests in `scripts/test_codex_update_release.py` for a
  validated private sibling install directory, unchanged bound binary during
  install/probe, intended-version checks, code-sign step ordering, parity-before-
  replacement, helper failure propagation, and zero-mutation dry-run output.
- [x] 5.2 Refactor `scripts/codex_env_setup` so the trusted installer can target
  an explicit validated candidate directory without moving or replacing the
  bound binary; keep provider/model/endpoint/auth inputs unchanged and make the
  installer portion of 5.1 GREEN.
- [x] 5.3 Add RED executable-swap journal tests for exact bound/candidate/backup
  siblings, no embedded binary bytes, mode/digest checks, prepared rollback,
  committed roll-forward, interruption before/after each rename, and foreign
  binary preservation.
- [x] 5.4 Extend the schema-v3 promotion plan with a typed executable-swap entry
  using sibling rename/digest recovery, or reuse an existing promotion primitive
  only if it satisfies the same exact contract; make 5.3 GREEN.
- [x] 5.5 Add RED wrapper tests proving `scripts/codex-switch update-internal`
  prepares capability/parity/config/overlay artifacts against the staged
  candidate, revalidates all fingerprints under the store lock, and never calls
  the bound-path compatibility smoke first.
- [x] 5.6 Integrate candidate staging, parity preparation, executable swap, and
  runtime bundle promotion into `run_update_internal_env_setup`; do not report
  success until the installed version, canonical binding, app-server smoke,
  capability receipt, and parity receipt postconditions all pass.
- [x] 5.7 Add RED handshake-failure tests proving the old binary backup and old
  runtime bundle are restored when version, binding, app-server, receipt,
  overlay, config, or parity verification fails after promotion.
- [x] 5.8 Retire the old binary backup only after the complete handshake; add
  restart-required output only after durable success and make 5.7 GREEN.
- [x] 5.9 Prove `set-bin internal <external-path>` uses the same parity bundle
  without copying, moving, deleting, or claiming ownership of the external
  backend.
- [x] 5.10 Run the complete update/release, transaction, runtime binding,
  parity, and profile suites on Python 3.9 and 3.12 before selecting task 6.

## 6. Diagnostics, Repair Routing, Packaging, and Docs

- [x] 6.1 Add RED verifier tests in `scripts/test_codex_verify.py` for missing,
  malformed, stale reference/runtime/provider/config/overlay/adapter evidence,
  core drift, unclassified drift, probe failure, optional-only queue, stable
  finding codes, report sanitization, and `--repair=none` zero writes.
- [x] 6.2 Implement parity receipt loading/evaluation in
  `scripts/codex_switch_verify.py`, reuse the same result in structured reports,
  and make 6.1 GREEN without regenerating evidence.
- [x] 6.3 Add RED status/Doctor/profile tests proving status, Doctor, and verify
  print the same health codes and queue ordering and distinguish optional sync
  work from unhealthy core drift.
- [x] 6.4 Integrate parity reporting into the narrow status and Doctor modules
  that already consume Runtime Binding/capability evidence; make 6.3 GREEN and
  avoid a second policy implementation.
- [x] 6.5 Add RED repair-routing tests proving an explicit parity repair routes
  through staged internal rebind, while normal status/Doctor/verify never patch
  receipt, overlay, config, launcher, or manifest in place.
- [x] 6.6 Implement the smallest existing-command repair route, preferring
  `set-bin internal <current-backend>` over a new public CLI surface unless the
  approved spec is updated first.
- [x] 6.7 Add package/release RED tests for the parity module, transitive
  imports, generated launcher references, immutable payload file set, and
  absence of retained probe/config evidence; update `scripts/package-release.sh`
  and make them GREEN.
- [x] 6.8 Update `README.md` and `SKILL.md` with the official-reference
  boundary, core versus optional findings, no-v1-fallback remediation, staged
  update semantics, and the explicit live Desktop acceptance gate.
- [x] 6.9 Run `rg` authority scans proving Runtime Binding contains no parity
  classification, Protocol Adapter contains no provider/overlay policy,
  Capability Receipt contains no official-reference policy, and parity has one
  production implementation.
- [x] 6.10 Run focused verifier, Doctor/status, package, parity, profile, and
  update/release suites on Python 3.9 and 3.12 before selecting task 7.

## 7. Integrated Verification and Main Review

- [x] 7.1 Run
  `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v` and the
  same command with system Python 3.9; require zero failures.
- [x] 7.2 Run the Protocol Adapter, Runtime Binding, transaction, verifier,
  update/release, and complete profile suites serially on Python 3.12, then
  repeat the project-required dual-runtime suites on Python 3.9.
- [x] 7.3 Run
  `openspec validate internal-official-feature-parity --strict --no-interactive`
  and `openspec validate --all --strict --no-interactive`; require zero
  validation failures.
- [x] 7.4 Run
  `python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json`
  and record every gate/result without editing generated guidance.
- [x] 7.5 Run Bash syntax for `scripts/codex-switch`,
  `scripts/codex_env_setup`, `install.sh`, `run.sh`, and
  `scripts/package-release.sh`; run Python 3.9/3.12 AST and production-import
  scans with bytecode disabled.
- [x] 7.6 Build and validate an isolated package from a safe `mktemp -d`
  destination, verify manifest/file/mode/import integrity, and prove no
  credential-bearing or retained-probe file is packaged.
- [x] 7.7 Run `git diff --check`, exact changed-file/write-set review, adapter/
  runtime/parity ownership scans, and a scenario-to-test coverage audit for all
  66 scenarios.
- [x] 7.8 Perform a read-only main-agent code review focused on false health,
  unsafe config/source mutation, transaction recovery, binary replacement,
  secret persistence, broad adapters, and missing rollback tests; resolve all
  in-scope findings before the Human Gate.
- [x] 7.9 Record commands, counts, RED/GREEN evidence, changed files, finding
  codes, receipt/overlay fixture digests, package result, residual optional
  queue, and live-gate prerequisites in
  `.planning/devflow/verification/internal-official-feature-parity.md`.

## 8. Human Gate and Live Desktop Acceptance

- [x] 8.1 Stop and obtain explicit user authorization for the supported local
  source install, same-backend parity rebind, full ChatGPT quit/reopen, real
  provider-backed typed Subagent task, and resulting profile/App mutations.
- [x] 8.2 After authorization, install the exact verified source only through:
  `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch CODEX_SWITCH_PYTHON="$(command -v python3.12)" /Users/cY/dev/codex-switch/install.sh`;
  verify immutable installed payload identity before any restart.
- [ ] 8.3 Close the saved same-backend preparation failure as one complete
  method-scoped evidence RED/GREEN, then—only after both new Human Gates—run
  the supported same-backend parity preparation/rebind for
  `/Users/cY/.local/bin/codex`, record the promoted manifest/capability receipt/
  parity receipt-v2/coverage/overlay/config digests, and require a clean status,
  Doctor, and `verify internal --repair=none`.

  **Saved RED authority:** the 2026-07-27 sanitized diagnostic is the exact
  acceptance failure: two `parity.feature.core_drift`, eight
  `parity.protocol.core_incompatible`, and three
  `parity.protocol.unclassified_drift` findings. Its eleven method-schema
  pairs, reason codes, and bounded extension facts are copied into
  `testdata/parity/current-method-coverage-redacted.json`; raw schema bundles,
  config, prompts, credentials, and process output are not copied.

  **Planning-only write set consumed by this revision:** only
  `openspec/changes/internal-official-feature-parity/{proposal.md,design.md,tasks.md,specs/codex-switch/spec.md}`,
  `TASK_LEDGER.md`, `.planning/STATE.md`,
  `.planning/devflow/verification/internal-official-feature-parity.md`, and
  `.planning/checkpoints/2026-07-27-parity-method-coverage-repair-planned.md`.
  No source, test, fixture, operator-doc, installed, live, dependency, or Git
  write belongs to the planning revision.

  **Implementation write set after `PARITY-8.3-IMPLEMENT`:**

  - production: `scripts/codex_switch_protocol_adapter.py`,
    `scripts/codex_switch_parity.py`;
  - tests/evidence fixture: `scripts/test_codex_protocol_config.py`,
    `scripts/test_codex_parity.py`,
    `testdata/parity/current-method-coverage-redacted.json`;
  - operator contract: `README.md`, `SKILL.md`;
  - main-owned canonical artifacts:
    `openspec/changes/internal-official-feature-parity/{proposal.md,design.md,tasks.md,specs/codex-switch/spec.md}`,
    `TASK_LEDGER.md`, `.planning/STATE.md`,
    `.planning/devflow/verification/internal-official-feature-parity.md`,
    `.planning/checkpoints/2026-07-27-parity-method-coverage-repair-red.md`,
    `.planning/checkpoints/2026-07-27-parity-method-coverage-repair-verified.md`,
    and
    `.planning/checkpoints/2026-07-27-parity-method-coverage-live-retry.md`.

  Any production/test/doc path outside that list is
  `BLOCKED_AWAITING_HUMAN`. Existing unrelated dirty paths remain untouched.
  Receipt consumers may be validated but not edited unless a concrete failing
  contract first proves the required write-set expansion and the user approves
  it.

  **RED tests:**

  1. Protocol Adapter evidence tests fail because the current global digest
     does not expose or bind the existing `thread/resume` ID/opaque-reasoning
     transform as a structured direction/method rule.
  2. Parity comparator tests fail because equivalent
     `anyOf(null,string)`/`type:[null,string]` forms still produce four core
     incompatibilities.
  3. The exact retained coverage fixture produces all thirteen saved error
     findings and proves the current policy stops before probes.
  4. Receipt tests fail because schema v1 has no sorted method-coverage or
     final post-probe evidence.
  5. Negative tests require changed schema digests, changed rule digests,
     missing rule IDs, reason-only/method-only/global-digest-only matches,
     newly observed optional extensions, failed typed-v2 evidence, and another
     observed `item_ids` dependency to remain unhealthy.

  The named test contract is:

  ```text
  ProtocolAdapterEvidenceTests
    test_rule_manifest_binds_every_actual_transform
    test_thread_resume_transform_and_manifest_share_one_rule
  ParityProtocolInventoryTests
    test_nullable_union_spellings_are_semantically_equal
  ParityMethodCoverageTests
    test_retained_thirteen_error_fixture_closes_only_as_one_final_policy
    test_global_method_reason_and_schema_pair_only_evidence_fail_closed
    test_exact_optional_extensions_escalate_when_observed_or_changed
    test_item_ids_requires_exact_resume_rule_and_no_other_dependency
    test_multi_agent_v2_requires_final_typed_probe
  ParityReceiptTests
    test_receipt_v2_round_trip_binds_sorted_method_coverage
    test_receipt_v1_cannot_imply_coverage
  ParityBundleTests
    test_uncovered_drift_stops_before_probe_and_final_policy_precedes_receipt
  ```

  **GREEN implementation contract:**

  1. Protocol Adapter exposes one canonical structured manifest for actual
     transforms; its rule-set digest is derived from that manifest, and the
     `thread/resume` production transform consumes the same named rule
     definition tested by the evidence suite.
  2. Parity canonicalizes the four nullable-string spellings as semantic
     equivalents and never labels them adapter-covered.
  3. Parity owns exact schema-pair dispositions for the current realtime/audio,
     Bedrock login, external-agent import, and listed-share extensions. Each
     produces a stable extension-level optional queue identifier only while
     unobserved; a fingerprint or observation change fails closed.
  4. `item_ids` is satisfied only through the exact observed resume-path rule;
     `multi_agent_v2` is provisional only through pre-probe eligibility and
     becomes healthy only after exact overlay/config and typed-v2 probe
     evidence.
  5. Preparation runs inventory/coverage, fail-closed eligibility, bounded
     probes, fingerprint revalidation, final policy, then receipt-v2
     construction. Unknown/uncovered drift stops before probes.
  6. The exact retained fixture finishes with zero errors for all thirteen
     saved findings and the exact deterministic optional queue. Removing any
     single proof recreates a stable error; no partial GREEN can pass.
  7. Receipt-v2 canonical round-trip, size/path checks, staleness, diagnostics,
     manifest ownership, and transaction inputs remain deterministic.
     Receipt-v1 is rejected as stale/unsupported and is never patched in place.

  **Focused implementation validation:**

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v
  PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v
  ```

  After those pass, run the unchanged receipt consumers read-only:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_verify.py -v
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_verify.py -v
  PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v
  ```

  Then run active/all strict OpenSpec, AI-plan lint, DevFlow workflow
  validation, dual-runtime AST/import for touched Python, isolated package
  validation, targeted/full `git diff --check`, exact write-set audit, and
  source-versus-package identity. Do not install or retry the live command from
  implementation verification.

  Exact source/package/control-plane commands:

  ```bash
  PYTHONDONTWRITEBYTECODE=1 python3.12 -c 'import ast, pathlib; [ast.parse(pathlib.Path(path).read_text(), filename=path) for path in ("scripts/codex_switch_protocol_adapter.py", "scripts/codex_switch_parity.py", "scripts/test_codex_protocol_config.py", "scripts/test_codex_parity.py")]'
  PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -c 'import ast, pathlib; [ast.parse(pathlib.Path(path).read_text(), filename=path) for path in ("scripts/codex_switch_protocol_adapter.py", "scripts/codex_switch_parity.py", "scripts/test_codex_protocol_config.py", "scripts/test_codex_parity.py")]'

  PACKAGE_ROOT="$(mktemp -d /private/tmp/codex-switch-parity-83.XXXXXX)"
  CODEX_SWITCH_DIST_DIR="$PACKAGE_ROOT" CODEX_SWITCH_PYTHON="$(command -v python3.12)" /bin/bash scripts/package-release.sh

  openspec validate internal-official-feature-parity --strict --no-interactive
  openspec validate --all --strict --no-interactive
  python3 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/lint_ai_plan.py openspec/changes/internal-official-feature-parity/tasks.md
  python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json
  git diff --check
  ```

  Independently inspect the package manifest/archive/import report, run
  `git diff --no-index --check /dev/null <path>` for every untracked task-8.3
  path while accepting only the normal clean-difference exit 1 with empty
  output, and compare `git status --short` against the exact write set before
  claiming source readiness.

  **Rollback and no-mutation contract:** a RED or GREEN failure changes no
  live receipt, overlay, config, manifest, launcher, active record, process, or
  installed release. Source rollback is limited to the exact task-8.3 write
  set and must preserve unrelated bytes. An authorized live retry uses the
  existing schema-v3 transaction: preparation failure leaves the old
  generation effective; a prepared interruption rolls back all targets; a
  committed interruption rolls forward; foreign state stops without overwrite.

  **Continuation:** after planning verification, stop at
  `PARITY-8.3-IMPLEMENT`. After implementation and source/package verification,
  checkpoint and stop at `PARITY-8.3-LIVE-RETRY`. After an authorized live
  retry, re-attest the current official bundle, shell/PATH/App/profile/backend
  ownership and every mutable config input; do not reuse the old internal-mode
  pid or config snapshot. Check 8.3 only after promoted receipt-v2 evidence and
  all three clean diagnostics pass. Task 8.4 remains a separate dependency and
  Human Gate.

  **Human Gates:**

  - `PARITY-8.3-IMPLEMENT`: authorize only the exact production/test/fixture/
    docs write set and isolated local tests. It does not authorize install,
    rebind, restart, provider traffic, dependency, Git, release, archive, or
    cleanup.
  - `PARITY-8.3-LIVE-RETRY`: after reviewed GREEN/package evidence, authorize
    the exact verified-source install if needed, the single same-backend
    preparation/rebind, its bounded provider-backed typed-v2 probe, and the
    resulting profile/runtime artifacts. It does not authorize task 8.4
    restart, task 8.5 Desktop task, Git, release, archive, or cleanup.

  A changed official/internal binary, schema pair outside the fixture,
  unresolved product classification, public compatibility expansion,
  dependency, additional live effect, or write-set expansion stops before
  implementation or retry.

  **Source/package milestone (2026-07-27):** `PARITY-8.3-IMPLEMENT` was
  consumed. The complete thirteen-error RED/GREEN, receipt-v2 negative matrix,
  dual-runtime Protocol Adapter 41/41, parity 93/93, verifier 30/30, Runtime
  Binding 75/75, read-only review, and isolated package/source identity checks
  pass. The user is prioritizing the official profile, so development pauses
  at `OFFICIAL_FIRST_PAUSE_READY` and `PARITY-8.3-LIVE-RETRY`. No live effect
  occurred, this checkbox remains open at 70/79, and tasks 8.4-8.7 are not
  dependency-ready.
- [ ] 8.4 Fully quit and reopen ChatGPT with a bounded one-shot controller; do
  not use `launchctl submit`; attest one new ChatGPT pid, GUI
  `CODEX_CLI_PATH`, managed launcher, proxy parent, exact backend child, and the
  promoted receipt/overlay/config generation.
- [ ] 8.5 Start a fresh Desktop task that explicitly requests an `explorer`
  child to return `parity-subagent-ok`; capture the parent spawn item, child
  `thread_spawn` source, `agentRole=explorer`, task-oriented Desktop-visible
  name/description, child marker, and parent completion marker.
- [ ] 8.6 Re-attest launcher/proxy/backend/receipt/overlay/config ownership after
  completion, capture the required Desktop screenshot/metadata evidence, and
  reject generic-turn, untyped, nickname-only, parent-only, or v1 fallback
  results.
- [ ] 8.7 Run final installed status, Doctor, verify/report, immutable payload
  validation, normal self-update no-op, and source-versus-installed identity
  checks; do not commit, push, tag, release, archive, or clean retained evidence.

## 9. Control-Plane Closure

- [ ] 9.1 Reconcile every completed checkbox with its exact evidence and update
  this `tasks.md` incrementally; no item becomes done from an agent report
  alone.
- [ ] 9.2 Update `TASK_LEDGER.md`, `.planning/STATE.md`, and the parity
  verification record with final ownership, optional queue, residual risks,
  live acceptance, and next action.
- [ ] 9.3 Run the complete final verification command set fresh after the last
  source/control-plane edit and record exact exit codes/counts.
- [ ] 9.4 Stop at the completion-review boundary. OpenSpec archive, Git effects,
  release/publication, retained-probe cleanup, and any optional synchronization
  item require separate authorization.

## Capability Slices

| Slice | Production-complete result | Validation | Cleanup |
|---|---|---|---|
| Reference/inventory | Deterministic bundled-reference, feature, protocol, and classification results | focused parity/adapter RED/GREEN | remove duplicate policy helpers only after authority scan |
| Receipt/overlay | Safe provider-bound receipt and source-preserving v2 overlay | receipt/overlay/path/TOCTOU tests | no source-catalog mutation or raw probe retention |
| Config/probes | Internal-only v2 projection, exact stale-key migration, bounded typed-role proof | Config Document/home-sync/probe tests | no v1 fallback or credential-bearing evidence |
| Runtime bundle/rebind | All parity-sensitive runtime files recover together | fault matrix, legacy marker, runtime/profile suites | retire compatibility adapter only after caller migration |
| Staged update | Bound binary remains last-known-good until parity handshake | installer/swap/rollback/update suites | remove only classified candidate/backup state after success |
| Diagnostics/package | One receipt drives health, queue, repair route, and packaged runtime | verify/Doctor/package/docs checks | no second policy implementation |
| Task-8.3 evidence repair | All thirteen saved errors close through exact semantic, adapter, optional-extension, and post-probe evidence | retained exact fixture, dual-runtime adapter/parity/receipt consumers, package and planning gates | no global/method-only suppression; receipt-v1 is regenerated, not patched |
| Live acceptance | Real Desktop typed Subagent and runtime ownership proof | pre/post attestation, metadata, markers, screenshot | preserve evidence; no unrelated live changes |

## Execution Ledger

| Slice | Owner | Write Set | Required Evidence | Human Gate | Next Outcome | Status |
|---|---|---|---|---|---|---|
| Reference/inventory | main, serialized | new parity module/test; adapter digest only | RED/GREEN and real schema/feature fixture comparison | new policy entry | CHECKPOINT_AND_CONTINUE | complete; tasks 1.1-1.13 pass on Python 3.12 and system Python 3.9, with deterministic sanitized inventory/classification evidence; task 2.1 next |
| Receipt/overlay | main, serialized | parity module/test and staged manifest metadata | safe-load, structural diff, source-unchanged log | broader overlay field | CONTINUE_NEXT_ITEM | complete; tasks 2.1-2.7 pass on Python 3.12 and system Python 3.9 with exact manifest binding, private staging, source byte/mode preservation, and no caller/final-path integration; task 3.1 next |
| Config/probes | main, serialized | parity/config-document/home-sync plus tests | exact-key RED/GREEN, bounded sanitized probe log | live provider probe | CONTINUE_NEXT_ITEM | complete; tasks 3.1-3.9 pass on their supported Python 3.12/system Python 3.9 routes, including parity 82/82, Config Document 29/29 on 3.12 with the established 3.9 parser boundary, projection 2/2, verifier 22/22, and native 3.9 sanitizer 2/2; task 4.1 next |
| Runtime bundle/rebind | main, serialized | transaction/bindings/wrapper/runtime/profile tests | schema-v3 fault matrix and legacy recovery | foreign live state | CONTINUE_NEXT_ITEM | complete; tasks 4.1-4.10 pass the integrated dual-runtime matrix. Review added one bounded guard so any `parity_` manifest field requires the complete shell/Desktop generation; parity 83/83, Protocol Adapter 39/39, Runtime Binding 65/65, and transaction 234/234 pass on Python 3.12 and system Python 3.9, complete profile passes 201/201 on Python 3.12, and the supported 3.9 profile routes pass 2/2; task 5.1 next |
| Staged update | main, serialized | env helper/wrapper/promotion/update tests | sibling install/swap/rollback log | real internal update | CONTINUE_NEXT_ITEM | complete; tasks 5.1-5.10 pass the slice-closure matrix. Python 3.12 passes update/release 123/123, transaction 239/239, Runtime Binding 75/75, parity 83/83, and complete profile 201/201. System Python 3.9 passes update/release 123/123, transaction 239/239, Runtime Binding 75/75, parity 83/83, and the supported profile projection routes 2/2; direct profile CLI exits 2 before store creation at the established Python 3.11+ `tomllib` boundary. No production code changed during 5.10. Task 6.1 next |
| Diagnostics/package | main, serialized | verify/Doctor/status/package/docs/tests | shared findings, package/import proof | public CLI expansion | VERIFY_ACTIVE_CHANGE | complete; tasks 6.1-6.10 share one parity report/classification owner, read-only diagnostics, staged repair routing, immutable package imports, operator docs, and clean authority boundaries. The slice-focused matrix passes 71/71 on Python 3.12.13 and 71/71 on system Python 3.9.6: 9 reference/ownership, 8 verifier, 4 profile diagnostics/package seams, 37 release-bundle, 10 staged-update, and 3 package/promotion/workflow adjacency tests per runtime. No production code changed during 6.10. Task 7.1 integrated parity verification is next |
| Integrated review | main | tests and control-plane evidence only | dual-runtime/full/static/package/diff review | unresolved production contract | BLOCKED_AWAITING_HUMAN or CONTINUE_NEXT_ITEM | complete through task 8.1 at 69/79. The verification record consolidates the automated/static/package/review evidence and records the user's explicit authorization for the exact-source install, same-backend rebind, resulting profile/App/runtime mutations, bounded ChatGPT restart, and one real provider-backed typed `explorer` task. Task 8.2 is next |
| Task-8.3 evidence repair | main, serialized after `PARITY-8.3-IMPLEMENT` | exact two production, two test, one fixture, two operator-doc, and main-owned control-plane sets named in 8.3 | complete thirteen-error RED/GREEN, receipt-v2 negative matrix, dual-runtime consumers, package/write-set proof | implementation consumed; live retry still required | BLOCKED_AWAITING_HUMAN | source/package verified at `OFFICIAL_FIRST_PAUSE_READY`: Protocol Adapter 41/41, parity 93/93, verifier 30/30, and Runtime Binding 75/75 pass on both runtimes; isolated package matches source. Stop at `PARITY-8.3-LIVE-RETRY`; task 8.3 remains unchecked at 70/79 |
| Live acceptance | main after explicit approval | supported local install and live profile/App state only | typed role, markers, screenshot, full ownership | required | BLOCKED_AWAITING_HUMAN | prior task-8.3 live attempt and diagnostic are retained RED evidence, but their runtime snapshot is stale because current ownership is official. No retry or task 8.4 may start before the evidence repair is implemented, verified, and `PARITY-8.3-LIVE-RETRY` is explicitly authorized |
| Closure | main | OpenSpec/ledger/state/evidence | fresh final command set | archive/Git/release/cleanup | COMPLETE | pending |

## SubAgent Strategy

No write worker starts by default because transaction, config, rebind, update,
and diagnostics share active dirty-worktree seams. A future worker is permitted
only for the new parity module/test pair after a validated Agent Task Contract
records a disjoint write set of exactly
`scripts/codex_switch_parity.py` and `scripts/test_codex_parity.py`. The worker
must stop before adapter, config, transaction, wrapper, package, OpenSpec,
ledger, state, or live effects. Main reviews the diff and reruns focused tests.
Read-only architecture or review workers may inspect any source but own no
writes.

## Spec Coverage Matrix

| Requirement | Primary Tasks |
|---|---|
| Verified official parity reference | 1.1-1.3 |
| Deterministic parity inventory | 1.4-1.7, 1.12 |
| Direction-aware core protocol parity | 1.6-1.11 |
| Explicit feature and model-metadata classification | 1.10-1.13 |
| Provider-bound parity receipt | 2.1-2.2, 2.5-2.7 |
| Source-preserving managed model overlay | 2.3-2.7 |
| Proven internal v2 config projection | 3.1-3.5, 4.6-4.8 |
| Isolated bounded parity probes | 3.6-3.9 |
| Crash-recoverable runtime parity bundle | 4.1-4.10 |
| Fail-safe staged internal binary update | 5.1-5.10 |
| Unified parity diagnostics and packaging | 6.1-6.10 |
| Exact method coverage, nullable equivalence, post-probe feature evidence, and receipt-v2 migration | 8.3 |
| Live Desktop typed-Subagent acceptance | 8.1-8.7 |

## Validation Commands

```bash
VALIDATION_ROOT="$(mktemp -d /private/tmp/codex-switch-parity.XXXXXX)"
export CODEX_SWITCH_SHELL_PROFILE="$VALIDATION_ROOT/.zshrc"

PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_parity.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_parity.py -v

PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_verify.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py

PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_verify.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_profile_switch.py

openspec validate internal-official-feature-parity --strict --no-interactive
openspec validate --all --strict --no-interactive
python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/validate_workflow_state.py \
  --repo /Users/cY/dev/codex-switch --json

bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
bash -n scripts/package-release.sh

PYTHONDONTWRITEBYTECODE=1 python3.12 -c 'import ast, pathlib; [ast.parse(path.read_text(), filename=str(path)) for path in pathlib.Path("scripts").glob("*.py")]'
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 -c 'import ast, pathlib; [ast.parse(path.read_text(), filename=str(path)) for path in pathlib.Path("scripts").glob("*.py")]'

git diff --check
```

## Risks / Rollback

- A Desktop bundle update invalidates receipt evidence by design; regeneration,
  not tolerance, is the recovery.
- Exact schema-pair extension records intentionally expire on any schema
  change; do not broaden them to method/reason wildcards to avoid maintenance.
- Receipt-v2 makes receipt-v1 unhealthy. Regeneration uses the existing staged
  repair transaction; there is no in-place receipt migration or compatibility
  fallback.
- Optional extension classification is bounded to the fixed core coding path.
  Observation of realtime-v3, audio, Bedrock login, external-agent
  memory/provider migration, or listed sharing escalates and stops rather than
  silently dropping semantics.
- Direction-aware schema comparison can encounter unsupported constructs; the
  stop condition is an unclassified finding, not a guessed result.
- Exact stale config removal changes an obsolete tuning value; schema-v3
  rollback preserves its old bytes.
- Multi-file promotion is recoverable rather than one-syscall atomic; marker
  state and exact old/new validation are the contract.
- Binary promotion crosses the install parent and store; exact sibling paths,
  digests, lock revalidation, and retained last-known-good constrain it.
- Live provider/Desktop behavior can fail independently of source correctness;
  retain source verification and report the live gate separately.

## Resume Contract

After interruption or compaction, read this file, `TASK_LEDGER.md`,
`.planning/STATE.md`, and
`.planning/devflow/verification/internal-official-feature-parity.md` if it
exists. Confirm the active Goal is `internal-official-feature-parity`, inspect
the dirty worktree without reverting unrelated files, and select the first
unchecked dependency-ready item. For task 8.3, inspect the latest
method-coverage planning checkpoint and stop at whichever of
`PARITY-8.3-IMPLEMENT` or `PARITY-8.3-LIVE-RETRY` has not been explicitly
authorized. Never infer either gate from the consumed task-8.1 approval.

## Review Checklist

- Every finding has stable category, code, severity, and health semantics.
- Optional-unless-observed escalation is covered by a test.
- No caller reconstructs parity policy outside the parity module.
- No overlay/config path mutates source catalog or credential material.
- Every promotion/recovery target has exact path, mode, digest, old/new, and
  foreign-state tests.
- Update success is impossible before post-promotion handshake.
- Reports and evidence are bounded and sanitized.
- No live effect occurs before its Human Gate.

## Final Verification

The change is complete only after tasks 1-9 are checked with fresh evidence,
all 75 scenarios map to passing tests or the authorized live acceptance, both
Python runtimes and all static/package/workflow gates pass, and the final
Desktop acceptance proves the same typed v2 behavior and runtime ownership
specified by the receipt. Archive and Git/release effects remain separate.
