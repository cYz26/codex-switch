# Tasks: Switch verification contract

## Target State

`codex-switch` has a target-profile verification command and one-key switches
run that verification before reporting success. Verification is CLI-first,
safe repair is bounded, and deeper Codex runtime smoke is explicit.

## Completion Contract

- [x] Regression tests prove standalone verification detects contaminated
      official configs.
- [x] Regression tests prove standalone verification reports missing plugin
      support snapshots without repair.
- [x] Regression tests prove safe repair refreshes missing plugin support
      snapshots.
- [x] Regression tests prove one-key switches run verification before doctor.
- [x] Regression tests prove runtime smoke runs the target profile Codex binary
      with target `CODEX_HOME`.
- [x] Focused tests, full test suite, syntax checks, OpenSpec validation,
      packaging, and diff checks pass or blockers are recorded.
- [x] Verification evidence and workflow state are updated.

## Capability Slices

### Slice 1: OpenSpec and red tests

**Status:** done

**Goal**
- Record the behavior contract and add failing tests before implementation.

**Files / Modules**
- `openspec/changes/switch-verification-contract/*`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add OpenSpec proposal, design, task ledger, and spec delta.
- [x] Add failing tests for official provider contamination.
- [x] Add failing tests for missing plugin support snapshot diagnostics.
- [x] Add failing tests for safe snapshot repair.
- [x] Add failing tests for one-key verification.
- [x] Add failing tests for runtime smoke.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_verify_reports_official_provider_contamination \
  CodexProfileSwitchTests.test_verify_reports_missing_plugin_support_snapshot_without_repair \
  CodexProfileSwitchTests.test_verify_safe_repair_refreshes_missing_plugin_support_snapshot \
  CodexProfileSwitchTests.test_wrapper_one_key_runs_verification_before_doctor \
  CodexProfileSwitchTests.test_verify_runtime_smoke_runs_profile_codex_with_target_home
```

### Slice 2: Verification command

**Status:** done

**Goal**
- Implement standalone `verify <profile>` with bounded safe repair, optional
  runtime smoke, optional exec smoke, and JSON report support.

**Files / Modules**
- `scripts/codex_switch_verify.py`
- `scripts/codex_profile_switch.py`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Implement active state and runtime config checks.
- [x] Implement official provider contamination check.
- [x] Implement plugin support snapshot existence/content checks and safe
      snapshot refresh.
- [x] Implement runtime smoke and explicit exec smoke.
- [x] Implement JSON report writing.
- [x] Register `verify` in argparse.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_verify_reports_official_provider_contamination \
  CodexProfileSwitchTests.test_verify_reports_missing_plugin_support_snapshot_without_repair \
  CodexProfileSwitchTests.test_verify_safe_repair_refreshes_missing_plugin_support_snapshot \
  CodexProfileSwitchTests.test_verify_runtime_smoke_runs_profile_codex_with_target_home
```

### Slice 3: One-key switch integration

**Status:** done

**Goal**
- Run verification by default in `codex-switch official/internal` after plugin
  repair and before doctor, with explicit skip/deeper-check options.

**Files / Modules**
- `scripts/codex-switch`
- `scripts/test_codex_profile_switch.py`

**Implementation**
- [x] Add `--skip-verify`, `--runtime-smoke`, `--exec-smoke <prompt>`, and
      `--verification-report` to one-key switch options.
- [x] Add a Verification section to one-key switch output.
- [x] Include verification status in the final summary.
- [x] Preserve existing plugin repair, doctor, and status behavior.

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_wrapper_one_key_runs_verification_before_doctor \
  CodexProfileSwitchTests.test_wrapper_one_key_repairs_plugins_before_doctor \
  CodexProfileSwitchTests.test_wrapper_prints_final_action_required_when_doctor_fails
```

### Slice 4: Final verification and evidence

**Status:** done

**Goal**
- Prove the full change and record durable evidence.

**Files / Modules**
- `.planning/STATE.md`
- `.planning/verification/<timestamp>-switch-verification-contract.md`
- `openspec/changes/switch-verification-contract/tasks.md`

**Validation Commands**
```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate switch-verification-contract --strict --no-interactive
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

**Verification Evidence**
- Focused verification contract tests passed, 5 tests.
- Neighboring one-key/plugin/doctor regression tests passed, 9 tests.
- Full `python3 scripts/test_codex_profile_switch.py` passed, 97 tests.
- `python3 -m py_compile scripts/*.py` passed.
- Shell syntax checks passed for `scripts/codex-switch`,
  `scripts/codex_env_setup`, `install.sh`, and `run.sh`.
- `openspec validate switch-verification-contract --strict --no-interactive`
  passed.
- `openspec validate --all --strict --no-interactive` passed 10 items.
- `scripts/package-release.sh` passed and wrote `dist/codex-switch.tar.gz`.
- `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh` passed
  and refreshed `/Users/cY/.local/share/codex-switch/current`.
- Installed `codex-switch --skip-self-update verify internal --repair=safe
  --report` passed and wrote
  `/Users/cY/.codex-switch/verification/20260630T115757Z-internal.json`.
- Installed `codex-switch --skip-self-update verify internal --repair=safe
  --runtime-smoke --report` passed and wrote
  `/Users/cY/.codex-switch/verification/20260630T115820Z-internal.json`.
- `codex-switch --skip-self-update doctor` passed.
- `git diff --check` passed.

## Risks / Rollback

- If runtime smoke is too expensive for normal switches, keep it opt-in only.
- If one-key verification finds an existing valid skip path, document the
  reason and require `--skip-verify` for that workflow.
- Do not archive this change until verification evidence exists and the archive
  gate is explicitly opened.
