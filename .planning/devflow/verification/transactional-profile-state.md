# Evidence: TPS-001

## Claim

Final evidence: all `transactional-profile-state` tasks and completion items
are implemented and verified. Every supported transaction entry reaches one store-wide classifier
before dispatch. Switch rollback now publishes an atomically consistent outer
lifecycle and journal state, an unreadable `backup.json` may fall back only to
a marker-bound verified `rolled_back` receipt, dry-run preserves terminal
markers byte-for-byte, and the next applying supported or custom route retires
valid terminal evidence before its first write. Switch rollback and prepared
recovery now make every reversed filesystem effect durable before terminal
publication, record a terminal recovery state for every journal effect,
preflight target-home identity before any recovery write, accept an
already-restored Desktop state idempotently, and recover across every required
checkpoint interruption. Restore-created parent cleanup is now a first-class
durable journal effect. Catchable failure and later-invocation recovery share
one engine, restore the exact prior directory mode, survive a second
interruption, fully preflight cleanup identity before any recovery write, and
strictly reread terminal evidence before marker cleanup. The overall
switch plan now captures state and inode immediately before every producing
read, verifies them immediately after the read, and carries the same frozen
evidence through every effect boundary. Product manifests, active state,
profile/base/target and composite configs, auth bytes, plugin snapshots, shell
input, binding inputs, shared entry sets and descendants, stale links, and both
sides of Desktop global-state read-modify-write reject drift before backup or
dependent action. File replacements now install the exact durable staged inode
through the pinned destination parent, and the journal rejects a different
produced inode before `applied`. Native directory actions record their produced
identity inside the adapter boundary and are checked after the action returns.
Repeated writes to one destination retain phase-specific stages and recover
through the full predecessor/identity chain. Action-before-checkpoint recovery
is covered for all 15 deterministic file phases plus target-home creation and
shared-directory copy. Restore apply, rollback, prepared recovery, and parent
cleanup now use attested staged/predecessor/produced identities and pinned
descriptor routes. Stable lexical symlink ancestors remain compatible, route
or stage replacement fails closed, unrelated later objects are preserved, and
directory recovery resumes after its safety payload inode was moved into place.
All recorded v1/v2 state modes and schema-v2 directory entry counts are now
strictly validated, both supported adopted-home roots share one normalized
authority check, and nested-home rollback preserves later non-empty or replaced
state. Init classification, managed prewrites, and optional capture now share
one inode-revalidated store lock and an explicit already-locked capture
dispatch. Successful supported switches now append structured outcome-correct
retained-marker guidance, and direct supported/custom/capture contention tests
are byte-preserving. Init capture failure now restores the exact pre-init store
tree and modes without emitting partial stdout. Switch terminal reread validates
the complete marker-bound entries, payload, identity, effect-chain, and finalize
evidence; claimed but invalid committed evidence remains blocked with its marker.
Every required 25-row review vector and all 36 OpenSpec scenarios now map to
existing named tests with no `WEAK` or `MISSING` row. Final dual-runtime,
legacy, strict OpenSpec, Bash, AST/import, contract, caller, stable-hash, and
diff gates pass.

## Commands Run

| Command | Exit | Evidence File / Output Summary |
|---|---:|---|
| `/usr/bin/python3 scripts/test_codex_transaction.py -q` | 0 | 207/207 passed on Python 3.9, then passed again after recording stable source hashes |
| `/opt/homebrew/bin/python3.12 scripts/test_codex_transaction.py -q` | 0 | 207/207 passed on Python 3.12, then passed again after recording stable source hashes |
| `/usr/bin/python3 -m unittest -q test_codex_profile_switch.py` | 0 | 123/123 legacy regressions passed |
| focused 6.7 staged-identity, repeated-path, file/directory interruption selections | 0 | exact staged inode, foreign file/directory identity rejection, repeated-path recovery, 15 file phases, and 2 directory families passed |
| focused 6.8 restore route/stage/identity/parent/interruption selections | 0 | exact file stage inode, lexical symlink stability/change, stage replacement, foreign-parent retention, parent recreation, and consumed directory-stage recovery passed |
| focused 6.9 strict metadata/adopted-home/nested-parent selections | 0 | three mandatory tests passed across their v1/v2, profile, and rollback submatrices |
| focused 6.10 init/capture locking selections | 0 | busy/pending byte identity, one lock acquisition, and exact successful output passed |
| focused 6.11 CLI/contention selections | 0 | committed retained-marker output, supported lock contention, and pending-capture custom blocking passed |
| focused 6.12 terminal/init/cleanup/drift/caller selections | 0 | strict terminal reread, restore cleanup retry, exact init rollback/output/lock, later-drift preservation, nested-parent retention, and dead-helper caller proof passed |
| focused terminal-stage/silent-write/nested-authority review selections | 0 | corrupt staged evidence and silent terminal corruption first reproduced false commit; nested created-parent authority first reproduced false rejection; all focused tests then passed |
| coverage-table name and sequence validator | 0 | 207 test methods discovered; 111 referenced names exist; 25/25 matrix rows and 36/36 scenario rows are contiguous and `COVERED` |
| Python 3.9 and 3.12 AST/import checks | 0 | transaction/switching/capture/lifecycle/test parsed and production modules imported without bytecode writes |
| AST import-use scan plus `rg` caller check | 0 | only dead switching wrapper import removed; live transaction/app-wrapper callers retained |
| `openspec validate transactional-profile-state --strict --no-interactive` | 0 | change valid |
| `openspec validate --all --strict --no-interactive` | 0 | 15/15 items passed |
| `bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh` | 0 | all named Bash entry points parsed |
| Python 3.9 and 3.12 AST/import checks | 0 | 9 files parsed and 8 production modules imported under each interpreter without bytecode writes |
| `validate_agent_task_contract.py --contract ...transaction-final-review-closure.md --json` | 0 | `ok: true`, zero errors, zero missing sections |
| final removed/live caller checks | 0 | zero callers for the bounded removed-helper set; retained backup/custom/restore/wrapper callers remain present |
| `git diff --check` | 0 | tracked diff clean |
| `git diff --no-index --check /dev/null scripts/codex_switch_transaction.py` | 1 | expected new-file diff status; no whitespace diagnostics |
| `git diff --no-index --check /dev/null scripts/test_codex_transaction.py` | 1 | expected new-file diff status; no whitespace diagnostics |

