# Tasks: Local Command Self Update

## Target State

Persistent local `codex-switch` commands keep their release-installed script
implementation in sync with the remote bundle through a bounded, skippable,
non-blocking self-update check.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Self-update regression tests

**Status:** done

**Goal**
- Lock the release-installed self-update behavior before production changes.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`
- `scripts/codex-switch`
- `run.sh`

**Implementation**
- [x] Add a test that installs the current wrapper under a fake
      `lib/current/scripts` path, points it at a fake newer tarball, runs
      `status`, and expects the command to execute the synced implementation.
- [x] Add a test that passes `--skip-self-update` and verifies the old local
      implementation remains in place.
- [x] Add source-checkout and sync-failure safety tests.
- [x] Extend the remote runner test to assert `CODEX_SWITCH_SKIP_SELF_UPDATE=1`
      is passed to the bundled wrapper.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_remote_runner_downloads_release_and_execs_command
```

### Slice 2: Wrapper self-update implementation

**Status:** done

**Goal**
- Add a safe, interval-gated, non-blocking self-update path to the wrapper.

**Files / Modules**
- `scripts/codex-switch`

**Implementation**
- [x] Add release install detection based on `CODEX_SWITCH_LIB_DIR/current/scripts`.
- [x] Add sync source resolution compatible with existing installer variables.
- [x] Add timestamp interval handling and skip flags.
- [x] Stage and swap the implementation directory.
- [x] Re-exec once after a successful sync.
- [x] Keep ordinary sync failures as warnings and continue with the old
      implementation.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install
bash -n scripts/codex-switch
```

### Slice 3: Runner, docs, package, and final verification

**Status:** done

**Goal**
- Keep direct remote execution efficient and document the local self-update
  behavior.

**Files / Modules**
- `run.sh`
- `README.md`
- `SKILL.md`
- `openspec/specs/codex-switch/spec.md`
- `.planning/verification/`
- `.planning/STATE.md`

**Implementation**
- [x] Export `CODEX_SWITCH_SKIP_SELF_UPDATE=1` from `run.sh` before exec.
- [x] Document self-update interval and skip controls.
- [x] Update the stable spec after verification.
- [x] Record verification evidence and workflow state.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
scripts/package-release.sh
test -x dist/run.sh && test -x dist/codex-switch/run.sh
git diff --check
openspec validate local-command-self-update --strict --json
openspec validate --all --strict --json
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Self-update regression tests | done | `.planning/verification/20260608125735-local-command-self-update-verification.md` |
| Wrapper self-update implementation | done | `.planning/verification/20260608125735-local-command-self-update-verification.md` |
| Runner, docs, package, and final verification | done | `.planning/verification/20260608125735-local-command-self-update-verification.md` |

## Acceptance Criteria

- [x] Eligible release-installed local commands sync from the configured remote
      bundle and re-exec once.
- [x] Source checkout commands do not self-modify by default.
- [x] Users can skip the mechanism with `--skip-self-update` or
      `CODEX_SWITCH_SKIP_SELF_UPDATE=1`.
- [x] The check interval prevents every invocation from hitting the network by
      default.
- [x] Remote `run.sh` avoids redundant self-update work.
- [x] Sync failures are non-blocking for ordinary commands.

## Final Verification

- [x] Focused regressions pass.
- [x] Full Python regression passes.
- [x] Shell syntax, package, tarball, diff, and OpenSpec checks pass.
- [x] Verification evidence is recorded.
