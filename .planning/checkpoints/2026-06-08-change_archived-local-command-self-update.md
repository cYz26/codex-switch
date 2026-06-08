---
checkpoint_id: 2026-06-08-change_archived-local-command-self-update
created_at: 2026-06-08T12:58:56+08:00
boundary: change_archived
project_mode: brownfield
phase_id: 01-foundation
change_id: none
compact_recommended: false
compact_status: not_needed
next_stage: commit_or_release
---

# Checkpoint: local command self-update archived

## Current goal

Make persistent local `codex-switch` commands sync their release-installed
implementation from the remote bundle before ordinary command execution.

## Completed work

- Added a bounded self-update check to `scripts/codex-switch`.
- Limited auto-sync to release-installed wrappers under
  `${CODEX_SWITCH_LIB_DIR:-~/.local/share/codex-switch}/current/scripts`.
- Added `--skip-self-update` and `CODEX_SWITCH_SKIP_SELF_UPDATE=1`.
- Added interval control through `CODEX_SWITCH_SELF_UPDATE_INTERVAL_SECONDS`.
- Kept source checkout execution immutable by default.
- Made ordinary sync failures non-blocking warnings.
- Updated `run.sh` to skip redundant wrapper self-update after it prepares the
  release bundle.
- Updated README, SKILL, stable OpenSpec spec, tests, and release package.
- Archived OpenSpec change `local-command-self-update` under
  `openspec/changes/archive/2026-06-08-local-command-self-update/`.

## Durable context written

- `.planning/STATE.md`
- `.planning/verification/20260608125735-local-command-self-update-verification.md`
- `.planning/checkpoints/2026-06-08-change_archived-local-command-self-update.md`
- `README.md`
- `SKILL.md`
- `run.sh`
- `scripts/codex-switch`
- `scripts/test_codex_profile_switch.py`
- `openspec/specs/codex-switch/spec.md`
- `openspec/changes/archive/2026-06-08-local-command-self-update/`
- `dist/run.sh`
- `dist/codex-switch.tar.gz`

## Validation performed

```text
command: python3 scripts/test_codex_profile_switch.py
result: passed: 26 tests OK
```

```text
command: python3 -m py_compile scripts/*.py
result: passed
```

```text
command: bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
result: passed
```

```text
command: scripts/package-release.sh && test -x dist/run.sh && test -x dist/codex-switch/run.sh && tar -tzf dist/codex-switch.tar.gz | rg '(^codex-switch/run.sh$|^codex-switch/scripts/codex-switch$|^codex-switch/scripts/test_codex_profile_switch.py$)'
result: passed
```

```text
command: openspec validate --all --strict --json
result: passed: 2 specs passed, 0 changes active, 0 failed
```

```text
command: openspec list
result: No active changes found.
```

```text
command: git diff --check
result: passed
```

## Risks

- Self-update depends on release tarball availability. Failures are non-blocking
  and the old local implementation continues to run.
- Self-update compares bundle `VERSION`; re-publishing the same version with
  changed scripts is intentionally not treated as a newer bundle.
- The worktree is dirty and not committed.

## Next action

Review the dirty worktree scope, then commit, tag, or publish according to the
desired release process.

## Compact instruction

State is updated. Compact is optional before a new thread or handoff.
