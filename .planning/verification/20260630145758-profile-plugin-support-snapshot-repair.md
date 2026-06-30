# Profile-local plugin support snapshot repair

Date: 2026-06-30 14:57:58 +0800

## Scope

Repeated official/internal switching could lose plugin support configuration
when the current source home no longer contained preserved shared plugin blocks.
The repair adds profile-local plugin support snapshots for marketplace,
plugin, skill, and hook trust settings, uses previous runtime/snapshot content
as fallback when a source home is narrowed, and keeps canonical profile config
profile-specific.

## Verification

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_target_runtime_when_source_lost_it \
  CodexProfileSwitchTests.test_internal_switch_restores_plugin_support_from_profile_snapshot_after_runtime_loss
```

Result: passed, 2 tests. Before implementation this failed because the
internal switch dropped `[marketplaces.cy-codex-skills]` and the
profile-local plugin support snapshot did not exist.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_ignores_unannotated_internal_runtime_seed \
  CodexProfileSwitchTests.test_official_switch_repairs_contaminated_managed_runtime_profile_seed \
  CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings \
  CodexProfileSwitchTests.test_internal_switch_merges_legacy_profile_layer_plugin_settings \
  CodexProfileSwitchTests.test_repair_plugins_disable_unavailable_stale_enabled_plugins \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_wrapper_internal_auto_updates_when_latest_differs
```

Result: passed, 7 tests.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 90 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
git diff --check
scripts/package-release.sh
```

Results: all passed. `scripts/package-release.sh` wrote
`dist/codex-switch.tar.gz`.

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
```

Result: installed
`/Users/cY/.local/bin/codex-switch -> /Users/cY/.local/share/codex-switch/current/scripts/codex-switch`.

## Real Workstation Check

```bash
codex-switch --skip-self-update official --skip-login --skip-update-check --skip-plugin-repair --skip-doctor --no-status --skip-launchctl
codex-switch --skip-self-update internal --skip-update-check --skip-launchctl
```

Result: final state is active `internal`; plugin repair reported no missing
enabled plugins; doctor passed; status showed active `CODEX_HOME` as
`/Users/cY/.codex-switch/homes/internal` and Desktop app CLI as
`/Users/cY/.codex-switch/bin/codex-internal-app`.

Observed files:

- `/Users/cY/.codex-switch/homes/internal/internal.plugin-support.config.toml`
- `/Users/cY/.codex-switch/profiles/internal/internal.plugin-support.config.toml`

Both contain the expected marketplace, plugin, and hook trust blocks. The
generated `/Users/cY/.codex-switch/bin/codex-internal-app` imports and calls
`refresh_profile_plugin_support_snapshot`.

## Residual Risk

The currently running Desktop app-server process was already alive before this
repair was installed. Restart Codex Desktop for that process to load the
updated app proxy and wrapper code.
