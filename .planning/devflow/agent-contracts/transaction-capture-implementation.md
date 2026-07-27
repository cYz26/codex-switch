# Agent Task Contract

## Goal
Implement dependency-ready tasks 3.1-3.4 of `transactional-profile-state` by strict vertical TDD: capture source preflight, cloned sibling staging, stale-auth removal under the approved policy, preservation of unmanaged profile artifacts, journaled directory exchange, deterministic incomplete-journal handling, and migration of direct/indirect capture callers to the lock-owned transaction receipt.

## Worker ID
`transaction-capture-implementation`

## Scope
Allowed write set for worker `transaction-capture-implementation` only:
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `scripts/codex_switch_capture.py`
- `scripts/codex_switch_lifecycle.py`

Read-only inputs include the approved `openspec/changes/transactional-profile-state/` artifacts, the reviewed restore transaction seam, current capture/init callers, and existing tests. Forbidden: do not edit any other path. You are not alone in the repository: preserve all unrelated/main-agent changes, do not revert them, and adapt to the current shared worktree.

## Constraints
The pre-agreed public seams are `execute_transaction(Store, TransactionRequest, dry_run=...)`, existing `capture_profile(...)`, `cmd_capture`, and indirect init capture. Tests must observe behavior through those seams and filesystem/receipt results, not private helpers. Work one vertical RED-to-GREEN cycle at a time and retain exact failure/pass evidence. Implement only tasks 3.1-3.4; do not implement switch/Desktop effects, runtime binding, updates, proxy behavior, release work, or custom-profile product expansion. Product behavior is official/internal; preserve legacy custom-name compatibility without treating it as a new supported product surface. Validate source config and required auth before replacing the destination. Clone the existing profile to a sibling stage so unmanaged files survive, replace the complete managed set, explicitly remove stale destination auth only when missing auth is allowed, and keep the old directory until finalization succeeds. A first-time mutating capture may create only the stable store root before acquiring its directory-inode lock; canonical store reads and remaining store creation occur under the lock. Incomplete stage/previous/journal state must recover safely or fail closed with no silent deletion. Use standard library only and `apply_patch` for edits. No live store, App, launchctl, install, network, Git commit/push, release, or profile switch.

## Verification
Add the exact RED tests named in tasks 3.1 and 3.3, plus only bounded guards needed to prove lock ownership and successful CLI-output compatibility. Finish with `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_codex_transaction.py -v`, `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v`, the existing capture/init-related regression subset identified from `scripts/test_codex_profile_switch.py`, Python 3.9 and 3.12 compile checks for changed modules, `openspec validate transactional-profile-state --strict --no-interactive`, and `git diff --check`. Tests use only temporary stores/homes and inject rename/finalization failures through a system-boundary adapter supplied in the transaction request.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus changed files; ordered RED/GREEN commands/results; tests added by name; implementation summary; cloned-artifact and auth assertions; directory-exchange/journal state matrix; rollback/finalization evidence; relevant legacy results; complete validation results; `git diff --stat`; residual risks; unverified areas; and incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`. Do not mark OpenSpec tasks or write ledger/state/evidence files; main owns those after independent review.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing public capture/init output or flags beyond the approved spec, deleting an ambiguous existing profile/journal, expanding the write set, migrating custom-profile persistence, touching live workstation state, adding a dependency, bypassing a failing test, or choosing between two recovery states that cannot be distinguished from durable evidence. If a required change lies outside the exclusive write set, report the exact seam and proposed path instead of editing it.
