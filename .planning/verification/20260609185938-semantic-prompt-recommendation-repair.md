# Verification: semantic prompt recommendation repair

## Context

User reported that the `openai-official` home prompt should recommend
`~/.codex`, while `internal` should recommend its managed home under
`~/.codex-switch/homes/`. The previous prompt implementation recommended the
currently resolved manifest value, which could make an auto-migrated or
unconfirmed `openai-official` binding under `homes/openai-official` appear as
the recommended choice.

## Changes Verified

- Prompt recommendations now come from profile semantics:
  - `openai-official` recommends the official home, defaulting to `~/.codex`.
  - `internal` recommends the managed internal home, defaulting to
    `~/.codex-switch/homes/internal`.
- The currently resolved manifest value remains available as a choice, but no
  longer overrides the semantic default.
- If the semantic default is forbidden by an active-profile conflict, the prompt
  still recommends a safe alternate directory first.
- README and OpenSpec now document the recommendation contract.

## Validation

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_interactive_prompt_prefers_semantic_default_for_unconfirmed_internal_home \
  CodexProfileSwitchTests.test_interactive_prompt_prefers_official_home_for_unconfirmed_official_home \
  CodexProfileSwitchTests.test_interactive_profile_change_prompts_target_away_from_active_home \
  CodexProfileSwitchTests.test_interactive_home_prompt_prioritizes_target_profile_and_recommended_option
```

Result: 4 tests OK.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: 46 tests OK.

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
