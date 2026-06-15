# Runtime Config Merge Follow-up Verification

Verified the `independent-profile-homes` follow-up for runtime-first config
merge behavior:

- Target profile runtime `config.toml` is preferred over canonical profile config
  when it is valid.
- Canonical profile config is used as fallback when target runtime config is
  missing or invalid.
- Canonical profile config is refreshed from validated runtime config without
  copying shared settings into canonical config.
- Generated runtime TOML includes managed `# codex-switch:` section comments for
  profile-specific and shared settings.
- Python 3.9 fallback TOML validation catches merge-damaging syntax errors when
  `tomllib` is unavailable.

## Commands

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_prefers_last_runtime_config_and_refreshes_canonical \
  CodexProfileSwitchTests.test_internal_switch_falls_back_to_canonical_when_last_runtime_config_is_invalid \
  CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings
```

Result: passed, 3 tests OK.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 37 tests OK.

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: passed.

```bash
openspec validate --all --strict --no-interactive
```

Result: passed, 4 items OK.

```bash
scripts/package-release.sh
```

Result: passed; wrote `dist/codex-switch.tar.gz`.

```bash
tar -tzf dist/codex-switch.tar.gz | rg '(^codex-switch/scripts/codex_switch_home_sync.py$|^codex-switch/scripts/codex_switch_restore.py$|^codex-switch/scripts/codex_switch_toml_validate.py$|^codex-switch/scripts/codex-switch$)'
```

Result: passed; packaged tarball includes the switch command, restore module,
home sync module, and TOML validator.

```bash
git diff --check
```

Result: passed.

## Workflow Notes

- `scripts/validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json`
  is unavailable in this checkout (`scripts/validate_workflow_state.py` does not
  exist).
- Archive remains closed by DevFlow gate; this change was not archived.

## Remaining Risks

- The basic TOML validator is intentionally conservative and supplements
  `tomllib` only when Python is older than 3.11. If Codex starts writing a TOML
  shape it rejects, add a regression case and narrow that validator.
- Live Codex Desktop behavior is covered by wrapper/LaunchAgent tests with fake
  binaries; no live Desktop process was launched.
