# Interactive Home Prompt Refinement Verification

Verified the `independent-profile-homes` follow-up for interactive home
selection:

- Interactive prompts ask for the target profile before the other independent
  profile.
- Prompt choices list the recommended home first and mark it as recommended.
- The other profile's current home remains available as the second normal
  choice when it is distinct.
- If independent profiles resolve to the same home in an interactive run, the
  switch prints a collision explanation and prompts for a different home instead
  of exiting immediately.
- Non-interactive same-home collisions still fail before mutation.

## Commands

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_interactive_home_prompt_prioritizes_target_profile_and_recommended_option \
  CodexProfileSwitchTests.test_interactive_same_home_collision_prompts_for_other_profile_home
```

Result: passed, 2 tests OK.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 42 tests OK.

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
git diff --check
```

Result: passed.

## Workflow Notes

- `scripts/validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json`
  is unavailable in this checkout (`scripts/validate_workflow_state.py` does not
  exist).
- Archive remains closed by DevFlow gate; this change was not archived.

## Remaining Risks

- Automated prompt tests use `CODEX_SWITCH_FORCE_HOME_PROMPT=1` with piped input
  rather than a real terminal session.
- Live Codex Desktop behavior is covered by wrapper/LaunchAgent tests with fake
  binaries; no live Desktop process was launched.
