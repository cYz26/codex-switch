---
checkpoint_id: 2026-07-26-parity-staged-update-verified
created_at: 2026-07-26T21:02:46+08:00
boundary: implementation_verified
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 5.7 handshake rollback RED
---

# Checkpoint: Staged Internal Update Promotion Verified

Date: 2026-07-26 21:02:46 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `implementation_verified`
Status: `CHECKPOINT_AND_CONTINUE`

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- Active Goal: `internal-official-feature-parity`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 45/79
- Completed item: task 5.6 staged update promotion GREEN
- Next dependency-ready item: task 5.7 handshake rollback RED
- Task 8.1 remains the explicit live Human Gate

## Verified Contract

- Public install-dir inputs retain the bound-profile directory contract.
- Real installs target only a fresh private mode-0700 sibling candidate.
- Candidate capability/parity/config/overlay/runtime preparation precedes
  bound replacement.
- Exact bound/candidate/backup paths enter one production promotion boundary.
- The store lock revalidates binary, manifest, official-reference, catalog,
  capability, and config fingerprints.
- The executable swap and schema-v3 runtime bundle commit together.
- Success output follows version, canonical Runtime Binding, app-server child,
  capability-receipt, and parity-receipt postconditions.

Task 5.7 still owns rollback after a failed post-promotion handshake. Task 5.8
still owns backup retirement and restart-required output.

## Fresh Evidence

```text
Staged update:
Python 3.12.13: 10/10
system Python 3.9.6: 10/10

Complete update/release:
Python 3.12.13: 123/123

Profile update routes:
Python 3.12.13: 30/30
system Python 3.9.6: 30/30

Complete profile:
Python 3.12.13: 201/201

Parity:
Python 3.12.13: 83/83
system Python 3.9.6: 83/83

Runtime Binding:
Python 3.12.13: 65/65
system Python 3.9.6: 65/65

Executable swap:
Python 3.12.13: 5/5
system Python 3.9.6: 5/5
```

The real `~/.zshrc` remained byte- and metadata-identical:

```text
SHA-256: 8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
inode: 48362010
size: 1959
mode: 600
mtime: 1785055828
ctime: 1785062545
```

Generated `scripts/__pycache__` residue: none.

## Post-Control-Plane Checks

```text
active strict OpenSpec: valid
all strict OpenSpec: 18 passed, 0 failed
OpenSpec apply progress: 45/79; task 5.7 next
Bash syntax: passed
Python 3.12 AST: 56/56 files
system Python 3.9 AST: 56/56 files
git diff --check: passed
```

## Durable Context Written

- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-staged-update-verified.md`

## Next Action

Execute task 5.7 as tests-only RED. Prove failed version, canonical binding,
app-server, capability receipt, overlay, config, or parity post-promotion
verification restores the old binary backup and complete old runtime bundle.
Do not implement backup retirement, print restart-required output, run a live
internal update, or cross Human Gate 8.1.
