# Agent Task Contract

## Goal
Close every actionable final-review and acceptance-coverage gap in `transactional-profile-state` on one stable snapshot. The completed system must classify all transaction evidence before every mutation route, publish and recover only complete bound durable state, install and verify the exact immutable staged plan, perform switch and restore recovery through fully preflighted identity-bound actions, keep `init --capture-current` under one non-nested store lock, satisfy every updated OpenSpec scenario, and map all 25 required RED/GREEN rows to direct named evidence.

## Worker ID
`transaction-review-closure`

## Stable Input Snapshot
- `scripts/codex_switch_transaction.py`: `953bdd5243684c22de5f18b5fa3b0214f723d53243432285140a53ef8dd7cf17`
- `scripts/test_codex_transaction.py`: `d30ca4b0a16ef7ec602c0d2e5a57d490135f3693778eacb298c2774a5920ff71`
- `scripts/codex_switch_restore.py`: `b4392bfb8629b864060f180c60dc047c9bde283ae995bcccab244384e832b41a`
- `scripts/codex_switch_switching.py`: `661247aae52c13938c535ecbef2eeeda2951a4b457949aeb97c12c7669189f27`
- `scripts/codex_switch_lifecycle.py`: `88ee4647817adaa6b1cffa244dcc7cbfb423317cfaa91b6c1905089b6d8ef1f0`
- `scripts/codex_switch_capture.py`: `902e57b9723eddae4139ff1e6f2c458554285dba66447f9bb0b8be199b4b8095`
- `scripts/codex_switch_launch.py`: `5f08c0a73753f22bd8f34f58695ea4d62751974ad34da6535857d5f8d55f1dc2`
- `scripts/codex_switch_io.py`: `86dd60ce5459b67c9f759c8c3a4dc24a9af9a3c3c8ffae42ef635118a85c2970`
- canonical OpenSpec: proposal `e867109f32cf71c837f7f94012496734366ac4ba5296bd8fc46df4e07730cde8`, design `46f8600cdc2b769aa0840c553cf999a95ff29ae23e6d13ad91af250c160339b4`, spec `4cef951e775ecddef457eddd6752e9e058557e621dddaf4888ed0b0fb2273576`, tasks `c5796d9065a30dcfe3ba476ba18e023e3fa55bd5a370bf2f7691ca8adfa75247`.

Stop before editing if any production/test hash differs. OpenSpec is main-owned and read-only for the worker; stop if its hashes drift because the implementation contract may have changed.

## Scope
Allowed write set for worker `transaction-review-closure` only:
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `scripts/codex_switch_restore.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_lifecycle.py`
- `scripts/codex_switch_capture.py`
- `scripts/codex_switch_launch.py`
- `scripts/codex_switch_io.py`

Read-only inputs include the full updated `openspec/changes/transactional-profile-state/`, the prior transaction contract, CLI dispatch, store/path/config helpers, and `scripts/test_codex_profile_switch.py`. Forbidden: all other paths, including OpenSpec/control-plane/evidence files, live profile stores, App bundles, launchctl state, plugin caches, network, dependency changes, Git staging/commit/push, install/update/release, or migration. You are the sole production writer but not alone in the worktree; preserve unrelated and main-agent edits and never revert them.

## Constraints
Use Python 3.9-compatible standard-library code, strict RED-before-GREEN TDD, temporary/fake stores and adapters only, one production writer, and the complete target state from the updated OpenSpec. Do not patch expectations to accept weaker behavior. A focused test is complete only when it asserts the pre-operation store snapshot, destination bytes/modes/object identities, journal/marker state, receipt/CLI output, and next-retry behavior relevant to that vector.

Product profiles remain only `openai-official`/`official` and `internal`. The custom route remains a compatibility route: it holds the common lock and gate, may retire validated terminal supported markers, and never arms a supported marker/journal. Preserve schema-v2, evidence-bounded v1, explicit v0 rejection, successful CLI output ordering, and the public `execute_transaction(Store, TransactionRequest, dry_run=...)` seam. No real Desktop or launchctl call may run.

