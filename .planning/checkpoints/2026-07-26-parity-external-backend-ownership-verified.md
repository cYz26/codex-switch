---
checkpoint_id: 2026-07-26-parity-external-backend-ownership-verified
created_at: 2026-07-26T22:11:08+08:00
boundary: characterization_verified
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 5.10 complete staged-update verification
---

# Checkpoint: External Backend Ownership Verified

Date: 2026-07-26 22:11:08 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `characterization_verified`
Status: `CONTINUE_NEXT_ITEM`

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- Active Goal: `internal-official-feature-parity`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 48/79
- Completed item: task 5.9 external backend ownership proof
- Next dependency-ready item: task 5.10 complete staged-update verification
- Task 8.1 remains the explicit live Human Gate

## Proven Contract

`set-bin internal <external-path>`:

- prepares and commits the same eight-target parity/runtime bundle;
- records no executable swap;
- never targets the external backend in the schema-v3 artifact set;
- preserves external device, inode, mode, link count, size, mtime, ctime,
  bytes, and parent directory entries;
- creates no persistent same-byte backend copy under the store; and
- binds the manifest and canonical runtime to the original external path.

## Fresh Evidence

```text
Python 3.12.13 focused ownership: 1/1 in 2.669s
system Python 3.9.6 focused ownership: 1/1 in 5.989s
Python 3.12.13 adjacent ownership/bundle/rollback: 3/3 in 7.752s
system Python 3.9.6 adjacent ownership/bundle/rollback: 3/3 in 17.639s
```

The first focused run on each runtime had one test-only missing-`stat` import
error in the final copy scan. Adding the import required no production change.

## Boundary Evidence

```text
~/.zshrc SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48897140
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785074064
```

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred.

## Durable Context Written

- `scripts/test_codex_runtime_binding.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-external-backend-ownership-verified.md`

## Next Action

Execute task 5.10. Run the complete update/release, transaction, Runtime
Binding, parity, and supported profile verification matrix on Python 3.12.13
and system Python 3.9.6 with a private validation shell profile. Review the
integrated staged-update diff, record exact counts, and only then select task
6.1. Do not run a live update/rebind or cross Human Gate 8.1.
