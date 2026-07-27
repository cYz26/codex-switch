---
checkpoint_id: 2026-07-26-parity-diagnostics-verified
created_at: 2026-07-26T23:30:34+08:00
boundary: task_complete
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Execute task 6.5 parity repair routing tests-only RED
---

# Checkpoint: Parity Diagnostics Integration Verified

Date: 2026-07-26 23:30:34 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `task_complete`
Status: `CONTINUE_NEXT_ITEM`

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- Active Goal: `internal-official-feature-parity`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 53/79
- Completed item: task 6.4 shared parity diagnostics integration
- Next dependency-ready item: task 6.5 repair-routing tests-only RED
- Task 8.1 remains the explicit live Human Gate

## Implementation

- One verifier-owned helper prints parity health, stable finding codes, and
  canonical queue rows.
- Verify reuses its single collected report.
- Status reports parity only for active internal.
- Doctor reuses its active internal Runtime Binding and parity error findings.
- Error messages are sanitized before command output.
- Read-only diagnostics do not prepare, repair, rewrite, download, or
  reclassify evidence.

## TDD Evidence

```text
Python 3.12.13: shared diagnostics 2/2 in 0.017s
system Python 3.9.6: shared diagnostics 2/2 in 0.016s
Python 3.12.13: ParityVerificationTests 6/6 in 0.026s
system Python 3.9.6: ParityVerificationTests 6/6 in 0.039s
Python 3.12.13: adjacent status/Doctor regressions 3/3 in 4.762s
Python 3.12 AST: 4/4 touched files
system Python 3.9 AST: 4/4 touched files
```

The two direct system-Python adjacent subprocess checks that do not select a
3.11+ interpreter stop at the established `tomllib` boundary before entering
the changed diagnostics. The supported explicit-interpreter Doctor route
passes.

## Incidental Finding

`DEFER_AND_CONTINUE`: an existing one-key internal fixture has no parity
receipt and now stops at `parity.receipt.missing`. Tasks 6.5/6.6 already own
the explicit staged rebind repair path. Task 6.4 did not add an in-place patch,
fallback, public CLI, or test-only production bypass.

## Boundary Evidence

```text
~/.zshrc SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
HEAD == origin/main: 0a9400d
```

No live profile, App, provider, internal install/update, receipt, overlay,
config, dependency, release, archive, provider/root-state migration, legacy
skill cleanup, destructive cleanup, Git history, or Human Gate 8.1 effect
occurred.

## Durable Context Written

- `scripts/codex_switch_verify.py`
- `scripts/codex_switch_status.py`
- `scripts/codex_switch_doctor.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-diagnostics-verified.md`

## Next Action

Execute task 6.5 as tests-only RED. Prove explicit parity repair routes through
the staged internal rebind path and ordinary status, Doctor, and
`verify --repair=none` never patch receipt, overlay, config, launcher, or
manifest in place. Do not implement task 6.6 or cross Human Gate 8.1.
