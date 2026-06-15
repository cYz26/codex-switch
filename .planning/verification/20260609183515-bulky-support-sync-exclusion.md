# Verification: bulky support sync exclusion repair

## Context

User reported `codex-switch official` appearing stuck after the `== Switch ==`
section. Investigation found an unfinalized backup under
`~/.codex-switch/backups/20260609T102453Z-switch-internal-to-openai-official`
and unchanged `~/.codex-switch/active.json`, indicating the real switch did not
complete. The dry-run plan was classifying large or credential-like home entries
such as `agent-kb`, `plugins`, `computer-use`, `cache`, `model-catalogs`, and
`sqlite` as shareable support state. Real switches could then recursively copy
or back up those directories with no progress output.

## Changes Verified

- `codex_switch_home_sync.py` excludes bulky support, credential-like, model
  catalog, installation/version, vendor/update, cache, and sqlite directory
  state from shared support plans.
- `codex_switch_app_wrapper.py` applies the same exclusion rules when linking
  support entries into the internal Desktop home.
- Independent switch output now prints backup and mutation progress before the
  long-running sections.
- README and OpenSpec contract now document the exclusion behavior.

## Validation

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_official_switch_excludes_bulky_support_state_from_sync_plan CodexProfileSwitchTests.test_internal_desktop_wrapper_isolates_response_runtime_state
```

Result: 2 tests OK.

```bash
/Users/cY/dev/codex-switch/scripts/codex-switch official --dry-run --skip-update-check --skip-login --skip-doctor --no-status
```

Result: dry-run OK. The backup plan no longer includes `agent-kb`, `plugins`,
`computer-use`, `cache`, `model-catalogs`, or `sqlite` for the current local
profile-home bindings.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: 43 tests OK.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
openspec validate --all --strict --no-interactive
scripts/package-release.sh
git diff --check
```

Results:

- Python compile: passed.
- Shell syntax: passed.
- OpenSpec strict validation: 4 passed, 0 failed.
- Package release: wrote `dist/codex-switch.tar.gz`.
- `git diff --check`: passed.

## Residual Notes

- Archive remains closed by gate; this change was not archived.
- The user's interrupted switch left an unfinalized backup directory and partial
  managed official-home support copies. The active record still points to
  `internal`, so the profile was not switched at the time of inspection.
