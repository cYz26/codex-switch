# Bidirectional Shared Settings Shrink Prevention Verification

Verified at: 2026-07-03T21:51:56+08:00

## Scope

Repair for the `independent-profile-homes` shared config sync contract:

- Internal Desktop wrapper startup must not narrow official shared settings when
  the internal app home has a smaller shared TOML config.
- `internal -> openai-official` switch generation must preserve target-only
  shared Desktop, memories, apps, plugin, and skill settings when the source
  runtime is narrowed.
- Plugin support snapshot refresh must keep existing richer plugin/skill/hook
  state as missing defaults when the runtime no longer contains those blocks.

## Red Verification

Before implementation, the focused regression command failed with 3 failures:

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_does_not_narrow_official_shared_settings \
  CodexProfileSwitchTests.test_official_switch_does_not_narrow_existing_shared_settings \
  CodexProfileSwitchTests.test_plugin_support_snapshot_refresh_does_not_shrink_to_runtime_loss
```

Observed failures:

- wrapper startup replaced the official `[desktop]` table with only
  `followUpQueueMode = "queue"`;
- official switch generated a narrowed official runtime config from the
  narrowed internal source;
- plugin support snapshot refresh overwrote an existing rich snapshot with an
  empty annotated snapshot.

## Green Verification

Focused repaired regressions:

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_does_not_narrow_official_shared_settings \
  CodexProfileSwitchTests.test_official_switch_does_not_narrow_existing_shared_settings \
  CodexProfileSwitchTests.test_plugin_support_snapshot_refresh_does_not_shrink_to_runtime_loss
```

Result: passed, 3 tests.

Adjacent regression set:

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_missing_shared_config_defaults_preserve_new_desktop_value \
  CodexProfileSwitchTests.test_app_proxy_restores_missing_shared_config_after_config_value_write \
  CodexProfileSwitchTests.test_app_proxy_restores_missing_shared_config_after_config_batch_write \
  CodexProfileSwitchTests.test_official_switch_repairs_contaminated_managed_runtime_profile_seed \
  CodexProfileSwitchTests.test_official_switch_ignores_unannotated_provider_runtime_when_explicit_layer_is_clean \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_target_runtime_when_source_lost_it \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_profile_snapshot_after_runtime_loss \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_source_profile_snapshot \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_does_not_narrow_official_shared_settings \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_preserves_official_personality \
  CodexProfileSwitchTests.test_verify_safe_repair_refreshes_missing_plugin_support_snapshot \
  CodexProfileSwitchTests.test_verify_reports_missing_plugin_support_snapshot_without_repair
```

Result: passed, 14 tests.

Full test suite:

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 120 tests.

Static and workflow validation:

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate independent-profile-homes --strict --no-interactive
openspec validate --all --strict --no-interactive
git diff --check
scripts/package-release.sh
```

Results:

- Python compile passed.
- Shell syntax checks passed.
- `openspec validate independent-profile-homes --strict --no-interactive`
  passed.
- `openspec validate --all --strict --no-interactive` passed 11 items.
- `git diff --check` passed.
- `scripts/package-release.sh` passed and wrote
  `/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz`.
- `CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh` passed and
  installed `/Users/cY/.local/bin/codex-switch` to the current local bundle.
- `codex-switch --skip-self-update status` passed after installation. It
  reported the active profile as `openai-official` and also reported the
  existing current-shell PATH mismatch where `PATH codex` still points at the
  internal plugin-appserver path; status recommends
  `eval "$(codex-switch shim-env)"` for that shell alignment.

## Notes

DevFlow project migration remains `migration_pending` due existing
`.codex/skills` and `.agents/skills` layout conflicts. No migration apply was
run as part of this repair.
