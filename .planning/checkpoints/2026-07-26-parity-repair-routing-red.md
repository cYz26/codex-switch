---
checkpoint_id: 2026-07-26-parity-repair-routing-red
created_at: 2026-07-26T23:36:01+08:00
boundary: tests_only_red
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Execute task 6.6 minimal parity repair route
---

# Checkpoint: Parity Repair Routing RED

Date: 2026-07-26 23:36:01 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `tests_only_red`
Status: `CONTINUE_NEXT_ITEM`

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- Active Goal: `internal-official-feature-parity`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 54/79
- Completed item: task 6.5 parity repair-routing tests-only RED
- Next dependency-ready item: task 6.6 minimal repair implementation
- Task 8.1 remains the explicit live Human Gate

## RED Evidence

```text
Python 3.12.13: 2 tests in 0.015s, 2 failures, 0 errors
system Python 3.9.6: 2 tests in 0.014s, 2 failures, 0 errors
```

The failures are exactly the absent `repair_internal_parity` seam and the
absence of a post-rebind parity recollection.

## Read-Only Evidence

```text
Python 3.12.13: 1/1 in 0.018s
system Python 3.9.6: 1/1 in 0.020s
```

Normal status, active-internal Doctor, and `verify --repair=none` preserve
manifest, receipt, overlay, profile config, and launcher inode, mode, size,
timestamps, and bytes exactly.

## Completion Contract for Task 6.6

- Add no public CLI.
- Use the current canonical internal backend.
- Delegate to existing `cmd_set_bin` with managed Desktop binding.
- Reuse staged parity preparation and schema-v3 bundle promotion.
- Recollect parity after repair and report only the fresh result.
- Leave normal status, Doctor, and `repair=none` read-only.

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

No production source, public CLI, live profile, App, provider, internal
install/update, dependency, release, archive, provider/root-state migration,
legacy skill cleanup, destructive cleanup, Git history, or Human Gate 8.1
effect occurred.

## Durable Context Written

- `scripts/test_codex_verify.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-repair-routing-red.md`

## Next Action

Execute task 6.6. Implement only the current-backend `cmd_set_bin` delegation
and post-repair parity recollection required by the two RED tests. Do not add a
public CLI, patch parity artifacts in place, or cross Human Gate 8.1.
