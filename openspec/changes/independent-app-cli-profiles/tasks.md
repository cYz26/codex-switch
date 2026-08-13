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
  self-update and internal update checks on real apply, keeps `--dry-run`
  zero-write/zero-network by bypassing both update layers, and rejects
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
- [x] 15.4 Record Auto Release run `31500533015` as a failed acceptance result
  and add focused RED coverage where deleting the only canonical zero-byte
  `starter` makes the tag-based Release readback return missing. Add guards for
  failed recreation, missing or non-draft readback, and tag movement before
  recreation.
- [x] 15.5 Revalidate tag identity, recreate one verified-tag draft Release,
  immediately require an empty draft readback, then continue through canonical
  upload, publish, and checksum verification. Apply the same create/readback
  contract when reconciliation begins with no Release. Read back after every
  exact starter deletion and stop using stale IDs if the Release disappears.
  Do not use `--clobber` or weaken existing uploaded/non-zero/duplicate/
  unknown-state guards.
- [x] 15.6 Run the focused recovery matrix, complete update/release and adjacent
  profile suites, Python/static/strict OpenSpec/workflow/diff checks, then
  update ledger, namespaced state, and verification evidence. Record a new
  Human Gate before any second commit, push, workflow rerun, or live Release
  mutation; the prior submit authority is consumed.
- [x] 15.7 Before consuming the second submit authority, inspect the complete
  push-triggered Auto Release plan. Record that release-relevant changes since
  `v0.1.14` select `reconcile_then_prepare`: after repairing `v0.1.14`, the
  workflow would create a release commit, atomically update `main` and tag
  `v0.1.15`, and publish the new Release. Stop at a new Human Gate because the
  current grant names only the `v0.1.14` repair and does not authorize the
  additional `v0.1.15` tag or publication target.

## 16. Bounded Release-Recreation Propagation Repair

- [x] 16.1 Add public `reconcile_release_assets` RED coverage for the exact
  post-delete consistency window: typed `Release.tag_name already exists` or
  server/transport creation failure with a still-missing readback later
  succeeds; successful creation with delayed visibility performs readback-only
  retries. Add terminal guards for permission/rate-limit/unknown validation,
  published/non-empty state, tag movement, and bounded retry exhaustion.
- [x] 16.2 Add a typed release-create failure classification at the GitHub
  adapter seam and implement at most five state-confirming create or readback
  attempts with deterministic 1/2/4/8 second production backoff. Revalidate the
  immutable tag and missing Release before every repeated create, accept only
  one empty draft readback, never recreate after create success, and preserve
  all starter-ID, checksum, no-`--clobber`, and conflict guards.
- [x] 16.3 Run the focused recreation matrix, complete Python 3.12
  update/release and adjacent profile suites, Python/Bash/JSON checks, strict
  active/all OpenSpec, DevFlow workflow validation, package identity where
  affected, and `git diff --check`. Record the existing INC-018 migration drift
  without applying it and complete an independent release-path review.
- [x] 16.4 Update the ledger, namespaced state, and verification record with
  RED/GREEN, exact changed files, validation, residual risks, the resolved
  `614cc025...` authority, and the remote prestate. Commit and fast-forward push
  only the verified repair/control-plane write set to `origin/main`. Completed
  by commit `6a5fa85`; the 34 MB Hook event log remained excluded.
- [x] 16.5 Monitor the first push-triggered Auto Release through terminal state.
  Record run `31666160863` as failed after draft creation and five tag-based
  readback attempts, with `origin/main=6a5fa85`, `v0.1.14=19a2433`,
  `v0.1.15` absent, published latest Release still `v0.1.13`, and all three
  canonical `v0.1.14` asset URLs returning 404. Do not claim publication.
- [x] 16.6 Add a public GitHub-adapter RED using the real API response shape:
  tag-specific inspection returns 404 while the authenticated paginated
  Releases collection contains the exact draft. On GREEN, select one exact
  `tag_name` match, preserve missing when no match exists, and reject duplicate,
  malformed, non-404, invalid-JSON, or unbounded states before mutation.
- [x] 16.7 Run the focused adapter/reconciliation matrix, complete Python 3.12
  update/release and adjacent profile suites, Python/Bash/JSON checks, active/all
  strict OpenSpec, DevFlow workflow validation, and `git diff --check`. Update
  proposal/design/spec/tasks, ledger, namespaced state, and verification with
  exact results and residual risks.
- [x] 16.8 Record a new Human Gate before another commit, push, workflow run,
  `v0.1.14` Release mutation, or `v0.1.15` tag/Release publication. The prior
  `614cc025...` authority was consumed by `6a5fa85` and run `31666160863`.
  The user's 2026-08-13 `授权` decision is recorded in
  `draft-release-discovery-submit-authority-grant.json`; gate `a40cea2a...` is
  resolved for the exact task 16.9 submit/release effects.
- [ ] 16.9 After fresh authorization, commit and fast-forward push only the
  verified draft-discovery repair/control-plane write set. Require
  `origin/main` plus the atomic `v0.1.15` tag to resolve to the release commit,
  published `v0.1.14` and `v0.1.15` Releases with exactly the canonical three
  assets, and independent size/checksum verification against deterministic
  manifests before claiming publication complete.

## 17. Official-Authoritative Shared Plugin Readiness

- [x] 17.1 Add public `reconcile_shared_configuration` RED coverage proving
  Official App Plugin/Skill desired state is authoritative: Official-only,
  internal-only, disjoint, overlapping, delete-versus-modify, and legacy
  pending-App drift all converge only toward the internal CLI without writing
  the Official App. Preserve unrelated internal runtime configuration and
  report secret-safe changed operations.
