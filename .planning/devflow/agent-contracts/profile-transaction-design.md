# Agent Task Contract

## Goal
Produce an implementation-ready, read-only design map for profile transaction safety: independent snapshot mode, one versioned backup schema, recursive restore preflight, atomic capture replacement, rollback, and store-scoped locking.

## Worker ID
`profile-transaction-design`

## Scope
Allowed read-only scope: inspect `scripts/codex_switch_switching.py`, `scripts/codex_switch_backup.py`, `scripts/codex_switch_restore.py`, `scripts/codex_switch_capture.py`, `scripts/codex_switch_plan.py`, `scripts/codex_switch_store.py`, `scripts/codex_switch_launch.py`, existing tests, and relevant OpenSpec artifacts.
Forbidden: do not modify any repository path; do not switch a profile, write the live store, invoke launchctl mutations, create releases, commit, or push.

## Constraints
The product profile set is only `openai-official`/`official` and `internal`; arbitrary-profile hardening is not part of this task. Preserve current successful shared-mode behavior and public CLI compatibility unless an explicit incompatibility is identified. Prefer a deep Profile Transaction module with a small interface and no production dependency.

## Verification
Not applicable: this is a read-only explorer task; verify by tracing each finding to exact callers, tests, mutation order, and rollback seams, and by reporting inspected files and residual risks.

## Evidence
Report status, changed files (`none` for this read-only task), inspected files and line-level findings, commands run, test logs or validation results (`not run` with rationale), proposed module interface, dependency-ordered TDD cases, migration/compatibility risks, unverified areas, and review needs.

## Human Gate
Wait for main-agent review before changing persistence compatibility beyond versioned backup migration, removing a supported CLI mode, touching live workstation state, expanding beyond the named findings, modifying files, or skipping the read-only verification contract.
