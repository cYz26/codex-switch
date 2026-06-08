# Tasks: Remote Script Runner

## Target State

Other projects can invoke `codex-switch` via a remote script without vendoring
this repository or requiring a PATH install.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Remote runner regression

**Status:** done

**Goal**
- Lock the direct remote execution contract before implementation.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`
- `run.sh`

**Implementation**
- [x] Add a failing test that builds a fake `codex-switch.tar.gz`, invokes
      `run.sh` with `CODEX_SWITCH_TARBALL_URL`, and expects command arguments
      to pass through.
- [x] Assert the runner installs into a stable local `current` directory.
- [x] Assert no public `codex-switch` symlink is created.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_remote_runner_downloads_release_and_execs_command
```

### Slice 2: Runner implementation and packaging

**Status:** done

**Goal**
- Implement the standalone remote runner and ship it in release output.

**Files / Modules**
- `run.sh`
- `scripts/package-release.sh`

**Implementation**
- [x] Add standalone `run.sh`.
- [x] Support release URL, version, source-dir, proxy, lib-dir, and dry-run
      overrides where practical.
- [x] Update packaging to copy `run.sh` into `dist/run.sh`.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_remote_runner_downloads_release_and_execs_command
bash -n run.sh
scripts/package-release.sh
```

### Slice 3: Docs and final verification

**Status:** done

**Goal**
- Document cross-project remote invocation and verify the full repository.

**Files / Modules**
- `README.md`
- `SKILL.md`
- `.planning/verification/`
- `.planning/STATE.md`

**Implementation**
- [x] Document the direct remote invocation command.
- [x] Run full verification.
- [x] Record evidence and update workflow state.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
python3 -m json.tool evals/evals.json >/dev/null
git diff --check
openspec validate remote-script-runner --strict --json
openspec validate --all --strict --json
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Remote runner regression | done | `.planning/verification/20260608115159-remote-script-runner-verification.md` |
| Runner implementation and packaging | done | `.planning/verification/20260608115159-remote-script-runner-verification.md` |
| Docs and final verification | done | `.planning/verification/20260608115159-remote-script-runner-verification.md` |

## Acceptance Criteria

- [x] Remote runner executes packaged `codex-switch` with provided args.
- [x] Remote runner uses a stable local implementation directory.
- [x] Remote runner does not create the PATH install symlink.
- [x] Release output includes `dist/run.sh`.
- [x] Verification commands pass or have recorded blockers.

## Final Verification

- [x] Focused regression passes.
- [x] Full Python regression passes.
- [x] Shell syntax, JSON, diff, package, and OpenSpec checks pass.
- [x] Verification evidence is recorded.