- [x] 17.2 Replace symmetric App/CLI source selection with one deep
  Official-to-internal readiness implementation. Automatically materialize and
  render every repairable internal drift, retain target CAS, source recheck,
  crash recovery, backend-owned cache lifecycle, exact Plugin identity
  attestation, and zero-write/zero-network current-generation behavior.
- [x] 17.3 Add public functional-preflight RED/GREEN coverage proving a
  repairable mismatch synchronizes before backend `execve`, emits bounded
  progress plus a verified-generation result, and starts the backend exactly
  once. Unsafe failures preserve last-known-good state, never execute the
  backend, and print the finding cause plus exact `sync-shared --dry-run`,
  `sync-shared`, and Doctor remediation instead of a bare error code.
- [x] 17.4 Make status, Doctor, verify, and `sync-shared` render one structured,
  secret-safe report with source/target, changed operations, automatic actions,
  readiness, and remediation. Keep diagnostics read-only, help/version bypassed,
  and remove the unshipped interactive source-choice/`resolve-shared` surface.
- [x] 17.5 Update README, SKILL, proposal/design/spec, ledger, namespaced state,
  and verification evidence with Official authority, internal derived-state
  semantics, explicit non-shared internal configuration preservation, and the
  absence of a watcher, reverse automatic sync, direct cache deletion, or broad
  configuration sharing.
- [x] 17.6 Run focused and adjacent shared/profile/runtime suites, complete
  Python 3.12 profile/update-release suites where affected, Python/Bash/JSON
  checks, package identity, strict active/all OpenSpec, DevFlow workflow,
  plugin-eval, and `git diff --check`. Complete an independent source review
  without a live functional backend, install, App mutation, Git/release effect,
  archive, migration, dependency, cleanup, credential, or destructive effect.

## 18. Split-Triggered Shared Readiness

- [x] 18.1 Add public-wrapper RED coverage proving real `split` and
  `internal --app-profile official` invoke shared synchronization exactly once
  after switch commit and before Plugin repair, verify, Doctor, or status.
  Prove a synchronization failure returns its code, stops every later step,
  and prints exact preview/apply/Doctor remediation. Prove both dry-run forms
  name the pending readiness boundary without invoking shared apply, installed
  self-update, network access, or any write.
- [x] 18.2 Implement the post-switch readiness step by routing through the
  existing `sync-shared` command rather than duplicating reconciliation in the
  wrapper or folding backend effects into the profile transaction. Keep the
  functional managed-CLI preflight as the fallback for later Official changes
  and older installed wrappers.
- [x] 18.3 Update README, SKILL, proposal/design/spec, ledger, namespaced state,
  and verification evidence with exact ordering, dry-run, failure, recovery,
  and authority boundaries.
- [x] 18.4 Run focused wrapper/shared tests, affected full Python 3.12 suites,
  Bash/Python/static/JSON checks, isolated package identity and behavior,
  strict active/all OpenSpec, DevFlow workflow, plugin-eval, and
  `git diff --check`. Complete a fresh review without a live split,
  functional backend, install, App/config/cache mutation, migration,
  dependency, Git/release effect, archive, cleanup, credential, or destructive
  effect.

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

The user's 2026-08-12 Official-authoritative repair request supersedes the
unshipped symmetric shared-conflict draft and authorizes task 17 source, tests,
README/SKILL, OpenSpec, ledger, namespaced-state, and verification-record
writes. It does not authorize a live functional backend command, installation,
App stop/restart/mutation, either live profile/config/cache mutation, project
migration, dependency change, consumption of task-16 Git/Release authority,
commit, push, release, archive, cleanup, credential, or destructive work.

The user's 2026-08-12 split-lifecycle refinement additionally authorizes task
18 source, tests, README/SKILL, OpenSpec, ledger, namespaced-state, and
verification-record writes. It does not authorize running a live split or
functional backend, installing source, stopping/restarting/mutating the App,
changing live config or Plugin caches, project migration, dependency change,
consuming task-16 Git/Release authority, commit, push, release, archive,
cleanup, credential, or destructive work.

The first submit authority was consumed by commit `85dc960` and Auto Release
run `31500533015`. The failed acceptance result keeps task 15 open for the
bounded source/test/control-plane repair in 15.4-15.6, but a second commit,
push, workflow rerun, or live Release mutation requires a new Human Gate.

The second submit authority permits the repair commit/push and `v0.1.14`
reconciliation. It does not by itself authorize the subsequently discovered
`v0.1.15` release commit, tag, or publication selected by the same workflow.

The user's 2026-08-12 `授权发布` decision resolves authority gate
`614cc0253ca0735cf2af34acc60564687b7b081de9fa2e417045ea447a851d38`
for task 16 source/test/OpenSpec/control-plane writes, one verified repair
commit and fast-forward push to `origin/main`, the push-triggered Auto Release
mutation required to restore `v0.1.14`, and the already-planned atomic
`v0.1.15` tag and Release publication. It does not authorize archive, project
migration, dependency/credential changes, manual broad Release edits, force
push, cleanup, or unrelated runtime effects.

That authority was consumed by commit `6a5fa85`, its fast-forward push to
`origin/main`, and Auto Release run `31666160863`. The user's 2026-08-13 failed
run report authorizes task 16.6-16.7 source, test, OpenSpec, ledger,
namespaced-state, and verification-record changes. The subsequent `授权`
decision resolves gate `a40cea2a...` for one verified commit and fast-forward
push to `origin/main`, the push-triggered `v0.1.14` recovery, and atomic
`v0.1.15` tag/Release publication. It does not authorize manual broad Release
edits, migration, dependency/credential change, archive, cleanup, force push,
or unrelated runtime effects.
