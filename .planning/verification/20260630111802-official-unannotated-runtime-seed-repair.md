# Verification: official unannotated runtime seed repair

Timestamp: 2026-06-30T11:18:02+08:00

## Scope

Repaired the `codex-switch official` regression where an unannotated
`~/.codex/config.toml` matching the internal source home's model/provider seed
could be treated as the official profile's last runtime config. In that state,
switching to official rewrote the official runtime, profile layer, and canonical
profile config with internal Azure model/provider settings even though
`openai-official.config.toml` still contained clean official settings.

## Change

- Added `CodexProfileSwitchTests.test_official_switch_ignores_unannotated_internal_runtime_seed`.
- Extended the existing contaminated-runtime guard so `openai-official` skips a
  runtime seed when it has a provider, explicit profile layers have no provider,
  and the runtime profile seed matches the internal source home profile seed.
- Compared generated seeds after stripping codex-switch managed comments, so
  annotation-only differences do not prevent contamination detection.
- Recorded the behavior in the active OpenSpec scenario and task ledger.

## Red / Green Evidence

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_official_switch_ignores_unannotated_internal_runtime_seed
```

Result before fix: failed because official runtime kept
`model = "internal-model"` and `model_provider = "azure"`.

Result after fix: passed.

## Validation Commands

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_official_switch_ignores_unannotated_internal_runtime_seed \
  CodexProfileSwitchTests.test_official_switch_repairs_contaminated_managed_runtime_profile_seed \
  CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings \
  CodexProfileSwitchTests.test_switch_preserves_live_shared_preferences
```

Result: passed, 4 tests.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 88 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n install.sh
bash -n run.sh
git diff --check
```

Result: passed.

```bash
openspec validate independent-profile-homes --strict --no-interactive
openspec validate --all --strict --no-interactive
```

Result: passed. Full OpenSpec validation reported 9 passed, 0 failed.

```bash
scripts/package-release.sh
CODEX_SWITCH_TARBALL_URL="file:///Users/cY/dev/codex-switch/dist/codex-switch.tar.gz" ./install.sh
```

Result: package and local install passed.

## Live Workstation Repair

- Backed up the contaminated official profile layer and canonical profile config
  to `/Users/cY/.codex-switch/backups/20260630111802-pre-official-layer-repair/`.
- Restored `/Users/cY/.codex/openai-official.config.toml` and
  `/Users/cY/.codex-switch/profiles/openai-official/config.toml` from
  `/Users/cY/.codex-switch/backups/20260630T025400Z-switch-internal-to-openai-official/4-openai-official.config.toml`.
- Verified a real `codex-switch --skip-self-update official --skip-login --skip-update-check --skip-plugin-repair --skip-doctor --no-status` generated official runtime, layer, and canonical config with `model = "gpt-5.5"` and without `model_provider = "azure"`.
- Switched back with `codex-switch --skip-self-update internal --skip-update-check --skip-plugin-repair --skip-doctor --no-status`.
- Final `codex-switch --skip-self-update status` reported active profile
  `internal`, LaunchAgent `CODEX_CLI_PATH` set to
  `/Users/cY/.codex-switch/bin/codex-internal-app`, and the running Desktop
  app-server still using the managed internal proxy chain.

## Risks

- The current live Codex Desktop process remained running throughout the repair.
  Status now matches internal again, but a later switch to official still
  requires fully quitting and reopening Codex Desktop for the running app
  process to pick up official `CODEX_CLI_PATH`.
