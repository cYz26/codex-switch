## 1. Active Selection and State Compatibility

- [x] 1.1 Add RED tests for requested internal-CLI/official-App selection,
  synchronized defaults, official alias normalization, legacy `active.json`,
  explicit split fields, partial/conflicting state, unsupported pairings, and
  `--app-profile` plus `--skip-app-cli` rejection.
- [x] 1.2 Add the immutable active-selection interface and make
  `codex_switch_record.py` plus the Python CLI parser write/consume additive
  `cli_profile` and `app_profile` fields while preserving `profile` as the CLI
  alias; rerun the named selection/parser tests GREEN.
- [x] 1.3 Run the adjacent Runtime Binding and profile-state tests and review
  the interface for duplicate legacy/new parsing before selecting task 2.1.

## 2. Recoverable Split Transaction

- [x] 2.1 Add RED transaction/profile tests proving the split dry-run names
  both targets, commit writes an internal shim/home plus official App binding,
  default same-profile switches remain unchanged, and unsupported requests
  mutate nothing.
- [x] 2.2 Extend switch planning and the transaction to freeze the CLI and App
  manifests/paths separately, prepare each surface from its selected profile,
  and commit one additive active record; pass the successful/default/dry-run
  RED matrix.
- [x] 2.3 Add RED fault/drift tests proving official Desktop apply failure and
  post-plan change of either selected target restore or preserve the prior shim,
  LaunchAgent, homes/config, and active record.
- [x] 2.4 Close the rollback/drift REDs through the existing journal, then run
  the complete transaction suite and focused profile-switch cases GREEN.

## 3. Split-Aware Status, Doctor, and Verify

- [x] 3.1 Add RED status/Doctor tests for separate CLI/App labels, healthy
  internal-CLI/official-App ownership, shell-only drift, App-only drift, and
  malformed active selection without cross-surface false findings.
- [x] 3.2 Update status and Doctor to consume the canonical active selection,
  resolve CLI and App bindings independently, and attest live Desktop only
  against the App binding; pass the named diagnostic tests GREEN.
- [x] 3.3 Add RED verifier tests proving runtime/exec checks use the internal
  binary/home, App-server/live attestation uses the official bundle/home,
  internal parity stays read-only, and legacy same-profile verification remains
  compatible.
- [x] 3.4 Update verifier collection/reporting to keep CLI and App bindings
  distinct, pass the named verifier tests, then run the complete verifier,
  Runtime Binding, and parity suites GREEN without changing parity policy.

## 4. One-Key Wrapper, Documentation, and Package

- [x] 4.1 Add RED wrapper/package tests proving
  `codex-switch internal --app-profile official` forwards the override through
  dry-run/apply, keeps update/plugin preparation on internal, reports both
  profiles, and requires the new module in an isolated release bundle.
- [x] 4.2 Update `scripts/codex-switch`, README, and SKILL with the explicit
  split command, safety boundary, status/verify behavior, and unchanged
  synchronized defaults; add the selection module to release requirements and
  pass the named wrapper/package tests GREEN.
- [x] 4.3 Run `plugin-eval analyze SKILL.md --format markdown` against the
  release counterpart, record score/findings/decisions, and run the complete
  update/release suite plus an isolated packaged split preview.

## 5. Integrated Completion Proof

- [x] 5.1 Run the complete profile, transaction, Runtime Binding, verifier,
  parity, and update/release suites fresh and record exact command counts.
- [x] 5.2 Run Python compile/import, Bash syntax, strict active/all OpenSpec,
  DevFlow workflow validation, isolated package/source identity, and
  `git diff --check`.
- [x] 5.3 Perform a read-only scope/change review: map every spec scenario to
  evidence, compare unrelated pre-existing parity/provider-migration paths,
  classify incidental findings, and resolve all in-scope blockers.
- [x] 5.4 Update this task list, `TASK_LEDGER.md`,
  `.planning/devflow/STATE.md`, and
  `.planning/devflow/verification/independent-app-cli-profiles.md` with the
  final evidence and residual risks; stop without install, live switch, App
  restart, archive, commit, push, release, dependency, cleanup, or destructive
  effect.

## 6. Shared Plugin and Skill Desired State

