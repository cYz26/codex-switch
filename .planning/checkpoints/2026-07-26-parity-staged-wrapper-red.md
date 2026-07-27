---
checkpoint_id: 2026-07-26-parity-staged-wrapper-red
created_at: 2026-07-26T19:24:06+08:00
boundary: tests_red
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 5.6 staged wrapper GREEN
---

# Checkpoint: Staged Update Wrapper RED

Date: 2026-07-26 19:24:06 +0800
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
- OpenSpec progress: 44/79
- Completed item: task 5.5 staged wrapper RED
- Next dependency-ready item: task 5.6 staged wrapper GREEN
- Task 8.1 remains the explicit live Human Gate

## RED Contract

`scripts/test_codex_update_release.py` now requires:

- a complete zero-mutation dry-run plan for staged capability/parity receipts,
  overlay, projected configs, runtime artifacts, locked fingerprints, and
  post-promotion-only bound smoke;
- candidate `app-server generate-json-schema` evidence before any bound
  executable invocation;
- exact bound/candidate/backup paths at one internal promotion boundary;
- complete capability/parity/overlay/config/runtime artifact roles; and
- binary, manifest, official-reference, catalog, capability, and config
  fingerprint revalidation while holding the store-root lock.

The temporary promotion driver exits 73 after locked revalidation and before
any promotion.

## Fresh Evidence

```text
Focused wrapper RED:
Python 3.12.13: 4 expected failures, 0 errors
system Python 3.9.6: 4 expected failures, 0 errors

Preserved installer GREEN:
Python 3.12.13: 6/6
system Python 3.9.6: 6/6

Pre-existing update/release:
Python 3.12.13: 113/113 in 225.396s

Dual-runtime syntax: passed
Focused git diff --check: passed
Generated test bytecode residue: none
```

The current failures are the missing task-5.6 wrapper integration, not fixture,
syntax, import, or unrelated baseline errors.

## Boundary Evidence

The real `~/.zshrc` remains at the stable post-task-5.3 identity:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

No production implementation, live profile, App, provider, internal
install/update, dependency, release, archive, provider/root-state migration,
legacy skill cleanup, destructive cleanup, or Git history effect occurred.

## Durable Context Written

- `scripts/test_codex_update_release.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-staged-wrapper-red.md`

## Next Action

Execute task 5.6. Integrate private sibling candidate staging, candidate
capability/parity/config/overlay preparation, exact executable swap, and
runtime-bundle promotion into `run_update_internal_env_setup`. Do not report
success until installed version, canonical Runtime Binding, app-server smoke,
capability receipt, and parity receipt postconditions pass. Do not run a live
update or cross Human Gate 8.1.
