# Verification: desktop wrapper runtime config comments

## Context

User reported that `config.toml` did not show section markers for shared and
profile-specific settings. Investigation found that normal `switch internal`
generation already wrote managed `# codex-switch:` comments, but the internal
Desktop wrapper rewrote the internal home config through an older unannotated
merge helper when the app launched.

## Changes Verified

- The Desktop wrapper now rebuilds the internal app/home runtime config through
  the same internal runtime config merge path used by profile switching.
- Wrapper-generated internal config keeps:
  - `# codex-switch: managed runtime config for profile internal`
  - `# codex-switch: profile-specific settings`
  - `# codex-switch: shared settings`
- Shared app-home edits are still folded back into the shared base config before
  the annotated runtime config is regenerated.

## Validation

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config
```

Result before fix: failed because the wrapper-generated config lacked
`# codex-switch: managed runtime config for profile internal`.

Result after fix: 1 test OK.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_desktop_wrapper_persists_app_home_plugin_state \
  CodexProfileSwitchTests.test_internal_switch_refreshes_desktop_wrapper_with_shared_config \
  CodexProfileSwitchTests.test_internal_switch_prefers_last_runtime_config_and_refreshes_canonical \
  CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings
```

Result: 4 tests OK.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: 46 tests OK.

```bash
python3 -m py_compile scripts/codex_switch_app_wrapper.py scripts/codex_switch_home_sync.py scripts/codex_switch_config.py scripts/test_codex_profile_switch.py
bash -n scripts/codex-switch && bash -n install.sh && git diff --check
```

Results:

- Python compile: passed.
- Shell syntax: passed.
- `git diff --check`: passed.

## Residual Notes

- Existing live/generated wrappers are refreshed by a subsequent internal
  switch or wrapper regeneration path; the source fix prevents future wrapper
  rewrites from dropping the managed section comments.
- Archive remains closed by gate; this change was not archived.
