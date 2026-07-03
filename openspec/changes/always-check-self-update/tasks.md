# Tasks: Always Check Self-Update

## Target State

Every ordinary release-installed `codex-switch` command checks whether the
local implementation needs to self-update before command execution. Explicit
skip controls and source checkout safety remain unchanged. Release bundles only
replace the local implementation when the release bundle version is newer.

## Completion Contract

- [x] Target State is implemented.
- [x] Every Capability Slice is done or blocked with a recorded reason.
- [x] Acceptance Criteria are checked.
- [x] Validation Commands have been run or documented as unavailable.
- [x] Verification evidence is recorded.
- [x] Workflow state is updated.

## Capability Slices

### Slice 1: Repeated-check regression

**Status:** done

**Goal**
- Prove the wrapper no longer suppresses self-update checks after a recent
  successful check.

**Files / Modules**
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Remove the test helper's forced zero interval so default behavior is
      exercised.
- [x] Add a failing test that runs a same-version release-installed wrapper
      twice and expects self-update status both times.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_local_wrapper_self_update_checks_every_invocation
```

### Slice 2: Wrapper cooldown removal

**Status:** done

**Goal**
- Remove cooldown/stamp gating while preserving explicit skip and re-exec loop
  controls.

**Files / Modules**
- `scripts/codex-switch`

**Implementation**
- [x] Remove `CODEX_SWITCH_SELF_UPDATE_INTERVAL_SECONDS` handling.
- [x] Remove `.last-self-update-check` reads and writes.
- [x] Ensure `maybe_self_update` checks after eligibility gates pass.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_local_wrapper_self_update_checks_every_invocation \
  CodexProfileSwitchTests.test_local_wrapper_self_update_reports_already_up_to_date \
  CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command \
  CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install \
  CodexProfileSwitchTests.test_source_checkout_wrapper_does_not_self_update
bash -n scripts/codex-switch
```

### Slice 3: Docs, specs, and state

**Status:** done

**Goal**
- Make the documented and specified behavior match per-invocation checks.

**Files / Modules**
- `README.md`
- `SKILL.md`
- `openspec/specs/codex-switch/spec.md`
- `openspec/changes/always-check-self-update/specs/codex-switch/spec.md`
- `.planning/STATE.md`
- `.planning/verification/`

**Implementation**
- [x] Remove cooldown wording and interval control examples.
- [x] Add or update requirements for every-invocation checks.
- [x] Record verification evidence and workflow state.

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
openspec validate always-check-self-update --strict --no-interactive
openspec validate --all --strict --no-interactive
```

### Slice 4: Version-ordered self-update

**Status:** done

**Goal**
- Prevent self-update from downgrading or overwriting a newer local
  implementation with an older published release bundle.

**Files / Modules**
- `install.sh`
- `scripts/codex-switch`
- `scripts/test_codex_profile_switch.py`
- `openspec/changes/always-check-self-update/specs/codex-switch/spec.md`
- `.planning/verification/`
- `.planning/STATE.md`

**Implementation**
- [x] Add a regression showing a newer local implementation is not replaced by
      an older release bundle.
- [x] Keep normal sync behavior when the release bundle version is newer.
- [x] Preserve same-version already-current behavior.
- [x] Bump the local source `VERSION` above the latest published release using
      a development suffix.
- [x] Reinstall the local checkout and verify ordinary commands do not
      downgrade it.
- [x] Record verification evidence and update workflow state.

**Validation Commands**
```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_does_not_self_update_to_older_release \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_self_updates_prerelease_to_formal_release \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_installer_preserves_local_source_version \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_self_update_reports_already_up_to_date -v
bash -n install.sh
bash -n scripts/codex-switch
```

## Execution Ledger

| Slice | Status | Evidence |
|---|---|---|
| Repeated-check regression | done | Focused RED failed before implementation; focused GREEN passed after implementation |
| Wrapper cooldown removal | done | Focused GREEN passed after implementation |
| Docs, specs, and state | done | `.planning/verification/20260622145941-always-check-self-update.md` |
| Version-ordered self-update | done | `.planning/verification/20260703221616-version-ordered-self-update.md` |

## Acceptance Criteria

- [x] Consecutive eligible release-installed wrapper invocations both print
      self-update check status.
- [x] Same-version checks still report already up to date.
- [x] Newer release checks still sync and re-exec once.
- [x] Explicit skips remain quiet.
- [x] Source checkout usage remains non-mutating.
- [x] Older release bundles do not replace newer local implementations.

## Final Verification

- [x] Focused regressions pass.
- [x] Full Python regression passes.
- [x] Shell syntax, package, diff, and OpenSpec checks pass.
- [x] Verification evidence is recorded.
- [x] Version-ordered self-update verification evidence is recorded.
