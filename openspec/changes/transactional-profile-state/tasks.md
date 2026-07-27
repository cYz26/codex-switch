# Transactional Profile State Implementation Plan

**Goal:** Make every supported official/internal switch, capture, and restore a lock-owned, fully preflighted transaction with schema-v2 recovery evidence and complete rollback.

**Architecture:** `codex_switch_transaction.py` owns the deep execution interface. Existing CLI modules become adapters; backup/path state and Desktop effects are internal seams. No public stale plan crosses the store lock.

**Tech Stack:** Python 3 standard library, `unittest`, macOS `fcntl`, existing Bash/Python CLI.

## Global Constraints

- Product profiles are `openai-official`/`official` and `internal`; arbitrary-profile hardening is out of scope.
- No live workstation profile/App switch, install, migration, release, commit,
  or push except the separately authorized final recovery and acceptance in
  task 8.4.
- No production dependency.
- Every production change follows a recorded RED then GREEN cycle.
- `TASK_LEDGER.md`, OpenSpec artifacts, `.planning/STATE.md`, and final evidence remain main-agent owned.

## Target State

Shared and snapshot modes operate inside the target independent home. Switch/capture/restore hold a directory-inode store lock, validate all sources and effects, create schema-v2 evidence, commit or roll back as one operation, and never falsely restore a legacy backup.

## Completion Contract

- [x] Every specification scenario has a focused regression.
- [x] Existing shared official/internal behavior remains characterized and green.
- [x] No v0/v1 directory restore or corrupt payload can mutate a target.
- [x] Injected filesystem, finalize, and Desktop-effect failures restore the pre-operation state.
- [x] Focused tests, full legacy tests, strict OpenSpec, syntax, and diff checks pass.
- [x] Known `ipc` and `mcp-oauth-locks` runtime state is excluded before shared-support backup planning, with a real Unix-socket regression and unknown-special-file fail-closed guard.
- [x] A byte-identical Desktop global-state merge claims no transaction
  ownership, preserves a concurrent App write, and leaves real merge writes
  identity-bound and fail closed.

## Critical Path

Directory lock and recursive state → versioned backup/preflight → transaction engine/effect rollback → restore → capture → switch/snapshot → integration cleanup.

## Incidental Finding Budget

One bounded RED/GREEN guard is allowed for another mutation already inside this write set. `--shared-config-base` plus snapshot semantics, shell-profile symlink policy, and custom-profile behavior are recorded but not implemented by this change.

## 1. Characterization and Core State

- [x] 1.1 Add GREEN characterization tests `test_shared_internal_switch_preserves_existing_config_and_auth_contract` and `test_shared_official_switch_preserves_existing_config_and_auth_contract` in `scripts/test_codex_transaction.py`; run `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v` and record their baseline.
- [x] 1.2 Add RED tests `test_concurrent_transaction_returns_busy_before_backup_or_read`, `test_store_directory_lock_is_released_after_failure`, and `test_dry_run_performs_no_store_write`; confirm failure with `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py TransactionTests.test_concurrent_transaction_returns_busy_before_backup_or_read TransactionTests.test_store_directory_lock_is_released_after_failure TransactionTests.test_dry_run_performs_no_store_write -v`.
- [x] 1.3 Create `scripts/codex_switch_transaction.py` with `TransactionRequest`, `TransactionReceipt`, directory-inode `_StoreLock`, and the single `execute_transaction()` interface; make the three lock/dry-run tests GREEN.
- [x] 1.4 Add RED tests for recursive file/symlink/mode/tree state, unsupported object kinds, payload containment, and canonical restore-target allowlists; implement deterministic state/digest helpers in `codex_switch_transaction.py` and make them GREEN.

## 2. Versioned Backup and Restore