## Required Design

### 1. One store-wide evidence classifier
Under `_StoreLock`, before operation dispatch or any init/custom/capture layout write, build one classification over:
- every store-root pending marker and its bound switch/restore journal;
- marker-required journals whose marker is missing;
- markerless legacy prepared switches;
- pre-marker restore evidence in `prepared` or `rollback_failed`;
- unfinished, malformed, or changed capture journals;
- terminal `committed`, `rolled_back`, or `recovered` evidence with a retained marker;
- corrupt, mismatched, multiple, ambiguous, or rollback-failed evidence.

Use this classifier for switch, capture, restore, `init --capture-current`, and custom apply. A marker-required effect-free journal may close as never started. A marker-required journal with any begun effect blocks and is never routed into legacy recovery. A valid legacy markerless prepared switch may recover before any operation. A pre-marker prepared/rollback-failed restore blocks every mutation. Dry-run returns precise pending guidance and changes zero bytes. Valid terminal evidence is retired before a new applying route; cleanup failure prevents the new route without reversing the terminal result.

### 2. Complete bound terminal evidence
Switch rollback must atomically publish outer `lifecycle` plus `switch_journal.state=recovered|rollback_failed` and complete effect terminal states. After verified rollback, independent `failure.json` must contain the exact marker name, operation, backup/transaction IDs, and marker-bound prepared digest. Pending classification may use only a fully matching `failure.json=rolled_back` when `backup.json` is unreadable; it may never accept an asserted digest without a trusted marker or accept incomplete/rollback-failed evidence.

If a terminal write raises after writing, authoritative reread for switch or restore validates the complete manifest against the retained marker: schema, operation, IDs, marker name, digest, `recovery_marker_required`, authority/allowlist provenance, non-empty entries, all payloads, complete applied effect chain, and terminal lifecycle/journal agreement. Minimal, unbound, or incomplete `committed` data retains the marker and does not return committed.

Marker cleanup status is structured and outcome-aware. Committed, rolled-back, and recovered warnings use the true outcome. Supported CLI output renders committed retained-marker guidance. Custom apply validates and retires terminal markers before its first write. Remove the marker only after durable terminal evidence.

### 3. Immutable inputs at the producing read
Eliminate read-then-later-freeze windows. The same read that produces a plan payload records its frozen state/bytes/identity for both product manifests, active collision input, configs, auth, plugin snapshots, shell profile, shared support entry set and descendants, Desktop source and target read-modify-write state, stale-link sources, wrapper/binding sources, and every indirect composite input. Apply only payloads derived from those exact frozen values. Revalidate each dependency before intent and after intent/before action through pinned descriptors.

Route identities are planned before effect begin; `begin()` must not bless a newer byte-identical route or link target. Repeated writes to one canonical destination use the previous planned/produced state as the next predecessor.

### 4. Install the persisted stage and verify produced identity
For every replacement, create, persist, and make durable a staged artifact and its device/inode identity before intent. Install that exact staged artifact descriptor-relatively instead of serializing a second fresh file. Before `applied`, verify the live destination is the persisted produced object through the pinned parent descriptor plus planned state. A byte-identical different inode cannot reach `applied`.

Recovery models repeated-path identity chains correctly: it validates intermediate produced identities against journaled chain state and the applicable live terminal state, not every historical identity against the final inode. Add action-before-observation interruptions for every deterministic filesystem family, including mkdir/chmod/remove.

### 5. Descriptor-relative restore and complete recovery planning
Replace path-based restore apply/recovery materialization with staged identity-bound descriptor-relative operations anchored to frozen allowlist provenance and lexical route guards. Validate staged source identity before copy/link/rename. Stable attested lexical symlink ancestors remain compatible; changed identity/target blocks before mutation.

