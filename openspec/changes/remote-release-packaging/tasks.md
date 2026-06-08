# Tasks: Remote Release Packaging

## Target State

Release publication is reproducible from GitHub Actions, and missing release
asset scenarios can recover by staging from a source archive for installer,
remote runner, and local self-update flows.

## Completion Contract

- [ ] Target State is implemented.
- [ ] Every Capability Slice is done or blocked with a recorded reason.
- [ ] Acceptance Criteria are checked.
- [ ] Validation Commands have been run or documented as unavailable.
- [ ] Verification evidence is recorded.
- [ ] Workflow state is updated.

## Capability Slices

### Slice 1: Regression tests

**Status:** done

**Goal**
- Lock the missing-release-asset fallback behavior and workflow asset contract
  before production changes.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`
- `.github/workflows/release.yml`
- `install.sh`
- `run.sh`
- `scripts/codex-switch`

**Implementation**
- [x] Add a test that runs `install.sh` with a missing primary bundle and a
      source archive fallback, then verifies the installed PATH command works.
- [x] Add a test that runs `run.sh` with a missing primary bundle and a source
      archive fallback, then verifies command arguments pass through and no PATH
      symlink is created.
- [x] Add a test that runs an installed wrapper self-update with a missing
      primary bundle and a source archive fallback, then verifies the synced
      wrapper executes.
- [x] Add a static workflow contract test for `permissions: contents: write`,
      package generation, and upload of `install.sh`, `run.sh`, and
      `codex-switch.tar.gz`.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_installer_falls_back_to_source_archive_and_installs_path_command
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_remote_runner_falls_back_to_source_archive_and_execs_command
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_self_update_falls_back_to_source_archive
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_release_workflow_uploads_required_assets
```

### Slice 2: Fallback implementation

**Status:** done

**Goal**
- Stage a valid codex-switch implementation from a source archive when release
  asset download fails.

**Files / Modules**
- `install.sh`
- `run.sh`
- `scripts/codex-switch`

**Implementation**
- [x] Add source archive URL resolution and extraction helpers.
- [x] Prefer local packaging with `scripts/package-release.sh`.
- [x] Preserve installer symlink behavior and remote runner no-symlink behavior.
- [x] Keep self-update failures non-blocking.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_installer_falls_back_to_source_archive_and_installs_path_command
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_remote_runner_falls_back_to_source_archive_and_execs_command
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_self_update_falls_back_to_source_archive
bash -n install.sh
bash -n run.sh
bash -n scripts/codex-switch
```

### Slice 3: Remote release workflow

**Status:** done

**Goal**
- Build and upload release assets from GitHub for tag releases.

**Files / Modules**
- `.github/workflows/release.yml`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add release workflow with tag and manual dispatch triggers.
- [x] Run tests, syntax checks, OpenSpec validation, and package generation.
- [x] Create or update the tag release and upload required assets with clobber.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_release_workflow_uploads_required_assets
```

### Slice 4: Docs, version, and final verification

**Status:** done

**Goal**
- Document the cross-project release path, record evidence, and publish a
  verified release tag.

**Files / Modules**
- `README.md`
- `SKILL.md`
- `VERSION`
- `openspec/specs/codex-switch/spec.md`
- `.planning/verification/`
- `.planning/STATE.md`

**Implementation**
- [x] Document `CODEX_SWITCH_SOURCE_TARBALL_URL` and GitHub Actions release
      publishing.
- [x] Update stable spec after validation.
- [x] Bump version for the release containing this behavior.
- [x] Run full validation and record evidence.
- [x] Commit, push, tag, and verify the direct remote release URL when GitHub
      publishes assets, or record the external blocker.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
python3 -m json.tool evals/evals.json
scripts/package-release.sh
test -x dist/run.sh
test -x dist/codex-switch/run.sh
git diff --check
openspec validate remote-release-packaging --strict --json
openspec validate --all --strict --json
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Regression tests | done | `.planning/verification/20260608144055-remote-release-packaging-verification.md` |
| Fallback implementation | done | `.planning/verification/20260608144055-remote-release-packaging-verification.md` |
| Remote release workflow | done | `.planning/verification/20260608144055-remote-release-packaging-verification.md` |
| Docs, version, and final verification | done | `.planning/verification/20260608144055-remote-release-packaging-verification.md` |

## Acceptance Criteria

- [x] GitHub Actions can build and upload release assets for `v*` tags.
- [x] `install.sh` can recover from a missing release bundle using a source
      archive fallback.
- [x] `run.sh` can recover from a missing release bundle using a source archive
      fallback and still avoids PATH symlink creation.
- [x] Local wrapper self-update can recover from a missing release bundle using
      a source archive fallback without making failures fatal.
- [x] Documentation includes direct remote invocation and fallback controls.
- [x] Verification evidence is recorded before any archive attempt.

## Final Verification

- [x] Focused fallback regressions pass.
- [x] Full Python regression passes.
- [x] Shell syntax, package, diff, and OpenSpec checks pass.
- [x] Remote release asset invocation is verified or blocked externally with
      evidence.
