# Settings Panel Pets, Plugins, and Skills Sync

Date: 2026-07-03

OpenSpec change: `independent-profile-homes`

## User Clarification

The affected Settings surface is the Desktop Settings sidebar:
General, Appearance, Configuration, Personalization, Pets, and Keyboard
shortcuts.

## Findings

- General/Appearance/Configuration/Personalization settings are split between
  `config.toml` and `.codex-global-state.json`.
- `config.toml` shared settings were already present in both official and
  internal homes.
- The sanitized `.codex-global-state.json` settings subset was already merged
  into the internal home by the prior repair, with prompt/thread/runtime keys
  excluded.
- The remaining missing Settings panel support was `pets/`: official home had
  `/Users/cY/.codex/pets`, while internal home did not. The directory was
  listed as non-shareable even though it backs a user-facing Settings panel.
- Plugins/marketplaces/hooks/MCP TOML config counts matched between official
  and internal homes during the audit: 25 plugins, 5 marketplaces, 43 hooks,
  and 2 MCP entries.
- Internal `skills` is a symlink to `/Users/cY/.codex/skills`.
- Internal `plugins` remains a profile-local cache directory, as designed.
  It is not copied or symlinked wholesale from official.
- DevFlow plugin-project migration sync-only remains `migration_pending` due
  to legacy `.codex/skills` duplicates/conflicts with `.agents/skills`. No
  migration apply was run.

## Repair

- Removed `pets` from the Python non-shareable home-entry list.
- Removed `pets` from the generated internal Desktop wrapper shell
  non-shareable list.
- Added regression coverage for switch-time and wrapper-startup `pets/`
  support sync.
- Updated README and `independent-profile-homes` OpenSpec design/spec/tasks.

## Red Evidence

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_syncs_pets_settings_support \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_pets_settings_support
```

Before implementation this failed because:

- `switch internal` did not materialize `pets/` in the internal home.
- The generated internal Desktop wrapper did not link `pets/` from the live
  official home.

## Green Evidence

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_syncs_pets_settings_support \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_pets_settings_support
```

Result: 2 tests passed.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_excludes_bulky_support_state_from_sync_plan \
  CodexProfileSwitchTests.test_internal_switch_syncs_pets_settings_support \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_pets_settings_support \
  CodexProfileSwitchTests.test_desktop_global_settings_state_sync_merges_safe_settings_only \
  CodexProfileSwitchTests.test_switch_syncs_desktop_global_settings_state_between_independent_homes \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_desktop_global_settings_state \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_doctor_accepts_active_profile_enabled_plugin_cache \
  CodexProfileSwitchTests.test_repair_plugins_installs_missing_profile_plugins
```

Result: 11 tests passed.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: 109 tests passed.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate independent-profile-homes --strict --no-interactive
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

Results:

- Python compile passed.
- Shell syntax checks passed.
- `independent-profile-homes` strict validation passed.
- Full OpenSpec strict validation passed 11 items.
- Release package generated `dist/codex-switch.tar.gz`.
- Diff whitespace check passed.

## Workstation Checks

Installed bundle refreshed:

```bash
./install.sh
```

Result:

```text
Installed codex-switch: /Users/cY/.local/bin/codex-switch -> /Users/cY/.local/share/codex-switch/current/scripts/codex-switch
```

Current internal home repaired for Pets support:

```text
/Users/cY/.codex-switch/homes/internal/pets -> /Users/cY/.codex/pets
```

Global Desktop settings safety check:

```text
global_state_exists: True
top_level_count: 13
atom_count: 60
denied_atom_keys_present: False
```

Plugins and Skills check:

```text
/Users/cY/.codex-switch/homes/internal/skills -> /Users/cY/.codex/skills
/Users/cY/.codex-switch/homes/internal/plugins is a profile-local directory
codex-switch --skip-self-update repair-plugins internal --dry-run:
No missing enabled plugins for internal
```

`codex-switch --skip-self-update verify internal --runtime-smoke --report`
passed runtime smoke but failed expected-active-profile assertions because the
active profile intentionally remained `openai-official`. The report path was
`/Users/cY/.codex-switch/verification/20260703T101005Z-internal.json`.

## Residual Risk

`plugins/` cache content is intentionally profile-local. Missing enabled
plugins should continue to be handled through `codex-switch repair-plugins
<profile>` rather than by copying another profile's cache.
