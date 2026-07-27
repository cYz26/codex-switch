---
checkpoint_id: 2026-07-26-parity-staged-internal-update-red
created_at: 2026-07-26T18:12:36+08:00
boundary: tests_red
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: true
compact_status: pending
next_stage: Execute task 5.2 staged installer GREEN
---

# Checkpoint: Staged Internal Update RED

Date: 2026-07-26 18:12:36 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Boundary: `tests_red`
Status: `CHECKPOINT_AND_CONTINUE`

## Resume State

- Repository: `/Users/cY/dev/codex-switch`
- Branch: `main`
- `HEAD` and `origin/main`: `0a9400d`
- Existing dirty-worktree changes: preserved
- Worktree status SHA-256:
  `413a3f1bcabbd67907b4440f7678b042c650c905a94fd6683b70ffb062ff067b`
- Active Goal: `internal-official-feature-parity`
- OpenSpec schema: `spec-driven`
- OpenSpec progress: 40/79
- Completed item: task 5.1 tests-only RED
- Next dependency-ready item: task 5.2 installer candidate GREEN
- Task 8.1 remains the explicit live Human Gate

## RED Contract

`scripts/test_codex_update_release.py` now contains seven
`CodexStagedInternalUpdateTests` for:

- validated mode-`0700` private sibling candidate installation;
- unchanged bound binary bytes and mode during installer/candidate probes;
- exact intended-version validation;
- code-sign before final candidate validation;
- exact installer failure propagation;
- complete zero-mutation dry-run reporting; and
- parity/compatibility before bound replacement.

All tests use temporary fake installer, `curl`, `codesign`, binary, store, and
home paths.

## Fresh Evidence

```text
Focused Python 3.12.13:
7 tests, 12 expected assertion failures, 0 errors

Focused system Python 3.9.6:
7 tests, the same expected RED methods, 0 errors

Complete Python 3.12.13 update/release:
120 tests, 12 expected assertion failures, 0 errors
All 113 pre-existing tests remain green

Dual-runtime AST: passed
Focused git diff --check: passed
```

The current behavior accepts non-sibling targets, creates mode-`0755`
candidate directories under `umask 022`, accepts a version mismatch, validates
before codesign, converts installer exit `17` to `1`, advertises an in-place
dry-run, omits staged parity/promotion details, and replaces the bound binary
before a failed compatibility probe.

## Durable Context Written

- `scripts/test_codex_update_release.py`
- `openspec/changes/internal-official-feature-parity/tasks.md`
- `TASK_LEDGER.md`
- `.planning/STATE.md`
- `.planning/devflow/verification/internal-official-feature-parity.md`
- `.planning/checkpoints/2026-07-26-parity-staged-internal-update-red.md`

## Scope and Gates

The real `~/.zshrc` remains unchanged at SHA-256
`8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4`,
inode `48028504`, size `1959`, mtime `1785055828`, and ctime `1785055828`.

No production source, live profile, App, provider, install, dependency,
release, archive, provider/root-state migration, legacy skill cleanup,
destructive cleanup, or Git history effect occurred. Commit, push, tag,
release, archive, and Human Gate 8.1 remain unauthorized.

## Next Action

Execute task 5.2. Refactor `scripts/codex_env_setup` so the trusted installer
targets only an explicit validated private sibling candidate directory, never
moves or replaces the bound binary, preserves the model/endpoint/auth inputs,
requires the intended candidate version, signs before final validation, and
propagates installer failure status. Do not implement executable swap, runtime
bundle promotion, full wrapper handshake, or live update effects in this task.