Stable SHA-256 values:

- `scripts/codex_switch_transaction.py`: `05b6a277b1c8685bb35c082bbbaa0fd4c3e5e991986fb2af182aa607d8d318e7`
- `scripts/codex_switch_switching.py`: `df1ee11d5d03b63f1d043641e65948d878eb5679fbef0f582bccd5380a1c70f1`
- `scripts/codex_switch_capture.py`: `9d305266ff6a152d79e73e794930aeb7a2b817e651fc9b47c16b207f313daef9`
- `scripts/codex_switch_lifecycle.py`: `df0054dfa5b3b82a6c210f15d27506bdf9df8c13744597c0acee9a35a6077fc9`
- `scripts/test_codex_transaction.py`: `b1b0b9ad6aa102c0d905fbd102fbfac42203d60d823d13b48be8be77efe1c955`
- `scripts/codex_switch_restore.py`: `b4392bfb8629b864060f180c60dc047c9bde283ae995bcccab244384e832b41a`
- `scripts/codex_switch_launch.py`: `5f08c0a73753f22bd8f34f58695ea4d62751974ad34da6535857d5f8d55f1dc2`
- `scripts/codex_switch_io.py`: `86dd60ce5459b67c9f759c8c3a4dc24a9af9a3c3c8ffae42ef635118a85c2970`
- `scripts/codex_switch_home_select.py`: `eab9c43935a7f3cab268b076fbce840cc0d26092858ae8e1473edc21d8b6a921`
- `scripts/codex_switch_plan.py`: `d3cdfd41cf809403b70a7188bc28353b01f18c3278db23b721f72164709e01b7`
- `scripts/codex_switch_backup.py`: `69d503ddcd965de3fb6586940b1550c08d59585093acf0d5952d42b4d37c223d`
- `scripts/test_codex_profile_switch.py`: `bacb00a9e022ee05f469c7b0d9a6bce3502be18e44dfb395d1321faf0283dd1e`

## TDD Evidence

- RED: `test_marker_required_switch_without_marker_blocks_cross_operation_capture`
  first completed the capture instead of raising; `test_pre_marker_restore_blocks_custom_mutation_gate`
  admitted the custom writer; `test_pre_marker_restore_blocks_init_before_store_writes`
  initialized files before raising. Each focused command exited 1 on the exact
  missing classifier/gate behavior.
- RED: `test_switch_rollback_publishes_atomic_terminal_manifest` observed an
  outer `rolled_back` lifecycle paired with a still-`prepared` journal;
  `test_unreadable_backup_manifest_during_failure_uses_in_memory_rollback`
  could not retry because corrupt `backup.json` had no trusted fallback;
  retained-marker guidance mislabeled rollback as committed; and the custom
  gate admitted a valid terminal marker without retiring it.
- RED: switch rollback and prepared recovery durability tests observed
  materialization followed directly by terminal publication with no explicit
  effect fsync; the target-home ensure identity test detected the mismatch only
  after three destination writes; effect-level terminal recovery state was
  absent; and a marker parent-sync failure after unlink produced guidance that
  claimed a marker still existed when it did not.
- RED: restore parent cleanup had no journal effect or recovery checkpoint;
  catchable cleanup failure recreated a prior `0751` directory as `0755`;
  hard interruption had no parent-recreation recovery action; complete
  recovery preflight did not bind the cleanup directory identity; and a corrupt
  or unbound committed terminal manifest could be accepted for marker cleanup.
- RED: every one of the 14 `test_planning_reads_are_frozen_atomically_for_every_switch_input`
  subcases completed without raising. A change after the producing read was
  adopted for manifests, active state, profile/base/target and composite
  configs, auth, plugin snapshots, Desktop source and target global state,
  shell profile, shared entry enumeration, stale links, and executable binding.
- RED: `test_switch_installs_persisted_stage_and_rejects_identity_change_before_applied`
  showed the destination inode differed from the journaled stage and accepted a
  byte-identical foreign inode. `test_interrupted_repeated_path_effect_chain_recovers`
  failed before its second action because the first result was compared with
  the final frozen state. A normal shared-directory action failed after changing
  its parent mode through the lexical helper, and
  `test_directory_effect_rejects_identity_change_before_applied` committed a
  same-tree foreign directory inode.
- RED: restore installed a fresh copy rather than the attested staged file
  inode, accepted a replaced staged artifact, followed a changed lexical
  symlink route during rollback, removed a foreign empty-parent replacement,
  and could not resume after directory recovery moved its safety payload before
  a second interruption.
- GREEN: those regressions plus real effect-free/begun switch and restore
  marker-loss, legacy markerless recovery, corrupt historical coexistence,
  pre-marker `prepared|rollback_failed`, multiple/corrupt evidence, capture
  journal, atomic terminal state, strictly bound fallback positive/negative
  cases, supported/custom cleanup retry, per-effect recovery terminal state,
  target-home early identity rejection, Desktop already-restored retry,
  durability interruption re-entry, prepared/marker/intent/action/applied/
  terminal/cleanup checkpoints, and dry-run byte-identity cases pass. Restore
  parent cleanup intent/action/applied ordering, exact-mode catchable
  rollback, second-interruption idempotence, cleanup-identity preflight before
  any recovery write, v1 file/symlink and nested-parent compatibility, and
  strict terminal reread cases pass. Full transaction suites pass 181/181 on
  Python 3.9 and 3.12. The producing-read tracker matrix then passes all 14
  cases before any backup creation, and full transaction suites pass 182/182
  on both runtimes. Phase-keyed durable stages, descriptor-relative hard-link
  installation, adapter-owned directory/symlink actions, native produced
  identity capture, and repeated-path recovery sources then make all task 6.7
  regressions pass; the full suites pass 187/187 on both runtimes.
- GREEN: restore file and directory stages retain exact identity through apply
  and recovery; lexical and canonical routes are descriptor-bound; parent
  cleanup/recreation carries inode evidence; safe no-action rollback tolerates
  an unrelated route change without following it; and recovery recognizes its
  own persisted produced identity after both file and directory interruptions.
  Full transaction suites pass 192/192 on both runtimes.
