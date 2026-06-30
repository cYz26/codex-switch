# Verification: switch verification contract

Timestamp: 2026-06-30T16:49:24+08:00

## Scope

Implemented the `switch-verification-contract` follow-up change. The repair
adds standalone `codex-switch verify <profile>`, integrates target-profile
verification into one-key `internal` and `official` switches after plugin
repair and before doctor, and supports bounded safe repair, optional runtime
smoke, explicit exec smoke, and JSON verification reports.

## Red / Green Evidence

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_verify_reports_official_provider_contamination \
  CodexProfileSwitchTests.test_verify_reports_missing_plugin_support_snapshot_without_repair \
  CodexProfileSwitchTests.test_verify_safe_repair_refreshes_missing_plugin_support_snapshot \
  CodexProfileSwitchTests.test_wrapper_one_key_runs_verification_before_doctor \
  CodexProfileSwitchTests.test_verify_runtime_smoke_runs_profile_codex_with_target_home
```

Result before implementation: failed because `verify` was not a valid command
and one-key switches had no Verification section.

Result after implementation: passed, 5 tests.

Submit-readiness addendum: the missing snapshot regression failed before the
final guard because plain `verify` returned success when both profile-local
plugin support snapshot files were absent. After the guard, the focused
missing-snapshot and safe-repair tests passed together.

## Validation Commands

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_wrapper_one_key_repairs_plugins_before_doctor \
  CodexProfileSwitchTests.test_wrapper_one_key_unavailable_plugin_reaches_doctor_without_repair_failure \
  CodexProfileSwitchTests.test_wrapper_one_key_can_skip_plugin_repair \
  CodexProfileSwitchTests.test_wrapper_prints_final_action_required_when_doctor_fails \
  CodexProfileSwitchTests.test_wrapper_one_key_official_checks_update_before_switch \
  CodexProfileSwitchTests.test_wrapper_one_key_official_can_skip_auto_login \
  CodexProfileSwitchTests.test_wrapper_one_key_can_skip_update_check \
  CodexProfileSwitchTests.test_running_desktop_problem_accepts_internal_proxy_child_app_server \
  CodexProfileSwitchTests.test_verify_safe_repair_refreshes_missing_plugin_support_snapshot
```

Result: passed, 9 tests.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 97 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: passed.

```bash
openspec validate switch-verification-contract --strict --no-interactive
openspec validate --all --strict --no-interactive
```

Result: passed. Full OpenSpec validation reported 10 passed, 0 failed.

```bash
scripts/package-release.sh
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
git diff --check
```

Result: passed. Packaging wrote `dist/codex-switch.tar.gz`, and install
refreshed `/Users/cY/.local/share/codex-switch/current`.

## Live Workstation Check

Before reinstalling, the PATH-installed `codex-switch` did not yet know the
new `verify` command. After packaging and installing the local bundle, the
installed command passed:

```bash
codex-switch --skip-self-update verify internal --repair=safe --report
codex-switch --skip-self-update verify internal --repair=safe --runtime-smoke --report
codex-switch --skip-self-update doctor
codex-switch --skip-self-update status
```

Results:

- `verify internal --repair=safe --report` passed.
- `verify internal --repair=safe --runtime-smoke --report` passed.
- The installed verifier refreshed
  `/Users/cY/.codex-switch/homes/internal/internal.plugin-support.config.toml`
  and `/Users/cY/.codex-switch/profiles/internal/internal.plugin-support.config.toml`.
- Verification reports:
  `/Users/cY/.codex-switch/verification/20260630T115757Z-internal.json`.
  `/Users/cY/.codex-switch/verification/20260630T115820Z-internal.json`.
- `doctor` passed.
- `status` reported active profile `internal`, active `CODEX_HOME`
  `/Users/cY/.codex-switch/homes/internal`, GUI and LaunchAgent
  `CODEX_CLI_PATH` pointing at
  `/Users/cY/.codex-switch/bin/codex-internal-app`, and the running app-server
  accepted via the managed app proxy.

## Residual Risk

Runtime smoke is intentionally opt-in because `plugin list --json` and
especially `exec --json` can depend on the target Codex binary, local
authentication, plugin state, network, and model availability. Standard
switches now verify local machine state by default; post-upgrade acceptance
should add `--runtime-smoke` and only add `--exec-smoke <prompt>` when a
model-backed smoke is explicitly desired.
