# Verification: active-home-aware prompt repair

## Context

User reported that running `codex-switch` did not prompt for profile home
selection. Local inspection showed both profile manifests already contained
`codex_home` values, so the previous logic treated them as configured and did
not prompt. The manifests did not distinguish user-confirmed selections from
automatic migration/collision bindings. The user also required that switching
to a different profile must not let the target profile reuse the current active
profile's Codex home.

## Changes Verified

- Home bindings loaded from a manifest are now classified as confirmed only when
  `home_selection_confirmed` is true.
- Interactive switches prompt to confirm unconfirmed manifest home bindings and
  persist the selected binding with `home_selection_confirmed`.
- When switching to a different target profile, the target profile's home is
  checked against the current active profile's recorded `codex_home`.
- Interactive switches prompt for a different target-profile home when it would
  reuse the active profile home.
- Non-interactive real switches fail before mutation for the same active-home
  conflict. Dry-runs remain read-only and non-prompting.

## Validation

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_interactive_prompt_confirms_legacy_manifest_home_binding \
  CodexProfileSwitchTests.test_interactive_profile_change_prompts_target_away_from_active_home
```

Result: 2 tests OK.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: 45 tests OK.

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
