# Verification: Plugin repair hardening

Timestamp: 2026-06-24T19:38:41+08:00

## Scope

- Made one-key `codex-switch internal --help` and
  `codex-switch official --help` side-effect free.
- Hardened `repair-plugins <profile>` so missing enabled plugins are installed
  only when they appear in the refreshed available plugin catalog.
- Unavailable enabled plugins are skipped by repair and left for
  `codex-switch doctor` to report as active-profile materialization issues.
- Updated `repair-plugins --dry-run` to avoid printing unverified
  `codex plugin add` commands before the available catalog is actually
  refreshed.

## Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_dry_run_does_not_claim_unverified_plugin_add \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_help_is_pure_help \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_skips_unavailable_enabled_plugins_after_catalog_refresh \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_unavailable_plugin_reaches_doctor_without_repair_failure \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_before_installing_missing_profile_plugins \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_repairs_plugins_before_doctor \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_repair_plugins_refreshes_available_catalog_when_enabled_plugins_are_installed \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_wrapper_one_key_can_skip_plugin_repair
```

Result: pass, 8 tests.

```bash
PYTHONPATH=scripts python3 scripts/test_codex_profile_switch.py
```

Result: pass, 82 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict
git diff --check
scripts/package-release.sh
```

Result: all pass. Release bundle generated at `dist/codex-switch.tar.gz`.

```bash
scripts/codex-switch internal --help
scripts/codex-switch official --help
scripts/codex-switch repair-plugins internal --dry-run
scripts/codex-switch repair-plugins openai-official --dry-run
codex-switch --skip-self-update status
```

Result:

- Help commands printed usage only; no dry-run, switch, update, plugin repair,
  doctor, or status sections appeared.
- `repair-plugins --dry-run` printed marketplace/catalog refresh commands and
  `would install if available` messages, not concrete `plugin add` commands.
- Active profile remained `openai-official`; active `CODEX_HOME` remained
  `/Users/cY/.codex`; Codex Desktop and app-server still point to the official
  app bundle.

```bash
CODEX_SWITCH_TARBALL_URL="file:///Users/cY/dev/codex-switch/dist/codex-switch.tar.gz" ./install.sh
codex-switch --skip-self-update internal --help
codex-switch --skip-self-update official --help
codex-switch --skip-self-update repair-plugins internal --dry-run
codex-switch --skip-self-update repair-plugins openai-official --dry-run
codex-switch --skip-self-update status
codex-switch --skip-self-update version
```

Result:

- The generated local release bundle was explicitly installed to
  `/Users/cY/.local/share/codex-switch/current`.
- Installed `codex-switch` reports version `0.1.9`.
- Installed one-key help commands remain side-effect free.
- Installed repair dry-run uses the catalog-aware `would install if available`
  output.
- Active profile remained `openai-official`.

## Residual

- `repair-plugins` still does not delete orphaned plugin caches and does not
  copy or symlink another profile's `plugins/` directory.
- Archive remains unavailable because the archive gate is closed.