- [x] 6.1 Add public-seam RED tests for official bootstrap, semantic no-op,
  single-side/identical changes, divergent and delete-vs-modify conflict,
  unstable source observation, secret-bearing marketplace rejection, and
  authoritative disable/removal without stale revival.
- [x] 6.2 Implement the deep shared-configuration module, additive store paths,
  name-and-value secret-safe projection, generation/baseline state, stable
  findings, target CAS, canonical/receipt persistence, and a private terminally
  removed prepared recovery journal; pass the task 6.1 matrix GREEN.
- [x] 6.3 Add RED/GREEN tests for the explicit personal-Skill root, missing-link
  creation, foreign/real/dangling/self-link failure, plugin-cache path remap,
  traversal/symlink escape rejection, and project-local Skill non-interference.
- [x] 6.4 Run focused config/document/store regressions and review that no
  caller independently implements merge direction, conflict, or receipt
  authority.

## 7. Independent Plugin Materialization

- [x] 7.1 Add RED tests for App add/update/same-selector-update/enable,
  disable/remove, portable-exact and backend-managed identity, unavailable and
  unverified catalogs, independent cache roots, running-process guard, and
  materialization failure rollback.
- [x] 7.2 Extend the plugin materialization seam with explicit desired
  identities, generation-scoped conditional repair, exact local verification,
  inspectable backend-managed receipts, deterministic active-version selection,
  and target-path verification; pass task 7.1 GREEN without sharing or deleting
  cache trees directly from codex-switch while leaving native installed-version
  lifecycle to the selected backend.
- [x] 7.3 Add the unchanged-generation zero-write/zero-network fast-path tests
  and prove stored receipts plus cache/config/canonical postconditions are
  re-attested before a ready receipt commits; missing/corrupt caches repair or
  block before backend execution.
- [x] 7.4 Run the complete plugin/profile adjacency and inspect failure
  injection at every persistent commit boundary for recovery, last-known-good
  config preservation, pre-backend materialization intent recovery,
  inherited store-lock leasing across real backend subprocesses and parent
  SIGKILL, collision-safe orphan generations, and untrusted backend-left cache
  evidence without direct codex-switch cleanup.

## 8. Lifecycle, Explicit Sync, Diagnostics, and Distribution

- [x] 8.1 Add RED Runtime Binding tests proving functional internal CLI
  preflight completes before `os.execve`, a blocked generation never calls the
  backend, unchanged state executes once, and `--help`/`--version` remain
  read-only.
- [x] 8.2 Integrate preflight after internal-generation validation without
  replacing `os.execve`; pass the lifecycle REDs and preserve Runtime Binding,
  TTY/process, and same-profile behavior.
- [x] 8.3 Add RED/GREEN command tests for `sync-shared --dry-run`, stopped-App
  apply, process-inventory failure/mismatched App process, commit-time second
  stopped proof before materialization and before main commit, target CAS,
  live-App pending behavior, and conflict/no-write handling.
- [x] 8.4 Make status, Doctor, and verify consume one read-only shared report;
  add the generation/pending/conflict/materialization finding matrix and run
  focused diagnostic suites GREEN.
- [x] 8.5 Update README, SKILL, wrapper command routing, release-required module
  list, package identity, and the reviewed configuration ownership matrix; pass
  focused wrapper/package tests.

## 9. Reopened Integrated Completion Proof

- [x] 9.1 Run fresh shared-configuration, Runtime Binding, transaction,
  verifier, profile, update/release, and parity suites; record exact counts and
  exclude interrupted/stale runs.
- [x] 9.2 Run Python/Bash static checks, strict active/all OpenSpec, DevFlow
  workflow validation, isolated package/source identity, and `git diff
  --check`.
- [x] 9.3 Run Plugin Eval against the isolated release counterpart and perform
  independent code/spec review; fix every in-scope blocker and classify every
  other-config finding without silently expanding ownership.
- [x] 9.4 Update this task list, `TASK_LEDGER.md`, namespaced state, and the
  verification record with final evidence, residual risks, pending live apply
  boundary, and exact non-effects.

## 10. Live Deployment Compatibility Closure

- [x] 10.1 Add one public installer RED proving a latest 22-path candidate can
  promote over exact 20-path `current` and `rollback` releases while retaining
  the previous current byte-for-byte; keep malformed historical lists rejected.