- RED: the task 6.9 validation matrix produced 37 failures. Missing/symlink
  state modes were not uniformly validated, v1 directory rejection hid an
  invalid mode, before/committed directory entry-count mismatches were accepted
  even with `--force`, lexical `..` and final-component symlink adopted homes
  were admitted, and a changed nested target-home directory could be deleted
  during catchable rollback.
- GREEN: `test_recorded_mode_and_directory_entry_count_validation_matrix`,
  `test_supported_adopted_home_authority_matrix`, and
  `test_failed_nested_home_cleanup_preserves_changed_or_non_empty_parent` pass.
  Valid modes through `0o7777`, both supported profiles, normalized/canonical
  authority boundaries, exact target-home inode cleanup, and retained later
  state are covered. Full transaction suites pass 195/195 on Python 3.9 and
  3.12; the legacy suite passes 123/123.
- RED: `test_init_capture_uses_one_store_lock_and_preserves_exact_output`
  observed two `_StoreLock` entries: init preflight released its lock before
  official manifest/config writes and capture then acquired a second lock.
- GREEN: `test_init_capture_busy_and_pending_are_byte_identical` and the
  single-lock/output regression pass. One active dispatcher now owns init
  classification and capture without reacquisition; busy and pending paths
  preserve the full store state while committed stdout remains byte-for-byte
  compatible. Full transaction suites pass 197/197 on Python 3.9 and 3.12;
  the legacy suite passes 123/123.
- RED: `test_committed_marker_cleanup_warning_is_rendered_by_switch_cli`
  committed and retained the marker correctly, but the supported switch CLI
  printed only `Switched` and `Backup`; the recovery guidance existed only in
  ignored preview lines.
- GREEN: `test_committed_marker_cleanup_warning_is_rendered_by_switch_cli`,
  `test_supported_switch_contention_is_byte_identical`, and
  `test_pending_capture_blocks_custom_before_write` pass. Successful receipts
  expose dedicated guidance lines, the CLI appends the actual `committed`
  cleanup outcome, and both contention paths preserve all observed bytes and
  create no transaction marker. Full transaction suites pass 200/200 on both
  runtimes; the legacy suite passes 123/123.
- RED: `test_switch_terminal_reread_rejects_unbound_committed_manifest`
  received `committed` for both an unbound transaction ID and a minimal empty
  committed object because the reread checked only lifecycle plus one finalize
  effect. `test_cmd_init_capture_failure_restores_pre_init_store_and_preserves_stdout_contract`
  found seven residual layout/profile entries and a root-mode change after an
  invalid capture source.
- GREEN: strict switch terminal validation now consumes the retained marker and
  validates binding, digest, approved entries, payloads, identities, ordered
  applied effect chain, stages, and unique terminal finalize. A claimed but
  invalid commit returns `rollback_failed` without cleanup or speculative
  rollback. Init snapshots only its managed file/directory prewrites beneath
  the same lock and restores missing/existing files, directory modes, and empty
  created layout on capture failure. Restore committed-marker cleanup retry and
  later external switch-target drift have direct passing regressions. The
  25-row/36-scenario tables reference only real tests; the focused 6.12 command
  passed 9/9.
- RED: the final completion review extended terminal reread with a mismatched
  persisted-stage digest and observed a false `committed` result. A second
  adapter silently wrote an unbound committed manifest without raising; the
  normal switch path trusted the in-memory return value, deleted the marker,
  and again reported `committed`. After those fixes, the first 206-test full
  rerun exposed a false `rollback_failed` for a valid nested adopted-home
  switch, and `test_nested_missing_manifest_home_recovers_before_retry` showed
  prepared recovery rejected its journaled ancestor-creation effect before any
  write.
- GREEN: committed-switch validation now reattests every staged file's actual
  state, inode, route, and identity equality with its installed result. Both
  normal and exception terminal paths consume the same authoritative on-disk
  validator before marker cleanup. Transaction-created ancestor authority is
  accepted only when it is a contiguous canonical backup-external chain named
  by a missing entry and covered by `target_home_ensure` effects whose own
  predecessor is missing; the same rule is shared by terminal validation and
  prepared recovery. Both nested-home tests and all terminal positive/negative
  tests pass. Final suites pass 207/207 on Python 3.9 and 3.12 plus 123/123
  legacy; the two transaction suites passed again against unchanged hashes.
- Regression check: `scripts/test_codex_transaction.py` on both supported local
  Python runtimes.

## Changed Files

- `scripts/codex_switch_transaction.py`: one store-wide recovery classifier,
  explicit unmarked evidence classes, safe effect-free closure, legacy switch
  recovery before any supported dispatch, shared custom/init preflight,
  atomic switch terminal lifecycle/journal writes, strict bound failure-record
  fallback, outcome-aware marker retirement/republish after uncertain unlink,
  effect-specific rollback/recovery durability, complete per-effect terminal
  state, read-only target-home recovery preflight, durable restore parent
  cleanup effects, exact-mode parent recreation, complete restore-recovery
  preflight, strict authoritative committed-restore validation, and one
  state-plus-inode planning-input tracker that brackets every direct or
  indirect producing read and supplies the immutable journal evidence; plus
  phase-keyed staged artifacts, exact inode installation, native produced
  identity checks, descriptor-relative shared file/tree/link actions, and
  predecessor-aware repeated-path recovery. Restore-specific stages, routes,
  target/parent identities, and recovery checkpoints now use the same
  descriptor-relative contract, including idempotent consumed-directory-stage
  recognition; plus uniform recorded-mode and directory-entry-count validation,
  supported adopted-home authority checks, and identity-bound catchable
  target-home cleanup; plus the inode-revalidated locked-store dispatcher used
  to keep init classification and capture under one lock; plus structured
  successful receipt guidance for retained marker cleanup; plus one strict
  on-disk committed-switch validator shared by normal and exceptional terminal
  paths, with actual staged state/inode/route reattestation and narrowly bounded
  contiguous created-parent authority for nested-home terminal/recovery paths.
- `scripts/codex_switch_capture.py`: optional internal locked-store dispatch
  avoids reacquiring the store lock while retaining the default public capture
  path and output/error contract.
- `scripts/codex_switch_home_select.py`: no production behavior change retained;
  the temporary canonical-string writer experiment was reverted to preserve
  stable macOS ancestor-alias compatibility.
