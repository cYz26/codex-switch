# Tasks: Isolate Desktop Session State

## Target State

Internal Codex Desktop uses a profile-local app home for response/session
runtime state while continuing to share stable workstation support assets and
generated profile config.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Regression test

**Status:** done

**Goal**
- Prove the wrapper removes stale live runtime symlinks and does not recreate
  excluded runtime state links.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`
- `scripts/codex_switch_app_wrapper.py`

**Implementation**
- [x] Add a regression test that creates live `sessions`, `history.jsonl`,
      `state_5.sqlite`, `state_5.sqlite-wal`, and `browser`, pre-seeds matching
      app-home symlinks, launches the generated internal wrapper, and expects no
      excluded symlink to remain.
- [x] Process note recorded: the focused red phase was not replayed in this
      session because the implementation was already present in the dirty
      working tree before verification began.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state
```

**Done When**
- [x] The focused regression exists and covers stale live runtime symlink
      removal plus future excluded-link prevention.

### Slice 2: Wrapper state isolation

**Status:** done

**Goal**
- Implement the smallest compatible wrapper change that enforces runtime-state
  isolation.

**Files / Modules**
- `scripts/codex_switch_app_wrapper.py`

**Implementation**
- [x] Add shell exclusion cases for known runtime state basenames and sqlite
      patterns.
- [x] Add shell cleanup that removes only app-home symlinks pointing into live
      `CODEX_HOME` for excluded entries.
- [x] Keep allowed shared asset linking and config overlay behavior unchanged.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state
```

**Done When**
- [x] The focused regression passes.

### Slice 3: Verification and state update

**Status:** done

**Goal**
- Prove the repair is complete and update canonical workflow evidence.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`
- `scripts/codex_switch_app_wrapper.py`
- `openspec/changes/isolate-desktop-session-state/tasks.md`
- `.planning/STATE.md`
- `.planning/verification/`

**Implementation**
- [x] Run full regression and syntax verification.
- [x] Record verification evidence.
- [x] Update this ledger and workflow state.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
git diff --check
```

**Done When**
- [x] Verification evidence exists and no acceptance criterion remains unchecked.

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Regression test | done | `.planning/verification/20260608112025-isolate-desktop-session-state-verification.md` |
| Wrapper state isolation | done | `.planning/verification/20260608112025-isolate-desktop-session-state-verification.md` |
| Verification and state update | done | `.planning/verification/20260608112025-isolate-desktop-session-state-verification.md` |

## Acceptance Criteria

- [x] Stale live runtime symlinks in the internal app home are removed by the
      wrapper.
- [x] Excluded runtime state is not symlinked from live `CODEX_HOME` on future
      wrapper launches.
- [x] Stable shared support assets and config overlay behavior continue to work.
- [x] Verification commands pass or have recorded blockers.

## Final Verification

- [x] Focused regression passes.
- [x] Full Python regression passes.
- [x] Syntax and diff checks pass.
- [x] Verification evidence is recorded.
