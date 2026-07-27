---
checkpoint_id: 2026-07-26-parity-staged-installer-verified
created_at: 2026-07-26T18:29:44+08:00
boundary: task_verified
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 5.3 executable-swap journal RED
---

# Checkpoint: Staged Installer Candidate Verified

Date: 2026-07-26 18:29:44 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `task_verified`
Status: `CHECKPOINT_AND_CONTINUE`

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`:
  `0a9400dca86ff94dcbc2b6868057e088781cc49f`
- Existing dirty-worktree changes: preserved
- Active Goal: `internal-official-feature-parity`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 41/79
- Completed item: task 5.2 staged installer candidate GREEN
- Next dependency-ready item: task 5.3 executable-swap journal RED
- Task 8.1 remains the explicit live Human Gate

## Completed Contract

`scripts/codex_env_setup` now:

- requires an explicit absent private sibling candidate directory;
- creates and validates it as mode `0700`;
- preserves installer model, Azure endpoint, auth input, and intended version;
- never moves, backs up, replaces, or deletes the bound binary;
- snapshots the bound executable through `O_NOFOLLOW` using
  dev/inode/mode/size/mtime/ctime/SHA-256 evidence;
- compares that identity after installer, code-sign, and version-probe
  boundaries;
- signs before exact final version validation; and
- propagates installer failure status unchanged.

Executable swap, runtime parity promotion, wrapper dry-run completion, and
post-promotion handshake remain later tasks.

## Fresh Evidence

```text
Mutation guard RED:
Python 3.12: 1 expected failure, 0 errors
system Python 3.9: 1 expected failure, 0 errors

Mutation guard GREEN:
Python 3.12: 1/1
system Python 3.9: 1/1

Installer/helper group:
Python 3.12: 6/6
native system Python 3.9 helper: 6/6

Complete staged class:
8 tests; only 2 intentional wrapper RED methods remain

Pre-existing update/release:
Python 3.12: 113/113

Bash syntax, dual-runtime test AST, focused diff check, and main review: passed
```

## Boundary Evidence

The real `~/.zshrc` remains unchanged:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48028504
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785055828
```

No live profile, App, provider, install, dependency, release, archive,
provider/root-state migration, legacy skill cleanup, destructive cleanup,
commit, push, tag, or other Git history effect occurred.

## Next Action

Execute task 5.3 by adding tests-only executable-swap journal RED coverage for
exact bound/candidate/backup sibling paths, no embedded binary bytes,
mode/digest validation, prepared rollback, committed roll-forward,
interruption before and after every rename, and foreign binary preservation.
Do not implement the swap journal until task 5.4.
