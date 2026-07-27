---
checkpoint_id: 2026-07-26-parity-executable-swap-red
created_at: 2026-07-26T18:48:44+08:00
boundary: tests_red
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 5.4 executable-swap journal GREEN
---

# Checkpoint: Executable-Swap Journal RED

Date: 2026-07-26 18:48:44 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `tests_red`
Status: `CHECKPOINT_AND_CONTINUE`

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- Active Goal: `internal-official-feature-parity`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 42/79
- Completed item: task 5.3 tests-only executable-swap RED
- Next dependency-ready item: task 5.4 executable-swap journal GREEN
- Task 8.1 remains the explicit live Human Gate

## RED Contract

`scripts/test_codex_transaction.py` now contains five executable-swap methods
covering:

- typed bound/candidate/backup paths, modes, and SHA-256 digests;
- no embedded binary bytes in the schema-v3 marker;
- rejection before marker publication for unsafe paths or identities;
- interruption before and after both sibling renames;
- prepared rollback of binary plus runtime bundle;
- committed roll-forward with the old backup retained; and
- fail-closed preservation of foreign bound/candidate/backup bytes.

The approved interface is one optional typed swap argument on the existing
deep `commit_runtime_binding_bundle()` seam.

## Fresh Evidence

```text
Python 3.12.13 focused:
5 tests, 23 expected assertion failures, 0 errors

system Python 3.9.6 focused:
5 tests, 23 expected assertion failures, 0 errors

Expected cause:
missing RuntimeBindingExecutableSwap

Pre-existing transaction baseline with isolated shell profile:
Python 3.12.13: 234/234 in 22.044s
system Python 3.9.6: 234/234 in 119.804s
```

## Shell-Profile Boundary Incident

An earlier unisolated baseline run atomically rewrote the real `~/.zshrc` with
byte-identical content. SHA-256, size, mode, and mtime stayed unchanged, but
inode changed from `48028504` to `48362010` and ctime became `1785062545`.
Both accepted isolated baseline runs then asserted the complete current file
hash/stat tuple before and after and observed no further change.

All later full transaction commands must set a private
`CODEX_SWITCH_SHELL_PROFILE`.

## Durable Context Written

- `scripts/test_codex_transaction.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-executable-swap-red.md`

## Scope and Gates

No production source, live profile, App, provider, internal install/update,
dependency, release, archive, provider/root-state migration, legacy skill
cleanup, destructive cleanup, or Git history effect occurred. Commit, push,
tag, release, archive, and Human Gate 8.1 remain unauthorized.

## Next Action

Execute task 5.4. Add the typed executable-swap marker entry to schema v3,
validate exact sibling paths, mode, and digest state, perform the two durable
renames before runtime artifact promotion, and recover binary plus text bundle
to one generation. Preserve schema-v1/v2 marker behavior and do not integrate
the wrapper or run a live update.
