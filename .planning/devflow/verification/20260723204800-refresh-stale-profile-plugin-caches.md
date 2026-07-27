# Refresh Stale Profile Plugin Caches Verification

## Scope

- Change: `refresh-stale-profile-plugin-caches`
- Production target: `scripts/codex_switch_plugins.py`
- Test target: `scripts/test_codex_profile_switch.py`
- Excluded: live profile/cache mutation, project refresh, App lifecycle, install,
  release, Git effects, and archive

## Baseline and Planning

- `openspec status --change refresh-stale-profile-plugin-caches`: 4/4 artifacts
  complete
- `openspec validate refresh-stale-profile-plugin-caches --strict`: passed
- `check_dependencies.py --capability test-first-execution --json`: ready;
  required `tdd` skill verified
- `validate_workflow_state.py --json`: `ok: true`; existing read-only legacy
  DevFlow root-state warning only

## RED

Initial module-style selection without `PYTHONPATH=scripts` failed during test
import because this repository's test module imports sibling scripts as
top-level modules. The corrected focused command was:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_stale_local_plugin_cache \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_keeps_current_cache_with_runtime_residue \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_skips_uninspectable_installed_source \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_skips_catalog_source_manifest_version_mismatch \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_uses_canonical_binding_cli_and_home \
  test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_blocks_stale_refresh_for_running_target_app_server \
  test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_refreshes_stale_plugins_before_verification_and_doctor
```

Result: 7 tests, 5 expected failures and 2 expected errors.

- stale cache: no `--version` call and no `plugin add`
- current/residue cache: no current-cache classification
- uninspectable source: no truthful skip classification
- source manifest mismatch: no truthful skip classification
- canonical runtime: module has no `resolve_store_runtime_binding` integration
- running target app-server: module has no observation/safety integration
- one-key: repair reaches verification/Doctor without refreshing stale cache

No production file was edited before this RED result.

## GREEN

The focused repair group is GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest \
  -k repair_plugins test_codex_profile_switch.CodexProfileSwitchTests
```

Result: 13/13 passed. This covers missing, unavailable,
`--disable-unavailable`, dry-run, stale, current, runtime residue,
uninspectable sources, source-manifest mismatch, canonical binding, explicit
target home, active-runtime blocking, and project-state non-mutation.

The one-key ordering group is GREEN:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3 -m unittest \
  test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_repairs_plugins_before_doctor \
  test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_runs_verification_before_doctor \
  test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_unavailable_plugin_reaches_doctor_without_repair_failure \
  test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_refreshes_stale_plugins_before_verification_and_doctor
```

Result: 4/4 passed.

Legacy official one-key tests that verify update, login, Responses smoke, or
Doctor behavior now pass `--skip-plugin-repair`. Plugin integration tests use
the isolated internal canonical binding fixture, while official canonical
selection remains covered by an injected binding test. No test executes the
workstation ChatGPT CLI for plugin maintenance.

Final implementation review added two bounded safety guards:

- An exact target backend app-server path blocks stale replacement even when
  process environment or proxy-parent observation is unavailable. The focused
  RED failed because no `SwitchError` was raised and `plugin add` ran; GREEN
  blocks before the write.
- `os.walk` errors are propagated into the existing uninspectable result
  instead of being silently ignored. The focused RED observed no `onerror`
  callback; GREEN passes the raising callback.

The obsolete selector-only catalog reducer was removed after structured
catalog parsing became the sole owner.

## Final Verification

- Python 3.9.6:
  `PYTHONDONTWRITEBYTECODE=1 python3 scripts/test_codex_profile_switch.py`
  passed 138/138 in 91.452 seconds.
- Python 3.12.13:
  `PYTHONDONTWRITEBYTECODE=1 /opt/homebrew/bin/python3.12
  scripts/test_codex_profile_switch.py` passed 138/138 in 90.697 seconds.
- One earlier Python 3.12 broad run hit the existing auto-update/app-server
  smoke timing path once; the isolated test immediately passed and the fresh
  complete rerun passed 138/138.
- Python 3.9 and 3.12 `py_compile` passed for
  `codex_switch_plugins.py`, `codex_profile_switch.py`, and
  `test_codex_profile_switch.py`.
- `openspec validate refresh-stale-profile-plugin-caches --strict`: passed.
- `validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json`:
  `ok: true`; only the pre-existing legacy root-state read-only warning
  remains.
- `bash -n scripts/codex-switch`: passed.
- `git diff --check`: passed.

Stable source hashes at final verification:

- `scripts/codex_switch_plugins.py`:
  `9400137b8b578ceb529e57d677dd5076c164c73ed3c1ed58d2908b7af2af5be6`
- `scripts/test_codex_profile_switch.py`:
  `bd47db7bd9f67d9f5554fb6120b2ea2d3bc917e22792f7fc68697c80197ff8b4`

Changed files owned by this change:

- `scripts/codex_switch_plugins.py`
- plugin-focused sections of `scripts/test_codex_profile_switch.py`
- bounded help in `scripts/codex_profile_switch.py` and `scripts/codex-switch`
- bounded plugin-repair documentation in `README.md`
- `openspec/changes/refresh-stale-profile-plugin-caches/**`
- this verification receipt

No live profile, plugin cache, project workflow, App lifecycle, install,
release, Git, or archive mutation was performed.

## Residual Risks

- Remote or otherwise uninspectable catalog sources are intentionally reported
  and skipped; codex-switch does not guess their source tree.
- A confirmed stale cache with a matching running target app-server requires
  the operator to quit ChatGPT, rerun repair, and reopen the App.
- The verified source is not installed into the local codex-switch release, so
  the running App and installed CLI do not gain this behavior until a
  separately authorized install/release action and App restart.
- Project workflow-state migration remains separately authorized. The existing
  `.planning/STATE.md` stayed read-only, and no
  `.planning/devflow/STATE.md` was synthesized.
