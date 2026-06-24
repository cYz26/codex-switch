# Verification: Plugin materialization repair

Timestamp: 2026-06-24T18:03:17+08:00

## Scope

- Added active-profile plugin materialization checks to `codex-switch doctor`.
- Added explicit `codex-switch repair-plugins <profile>` remediation for
  enabled plugins missing from the target profile's `CODEX_HOME` plugin cache.
- Added automatic one-key post-switch plugin repair before doctor, with
  `--skip-plugin-repair` as the opt-out.
- Preserved the independent-home boundary: `plugins/` remains profile-local and
  is not copied or symlinked between profiles.

## Commands

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_doctor_reports_missing_active_profile_enabled_plugin_cache \
  CodexProfileSwitchTests.test_doctor_accepts_active_profile_enabled_plugin_cache \
  CodexProfileSwitchTests.test_repair_plugins_installs_missing_profile_plugins \
  CodexProfileSwitchTests.test_wrapper_one_key_repairs_plugins_before_doctor \
  CodexProfileSwitchTests.test_wrapper_one_key_can_skip_plugin_repair \
  CodexProfileSwitchTests.test_internal_switch_merges_legacy_profile_layer_plugin_settings \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state
```

Result: pass, 8 tests.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: pass, 76 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate independent-profile-homes --strict --no-interactive
git diff --check
```

Result: all pass.

## Residual

- `repair-plugins` intentionally installs only enabled plugins that are missing
  from the selected profile home. It does not delete orphaned plugin caches and
  does not synchronize another profile's `plugins/` directory.
- Low-level `codex-switch switch <profile>` remains a pass-through command and
  does not run the one-key post-switch repair flow.
- Archive remains unavailable because the archive gate is closed.