- [x] 10.2 Generalize historical release validation to the exact supported
  16-path and 20-path manifest generations, update both trusted bootstrap
  hashes, and pass the focused installer RED/GREEN plus adjacent promotion
  regressions.
- [ ] 10.3 Build and validate a fresh isolated package, install it through the
  supported immutable promotion path, then apply
  `codex-switch internal --app-profile official --skip-update-check` without
  crossing the separate internal-0.145 compatibility gate or restarting the
  already-official App.
- [ ] 10.4 Verify installed/source identity, split CLI/App ownership,
  Plugin/Skill shared-generation health, Doctor/verify results, current and
  rollback references, and internal update-check preservation; record exact
  live effects and exclusions in the ledger, state, and verification record.

## 11. Concise Split Command

- [x] 11.1 Add public-wrapper RED tests proving `codex-switch split` routes to
  the existing internal-CLI/official-App workflow, preserves ordinary wrapper
  self-update and internal update checks, supports `--dry-run`, and rejects
  split-scoped options outside the shortcut plus App-profile overrides on the
  fixed preset.
- [x] 11.2 Add RED coverage proving `split --keep-version` suppresses both
  codex-switch self-update and internal update detection/promotion while still
  retaining Plugin repair, verify, Doctor, status, and ordinary result
  handling; implement the smallest wrapper-only normalization and pass the
  focused matrix GREEN.
- [x] 11.3 Update wrapper help, README, and SKILL; run focused and adjacent
  profile/update/release tests, Bash syntax, strict OpenSpec, workflow state,
  package identity, and `git diff --check` without changing switch,
  transaction, parity, or shared-configuration policy.
- [x] 11.4 Record RED/GREEN and residual live-state gates in the ledger, state,
  and verification record; build and validate a fresh isolated package,
  install it through immutable promotion, and verify installed help plus the
  shortcut in an isolated non-mutating preview without stopping the App or
  applying the live split.

## 12. Live Bootstrap Portable-Identity Repair

- [x] 12.1 Record the live root cause and add public-seam RED tests using the
  target backend's real JSON shape: an older installed `portable_exact`
  version with a safely resolved newer source must update successfully, while
  a genuinely mismatched source receives a precise non-`unsafe_cache` finding.
- [x] 12.2 Separate backend-reported target version from portable source
  identity, retain exact source and post-add target attestation, preserve
  config/receipt rollback, and pass task 12.1 GREEN without direct
  codex-switch copying, linking, or deleting of either workstation cache;
  native target-backend replacement remains backend-owned.
- [x] 12.3 Add public functional-preflight progress RED/GREEN coverage for
  flushed source-attestation and materialization phase messages; keep
  help/version read-only and unchanged committed generations zero-write and
  zero-network, then update README and SKILL operator expectations.
- [x] 12.4 Run fresh focused and broad shared/runtime/profile suites plus
  Python/Bash, strict OpenSpec, workflow, package-identity, Plugin Eval, and
  diff checks; update the ledger, namespaced state, and verification record
  with exact evidence and no live `codex`, split, install, App, cache, Git,
  release, archive, migration, or cleanup effect.

## 13. Backend-Managed Functional Acceptance Repair

- [x] 13.1 Record the live root cause and add production-seam RED tests using
  the real catalog shape: installed internal target version older than the
  exact current official source, installed record precedence over an available
  duplicate, mandatory native reconcile, one fresh post-add batch catalog, and
  precise unverified-target failures.
- [x] 13.2 Preserve installed and available catalog provenance, attest desired
  source identity independently from target version, reconcile every pending
  `backend_managed` selector through the internal backend, and attest each
  independent target from the fresh catalog before receipt commit. Preserve
  portable behavior and config rollback; allow backend-owned replacement of
  prior installed versions while prohibiting direct codex-switch cache
  copy/link/delete.
- [x] 13.3 Run fresh focused and broad shared/runtime/profile suites plus
  Python/Bash, strict OpenSpec, workflow, package identity, release-counterpart
  Plugin Eval, diff checks, and independent spec/standards reviews; update
  README, SKILL, ledger, namespaced state, and verification evidence.
- [x] 13.4 Run exactly one non-interactive functional command through the
  current managed internal CLI shim while the official App remains running;
  prove exit zero, shared generation/receipts, internal backend dispatch,
  independently safe target caches, native installed-version lifecycle effects,
  and unchanged App binding/process state, then record exact effects and
  exclusions and reconcile the confirmed lifecycle contract.