- [x] 2.1 Add RED tests `test_snapshot_switch_creates_schema_v2_restorable_backup`, `test_restore_rejects_v0_files_manifest`, `test_restore_accepts_attested_v1_file_and_symlink`, and `test_restore_rejects_v1_directory_even_with_force`.
- [x] 2.2 Implement schema-v2 `prepared|committed|rolled_back|rollback_failed` manifests and explicit v1/v0 readers in `scripts/codex_switch_restore.py`; retire `backup_live_files()` from supported official/internal writing while retaining its explicitly required custom compatibility caller; make 2.1 GREEN.
- [x] 2.3 Add RED tests `test_restore_preflights_later_missing_payload_before_first_mutation`, `test_restore_rejects_payload_escape`, `test_restore_rejects_unapproved_absolute_target`, and `test_restore_detects_changed_directory_descendant`.
- [x] 2.4 Move complete restore preflight, recursive post-state comparison, and staging before mutation into the transaction module; make 2.3 GREEN and verify zero target changes on every failure.
- [x] 2.5 Add RED tests `test_failed_restore_rolls_back_applied_entries`, `test_restore_creates_reversible_safety_backup`, and `test_rollback_failure_preserves_material_and_backup_id`; implement restore safety backup, reverse rollback, and failure receipts; make them GREEN.

## 3. Transactional Capture

- [x] 3.1 Add RED tests `test_invalid_capture_toml_preserves_existing_profile`, `test_required_auth_capture_failure_preserves_existing_profile`, `test_allowed_missing_auth_removes_stale_auth`, and `test_capture_preserves_unmanaged_plugin_support_files`.
- [x] 3.2 Implement cloned sibling staging for managed capture files in `scripts/codex_switch_capture.py` through `execute_transaction()`; validate before rename, preserve unmanaged files, explicitly remove absent allowed auth, and make 3.1 GREEN.
- [x] 3.3 Add RED tests `test_capture_second_rename_failure_restores_previous_profile`, `test_capture_finalize_failure_restores_previous_profile`, and `test_capture_recovers_or_rejects_incomplete_journal`; retain the old directory through finalization, add deterministic recovery classification, and make them GREEN.
- [x] 3.4 Migrate `cmd_capture` and indirect `cmd_init` capture callers to the transaction receipt without changing successful CLI output; run all capture/init tests in `scripts/test_codex_transaction.py` plus existing matching tests from `scripts/test_codex_profile_switch.py`.

## 4. Transactional Switch and Desktop Effects

- [x] 4.1 Add RED tests `test_internal_snapshot_targets_internal_home_only`, `test_snapshot_never_copies_official_auth_to_internal`, and `test_missing_binding_fails_dry_run_before_backup`.
- [x] 4.2 Replace snapshot/live-home dispatch in `scripts/codex_switch_switching.py` and `scripts/codex_switch_plan.py` with the lock-owned transaction planner; keep config strategy separate from target home and make 4.1 GREEN.
- [x] 4.3 Add RED failure-injection tests for shim write, plist write, GUI setenv, bootout, bootstrap, active-record write, and backup finalize; each test asserts home/config/auth/shim/plist/env/service/active state is restored.
- [x] 4.4 Implement `_DesktopBindingAdapter` around `scripts/codex_switch_launch.py`, journal every effect, apply `active.json` last, and make 4.3 GREEN; rollback failure must report `backup_id` and preserve recovery material.
- [x] 4.5 Fail closed on malformed existing `active.json` before collision checks; add `test_malformed_active_record_blocks_transaction_without_writes` and make it GREEN.
- [x] 4.6 Migrate `cmd_switch` and supported one-key official/internal callers to `execute_transaction()`; remove legacy backup writes from those paths while preserving the out-of-scope custom-profile compatibility route.

## 5. Cleanup and Verification