- `scripts/codex_switch_switching.py`: custom compatibility routing propagates
  dry-run state into the common mutation gate so preview never retires evidence;
  supported success output appends structured transaction guidance. The one
  statically proven dead wrapper-path import was removed.
- `scripts/codex_switch_lifecycle.py`: init holds one shared recovery-classified
  store lock across layout, official manifest/config writes, optional capture,
  and output; failed optional capture restores the exact pre-init managed state
  and prior directory modes before propagating the original error.
- `scripts/test_codex_transaction.py`: focused cross-operation recovery-gate,
  corruption, ambiguity, dry-run, custom, init, restore parent-cleanup,
  recovery-interruption, complete-preflight, terminal-reread, and 14-family
  read-to-freeze regressions, plus exact stage/identity, repeated-path, all-file
  action-interruption, directory action/interruption, silent terminal
  corruption, staged terminal tampering, and nested-home recovery coverage.
- `.agents/skills/diagnosing-bugs/**`: refreshed project-local pinned
  methodology resource required by the DevFlow execution gate.

## Risks / Gaps

- No in-scope implementation or verification gap remains for this change.
- Tests use isolated temporary stores, fake Desktop state, and child processes;
  the explicitly out-of-scope live workstation switch/rebind remains unrun.
- No live workstation profile/App/launchctl/install/update/release action ran.

## Required 25-Row Matrix

Every row is mapped to an executable, individually named regression. `COVERED`
means the named test exists in `scripts/test_codex_transaction.py` and the
focused task-6.12 selection passed; full dual-runtime evidence is recorded by
task 6.13.

| Row | Required vector | Named regression coverage | Status |
|---:|---|---|---|
| 1 | Catchable error after terminal switch write remains committed | `test_terminal_switch_write_followed_by_catchable_error_stays_committed` | COVERED |
| 2 | Catchable error after terminal restore write remains committed | `test_terminal_restore_write_followed_by_catchable_error_stays_committed` | COVERED |
| 3 | Backup, journal, marker, `atomic_write`, and `_atomic_write_at` are durable before intent/action | `test_atomic_write_fsyncs_file_then_parent_without_chmod_existing_parent`<br>`test_descriptor_atomic_write_fsyncs_parent_after_rename`<br>`test_switch_publishes_bound_marker_after_durable_backup_before_first_intent`<br>`test_restore_publishes_bound_marker_before_first_intent_and_action` | COVERED |
| 4 | Prepared/marker/intent/action/applied/terminal/unlink interruption classification | `test_switch_prepared_marker_intent_and_applied_interruptions_recover`<br>`test_hard_interruption_after_filesystem_mutation_recovers_before_fresh_transaction`<br>`test_hard_interruption_at_backup_finalize_recovers_before_fresh_transaction`<br>`test_hard_interruption_after_atomic_backup_finalize_stays_committed`<br>`test_switch_rollback_marker_cleanup_failure_is_retryable_and_retires_marker` | COVERED |
| 5 | Corrupt/missing/mismatched/multiple/rollback-failed evidence blocks all new writes | `test_corrupt_pending_marker_blocks_every_supported_mutation_without_writes`<br>`test_unreadable_backup_manifest_rejects_unbound_failure_records_without_writes`<br>`test_prepared_switch_missing_later_payload_blocks_before_first_recovery_write`<br>`test_mismatched_pending_transaction_id_blocks_without_writes`<br>`test_multiple_pending_markers_block_without_writes`<br>`test_pending_rollback_failed_evidence_blocks_without_writes`<br>`test_switch_terminal_reread_rejects_silent_corruption_before_marker_cleanup` | COVERED |
| 6 | Unrelated corrupt history is ignored and bounded legacy markerless switch recovery remains compatible | `test_legacy_markerless_switch_recovers_before_cross_operation_capture` | COVERED |
| 7 | Missing-marker provenance, pre-marker restore, and bound failure fallback are fail-closed | `test_effect_free_marker_required_switch_without_marker_is_closed_before_capture`<br>`test_marker_required_switch_without_marker_blocks_cross_operation_capture`<br>`test_effect_free_marker_required_restore_without_marker_closes_before_retry`<br>`test_begun_marker_required_restore_without_marker_blocks_before_writes`<br>`test_pre_marker_restore_states_block_every_transaction_operation`<br>`test_unreadable_backup_manifest_during_failure_uses_in_memory_rollback`<br>`test_unreadable_backup_manifest_rejects_unbound_failure_records_without_writes` | COVERED |
| 8 | Cross-operation pending gates, matching capture retry, and dry-run/blocked byte identity | `test_dry_run_reports_pending_switch_recovery_without_writes`<br>`test_pre_marker_restore_states_block_every_transaction_operation`<br>`test_unfinished_capture_is_store_wide_gate_and_dry_run_is_read_only`<br>`test_capture_recovers_prepared_journal_before_rejecting_invalid_retry_source`<br>`test_init_capture_busy_and_pending_are_byte_identical` | COVERED |
| 9 | Restore recovers after first-target interruption, a second interruption, and an idempotent retry | `test_restore_recovery_is_idempotent_across_second_hard_interruption`<br>`test_restore_directory_recovery_is_idempotent_after_stage_move` | COVERED |
| 10 | Restore recovery consumes frozen adopted-home authority after manifest mutation | `test_restore_recovery_uses_frozen_allowlist_after_manifest_mutation` | COVERED |
| 11 | Restore parent-cleanup interruption restores prior state | `test_restore_parent_cleanup_failure_restores_removed_parent_and_prior_mode`<br>`test_restore_parent_cleanup_hard_interruption_recovers_idempotently` | COVERED |
| 12 | Desktop already at `desktop_before` is accepted idempotently | `test_prepared_switch_recovery_accepts_desktop_already_restored_without_reconcile` | COVERED |
| 13 | Every deterministic filesystem effect family recovers after action/before-applied | `test_every_deterministic_file_effect_recovers_after_action_before_applied`<br>`test_every_deterministic_directory_effect_recovers_after_action_before_applied` | COVERED |
| 14 | Late active/shell/plugin/auth/shared/composite drift is rejected before overwrite | `test_switch_rejects_late_active_drift_before_active_action`<br>`test_switch_rejects_late_shell_profile_drift_before_shell_action`<br>`test_switch_rejects_late_plugin_snapshot_drift_before_snapshot_action`<br>`test_switch_rejects_late_auth_source_drift_before_auth_action`<br>`test_switch_rejects_late_shared_source_drift_before_shared_action`<br>`test_switch_rejects_late_composite_config_source_drift_before_config_action` | COVERED |
| 15 | Symlink/byte-identical route swaps are rejected and pinned parent prevents redirection | `test_switch_pinned_parent_prevents_symlink_redirection_after_route_validation`<br>`test_switch_rejects_changed_attested_symlink_ancestor_before_overwrite`<br>`test_switch_rejects_canonical_parent_swap_between_route_check_and_open`<br>`test_restore_rejects_parent_symlink_swap_before_materialize` | COVERED |
| 16 | Foreign inode after interrupted replacement cannot satisfy persisted-stage identity | `test_switch_recovery_rejects_byte_identical_foreign_inode_after_interruption`<br>`test_switch_installs_persisted_stage_and_rejects_identity_change_before_applied` | COVERED |
| 17 | Late external target drift is never overwritten by rollback | `test_switch_rollback_preserves_later_change_to_already_produced_target`<br>`test_restore_late_external_drift_fails_closed_without_reverse_writes` | COVERED |
| 18 | Existing home mode survives success/failure, new home is `0700`, and nested created chains clean safely | `test_adopted_manifest_home_switch_is_restorable_and_preserves_mode`<br>`test_switch_rollback_preserves_later_change_to_already_produced_target`<br>`test_first_switch_failure_removes_new_target_home`<br>`test_nested_missing_manifest_home_records_and_removes_full_created_chain`<br>`test_nested_missing_manifest_home_recovers_before_retry`<br>`test_failed_nested_home_cleanup_preserves_changed_or_non_empty_parent` | COVERED |
| 19 | Adopted official/internal home backups restore successfully | `test_supported_adopted_home_authority_matrix`<br>`test_adopted_manifest_home_switch_is_restorable_and_preserves_mode` | COVERED |
| 20 | Empty entries and invalid v1/v2 modes fail before safety backup even with force | `test_restore_rejects_empty_v1_and_v2_entries_before_safety_backup_even_with_force`<br>`test_restore_rejects_invalid_recorded_modes_before_safety_backup_even_with_force`<br>`test_recorded_mode_and_directory_entry_count_validation_matrix` | COVERED |
| 21 | Out-of-authority or missing/corrupt later recovery evidence fails before the first write | `test_restore_rejects_unapproved_absolute_target`<br>`test_prepared_switch_missing_later_payload_blocks_before_first_recovery_write`<br>`test_restore_preflights_later_missing_payload_before_first_mutation`<br>`test_prepared_restore_recovery_preflights_parent_cleanup_identity_before_any_write` | COVERED |
| 22 | Switch/restore cleanup failure remains committed, is visible, and next apply retires the marker | `test_committed_marker_cleanup_warning_is_rendered_by_switch_cli`<br>`test_restore_committed_marker_cleanup_failure_is_retryable_and_retires_marker`<br>`test_custom_gate_retires_valid_committed_terminal_marker`<br>`test_switch_rollback_marker_cleanup_failure_is_retryable_and_retires_marker` | COVERED |
| 23 | Stable lexical symlink ancestor remains compatible; identity/target change fails closed | `test_switch_accepts_stable_attested_symlink_ancestor`<br>`test_switch_rejects_changed_attested_symlink_ancestor_before_overwrite`<br>`test_restore_attests_stable_lexical_symlink_route_and_rejects_change` | COVERED |
| 24 | Custom apply receives busy, writes nothing, and never creates supported marker evidence | `test_custom_apply_respects_common_store_lock_without_marker`<br>`test_pending_capture_blocks_custom_before_write` | COVERED |
| 25 | Removed transaction helpers have no callers while compatibility callers remain | `test_removed_transaction_helpers_have_no_callers_and_compatibility_callers_remain` | COVERED |

