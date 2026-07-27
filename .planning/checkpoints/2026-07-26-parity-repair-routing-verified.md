---
checkpoint_id: 2026-07-26-parity-repair-routing-verified
created_at: 2026-07-26T23:44:05+08:00
boundary: task_complete
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Execute task 6.7 package parity TDD
---

# Checkpoint: Parity Repair Routing Verified

Date: 2026-07-26 23:44:05 +0800
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
- OpenSpec progress: 55/79
- Completed item: task 6.6 minimal parity repair integration
- Next dependency-ready item: task 6.7 package/release parity TDD
- Task 8.1 remains the explicit live Human Gate

## Implementation

- Added no public CLI.
- Explicit unhealthy internal safe repair delegates to the existing staged
  `cmd_set_bin internal <current-backend>` route.
- Managed Desktop binding remains mandatory.
- Verify reloads Runtime Binding and recollects parity after repair.
- Only the fresh parity result is printed and evaluated.
- Normal status, Doctor, and `verify --repair=none` remain read-only.

## TDD Evidence

```text
RED Python 3.12.13: 2 failures, 0 errors in 0.014s
RED system Python 3.9.6: 2 failures, 0 errors in 0.018s
GREEN Python 3.12.13: focused 2/2; parity verifier 8/8
GREEN system Python 3.9.6: focused 2/2; parity verifier 8/8
read-only artifact characterization: 1/1 on both runtimes
dual-runtime syntax: passed
targeted diff hygiene: passed
```

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

No live rebind, profile, App, provider, internal install/update, public CLI,
direct receipt/overlay/config/launcher/manifest patch, dependency, release,
archive, provider/root-state migration, legacy skill cleanup, destructive
cleanup, Git history, or Human Gate 8.1 effect occurred.

## Durable Context Written

- `scripts/codex_switch_verify.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-repair-routing-verified.md`

## Next Action

Execute task 6.7 by TDD. Add package/release RED coverage for the parity module,
its transitive imports, generated launcher references, immutable payload file
set, and exclusion of retained probe/config evidence; then make only that
contract GREEN. Do not start docs task 6.8 or cross Human Gate 8.1.
