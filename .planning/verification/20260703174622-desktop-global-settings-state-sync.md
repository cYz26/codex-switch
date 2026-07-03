# Desktop Global Settings State Sync

Date: 2026-07-03

OpenSpec change: `independent-profile-homes`

## Root Cause

`config.toml` shared settings were already syncing between official and
internal homes. The missing settings were Desktop/Electron state stored in
`.codex-global-state.json`. That file was correctly excluded from generic
cross-home sync with credentials and runtime state, but the exclusion also
prevented safe UI/settings values from following the internal profile.

## Repair

- Keep `.codex-global-state.json` excluded from generic shared-support copy and
  link plans.
- Add a sanitized Desktop global-state merge helper that copies allowlisted
  top-level Desktop settings and allowlisted `electron-persisted-atom-state`
  keys only.
- Preserve profile-local prompt history, thread permissions, prompt drafts,
  queued follow-ups, remote thread summaries, unread-thread state, remote
  routing identifiers, and credentials.
- Call the helper from independent switch flows and from the generated internal
  Desktop wrapper.
- Update README and the `independent-profile-homes` OpenSpec design/spec/tasks.

## Red Evidence

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_desktop_global_settings_state_sync_merges_safe_settings_only \
  CodexProfileSwitchTests.test_switch_syncs_desktop_global_settings_state_between_independent_homes \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_desktop_global_settings_state
```

Before implementation this failed because:

- `merge_desktop_global_state_settings` did not exist.
- `switch internal` did not create the target
  `.codex-global-state.json`.
- The internal Desktop wrapper left stale app-home Desktop settings unchanged.

## Green Evidence

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_desktop_global_settings_state_sync_merges_safe_settings_only \
  CodexProfileSwitchTests.test_switch_syncs_desktop_global_settings_state_between_independent_homes \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_desktop_global_settings_state
```

Result: 3 tests passed.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_excludes_bulky_support_state_from_sync_plan \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state \
  CodexProfileSwitchTests.test_official_switch_syncs_shared_state_back_without_internal_runtime \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_preserves_official_personality \
  CodexProfileSwitchTests.test_desktop_global_settings_state_sync_merges_safe_settings_only \
  CodexProfileSwitchTests.test_switch_syncs_desktop_global_settings_state_between_independent_homes \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_syncs_desktop_global_settings_state
```

Result: 9 tests passed.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: 107 tests passed.

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
- `independent-profile-homes` OpenSpec validation passed.
- Full OpenSpec strict validation passed 11 items.
- Release package generated `dist/codex-switch.tar.gz`.
- Diff whitespace check passed.

## Workstation Repair

Installed bundle refreshed:

```bash
./install.sh
```

Result:

```text
Installed codex-switch: /Users/cY/.local/bin/codex-switch -> /Users/cY/.local/share/codex-switch/current/scripts/codex-switch
```

Current workstation internal home repaired without switching profiles:

```bash
PYTHONPATH=/Users/cY/dev/codex-switch/scripts python3 - <<'PY'
from pathlib import Path
from codex_switch_home_sync import sync_desktop_global_state_settings
source = Path('/Users/cY/.codex')
target = Path('/Users/cY/.codex-switch/homes/internal')
print(sync_desktop_global_state_settings(source, target))
PY
```

Result:

```text
/Users/cY/.codex-switch/homes/internal/.codex-global-state.json
```

Key-only safety check showed top-level settings keys and 60 allowed atom keys,
with no copied `prompt-history`, `heartbeat-thread-permissions-by-id`,
`composer-prompt-drafts-v1`, `unread-thread-ids-by-host-v1`,
`remote-thread-summaries:*`, or `thread-client-id-v1:*` atom keys.

`codex-switch --skip-self-update status` confirmed the active profile remained
`openai-official`; no profile switch was performed during the workstation
repair.

## Residual Risk

The atom-state allowlist intentionally favors known Desktop UI/settings keys.
If future Desktop builds introduce new settings keys inside
`electron-persisted-atom-state`, those keys may need to be added after local
inspection. This is safer than copying unknown thread/session state.
