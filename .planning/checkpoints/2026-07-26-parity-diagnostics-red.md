---
checkpoint_id: 2026-07-26-parity-diagnostics-red
created_at: 2026-07-26T23:20:59+08:00
boundary: tests_only_red
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Execute task 6.4 narrow diagnostics integration
---

# Checkpoint: Parity Diagnostics RED

Date: 2026-07-26 23:20:59 +0800
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
- OpenSpec progress: 52/79
- Completed item: task 6.3 status/Doctor/profile tests-only RED
- Next dependency-ready item: task 6.4 narrow diagnostics integration
- Task 8.1 remains the explicit live Human Gate

## RED Evidence

```text
Python 3.12.13: 2 tests in 0.027s, 6 failures, 0 errors
system Python 3.9.6: 2 tests in 0.026s, 6 failures, 0 errors
```

The first run exposed one tests-only verify fixture problem because the
temporary store had no internal manifest. An empty manifest stub now lets
verify reach the injected report. The final failures are exactly:

- status and Doctor do not call `collect_parity_report`; and
- verify collects once but does not print shared parity health, finding codes,
  or the optional synchronization queue.

## Completion Contract for Task 6.4

- Reuse verifier-owned parity collection and presentation.
- Collect exactly once in each command path.
- Print one deterministic health line.
- Print stable finding codes in deterministic order.
- Print the optional queue in deterministic category/identifier/code order.
- Make unhealthy parity fail Doctor and verify, but keep status read-only and
  nonzero-free.
- Do not regenerate, repair, rewrite, download, or reclassify parity evidence.

## Boundary Evidence

```text
active strict OpenSpec: valid
all strict OpenSpec: 18/18
OpenSpec apply: 52/79, task 6.4 first
workflow validator: ok=true, issues=0
workflow warning: existing legacy root-state migration reminder
Python 3.12 AST: passed
system Python 3.9 AST: passed
git diff --check: passed
touched trailing whitespace: none
generated scripts bytecode residue: none
~/.zshrc SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
HEAD == origin/main: 0a9400d
```

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, Git history, or Human Gate 8.1 effect occurred.

## Durable Context Written

- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-diagnostics-red.md`

## Next Action

Execute task 6.4. Add only the shared deterministic parity presentation and
narrow status/Doctor integrations needed to make the two task-6.3 tests GREEN.
Do not start repair routing, add a public CLI, run live effects, or cross Human
Gate 8.1.