## 14. Managed Runtime-Config Render Idempotence

- [x] 14.1 Add a focused RED proving that two consecutive last-runtime renders
  with unchanged profile/shared inputs currently add a blank line and change
  the bytes.
- [x] 14.2 Remove only blank lines immediately preceding generated managed
  annotations before re-annotation; preserve unrelated user formatting and
  pass the focused repeated-render regression GREEN.
- [x] 14.3 Run adjacent config/profile tests, Python/static/strict OpenSpec and
  diff checks, then update ledger, namespaced state, and verification evidence.
  Do not rewrite live config, switch/install, act on the App, activate
  dependencies, or perform Git/release/archive/cleanup effects.

## 15. Failed Release-Upload Starter Recovery

- [x] 15.1 Add focused RED coverage for the observed `v0.1.14` shape: the
  normal uploaded-asset view is empty, the explicit release-assets inventory
  contains same-name zero-byte `starter` residue, and the current reconciler
  attempts `install.sh` upload and receives `asset under the same name already
  exists`. Add conflict guards for non-zero and unsupported records.
- [x] 15.2 Make the GitHub adapter inventory paginated asset records with exact
  ID/name/state/size, delete only a canonical zero-byte `starter` after a fresh
  tag-identity check, read back before upload, and retain download/hash
  verification plus the prohibition on `--clobber`.
- [x] 15.3 Run focused and complete update/release tests, adjacent profile
  release tests, Python/static/strict OpenSpec/workflow/diff checks, then update
  ledger, namespaced state, and verification evidence. Do not mutate a live
  GitHub Release, rerun a workflow, apply the pending DevFlow migration, or
  perform dependency, commit, push, archive, or cleanup effects.

## Execution Policy

The user's implementation request authorizes the source, test, documentation,
OpenSpec, ledger, namespaced-state, and verification-record write set named in
the design. The 2026-08-06 deployment request additionally authorizes the exact
task 10 immutable install and internal-CLI/official-App switch, but not the
available internal 0.145 binary upgrade, App restart, Git effect, release,
archive, cleanup, dependency, credential, or destructive action. Execution is
`auto-until-terminal`; each completed item continues to the next
dependency-ready checkbox. Any new profile combination, public state expansion
beyond the specified additive active fields and shared-capability sidecar,
parity/proxy/update policy change, or other excluded effect is a Human Gate.
The 2026-08-10 shortcut confirmation additionally authorizes task 11 source,
test, documentation, control-plane, isolated package, and immutable local
installation effects. It does not authorize App stop/restart, live split
activation, internal binary update, parity repair, release, archive, Git
effects, cleanup, dependency, credential, or destructive work.

The later 2026-08-10 live-bootstrap repair confirmation additionally
authorizes task 12 source, test, README/SKILL, OpenSpec, ledger,
namespaced-state, and verification-record effects. It does not authorize live
Plugin/cache mutation, another install, functional `codex` or split retry, App
stop/restart, internal update, project migration, Git, release, archive,
cleanup, dependency, credential, or destructive work.

The user's 2026-08-11 systemic-repair confirmation additionally authorizes
task 13 source, test, README/SKILL, OpenSpec, ledger, namespaced-state, and
verification-record changes plus one functional command through the current
managed internal CLI shim. The acceptance command may perform bounded internal
backend Plugin add/update operations, profile-local config restoration, target
cache writes owned by that backend, and shared-generation/receipt writes while
the official App remains running, including native replacement or removal of
prior installed versions. It does not authorize split retry, another install,
App stop/restart/mutation, internal binary update, standalone cache cleanup,
direct codex-switch cache copy/link/delete, project migration, dependency
change, Git, release, archive, credential, or destructive work. The user's
later explicit confirmation assigns Plugin installed-cache lifecycle to the
native backend and removes the earlier retention guarantee without authorizing
any additional live command.

The user's 2026-08-11 report of the failed `v0.1.14` Action authorizes task 15
source, test, OpenSpec, ledger, namespaced-state, and verification-record
changes only. It does not authorize a live GitHub Release deletion/upload,
workflow rerun, DevFlow migration apply, dependency change, commit, push,
archive, or cleanup.
