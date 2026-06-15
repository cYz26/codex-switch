# Verification: invalid reasoning effort runtime guard

## Scope

Fix the managed internal home config merge path so a valid TOML runtime config
cannot keep an unsupported `model_reasoning_effort` such as `max` when the
configured model catalog declares the selected model only supports
`low`, `medium`, `high`, and `xhigh`.

## Root Cause

`build_internal_home_config` preferred the target profile's last valid runtime
`config.toml` whenever TOML parsing succeeded. That preserved legitimate
runtime profile edits, but it also treated semantically unsupported settings as
valid. After the Codex App UI wrote `model_reasoning_effort = "max"` into the
managed internal home, the next runtime config rebuild kept `max` instead of
falling back to the canonical internal profile's supported `xhigh`.

## Change

- Added a regression test for a runtime seed with `model_reasoning_effort =
  "max"` and a model catalog that supports only `low`, `medium`, `high`, and
  `xhigh`.
- Added catalog-aware seed validation in `scripts/codex_switch_home_sync.py`.
  When `model`, `model_catalog_json`, and `model_reasoning_effort` are present
  and the catalog explicitly lists supported reasoning levels for the model,
  unsupported runtime efforts are rejected and the canonical profile seed is
  used instead.
- Kept runtime-first behavior unchanged when no catalog, no matching model, or
  no supported reasoning level metadata is available.
- Regenerated the local active internal home config from the fixed source; the
  live managed config now contains `model_reasoning_effort = "xhigh"`.

## Red / Green Evidence

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_internal_switch_falls_back_when_runtime_reasoning_effort_is_unsupported
```

Result before fix: failed because the generated runtime config still contained
`model_reasoning_effort = "max"`.

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_falls_back_when_runtime_reasoning_effort_is_unsupported \
  CodexProfileSwitchTests.test_internal_switch_prefers_last_runtime_config_and_refreshes_canonical \
  CodexProfileSwitchTests.test_internal_switch_falls_back_to_canonical_when_last_runtime_config_is_invalid \
  CodexProfileSwitchTests.test_canonical_refresh_does_not_resurrect_removed_profile_settings
```

Result after fix: passed, 4 tests.

## Validation Commands

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 53 tests.

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: passed.

```bash
openspec validate --all --strict --json
```

Result: passed, 4 items.

```bash
scripts/package-release.sh
```

Result: passed, wrote `dist/codex-switch.tar.gz`.

```bash
git diff --check
```

Result: passed.

## Fresh Verification 2026-06-10T22:55:11+0800

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 53 tests in 15.621s.

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
openspec validate --all --strict --json
```

Result: passed, 4 items.

```bash
git diff --check
```

Result: passed.

```bash
CODEX_SWITCH_SKIP_SELF_UPDATE=1 scripts/codex-switch internal --skip-update-check --skip-doctor --no-status --skip-launchctl --skip-login
```

Result: passed, regenerated `/Users/cY/.codex-switch/homes/internal/config.toml`.

```bash
rg -n 'model_reasoning_effort\s*=\s*"(max|xhigh)"' \
  /Users/cY/.codex-switch/homes/internal/config.toml \
  /Users/cY/.codex-switch/profiles/internal/config.toml
```

Result: both files report `model_reasoning_effort = "xhigh"` and no `max`.

## Notes

- `plugin_project_migration.py --repo /Users/cY/dev/codex-switch --json`
  still reports stale project-local DevFlow skill symlinks. I did not apply the
  migration because apply mode is a separate project-local mutation.
- `codex-switch doctor` still reports that the already-running Desktop
  app-server command path is `/Users/cY/.local/bin/codex` instead of the wrapper.
  The active process environment already has `CODEX_HOME` and `CODEX_CLI_PATH`
  set for internal, and the generated config has been repaired. Quit and reopen
  Codex Desktop to force a fresh app-server process and UI reload.
- Archive remains closed by gate.