Before the first switch or restore recovery write, simulate and validate the entire action list: entries/payloads, current states, route and staged/produced identities, repeated paths, target-home ensure, directory create/chmod/remove, Desktop chain, active state, parent cleanup, and canonical allowlist. A problem in the last action changes zero earlier targets.

Every apply/rollback/recovery file, tree, link, deletion, directory, chmod, and parent cleanup reaches an effect-specific durability boundary before `applied` or terminal publication.

### 6. Journal original-parent cleanup
Restore parent cleanup is a first-class journal effect before `rmdir`: expected state and identity, approved route, intent, planned missing state, observed result, and parent fsync. Reverse recovery recreates the exact prior directory and mode before children when safe. It is idempotent across a second interruption. It removes only the exact transaction-created empty identity; a replaced, non-empty, or otherwise changed directory remains untouched and yields precise retained recovery evidence.

### 7. Strict metadata and authority
Validate every recorded mode position and state kind in v1/v2, including file/directory/symlink/missing before, pre, post, committed, and journal states. Reject bool, negative, or `>0o7777`; accept valid special bits through `0o7777`. Validate schema-v2 directory `entry_count` against recursive attestation. `--force` bypasses only current-state conflict.

Cover adopted homes for both supported profiles. Reject relative, non-canonical, or `backups/`-contained manifest homes before mutation. Existing mode is preserved; missing nested homes are `0700` and their full exact created chain is removed after failed switch or historical restore only while unchanged and empty.

### 8. Lock-owned init capture
`cmd_init --capture-current` must perform pending classification, silent official manifest/config initialization, capture, and receipt creation under one store lock. Use a private already-locked dispatch or dedicated transaction operation; do not recursively acquire `_StoreLock`. Busy, pending, validation failure, or capture failure restores the complete pre-init store state and produces no marker/backup/partial official files. Successful output remains capture receipt first, then `Initialized` and shim lines. Normal `cmd_capture` retains its public behavior.

### 9. Coverage closure and cleanup
Add direct named regressions for every previously missing/weak row from the 25-row matrix, including:
1. prepared journal, marker publication, intent, action, applied, terminal write, marker unlink, and marker parent-sync interruption points;
2. corrupt marker/manifest/payload, mismatched IDs/digest, multiple markers, rollback-failed, bound failure fallback, and all switch/capture/restore/custom/init gate combinations;
3. unrelated corrupt historical evidence plus valid legacy markerless switch recovery;
4. missing-marker effect-free versus begun switch/restore and pre-marker restore blocking;
5. restore parent cleanup interruption/retry and Desktop already-restored retry;
6. every deterministic file/directory action-before-checkpoint recovery;
7. failed switch existing-home mode preservation, failed nested chain cleanup, and later non-empty parent retention;
8. prepared recovery out-of-allowlist and corrupt-later-payload/identity before first write;
9. switch/restore terminal cleanup failure plus next-apply retirement;
10. supported switch contention, pending capture blocking custom, and `init --capture-current` busy/pending byte identity.

Remove only dead imports/helpers proven by final `rg`; preserve all live compatibility callers.