## OpenSpec Scenario Map

| # | OpenSpec scenario | Named regression coverage | Status |
|---:|---|---|---|
| 1 | Snapshot mode preserves independent homes | `test_internal_snapshot_targets_internal_home_only`<br>`test_snapshot_never_copies_official_auth_to_internal` | COVERED |
| 2 | Dry-run rejects an invalid required binding | `test_missing_binding_fails_dry_run_before_backup` | COVERED |
| 3 | Late Desktop binding failure rolls back the switch | `test_gui_setenv_failure_rolls_back_complete_switch_state`<br>`test_bootout_failure_rolls_back_complete_switch_state`<br>`test_bootstrap_failure_rolls_back_complete_switch_state` | COVERED |
| 4 | Every switch backup is restorable by the current schema | `test_snapshot_switch_creates_schema_v2_restorable_backup`<br>`test_adopted_manifest_home_switch_is_restorable_and_preserves_mode` | COVERED |
| 5 | Legacy manifest is rejected explicitly | `test_restore_rejects_v0_files_manifest` | COVERED |
| 6 | V1 compatibility is evidence-bounded | `test_restore_accepts_attested_v1_file_and_symlink`<br>`test_restore_rejects_v1_directory_even_with_force` | COVERED |
| 7 | Missing or corrupt payload causes zero mutations | `test_restore_preflights_later_missing_payload_before_first_mutation`<br>`test_restore_rejects_payload_escape`<br>`test_restore_rejects_corrupt_payload_before_first_mutation` | COVERED |
| 8 | Recursive directory conflict blocks non-force restore | `test_restore_detects_changed_directory_descendant` | COVERED |
| 9 | Restore creates a rollback backup | `test_restore_creates_reversible_safety_backup`<br>`test_failed_restore_rolls_back_applied_entries` | COVERED |
| 10 | Required auth failure preserves the previous profile | `test_required_auth_capture_failure_preserves_existing_profile` | COVERED |
| 11 | Allowed missing auth clears stale credentials | `test_allowed_missing_auth_removes_stale_auth`<br>`test_capture_preserves_unmanaged_plugin_support_files` | COVERED |
| 12 | Invalid TOML preserves the previous profile | `test_invalid_capture_toml_preserves_existing_profile` | COVERED |
| 13 | Concurrent mutation receives busy result | `test_concurrent_transaction_returns_busy_before_backup_or_read`<br>`test_first_capture_busy_race_does_not_chmod_store_root_before_lock` | COVERED |
| 14 | Malformed active record fails closed | `test_malformed_active_record_blocks_transaction_without_writes` | COVERED |
| 15 | Prepared evidence is durable before mutation intent | `test_switch_publishes_bound_marker_after_durable_backup_before_first_intent`<br>`test_restore_publishes_bound_marker_before_first_intent_and_action`<br>`test_capture_fsyncs_stage_and_prepared_journal_before_both_renames` | COVERED |
| 16 | Every mutation route uses one recovery gate | `test_corrupt_pending_marker_blocks_every_supported_mutation_without_writes`<br>`test_capture_journal_blocks_custom_and_init_routes_before_writes`<br>`test_pre_marker_restore_states_block_every_transaction_operation` | COVERED |
| 17 | Missing marker is interpreted by journal provenance | `test_effect_free_marker_required_switch_without_marker_is_closed_before_capture`<br>`test_marker_required_switch_without_marker_blocks_cross_operation_capture`<br>`test_effect_free_marker_required_restore_without_marker_closes_before_retry`<br>`test_begun_marker_required_restore_without_marker_blocks_before_writes` | COVERED |
| 18 | Legacy markerless evidence remains bounded | `test_legacy_markerless_switch_recovers_before_cross_operation_capture`<br>`test_pre_marker_restore_states_block_every_transaction_operation` | COVERED |
| 19 | Verified independent rollback evidence survives manifest corruption | `test_unreadable_backup_manifest_during_failure_uses_in_memory_rollback`<br>`test_unreadable_backup_manifest_rejects_unbound_failure_records_without_writes` | COVERED |
| 20 | Terminal marker cleanup is retryable and visible | `test_committed_marker_cleanup_warning_is_rendered_by_switch_cli`<br>`test_restore_committed_marker_cleanup_failure_is_retryable_and_retires_marker`<br>`test_switch_rollback_marker_cleanup_failure_is_retryable_and_retires_marker`<br>`test_custom_gate_retires_valid_committed_terminal_marker` | COVERED |
| 21 | Read-to-freeze changes cannot be adopted | `test_planning_reads_are_frozen_atomically_for_every_switch_input`<br>`test_switch_rejects_late_composite_config_source_drift_before_config_action` | COVERED |
| 22 | Replacement installs the recorded staged artifact | `test_switch_installs_persisted_stage_and_rejects_identity_change_before_applied`<br>`test_restore_installs_the_attested_staged_file_inode` | COVERED |
| 23 | Identity change before applied checkpoint is not accepted | `test_switch_recovery_rejects_byte_identical_foreign_inode_after_interruption`<br>`test_directory_effect_rejects_identity_change_before_applied` | COVERED |
| 24 | Repeated effects on one destination form a chain | `test_interrupted_repeated_path_effect_chain_recovers` | COVERED |
| 25 | Directory effects use the same identity contract | `test_every_deterministic_directory_effect_recovers_after_action_before_applied`<br>`test_nested_missing_manifest_home_recovers_before_retry`<br>`test_failed_nested_home_cleanup_preserves_changed_or_non_empty_parent` | COVERED |
| 26 | Attested lexical symlink ancestor remains compatible | `test_switch_accepts_stable_attested_symlink_ancestor`<br>`test_switch_rejects_changed_attested_symlink_ancestor_before_overwrite`<br>`test_restore_attests_stable_lexical_symlink_route_and_rejects_change` | COVERED |
| 27 | Later invalid recovery evidence causes zero earlier writes | `test_prepared_switch_missing_later_payload_blocks_before_first_recovery_write`<br>`test_prepared_switch_recovery_preflights_target_home_ensure_identity_before_any_write`<br>`test_prepared_restore_recovery_preflights_parent_cleanup_identity_before_any_write` | COVERED |
| 28 | Switch rollback is durable before terminal publication | `test_switch_rollback_effects_are_durable_before_rolled_back_terminal_write`<br>`test_prepared_switch_recovery_effects_are_durable_before_recovered_terminal_write` | COVERED |
| 29 | Restore parent cleanup is recoverable | `test_restore_parent_cleanup_effect_is_journaled_and_durable_before_commit`<br>`test_restore_parent_cleanup_failure_restores_removed_parent_and_prior_mode`<br>`test_restore_parent_cleanup_hard_interruption_recovers_idempotently` | COVERED |
| 30 | Desktop already restored is idempotent | `test_prepared_switch_recovery_accepts_desktop_already_restored_without_reconcile` | COVERED |
| 31 | Terminal reread requires complete marker-bound evidence | `test_restore_terminal_reread_rejects_unbound_or_incomplete_committed_manifest_without_marker_cleanup`<br>`test_switch_terminal_reread_rejects_unbound_committed_manifest`<br>`test_switch_terminal_reread_rejects_silent_corruption_before_marker_cleanup` | COVERED |
| 32 | Busy or pending init capture is byte-identical | `test_init_capture_busy_and_pending_are_byte_identical`<br>`test_cmd_init_capture_failure_restores_pre_init_store_and_preserves_stdout_contract` | COVERED |
| 33 | Successful init capture avoids nested locking | `test_init_capture_uses_one_store_lock_and_preserves_exact_output` | COVERED |
| 34 | Custom apply shares the gate without claiming the protocol | `test_custom_apply_respects_common_store_lock_without_marker`<br>`test_pending_capture_blocks_custom_before_write`<br>`test_custom_gate_retires_valid_committed_terminal_marker` | COVERED |
| 35 | Empty and malformed state metadata is rejected uniformly | `test_restore_rejects_empty_v1_and_v2_entries_before_safety_backup_even_with_force`<br>`test_recorded_mode_and_directory_entry_count_validation_matrix` | COVERED |
| 36 | Both supported adopted homes are evidence-bounded | `test_supported_adopted_home_authority_matrix`<br>`test_adopted_manifest_home_switch_is_restorable_and_preserves_mode` | COVERED |

