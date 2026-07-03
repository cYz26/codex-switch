# Switch Shell Bootstrap Alignment

## Summary

Profile switches now maintain command-line Codex alignment in the same managed
flow as Desktop/App alignment. When a switch updates the codex-switch CLI shim,
it also installs or refreshes a marker-managed shell startup block that prepends
the store `bin` directory to PATH and clears the shell command lookup cache.

This intentionally does not overwrite arbitrary existing `codex` binaries on
PATH. A child `codex-switch` process cannot mutate an already-running parent
shell's in-memory PATH, so current-shell drift remains visible in status; new
shells inherit the managed bootstrap after the next switch.

## Red Evidence

Before implementation, focused tests failed as expected:

```text
FAIL: test_switch_installs_shell_bootstrap_for_cli_alignment
AssertionError: 'Shell CLI bootstrap:' not found

FAIL: test_switch_replaces_existing_shell_bootstrap_without_duplication
AssertionError: '/old/codex-switch/bin' unexpectedly found
```

The explicit opt-out test already passed because no bootstrap behavior existed.

## Validation Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_switch_installs_shell_bootstrap_for_cli_alignment \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_switch_replaces_existing_shell_bootstrap_without_duplication \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_switch_can_skip_shell_bootstrap
```

Result: pass, 3 tests.

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_status_reports_shell_codex_alignment \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_internal_update_check_skips_blocked_latest_on_fallback \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_pins_blocked_current_to_fallback \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_internal_auto_update_resumes_for_successor_latest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_update_internal_command_pins_blocked_latest_without_explicit_version
```

Result: pass, 5 tests.

```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
```

Result: pass, 117 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n scripts/codex-switch scripts/codex_env_setup
git diff --check
openspec validate internal-app-protocol-compat --strict --no-interactive
openspec validate --all --strict --no-interactive
```

Results: pass. OpenSpec validated all 11 items.

## Packaging And Installed Checks

```bash
scripts/package-release.sh
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
```

Results: package generated
`/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz`; installed
`/Users/cY/.local/bin/codex-switch ->
/Users/cY/.local/share/codex-switch/current/scripts/codex-switch`.

```bash
codex-switch --skip-self-update shim-env
```

Result:

```text
export PATH="/Users/cY/.codex-switch/bin:$PATH"
hash -r 2>/dev/null || true
```

```bash
CODEX_SWITCH_SHELL_PROFILE=/tmp/codex-switch-shell-bootstrap-check.zshrc \
  codex-switch --skip-self-update switch openai-official --dry-run --skip-launchctl |
  rg 'command-line codex PATH bootstrap|/tmp/codex-switch-shell-bootstrap-check.zshrc'
```

Result:

```text
- /tmp/codex-switch-shell-bootstrap-check.zshrc
- ensure command-line codex PATH bootstrap: /tmp/codex-switch-shell-bootstrap-check.zshrc
```

```bash
codex-switch --skip-self-update status | rg 'PATH codex|Switch shim|PATH codex alignment|Shell CLI'
```

Result: current already-open shell still resolves bare `codex` to the stale
plugin-appserver path and status reports the mismatch plus remediation:

```text
PATH codex: /Users/cY/.codex-switch/homes/internal/plugins/.plugin-appserver/codex
PATH codex version: codex-cli 0.142.5
Switch shim: /Users/cY/.codex-switch/bin/codex
PATH codex alignment: mismatch (expected switch shim /Users/cY/.codex-switch/bin/codex)
PATH codex remediation: eval "$(codex-switch shim-env)"
```

## Notes

- No real workstation profile switch was run for this verification; active
  profile remains `openai-official`.
- The next real switch that updates the command-line shim will install or
  refresh the managed shell bootstrap in the selected shell profile.
- Use `CODEX_SWITCH_SKIP_SHELL_BOOTSTRAP=1` to skip shell startup mutation in
  controlled environments.
- Archive remains closed by DevFlow gate and was not attempted.
