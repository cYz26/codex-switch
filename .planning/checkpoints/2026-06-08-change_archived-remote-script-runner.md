---
checkpoint_id: 2026-06-08-change_archived-remote-script-runner
created_at: 2026-06-08T11:54:27+08:00
boundary: change_archived
project_mode: brownfield
phase_id: 01-foundation
change_id: none
compact_recommended: false
compact_status: not_needed
next_stage: commit_or_release
---

# Checkpoint: remote script runner archived

## Current goal

Enable `codex-switch` to be invoked directly from a remote `run.sh` script in
other projects without requiring a local PATH install.

## Completed work

- Added `run.sh` as a remote runner that downloads or copies the release bundle
  into a stable implementation directory and executes bundled
  `scripts/codex-switch` with forwarded arguments.
- Updated release packaging so `dist/run.sh` exists and the tarball contains
  `codex-switch/run.sh`.
- Updated README and skill usage examples to show direct remote invocation.
- Added regression coverage for downloading a release bundle and executing a
  command through the runner.
- Archived OpenSpec change `remote-script-runner` under
  `openspec/changes/archive/2026-06-08-remote-script-runner/`.
- Updated `.planning/STATE.md` to close the active change and disable the
  archive gate.

## Durable context written

- `.planning/STATE.md`
- `.planning/verification/20260608115159-remote-script-runner-verification.md`
- `.planning/checkpoints/2026-06-08-change_archived-remote-script-runner.md`
- `.planning/phases/01-foundation/REVIEW.md`
- `README.md`
- `SKILL.md`
- `run.sh`
- `scripts/package-release.sh`
- `scripts/test_codex_profile_switch.py`
- `openspec/specs/codex-switch/spec.md`
- `openspec/changes/archive/2026-06-08-remote-script-runner/`
- `dist/run.sh`
- `dist/codex-switch.tar.gz`

## Validation performed

```text
command: openspec validate --all --strict --json
result: passed: 2 specs passed, 0 changes active, 0 failed
```

```text
command: openspec list
result: No active changes found.
```

```text
command: python3 scripts/test_codex_profile_switch.py
result: passed: 22 tests OK
```

```text
command: python3 -m py_compile scripts/*.py
result: passed
```

```text
command: bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh && bash -n dist/run.sh && bash -n dist/codex-switch/run.sh
result: passed
```

```text
command: scripts/package-release.sh
result: passed: dist/codex-switch.tar.gz rebuilt
```

```text
command: test -x dist/run.sh && test -x dist/codex-switch/run.sh && tar -tzf dist/codex-switch.tar.gz | rg '(^codex-switch/run.sh$|^codex-switch/scripts/codex-switch$)'
result: passed: codex-switch/run.sh and codex-switch/scripts/codex-switch present
```

```text
command: git diff --check
result: passed
```

## Risks

- Plugin Eval still reports score 77/100, grade C, risk high for the release
  target because the installable package intentionally includes executable CLI
  source under `scripts/`; the deferral and residual risk are recorded in
  `.planning/verification/20260608115159-remote-script-runner-verification.md`.
- Existing Python complexity remains a deferred refactor opportunity outside
  this change.
- The worktree is dirty and not committed.

## Next action

Review the dirty worktree scope, then commit, tag, or publish according to the
desired release process.

## Compact instruction

State is updated. Compact is optional before a new thread or handoff.