## Reviewer Notes

- The repository `code-review` skill could not form an isolated three-dot diff
  because the transaction module is still an untracked new file. The scoped
  fallback review used the recorded pre-slice SHA-256 values, tasks 6.2-6.5,
  named RED/GREEN regressions, and current caller map.
- No 6.2-6.9 scope finding remains. The supported switch CLI still omits some
  successful receipt guidance; that explicitly remains task 6.11 rather than
  weakening or expanding this terminal-evidence slice. The known init lock gap
  remains task 6.10.
- 2026-07-23: TPS final-review task 6.8 completed by TDD. Restore apply,
  rollback, prepared recovery, and parent cleanup now operate through attested
  route descriptors and require exact predecessor, staged, and produced object
  identities. Recovery checkpoints its own action evidence, authorizes only
  journaled exact-mode parent recreation, and resumes after a consumed
  directory safety stage. Stable/changed lexical symlink, stage replacement,
  later-state preservation, foreign empty-parent, and double-interruption
  cases pass. Python 3.9 and 3.12 each passed 192/192; strict OpenSpec,
  dual-runtime AST, stable hashes, and diff checks passed. Task 6.9 is next; no
  live or Git mutation ran.
- 2026-07-23: TPS final-review task 6.9 completed by TDD. Strict state metadata,
  recursive directory counts, both supported adopted-home roots, and
  identity-bound failed nested-home cleanup now satisfy the recorded contract.
  Python 3.9 and 3.12 each passed 195/195; the legacy suite passed 123/123;
  strict OpenSpec, dual-runtime AST, stable hashes, and diff checks passed.
  Task 6.10 is next; no live or Git mutation ran.
