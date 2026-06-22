# Verification: always-check-self-update

Date: 2026-06-22

## Scope

Verify `always-check-self-update`, which removes the local wrapper self-update
cooldown so every ordinary release-installed `codex-switch` invocation checks
whether the implementation needs to sync.

## Implementation Summary

- Added a regression test that invokes a same-version release-installed wrapper
  twice and requires self-update status on both invocations.
- Removed the Bash wrapper's interval/stamp gate and no longer writes
  `.last-self-update-check`.
- Kept explicit skip controls, source checkout safety, non-blocking failure
  behavior, and re-exec loop prevention unchanged.
- Updated README, SKILL.md, the stable OpenSpec spec, the new change artifacts,
  and stale interval wording in `self-update-status`.

## RED Evidence

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_self_update_checks_every_invocation
```

Result before implementation: failed as expected. The second invocation had
empty stderr, so it did not report `codex-switch self-update: checking latest
release`.

## Commands And Results

```bash
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_local_wrapper_self_update_checks_every_invocation \
  CodexProfileSwitchTests.test_local_wrapper_self_update_reports_already_up_to_date \
  CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command \
  CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install \
  CodexProfileSwitchTests.test_source_checkout_wrapper_does_not_self_update
```

Result: `Ran 5 tests`, `OK`.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: `Ran 66 tests in 18.116s`, `OK`.

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
openspec validate always-check-self-update --strict --no-interactive && openspec validate self-update-status --strict --no-interactive && openspec validate --all --strict --no-interactive
```

Result: `Change 'always-check-self-update' is valid`, `Change
'self-update-status' is valid`, `Totals: 9 passed, 0 failed (9 items)`.

```bash
scripts/package-release.sh
```

Result: wrote `/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz` and exited
0.

```bash
git diff --check
```

Result: exit 0.

## Local Install Refresh

```bash
scripts/package-release.sh
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch/dist/codex-switch ./install.sh
```

Result: installed `/Users/cY/.local/bin/codex-switch` to
`/Users/cY/.local/share/codex-switch/current/scripts/codex-switch`, version
`0.1.7`.

```bash
rg -n "SELF_UPDATE_INTERVAL|self_update_interval_due|last-self-update|checking latest release|already up to date" ~/.local/share/codex-switch/current/scripts/codex-switch
```

Result: the installed wrapper only contains the check-start and already-current
status lines; no interval or stamp gate remains.

```bash
for i in 1 2; do echo "run $i"; codex-switch status 2>&1 | sed -n '/codex-switch self-update/p'; done
```

Result: both runs printed `codex-switch self-update: checking latest release...`
and `codex-switch self-update: already up to date 0.1.7`.

## Remaining Risk

Every ordinary release-installed invocation now performs a release-source check,
so command startup may pay network cost more often than before. Explicit skip
controls remain available for scripts or offline runs.
