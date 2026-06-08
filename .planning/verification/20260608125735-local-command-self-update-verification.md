# Verification: local-command-self-update

## Metadata

- Change: `local-command-self-update`
- Recorded at: 2026-06-08T12:57:35+08:00
- Result: passed

## Commands

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install CodexProfileSwitchTests.test_remote_runner_downloads_release_and_execs_command
```

Initial TDD result: failed before implementation.

```text
FAILED (failures=2, errors=1)
```

```bash
python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command CodexProfileSwitchTests.test_local_wrapper_skip_self_update_keeps_existing_install CodexProfileSwitchTests.test_source_checkout_wrapper_does_not_self_update CodexProfileSwitchTests.test_self_update_failure_does_not_block_local_command CodexProfileSwitchTests.test_remote_runner_downloads_release_and_execs_command
```

Result: passed.

```text
.....
----------------------------------------------------------------------
Ran 5 tests in 1.102s

OK
```

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed.

```text
..........................
----------------------------------------------------------------------
Ran 26 tests in 8.084s

OK
```

```bash
python3 -m py_compile scripts/*.py
```

Result: passed.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: passed.

```bash
openspec validate local-command-self-update --strict --json && openspec validate --all --strict --json
```

Result: passed. Summary after implementation: `local-command-self-update` valid, 2 stable specs valid, 1 active change valid, 0 failed.

```bash
scripts/package-release.sh && test -x dist/run.sh && test -x dist/codex-switch/run.sh && tar -tzf dist/codex-switch.tar.gz | rg '(^codex-switch/run.sh$|^codex-switch/scripts/codex-switch$|^codex-switch/scripts/test_codex_profile_switch.py$)'
```

Result: passed.

```text
/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz
codex-switch/run.sh
codex-switch/scripts/test_codex_profile_switch.py
codex-switch/scripts/codex-switch
```

```bash
git diff --check
```

Result: passed.

```bash
openspec archive local-command-self-update --skip-specs -y
```

Result: passed. Change archived as `2026-06-08-local-command-self-update`.

```bash
openspec validate --all --strict --json
```

Post-archive result: passed. Summary: 2 stable specs passed, 0 active changes,
0 failed.

```bash
openspec list
```

Post-archive result: `No active changes found.`

## Evidence Summary

- Local release-installed wrapper self-update: covered and passing.
- Skip controls: `--skip-self-update` covered and passing.
- Source checkout safety: covered and passing.
- Non-blocking sync failure: covered and passing.
- Remote runner redundant self-update skip: covered and passing.
- Release package rebuilt and contains updated wrapper and runner.
- OpenSpec change archived after verification, with stable spec already updated.

## Risks

- The self-update check relies on release tarball availability. Failures are
  intentionally non-blocking and only warn, so users may continue on an older
  implementation until the next successful check.
- Auto-sync is version-based. Re-publishing a release asset with the same
  `VERSION` is not treated as a newer bundle.