- 2026-07-23: TPS final-review task 6.10 completed by TDD. Init classification,
  managed prewrites, optional capture, and final output now execute beneath one
  inode-revalidated lock; capture consumes an explicit already-held dispatcher.
  Python 3.9 and 3.12 each passed 197/197; the legacy suite passed 123/123;
  strict OpenSpec, dual-runtime AST, stable hashes, and diff checks passed.
  Task 6.11 is next; no live or Git mutation ran.
- 2026-07-23: TPS final-review task 6.11 completed by TDD. Successful supported
  switches append the true committed retained-marker guidance; supported lock
  contention and pending-capture custom blocking are directly byte-identity
  tested. AST/`rg` caller checks removed only one proven dead import. Python 3.9
  and 3.12 each passed 200/200; the legacy suite passed 123/123; strict
  OpenSpec, dual-runtime AST/import, stable hashes, and diff checks passed.
  Task 6.12 is next; no live or Git mutation ran.
- 2026-07-23: TPS final-review task 6.12 completed. Strict terminal-switch
  reread and exact init-failure rollback closed the two genuine audit gaps;
  restore committed-marker retry, later external target preservation, existing
  home-mode preservation, and removed-helper caller retention now have direct
  named regressions. The evidence maps all 25 required rows and all 36 OpenSpec
  scenarios to 109 existing test methods; an AST/regex validator confirmed no
  missing name or sequence. The focused selection passed 9/9 and strict
  OpenSpec validation passed. Task 6.13 is next; no live or Git mutation ran.
- 2026-07-23: TPS final-review task 6.13 completed after final source review.
  Stage-state tampering and a silently corrupt non-raising terminal writer first
  reproduced false switch commits; both normal and exceptional terminal paths
  now validate the same complete on-disk marker-bound evidence before cleanup.
  The first full rerun then exposed a too-narrow nested-home authority check;
  terminal and prepared recovery now share a contiguous, canonical,
  missing-predecessor created-parent contract. Final results are 207/207 on
  Python 3.9, 207/207 on Python 3.12, and 123/123 legacy. Both transaction
  suites passed again against unchanged recorded hashes. Strict TPS and all
  OpenSpec validation passed (15/15), Bash parsed, both AST/import checks passed,
  the Agent Task Contract reported `ok: true`, caller checks passed, and tracked
  plus relevant untracked whitespace checks produced no diagnostics. No live
  workstation, install, update, release, network, or Git publication action ran.

## TPS-002 Runtime-State Incident Reopen

### RED

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_official_shared_dry_run_ignores_profile_local_runtime_sockets \
  TransactionTests.test_official_shared_dry_run_rejects_unknown_special_file -v
```

Result: exit 1, two tests in 0.066 seconds. The real `AF_UNIX` socket under
`internal/ipc/ipc.sock` reached recursive transaction state capture and raised
`Unsupported filesystem object kind`; the unknown
`internal/unknown-runtime.sock` protection test passed. This isolates the
defect to known runtime ownership classification before shared-support
planning. No backup, destination, active-state, live profile, App, installed
release, or Git mutation occurred.

### GREEN

The exact runtime names were added to `RUNTIME_STATE_NAMES`. Transaction
planning now freezes an identity-bound projection containing recursively
attested shared candidates plus top-level stale runtime/non-shareable symlink
candidates, re-enumerating to detect additions or removals without traversing
runtime directories.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_official_shared_dry_run_ignores_profile_local_runtime_sockets \
  TransactionTests.test_official_shared_dry_run_rejects_unknown_special_file \
  TransactionTests.test_planning_reads_are_frozen_atomically_for_every_switch_input \
  TransactionTests.test_switch_rejects_late_shared_source_drift_before_shared_action -v
```

Result: exit 0, four tests passed in 0.412 seconds. Python 3.12 compile and
scoped `git diff --check` also passed.

### Target-Home Follow-up RED

The incident regression was extended so both the internal source home and the
existing official target home held live sockets beneath `ipc` and
`mcp-oauth-locks`.

Command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_official_shared_dry_run_ignores_profile_local_runtime_sockets -v
```

Result: exit 1, one test in 0.059 seconds. Source runtime classification no
longer failed, but the existing official target home still received a no-op
`target_home_ensure`. Its whole-tree before-state capture reached
`official/ipc/oi.sock` and raised `Unsupported filesystem object kind`. This
proved the remaining recursion was target-directory effect planning rather
than shared-support enumeration.

### Final GREEN

`target_home_ensure` effects are now created only for the missing directory
chain returned by `_missing_parent_paths()`. Existing target homes are not
recursively captured merely to ensure them; their actual target writes retain
the existing route, predecessor, staged-artifact, and produced-identity guards.

Focused command:

```bash
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py \
  TransactionTests.test_official_shared_dry_run_ignores_profile_local_runtime_sockets \
  TransactionTests.test_official_shared_dry_run_rejects_unknown_special_file \
  TransactionTests.test_first_switch_failure_removes_new_target_home \
  TransactionTests.test_first_shared_switch_restore_removes_created_target_home \
  TransactionTests.test_adopted_manifest_home_switch_is_restorable_and_preserves_mode \
  TransactionTests.test_nested_missing_manifest_home_records_and_removes_full_created_chain \
  TransactionTests.test_nested_missing_manifest_home_recovers_before_retry \
  TransactionTests.test_prepared_switch_recovery_preflights_target_home_ensure_identity_before_any_write \
  TransactionTests.test_every_deterministic_directory_effect_recovers_after_action_before_applied -v
