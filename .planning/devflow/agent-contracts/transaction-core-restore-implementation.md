# Agent Task Contract

## Goal
Implement dependency-ready slices 1 and 2 of `transactional-profile-state` by strict vertical TDD: store-directory locking, one public transaction execution seam, recursive path state, schema-v2 backup/restore, legacy compatibility gates, complete restore preflight, safety backup, and reverse rollback.

## Worker ID
`transaction-core-restore-implementation`

## Scope
Allowed write set for worker `transaction-core-restore-implementation` only:
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `scripts/codex_switch_backup.py`
- `scripts/codex_switch_restore.py`
- `scripts/codex_switch_store.py`

Read-only inputs include the approved `openspec/changes/transactional-profile-state/` artifacts, current callers, existing tests, and project instructions. Forbidden: do not edit any other path. You are not alone in the repository: preserve all unrelated/main-agent changes, do not revert them, and adapt imports to the current shared tree.

## Constraints
The pre-agreed public test seams are `execute_transaction(Store, TransactionRequest, dry_run=...)` and the existing restore CLI adapter; tests must observe behavior through those seams and filesystem results, not private helpers. Work one vertical RED to GREEN cycle at a time; capture the exact failing assertion before production code and the exact passing command after. Implement only tasks 1.2-1.4 and restore-relevant tasks 2.1-2.5; do not implement capture, switch, Desktop effects, runtime binding, arbitrary profiles, or speculative abstractions. Preserve official/internal successful behavior, public restore output unless the spec changes it, and v1 attested file/symlink/missing compatibility. v0 and v1 directories fail before mutation. Use standard library only and `apply_patch` for edits. No live store, launchctl, App, install, network, Git commit/push, release, or profile switch.

## Verification
Run focused RED/GREEN commands after each cycle and finish with `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v`, the restore/backup-related existing regression subset you identify from `scripts/test_codex_profile_switch.py`, `PYTHONDONTWRITEBYTECODE=1 python3.12 -m py_compile` for changed Python modules, `openspec validate transactional-profile-state --strict --no-interactive`, and `git diff --check`. Tests must use temporary stores and may inject filesystem failures only through a system-boundary adapter or public transaction test seam.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus changed files; the ordered RED and GREEN commands/results; tests added by name; implementation summary; legacy compatibility matrix; rollback and zero-mutation assertions; complete test logs or validation results; `git diff --stat`; residual risks; unverified areas; incidental findings with `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`; and review needs. Do not mark OpenSpec task checkboxes or write ledger/state/evidence files; main owns those updates after independent review.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing a public CLI/persistence contract beyond approved v2/v1/v0 behavior, accepting unverified legacy directory/payload data, expanding the write set, deleting historical backups, touching live workstation state, adding a dependency, implementing custom-profile behavior, or bypassing a failing test. If a required change lies outside the exclusive write set, report the exact seam and proposed path instead of editing it.
