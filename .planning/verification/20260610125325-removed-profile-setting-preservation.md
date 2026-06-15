# Verification: removed profile setting preservation

## Scope

After fixing official Desktop personality preservation, I audited related
profile/config merge paths for the same failure pattern: old profile-specific
settings being reintroduced while syncing or refreshing config files.

## Findings

- The internal Desktop wrapper foldback path now preserves official runtime
  profile settings while overlaying only shared app-home settings.
- The remaining risky path was canonical profile refresh. It used the old
  canonical fallback to fill every missing profile-specific key, which could
  resurrect removed optional settings such as `personality` or
  `model_provider`.
- Legacy shared-config switching still intentionally writes shared-only
  `config.toml` plus a separate `<profile>.config.toml`; that is the legacy
  model and not the independent-home runtime merge path.

## Change

- Added `test_canonical_refresh_does_not_resurrect_removed_profile_settings`.
- Limited canonical refresh fallback filling to `cli_auth_credentials_store`,
  preserving structural auth metadata while respecting removals of optional
  runtime profile settings.
- Updated OpenSpec, README, tasks ledger, and workflow state with the removal
  preservation contract.

## Red / Green Evidence

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_canonical_refresh_does_not_resurrect_removed_profile_settings
```

Result before fix: failed because `model_provider = "old-provider"` and
`personality = "pragmatic"` were copied from the old canonical fallback into
the refreshed canonical profile config.

Result after fix: passed.

Focused adjacent check:

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_canonical_refresh_does_not_resurrect_removed_profile_settings CodexProfileSwitchTests.test_internal_switch_prefers_last_runtime_config_and_refreshes_canonical CodexProfileSwitchTests.test_official_switch_preserves_last_official_runtime_profile_settings CodexProfileSwitchTests.test_switch_preserves_live_shared_preferences
```

Result: passed, 4 tests.

## Validation Commands

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 52 tests.

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
bash -n scripts/codex-switch && if [ -f scripts/codex_env_setup ]; then bash -n scripts/codex_env_setup; fi && bash -n install.sh && bash -n run.sh
```

Result: passed.

```bash
openspec validate --all --strict --no-interactive
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

## Risks

- No live Codex Desktop process was launched; wrapper behavior is covered by
  generated-wrapper tests with fake Codex binaries.
- Archive remains closed by gate.
