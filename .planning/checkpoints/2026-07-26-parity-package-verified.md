---
checkpoint_id: 2026-07-26-parity-package-verified
created_at: 2026-07-26T23:53:25+08:00
boundary: task_complete
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Execute task 6.8 parity docs
---

# Checkpoint: Parity Package Verified

Date: 2026-07-26 23:53:25 +0800
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
- OpenSpec progress: 56/79
- Completed item: task 6.7 parity package integration
- Next dependency-ready item: task 6.8 docs-only parity contract
- Task 8.1 remains the explicit live Human Gate

## Implementation

- Parity and generated-launcher runtime modules are manifest-required.
- Generated script references must resolve to package-local Python files.
- All packaged non-test modules import in an isolated immutable copy.
- Import failure or payload mutation blocks finalization.
- `package-release.sh` selects Python 3.11+ with `tomllib`.
- Historical legacy canonicalization supplies inert placeholders for newly
  required modules.

## TDD Evidence

```text
RED: 5 methods, 8 failures, 0 errors on Python 3.12.13 and system Python 3.9.6
GREEN: focused package 5/5 on both runtimes
adjacent release/promotion: 4/4 on both runtimes
profile package adapter: 1/1 on both runtimes
Bash syntax, dual-runtime AST, targeted diff hygiene: passed
```

## Isolated Package

```text
manifest files: 66
manifest directories: 5
required paths: 20
archive members: 73
archive size: 522880 bytes
payload SHA-256: bbd79beaf00d33a48009630284ac84bb8547e215f2122e2fb1781d59c8428ae5
parity present: true
retained probe/config evidence present: false
bytecode present: false
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

No live profile, App, provider, internal install/update, dependency, release
publication, OpenSpec archive, provider/root-state migration, legacy skill
cleanup, retained-evidence cleanup, destructive cleanup, Git history, or Human
Gate 8.1 effect occurred.

## Durable Context Written

- `scripts/codex_switch_release_bundle.py`
- `scripts/package-release.sh`
- `scripts/codex_switch_promotion.py`
- `scripts/test_codex_update_release.py`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-package-verified.md`

## Next Action

Execute task 6.8 as docs-only work. Update `README.md` and `SKILL.md` with the
approved reference boundary, health/queue distinction, no-v1-fallback repair
route, staged update semantics, and explicit Human Gate 8.1. Do not start task
6.9 or run any live effect.
