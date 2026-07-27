# Agent Task Contract

## Goal
Repair every actionable transactional-switch review finding on the current stable implementation through one serialized RED-to-GREEN slice: freeze and recheck all switch inputs, roll back only mutations begun by this transaction, persist enough switch intent/effect state to recover or fail closed after a hard interruption, keep active-record restoration last, reconcile partially successful Desktop commands, make dry-run collision validation identical to apply, and preserve the custom legacy route's usable backup lifecycle.

## Worker ID
`transaction-switch-review-fixes`

## Scope
Allowed write set for worker `transaction-switch-review-fixes` only:
- `scripts/codex_switch_transaction.py`
- `scripts/test_codex_transaction.py`
- `scripts/codex_switch_restore.py`
- `scripts/codex_switch_launch.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_backup.py`
- `scripts/codex_switch_home_select.py`

Read-only inputs include `openspec/changes/transactional-profile-state/`, the accepted capture implementation, `scripts/test_codex_profile_switch.py`, existing helpers, and current control-plane/evidence files. Forbidden: edit any other path, including OpenSpec tasks, `TASK_LEDGER.md`, `.planning/STATE.md`, verification records, or the main-owned legacy fixture. You are not alone in the repository: preserve unrelated/main-agent changes, do not revert them, and adapt to the shared worktree.

## Constraints
Keep the public `execute_transaction(Store, TransactionRequest, dry_run=...)` seam and successful CLI output. Product profiles remain only `internal` and `openai-official`; do not generalize profile names. Preserve the legacy custom-profile command route, but a successful custom switch must not advertise an unusable schema-v2 `prepared` backup. Do not weaken schema-v2/v1/v0 restore attestation or the already accepted capture state machine.

Build a genuinely immutable switch plan. Freeze every source payload that apply consumes, including snapshot auth bytes, and capture source states for manifests/config/auth plus required `codex_bin` and `app_cli_path` bindings. Recheck relevant frozen source/binding states before mutation and again before active/finalize; a changed or missing binding must roll back and cannot produce a committed active record. Never reread credentials during apply. The exact planned missing managed-internal wrapper exception may remain, but all other bindings must stay executable and unchanged.

Maintain an ordered in-memory mutation journal and a durable schema-v2 switch journal. Record intent before each filesystem/Desktop effect and applied completion after it. Normal rollback may restore only paths whose mutation was begun by this transaction; it must preserve an external change to a backup entry that the transaction never reached. Active is restored only after all other filesystem paths, created-directory cleanup, and Desktop observations are restored. If `backup.json` becomes unreadable during failure handling, use the already validated in-memory plan/material to continue best-effort filesystem and Desktop rollback, return a receipt with the backup ID, and retain an independent usable failure/recovery record instead of escaping without classification.

Before a new mutating transaction, detect a prior schema-v2 switch left `prepared`. Persist sufficient prior Desktop observation and per-effect state to recover deterministically; if an interrupted effect is genuinely ambiguous, fail closed with its backup ID and recovery guidance before any new backup or destination write. A dry-run must remain zero-write and report the pending recovery requirement rather than mutating it. Add hard-interruption/retry coverage at filesystem, Desktop, active, and finalize boundaries. Do not claim crash recovery from catchable `OSError` tests alone.

Desktop rollback must reconcile observed GUI environment and service-loaded state, not assume a nonzero `launchctl` status means zero side effects. Tests must cover setenv, bootout, and bootstrap that mutate fake state and then return nonzero. No test or implementation verification may invoke real `launchctl`; inject the fake runner and UID provider. Remove the dry-run-only active-home collision bypass so preview and apply validate the same plan.

Use Python standard library only and `apply_patch` for edits. Work one bounded RED then GREEN vector at a time. No live store/App/profile switch, real launchctl, network, install/update/plugin mutation, release, Git stage/commit/push, dependency change, or workstation mutation.

## Verification
Add individually named RED regressions for: unchanged required binding at commit; `codex_bin` deletion during apply; app CLI drift; snapshot auth source drift with frozen payload; preservation of an untouched external auth change during earlier failure; custom successful backup lifecycle; dry-run active-home collision; hard interruption after a filesystem mutation followed by a fresh transaction; hard interruption after Desktop effects followed by a fresh transaction; hard interruption after active write/finalize boundary; unreadable `backup.json` during failure; active restored after other filesystem/Desktop state; and post-side-effect nonzero setenv/bootout/bootstrap reconciliation. Record each RED failure reason and matching GREEN result.

Then run `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_transaction.py -v`, `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_transaction.py -v`, the directly affected legacy tests under Python 3.12, and the full `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py`. Run Python 3.9/3.12 compile or AST/import checks for every changed module, `openspec validate transactional-profile-state --strict --no-interactive`, and `git diff --check`. All filesystem/process fixtures must use temporary roots and fake Desktop adapters.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` plus exact changed files; stable SHA-256 values; exact commands run; ordered RED/GREEN test logs and validation results with test names; frozen-input/state vectors; normal applied-path rollback evidence; prepared-switch interruption/recovery matrix; corrupt-manifest fallback receipt/evidence; active-last rollback order; Desktop partial-command reconciliation events; custom/dry-run compatibility results; dual-interpreter/full legacy results; strict/syntax/diff results; residual risks; explicit unverified areas; and incidental findings classified as `CONTINUE_WITH_MINIMAL_GUARD`, `DEFER_AND_CONTINUE`, or `BLOCKED_AWAITING_HUMAN`. Do not mark OpenSpec tasks or edit main-owned control-plane/evidence files.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing a public CLI/persistence contract beyond the approved schema-v2 recovery design, weakening backup or source attestation, discarding ambiguous recovery material, auto-recovering an effect that cannot be distinguished safely, expanding the write set, touching live Desktop/workstation state, adding a dependency, bypassing a failing test, or changing the accepted capture semantics. If a required repair needs another file, report the exact seam and proposed path instead of editing it.
