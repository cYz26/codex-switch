# Verification: Plugin catalog refresh repair

Timestamp: 2026-06-24T18:21:47+08:00

## Scope

- Extended `codex-switch repair-plugins <profile>` so it refreshes the target
  profile's plugin marketplace/catalog view before checking missing enabled
  plugins.
- The repair now runs the profile's configured Codex binary with
  `CODEX_HOME` set to the profile home for:
  - `codex plugin marketplace upgrade --json`
  - `codex plugin list --available --json`
  - `codex plugin add <selector>` for missing enabled plugins
- Preserved the independent-home boundary: `plugins/` remains profile-local and
  is not copied or symlinked between profiles.
- Added regression coverage for both missing enabled plugins and the
  already-installed state, so available catalog priming cannot be skipped by an
  early return.

## Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_before_installing_missing_profile_plugins \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_when_enabled_plugins_are_installed
```

Initial result: failed as expected before implementation. The existing repair
only called `plugin add` when an enabled plugin was missing and returned early
without invoking Codex CLI when enabled plugins were already installed.

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_before_installing_missing_profile_plugins \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_when_enabled_plugins_are_installed
```

Result after implementation: pass, 2 tests.

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_doctor_reports_missing_active_profile_enabled_plugin_cache \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_doctor_accepts_active_profile_enabled_plugin_cache \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_installs_missing_profile_plugins \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_before_installing_missing_profile_plugins \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_when_enabled_plugins_are_installed \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_repairs_plugins_before_doctor \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_can_skip_plugin_repair
```

Result: pass, 7 tests.

```bash
PYTHONPATH=scripts python3 scripts/test_codex_profile_switch.py
```

Result: pass, 78 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
openspec validate independent-profile-homes --strict --no-interactive
git diff --check
```

Result: all pass. OpenSpec reported `Change 'independent-profile-homes' is valid`.

## Residual

- This change does not share, copy, or symlink another profile's `plugins/`
  directory. Installed plugin caches remain profile-local.
- `repair-plugins` now depends on the selected profile's Codex CLI supporting
  `plugin marketplace upgrade --json` and `plugin list --available --json`.
- A real Desktop UI refresh may still require quitting and reopening Codex
  Desktop if it already has stale plugin-list state in memory.
- Archive remains unavailable because the archive gate is closed.