- [x] 5.1 Remove superseded duplicate planning/apply/restore helpers only after `rg` proves no supported official/internal caller remains; retain explicit v0/v1 readers, required custom callers, and recovery diagnostics.
- [x] 5.2 Run `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v` and require zero failures.
- [x] 5.3 Run `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` and require all legacy regressions to pass.
- [x] 5.4 Run `openspec validate transactional-profile-state --strict --no-interactive`, `bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh`, Python 3.12 AST/import checks for changed modules, and `git diff --check`.
- [x] 5.5 Record RED/GREEN commands, changed files, rollback evidence, compatibility limits, and residual risks in `.planning/devflow/verification/transactional-profile-state.md`; update this checklist only after the evidence passes.

## 6. Final Review Closure

- [x] 6.1 Re-run the stable 154-test snapshot under Python 3.9 and 3.12, map the 25 required vectors, and record independent review findings before further production edits.
- [x] 6.2 Add RED tests for one store-wide classifier: marker-required missing-marker switch/restore, markerless legacy switch, pre-marker restore `prepared|rollback_failed`, capture journal, corrupt/multiple evidence, dry-run byte identity, and switch/capture/restore/custom/init cross-operation gating; make them GREEN before dispatch.
- [x] 6.3 Add RED tests for atomically consistent switch rollback terminal evidence, bound `failure.json` fallback, terminal-marker cleanup retry/guidance, and custom-route terminal-marker retirement; make them GREEN without weakening corrupt-evidence handling.
- [x] 6.4 Add RED tests for switch rollback/recovery durability, complete prepared-recovery simulation before the first write, target-home ensure identity, Desktop already-restored retry, and every required prepared/marker/intent/action/applied/terminal/cleanup interruption point; make them GREEN.
- [x] 6.5 Add RED tests and implementation for restore parent-cleanup journal effects, durability, catchable rollback, second interruption, exact prior mode recreation, complete preflight, and terminal reread validation; make them GREEN through one shared recovery engine.
- [x] 6.6 Add RED tests for read-to-freeze changes across all direct and indirect plan inputs, including Desktop target RMW state; freeze each value at its producing read and revalidate before the dependent effect.
- [x] 6.7 Add RED tests proving the exact persisted staged artifact is installed, produced identity is checked before `applied`, repeated-path predecessor/identity chains recover, and every deterministic file and directory effect recovers after action-before-checkpoint interruption; make them GREEN with descriptor-relative operations.
- [x] 6.8 Replace path-based restore apply/recovery and parent cleanup with attested staged identities and descriptor-relative route-bound actions; cover stable attested lexical symlink compatibility, changed route identity, staged identity mismatch, later unrelated state preservation, and foreign empty-parent retention.
- [x] 6.9 Extend strict validation tests across every v1/v2 before/after/committed state kind and mode position, legal special bits, directory `entry_count`, both supported adopted homes, relative/non-canonical/backup-contained homes, failed nested-home rollback, and non-empty later parent edits.
- [x] 6.10 Move `cmd_init --capture-current` prewrites into one lock-owned already-locked dispatch; add busy/pending byte-identity and exact successful-output tests without nested lock acquisition.
- [x] 6.11 Render outcome-correct retained-marker guidance in successful CLI output, add missing custom/capture contention regressions, and remove only reviewer-proven dead imports after caller checks.
- [x] 6.12 Re-map every one of the 25 required matrix rows and every OpenSpec scenario to named tests; no row may remain `WEAK` or `MISSING`.
- [x] 6.13 Run dual-interpreter transaction suites, the 123-test legacy suite, strict OpenSpec, Bash syntax, dual-interpreter AST/import, contract validation, caller checks, stable hashes, and `git diff --check`; record fresh evidence before checking any completion item.

## 7. Runtime-State Incident Closure