## Required RED/GREEN Tests
At minimum add individually named tests for every reviewer reproduction and the coverage list above. These exact names are mandatory unless a clearer name is recorded in the evidence with a one-to-one mapping:
- `test_missing_marker_begun_restore_blocks_every_mutation_before_writes`
- `test_missing_marker_begun_marker_required_switch_blocks_instead_of_legacy_recovery`
- `test_markerless_legacy_prepared_switch_gates_capture_and_restore`
- `test_markerless_pre_marker_restore_prepared_or_rollback_failed_blocks_every_mutation`
- `test_switch_rollback_marker_cleanup_failure_is_retryable_and_retires_marker`
- `test_bound_rolled_back_failure_record_allows_marker_retirement_after_manifest_corruption`
- `test_restore_parent_cleanup_failure_restores_removed_parent_and_prior_mode`
- `test_restore_parent_cleanup_hard_interruption_recovers_idempotently`
- `test_switch_rollback_effects_are_durable_before_rolled_back_terminal_write`
- `test_prepared_switch_recovery_effects_are_durable_before_recovered_terminal_write`
- `test_prepared_switch_recovery_preflights_target_home_ensure_identity_before_any_write`
- `test_restore_terminal_reread_rejects_unbound_or_incomplete_committed_manifest_without_marker_cleanup`
- `test_switch_terminal_reread_rejects_unbound_committed_manifest`
- `test_rolled_back_marker_cleanup_warning_uses_rolled_back_state`
- `test_committed_marker_cleanup_warning_is_rendered_by_switch_cli`
- `test_custom_apply_retires_terminal_pending_marker_before_write`
- `test_cmd_init_capture_busy_or_pending_gate_is_byte_identical`
- `test_cmd_init_capture_failure_restores_pre_init_store_and_preserves_stdout_contract`
- `test_planning_reads_are_frozen_atomically_for_every_switch_input`
- `test_switch_installs_persisted_stage_and_rejects_identity_change_before_applied`
- `test_interrupted_repeated_path_effect_chain_recovers`
- `test_restore_apply_and_recovery_use_bound_route_and_staged_identity`
- `test_every_deterministic_directory_effect_recovers_after_action_before_applied`
- `test_switch_rollback_preserves_later_change_to_already_produced_target`
- `test_supported_adopted_home_authority_matrix`
- `test_recorded_mode_and_directory_entry_count_validation_matrix`
- `test_failed_nested_home_cleanup_preserves_changed_or_non_empty_parent`

Record initial RED failure reasons and exact GREEN commands. Do not invent RED evidence for tests that genuinely pass; if an expected gap is already fixed, report the direct evidence and continue.

## Verification
Run and return exact results for:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py
openspec validate transactional-profile-state --strict --no-interactive
bash -n scripts/codex-switch install.sh run.sh scripts/package-release.sh
git diff --check
PYTHONDONTWRITEBYTECODE=1 python3.12 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/validate_agent_task_contract.py --contract .planning/devflow/agent-contracts/transaction-final-review-closure.md --json
```

Also run Python 3.9 and 3.12 AST/import checks for every changed module, direct focused commands for each required test group, final `rg` caller/import proof, and a fresh 25-row acceptance map. Record stable SHA-256 for every changed file, then rerun both transaction suites against unchanged hashes.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` with:
- exact changed files and final hashes;
- exact commands run for every focused and full verification gate;
- complete test logs or validation results, including exit codes and pass/fail counts;
- complete ordered RED then GREEN results for every required group;
- one table mapping every updated OpenSpec scenario and all 25 matrix rows to named passing tests;
- classifier results for all evidence/operation/dry-run combinations;
- durability ordering for apply, rollback, recovery, terminal publication, and cleanup;
- immutable input, route, staged/produced identity, repeated-path, and later-change results;
- restore parent cleanup, full preflight, second interruption, Desktop, and terminal reread results;
- strict metadata/adopted-home/nested-chain matrices;
- init/custom/CLI compatibility results;
- dual-interpreter/full legacy/strict/syntax/import/diff/contract results;
- residual risks and every unverified area;
- incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`.

Do not edit or mark OpenSpec tasks, verification records, `TASK_LEDGER.md`, or `.planning/STATE.md`.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing the public CLI, changing successful stdout ordering, changing product profiles, removing the custom route, rewriting historical backups, accepting ambiguous/unallowlisted evidence, weakening schema-v0/v1/v2 validation, adding a dependency, expanding the write set, invoking live Desktop/store state, bypassing a failing test, or performing Git/install/update/release/network actions. If a required fix needs another file, report the exact seam and reason without editing it.
