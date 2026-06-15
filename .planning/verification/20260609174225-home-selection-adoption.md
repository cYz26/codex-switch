# Home Selection and Adoption Verification

Verified the `independent-profile-homes` follow-up for profile home
selection/adoption:

- `--internal-codex-home <path>` lets `internal` adopt an existing Codex home.
- When `internal` adopts the previous official home and official was not
  explicitly locked to that same path, `openai-official` is assigned a distinct
  managed home under the switch store.
- Profile home bindings are persisted in `profiles/<profile>/manifest.json`.
- Explicit identical official/internal homes are rejected before mutation.
- Wrapper commands forward `--internal-codex-home` through to the Python switcher.
- TTY switches can prompt for existing-home, managed-home, or custom-path
  choices when a profile has no persisted binding and no CLI path was provided.

## Commands

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_internal_switch_can_adopt_live_home_and_move_official_home \
  CodexProfileSwitchTests.test_switch_rejects_explicit_identical_independent_homes \
  CodexProfileSwitchTests.test_wrapper_forwards_internal_codex_home_option
```

Result: passed, 3 tests OK.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 40 tests OK.

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

- Interactive home selection is covered by resolver structure and command
  parsing; automated tests cover explicit adoption and collision behavior rather
  than a real TTY session.
- Live Codex Desktop behavior is covered by wrapper/LaunchAgent tests with fake
  binaries; no live Desktop process was launched.
