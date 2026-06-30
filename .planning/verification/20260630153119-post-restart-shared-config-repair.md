# Post-restart shared config repair

Date: 2026-06-30 15:31:19 +0800

## Scope

After restarting Codex Desktop, the active internal Desktop app-server loaded
the repaired wrapper, but the workstation did not recover older/official
shared configuration because the current official/internal runtime configs and
profile-local plugin support snapshots had already been narrowed. The
official profile layer was also polluted again because an unannotated
provider runtime was not an exact profile-seed match for the internal source
home and was still accepted as the official runtime seed.

## Additional Repair

- `openai-official` now skips any unannotated runtime seed containing
  `model_provider` when an explicit official profile layer has a `model` and
  no provider.
- Profile config generation now treats the source profile's
  `<profile>.plugin-support.config.toml` as shared fallback defaults, while
  target runtime and target snapshot plugin settings keep precedence.

## Regression Verification

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_ignores_unannotated_provider_runtime_when_explicit_layer_is_clean \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_source_profile_snapshot
```

Result: failed before implementation, then passed after the repair.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_ignores_unannotated_internal_runtime_seed \
  CodexProfileSwitchTests.test_official_switch_ignores_unannotated_provider_runtime_when_explicit_layer_is_clean \
  CodexProfileSwitchTests.test_official_switch_repairs_contaminated_managed_runtime_profile_seed \
  CodexProfileSwitchTests.test_official_switch_keeps_managed_runtime_model_without_provider \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_target_runtime_when_source_lost_it \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_profile_snapshot_after_runtime_loss \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_source_profile_snapshot \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_repair_plugins_disable_unavailable_stale_enabled_plugins
```

Result: passed, 9 tests.

```bash
python3 scripts/test_codex_profile_switch.py
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
git diff --check
scripts/package-release.sh
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
```

Results: all passed. The full test file passed 92 tests, OpenSpec validation
passed 9 items, release packaging wrote `dist/codex-switch.tar.gz`, and the
local bundle was installed.

## Workstation Restoration

Before restoring, current config files were backed up under:

`/Users/cY/.codex-switch/backups/20260630152911-pre-post-restart-shared-config-repair/`

Restoration sources:

- Rich shared config:
  `/Users/cY/.codex-switch/backups/20260630T062435Z-switch-openai-official-to-internal/3-config.toml`
- Clean official profile layers:
  `/Users/cY/.codex-switch/backups/20260630T065702Z-switch-internal-to-openai-official/4-openai-official.config.toml`
  and `6-config.toml`

After regeneration and a real `official -> internal` switch cycle:

- `/Users/cY/.codex/config.toml` is official `gpt-5.5` and has no
  `model_provider`.
- `/Users/cY/.codex-switch/homes/internal/config.toml` is internal Azure.
- Official and internal runtime/snapshot configs contain 5 marketplaces, 24
  plugin blocks, and 43 hook trust blocks.
- `agent-kb@cy-codex-skills`, `lark-feishu-ops@cy-codex-skills`,
  `pdf@openai-primary-runtime`, and `game-design-workshop@game-design-workshop`
  are present and enabled where expected.
- `codex-switch --skip-self-update doctor` passed.
- `CODEX_HOME=/Users/cY/.codex-switch/homes/internal codex plugin list --json`
  reported the restored enabled plugin set.

## Remaining Operational Note

The final switch regenerated the Desktop wrapper. Restart Codex Desktop once
more so the running app-server process reloads the latest installed proxy code.
