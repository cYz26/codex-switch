# Agent Task Contract

## Goal
Complete dependency-ready tasks 1.1, 2.1-2.2, and 4.1-4.6 of `transactional-profile-state` through strict vertical TDD: characterize shared official/internal contracts; route both shared and snapshot strategies into their target independent homes; create committed schema-v2 restorable switch backups; preflight required CLI/App bindings before backup even in dry-run; fail closed on malformed active state; and journal/roll back every filesystem and Desktop binding effect through one lock-owned transaction.

## Worker ID
`transaction-switch-effects-implementation`

## Scope
Allowed write set for worker `transaction-switch-effects-implementation` only:
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `scripts/codex_switch_backup.py`
- `scripts/codex_switch_restore.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_plan.py`
- `scripts/codex_switch_launch.py`

Read-only inputs include the approved `openspec/changes/transactional-profile-state/` artifacts, the reviewed core/restore/capture transaction seam, existing home/config/shim/shell/wrapper/record helpers, `scripts/codex_profile_switch.py`, `scripts/codex-switch`, and legacy regression tests. Forbidden: do not edit any other path. You are not alone in the repository: preserve all unrelated/main-agent changes, do not revert them, and adapt to the current shared worktree.

## Constraints
The pre-agreed public seam is `execute_transaction(Store, TransactionRequest, dry_run=...)`; supported product identities are `internal` and `openai-official`, with `official` remaining only the existing public alias where current callers already normalize it. Do not generalize profile names or reinterpret raw custom-profile compatibility. Supported shared and snapshot modes must both target the selected product's independent home; config strategy must not select the destination home. Preserve the legacy custom-profile route and its output/leniency, but remove `backup_live_files()` as a writer from supported official/internal paths. Freeze the entire mutation set under the store lock; do not re-enumerate shared support during apply. Resolve and preflight `codex_bin` and `app_cli_path` before backup or mutation, including dry-run, and reject missing, relative, nonexistent, directory, or non-executable paths.

Create a committed schema-v2 backup for every successful supported switch, including snapshot, and prove it restores config/auth/home support, shim, plist, active record, and relevant modes/tree state. Preserve official auth isolation: an internal snapshot must never source credentials from the official home. Parse existing `active.json` strictly and fail closed before writes when it is invalid JSON, non-object, or has an invalid required shape. Apply `active.json` last and finalize the backup only afterward; finalization failure must roll back active and all prior effects.

Implement an injected `_DesktopBindingAdapter` (or equivalently bounded internal seam) around `scripts/codex_switch_launch.py` that observes/preflights plist, GUI `CODEX_CLI_PATH`, and service loaded state; journals successful `setenv`/`unsetenv`, `bootout`, and `bootstrap`; and restores their prior observations on failure. Tests must inject a fake runner/uid provider and must never execute real `launchctl`. Bootout failures are errors. Treat service and GUI-env restoration as coupled because bootstrap's RunAtLoad may set the environment again. Every injected failure at shim write, plist write, GUI setenv, bootout, bootstrap, active write, and backup finalize must restore the complete pre-operation state and return `rolled_back` with the backup ID; injected rollback failure must return `rollback_failed` and retain recovery material. Work one vertical RED-to-GREEN cycle at a time and retain exact evidence. Use Python 3 standard library only and `apply_patch` for edits. No live store, App, launchctl, install, network, Git commit/push, release, plugin mutation, or workstation profile switch.

## Verification
First add and run the two GREEN characterization tests named in task 1.1. Then add the exact RED tests named in tasks 2.1, 4.1, and 4.5 plus seven individually named effect-failure tests for shim write, plist write, GUI setenv, bootout, bootstrap, active write, and backup finalize; include one rollback-failure guard and bounded event-order assertions proving active applies last and finalize follows it. Run each RED alone before implementation and the same test GREEN afterward. Finish with `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_codex_transaction.py -v`, `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v`, the directly affected shared/snapshot/restore/binding legacy subset from `scripts/test_codex_profile_switch.py` under both available interpreters where practical, Python 3.9 and 3.12 compile checks for all changed modules, `openspec validate transactional-profile-state --strict --no-interactive`, and `git diff --check`. All tests use only temporary stores/homes and injected Desktop effects.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus changed files; ordered RED/GREEN commands and results; tests added by name; shared/snapshot config-auth assertions; immutable mutation-set evidence; binding preflight matrix; schema-v2 backup/restore evidence; malformed-active matrix; Desktop apply/rollback event matrix; rollback-failure receipt/material evidence; complete dual-interpreter and legacy validation results; `git diff --stat`; residual risks; unverified areas; and incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`. Do not mark OpenSpec tasks or write ledger/state/evidence files; main owns those after independent review.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing public switch output or flags beyond the approved spec, removing or reinterpreting custom-profile compatibility, weakening backup attestation, deleting ambiguous recovery material, expanding the write set, touching real Desktop/workstation state, adding a dependency, bypassing a failing test, or choosing between two recovery states that cannot be distinguished from durable evidence. If a required change lies outside the exclusive write set, report the exact seam and proposed path instead of editing it.
