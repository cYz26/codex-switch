# Tasks: Self-Update Status Output

## Target State

Release-installed `codex-switch` commands show self-update status when a check
actually runs: check start, already-current result, sync result, or existing
failure warning. Explicitly skipped and interval-skipped checks stay quiet.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Status regression tests

**Status:** done

**Goal**
- Lock the user-visible self-update output before production changes.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add a failing test for same-version due check status output.
- [x] Extend sync-needed and skip tests to assert status output.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_local_wrapper_self_update_reports_already_up_to_date \
  CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command \
  CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install
```

### Slice 2: Wrapper output implementation

**Status:** done

**Goal**
- Print concise status messages from the existing self-update path.

**Files / Modules**
- `scripts/codex-switch`

**Implementation**
- [x] Print check-start status after eligibility and interval gates pass.
- [x] Print already-up-to-date status when staged and current versions match.
- [x] Preserve existing sync success and warning messages.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_local_wrapper_self_update_reports_already_up_to_date \
  CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command \
  CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install \
  CodexProfileSwitchTests.test_self_update_failure_does_not_block_local_command
bash -n scripts/codex-switch
```

### Slice 3: Docs, state, and final verification

**Status:** done

**Goal**
- Document the status output behavior and record verification evidence.

**Files / Modules**
- `README.md`
- `SKILL.md`
- `openspec/specs/codex-switch/spec.md`
- `.planning/STATE.md`
- `.planning/verification/`
- `openspec/changes/self-update-status/tasks.md`

**Implementation**
- [x] Document check-start, already-current, sync, and warning output.
- [x] Update stable spec.
- [x] Record verification evidence.
- [x] Update workflow state.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
python3 -m json.tool evals/evals.json >/dev/null
scripts/package-release.sh
git diff --check
openspec validate self-update-status --strict --no-interactive
openspec validate --all --strict --no-interactive
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Status regression tests | done | `.planning/verification/20260615185911-self-update-status-verification.md` |
| Wrapper output implementation | done | `.planning/verification/20260615185911-self-update-status-verification.md` |
| Docs, state, and final verification | done | `.planning/verification/20260615185911-self-update-status-verification.md` |

## Acceptance Criteria

- [x] Due same-version checks print check-start and already-current status.
- [x] Due sync-needed checks print check-start and synced-version status.
- [x] Explicit self-update skips remain quiet.
- [x] Existing failure warning behavior remains intact.

## Final Verification

- [x] Focused regressions pass.
- [x] Full Python regression passes.
- [x] Shell syntax, package, diff, and OpenSpec checks pass.
- [x] Verification evidence is recorded.