```

Result: exit 0, 9/9 tests passed in 1.645 seconds.

### Full Verification

- `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v`
  passed 213/213 in 18.852 seconds.
- `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py`
  ran all 179 tests in 196.688 seconds: 175 passed and four existing one-key
  internal-update fixtures errored. Captured stderr for every error was
  `plugin catalog is unverified (invalid_json)` from the in-progress
  `fail-safe-update-release` fake CLI; the switch and, where required,
  app-server verification had already succeeded. No failing test exercised
  the TPS directory/runtime change.
- `openspec validate transactional-profile-state --strict --no-interactive`
  passed.
- `bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh`,
  Python 3.12 compile for the changed transaction/home-sync/test modules, and
  scoped plus repository `git diff --check` passed.
- The repository-source command
  `scripts/codex-switch --skip-self-update official --dry-run
  --skip-update-check --skip-plugin-repair --skip-verify --skip-login
  --skip-launchctl --skip-app-cli --skip-shim --skip-doctor --no-status`
  returned exit 0, `Outcome: DRY RUN OK`, and empty stderr.
- A bounded snapshot of the canonical control plane, complete backups tree,
  official managed targets, and runtime socket identity contained 33,717
  entries and retained SHA-256
  `f079b653f75690bff3aad70a69e3e48a41db599245166f7a00e811d0defe7382`
  before and after. `/Users/cY/.codex/ipc/ipc.sock` retained mode, device, and
  inode identity.
- Two broader exploratory snapshots were not used as no-write evidence because
  the running environment concurrently changed known runtime/shared content
  (`process_manager/chat_processes.json` and one visualization file). Both
  dry-runs still returned `DRY RUN OK`; the final bounded snapshot isolates the
  transaction-owned evidence from those external writers.

No source installation, live official switch, App restart, failed-backup
cleanup, release, commit, push, or archive action ran. Those remain separate
Human Gates.

## TPS-003 Desktop Global-State No-Op Final Closure

Date: 2026-07-26 01:42:33 +0800

### Source Verification

The final no-op ownership contract is covered by four focused regressions:

- `test_shared_switch_preserves_concurrent_desktop_global_state_after_noop_merge`
- `test_shared_switch_real_desktop_global_state_merge_remains_identity_bound`
- `test_legacy_noop_desktop_rollback_failed_marker_recovers_safely`
- `test_legacy_noop_desktop_recovery_rejects_any_evidence_mismatch`

Fresh results:

| Command | Result |
|---|---|
| focused Desktop no-op and legacy-recovery selection | 4/4 passed in 0.971s |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v` | 219/219 passed in 23.987s |
| `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py` | 198/198 passed in 264.317s |
| `openspec validate --all --strict --no-interactive` | 17/17 passed |
| Bash syntax for the five production shell entrypoints | passed |
| Python 3.12.13 AST/import harness | AST 54/54, imports 46/46 |
| System Python 3.9.6 AST/import harness with the supported Python 3.12 runtime selection | AST 54/54, imports 46/46 |
| isolated `scripts/package-release.sh` plus `validate_release_outputs` | version `0.1.13`, 64 files, 389451-byte archive, payload `ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab` |
| `git diff --check` | passed |

The evidence-mismatch regression includes a preceding real `config_write`
whose before and planned states differ. The compatibility classifier releases
only the later exact Desktop no-op effect and never releases that real write.

### Supported Live Recovery

The installed current release is the exact verified payload:

```text
/Users/cY/.local/share/codex-switch/releases/ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab
```

The supported live command was:

```bash
/Users/cY/.local/bin/codex-switch official \
  --skip-update-check --skip-plugin-repair
```

It retired the pending marker for
`20260725T123636Z-switch-internal-to-openai-official`. That backup is now
`rolled_back` with journal state `recovered` and recovery note
`legacy Desktop global-state no-op ownership ignored`. Only effects 22 through
30 carry `preserved App-owned state from legacy no-op`; every real planned
change retained normal fail-closed recovery.

The fresh official transaction committed as
`20260725T171620Z-switch-internal-to-openai-official`. Its initial process
returned action-required because the already-running App still owned the prior
internal chain; the transaction itself remained committed.

After the authorized App restart, ChatGPT pid `92488` spawned official
app-server pid `92903` from
`/Applications/ChatGPT.app/Contents/Resources/codex`. The App reported
`0.146.0-alpha.3.1`, completed the initialize handshake, mounted its routes,
and successfully routed `config/read`, `model/list`, `thread/list`, plugin,
skills, and MCP status requests. The relevant log is:

```text
/Users/cY/Library/Logs/com.openai.codex/2026/07/25/codex-desktop-2655f576-738d-439a-b6b0-8cac444bbf1d-92488-t0-i1-172041-0.log
```

The App stopped that official app-server normally at
`2026-07-25T17:21:07.563Z`.

### Internal Restoration

The supported restore committed as
`20260725T172136Z-switch-openai-official-to-internal`. Current read-only
ownership is:

- active profile: `internal`;
- shell and profile backend: `/Users/cY/.local/bin/codex`;
- Desktop launcher: `/Users/cY/.codex-switch/bin/codex-internal-app`;
- ChatGPT pid: `95489`;
- managed proxy pid: `95838`, loaded from payload `ed5d74c1...28ab`;
- backend app-server pid: `95842`, `/Users/cY/.local/bin/codex`;
- `launchctl` `CODEX_CLI_PATH`:
  `/Users/cY/.codex-switch/bin/codex-internal-app`.

Fresh repository-source `status`, `verify internal --repair=none`, and
`doctor` all returned zero. No commit, push, tag, release, OpenSpec archive,
dependency change, provider migration, or destructive cleanup was performed.
