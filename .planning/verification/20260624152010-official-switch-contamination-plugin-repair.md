# Verification: Official switch contamination and plugin layer repair

Timestamp: 2026-06-24T15:20:10+08:00

## Scope

- Repaired `independent-profile-homes` regression where a managed official
  runtime config could keep internal-only model/provider settings.
- Repaired legacy profile-layer plugin support merging for independent profile
  homes.
- Refreshed the real workstation state to end on `openai-official`.
- Installed the repaired packaged implementation to
  `/Users/cY/.local/share/codex-switch/current`.

## Commands

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_repairs_contaminated_managed_runtime_profile_seed \
  CodexProfileSwitchTests.test_official_switch_keeps_managed_runtime_model_without_provider \
  CodexProfileSwitchTests.test_internal_switch_merges_legacy_profile_layer_plugin_settings
```

Result: pass, 3 tests.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings \
  CodexProfileSwitchTests.test_official_switch_syncs_shared_state_back_without_internal_runtime \
  CodexProfileSwitchTests.test_internal_switch_uses_managed_home_and_backup_plan \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_preserves_official_personality \
  CodexProfileSwitchTests.test_official_switch_excludes_bulky_support_state_from_sync_plan
```

Result: pass, 7 tests.

```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict
scripts/package-release.sh
git diff --check
```

Result: all pass. Full unit suite: 71 tests.

## Live Workstation Repair

```bash
scripts/codex-switch --skip-self-update official --skip-login --skip-update-check --skip-doctor --no-status
scripts/codex-switch --skip-self-update internal --skip-update-check --skip-doctor --no-status
scripts/codex-switch --skip-self-update official --skip-login --skip-update-check --skip-doctor --no-status
CODEX_SWITCH_TARBALL_URL="file:///Users/cY/dev/codex-switch/dist/codex-switch.tar.gz" ./install.sh
/Users/cY/.local/bin/codex-switch status
```

Result:

- Active profile is `openai-official`.
- Active `CODEX_HOME` is `/Users/cY/.codex`.
- LaunchAgent and GUI `CODEX_CLI_PATH` point to
  `/Applications/Codex.app/Contents/Resources/codex`.
- Official home config no longer contains internal model/provider settings.
- Managed internal home config contains restored plugin enablement blocks.
- Installed implementation reports version `0.1.9` and includes the repair.
- Self-update reports `already up to date 0.1.9` and does not replace the
  installed repaired implementation.

Residual:

- `codex-switch doctor` still reports the already-running Codex Desktop and
  app-server processes were launched with the previous internal paths. This is
  expected until Codex Desktop is fully quit and reopened.
