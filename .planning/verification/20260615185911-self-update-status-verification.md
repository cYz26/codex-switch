# Verification: self-update status output

Date: 2026-06-15

## Scope

Verify `self-update-status`, which adds visible status messages when a
release-installed `codex-switch` wrapper performs a due self-update check.

## Implementation Summary

- Added a check-start status line after self-update eligibility and interval
  gates pass.
- Added an already-up-to-date status line when the staged bundle version
  matches the current installed bundle version.
- Kept the existing synced-version line for successful updates.
- Kept skipped self-update invocations quiet.
- Documented the output contract in README, SKILL.md, OpenSpec change, and the
  stable spec.

## Commands And Results

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_local_wrapper_self_update_reports_already_up_to_date \
  CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command \
  CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install \
  CodexProfileSwitchTests.test_self_update_failure_does_not_block_local_command
```

Result: `Ran 4 tests`, `OK`.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: `Ran 61 tests in 17.373s`, `OK`.

```bash
python3 -m py_compile scripts/*.py
```

Result: exit 0.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: exit 0.

```bash
python3 -m json.tool evals/evals.json >/dev/null
```

Result: exit 0.

```bash
scripts/package-release.sh
```

Result: wrote `/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz` and exited
0.

```bash
git diff --check
```

Result: exit 0.

```bash
openspec validate self-update-status --strict --no-interactive
```

Result: `Change 'self-update-status' is valid`.

```bash
openspec validate --all --strict --no-interactive
```

Result: `Totals: 6 passed, 0 failed (6 items)`.

## Remaining Risk

This is a release-relevant CLI behavior change. Remote auto-release and
installed-command verification remain post-merge concerns after the change lands
on `main`.