- [x] 7.1 Record the installed `0.1.13` official-switch socket failure in the proposal, design, delta spec, `TASK_LEDGER.md`, and the existing change's execution ledger; do not create a second change.
- [x] 7.2 Add `test_official_shared_dry_run_ignores_profile_local_runtime_sockets` with real Unix sockets under `ipc` and `mcp-oauth-locks`; run it against the pre-fix implementation and record the exact RED.
- [x] 7.3 Add only `ipc` and `mcp-oauth-locks` to `RUNTIME_STATE_NAMES`, replace whole-home parent freezing with an identity-bound filtered shared-entry-set observation that still detects candidate additions, removals, and recursive drift, and create `target_home_ensure` effects only for genuinely missing directory chains; make the incident regression GREEN and retain a focused guard proving an unknown special shared-support object still fails closed before backup publication.
- [x] 7.4 Run the focused incident tests, complete transaction and profile suites, strict OpenSpec validation, syntax/diff checks, and a repository-source read-only official dry-run; record results and leave install/live official switch as a separate Human Gate.

## 8. Desktop Global-State No-Op Incident Closure

- [x] 8.1 Add
  `test_shared_switch_preserves_concurrent_desktop_global_state_after_noop_merge`
  and run it against the current implementation; require the deterministic RED
  to reproduce `rollback_failed`, retained pending evidence, and preservation
  of the concurrent App-owned target bytes.
- [x] 8.2 Split the Desktop target producing-read observation from other shared
  inputs; when the merge is byte-identical, release that observation and omit
  the path from planned commit states, backup, staging, journal, and rollback.
  Keep the existing retained observation and staged effect when bytes differ;
  make 8.1 GREEN and add a focused guard for the real-merge path. Add a strict
  legacy-recovery regression that accepts only the exact marker-bound no-op
  `rollback_failed` shape and preserves the current App-owned target.
- [x] 8.3 Reproduce the live recovery failure with a preceding byte-identical
  shared-support effect that receives a later external write; require RED
  before expanding the exact marker-bound compatibility classifier to release
  only strictly evidenced no-op effects, preserve the later write, and keep
  every real planned change fail closed.
- [x] 8.4 Run the focused incident tests, complete transaction/profile suites,
  strict OpenSpec, static/package checks, reinstall the current source, recover
  the retained live transaction through the supported path, and repeat the
  authorized official/internal Desktop acceptance.

## Execution Ledger

| Slice | Owner | Write Set | Evidence | Human Gate | Next Outcome | Status |
|---|---|---|---|---|---|---|
| Core state and lock | delegated worker | transaction module and transaction test | focused RED/GREEN log | scope/compatibility expansion | CONTINUE_NEXT_ITEM | done |
| Backup and restore | delegated worker | backup/restore plus transaction module/test | corruption/conflict/rollback log | v1 behavior beyond spec | COMPLETE | done |
| Capture | delegated worker | capture/lifecycle integration plus transaction test | atomic replacement log | public capture contract expansion | CONTINUE_NEXT_ITEM | done |
| Switch/effects | delegated worker then main integration | switching/plan/launch plus transaction test | injected-effect rollback log | live launchctl action | COMPLETE | done |
| Final verification | main | control plane and evidence only | full commands | external effects | COMPLETE | done |
| Final review closure | serialized worker then independent reviewers | transaction/restore/switching/lifecycle/launch/I/O plus transaction tests | 25-row matrix and stable-hash rerun | compatibility or write-set expansion | COMPLETE | done |
| Runtime-state incident closure | main | home-sync classification, transaction regression, control plane, evidence | real Unix-socket RED/GREEN plus full regressions | install or live official switch | COMPLETE | done |
| Desktop global-state no-op incident closure | main | transaction planner/test plus control plane/evidence | deterministic concurrent-write RED/GREEN plus full/live regressions | live recovery, install, and App restart already authorized | COMPLETE | done |

## Validation Commands

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
openspec validate transactional-profile-state --strict --no-interactive
bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh
git diff --check
```

## Risks / Rollback

- Directory exchange is journaled rollback, not a single-syscall swap.
- v1 directories and v0 manifests remain preserved but are intentionally not auto-restored.
- Roll back by restoring pre-change source; no implementation test mutates the live store.
