# Version-Ordered Self-Update

## Scope

This verification covers the follow-up repair for `always-check-self-update`:
automatic release self-update must compare versions by ordering, not merely by
string inequality.

## Root Cause

The wrapper previously replaced the installed implementation whenever the
staged release bundle `VERSION` differed from the current installed `VERSION`.
That made local source installs fragile: a local development build could be
overwritten or downgraded by an older published release solely because the
strings were different.

## Implementation

- `sync_self_update` now replaces the current implementation only when the
  staged bundle version is newer than the current bundle version.
- Same-version and older-release checks remove the staged bundle and report the
  current implementation as already up to date.
- Prerelease ordering treats `0.1.13-dev` as newer than `0.1.12` but older
  than formal `0.1.13`, so a later real release can still take over.
- The temporary local-source marker path was removed from `install.sh` and
  `scripts/codex-switch`.
- The local checkout `VERSION` is now `0.1.13-dev`, which is higher than the
  currently published `0.1.12` release.

## RED Evidence

Before implementation:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_does_not_self_update_to_older_release \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_installer_preserves_local_source_version -v
```

Result: failed as expected. A local installed wrapper at `0.1.13-dev` was
overwritten by a remote release bundle at `0.1.12`.

## GREEN Evidence

After implementation:

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_does_not_self_update_to_older_release \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_self_updates_prerelease_to_formal_release \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_installer_preserves_local_source_version \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_self_updates_release_install_before_command \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_local_wrapper_self_update_reports_already_up_to_date -v
```

Result: passed, 5 tests.

## Installed Verification

```bash
CODEX_SWITCH_SOURCE_DIR=/Users/cY/dev/codex-switch ./install.sh
```

Result: installed `/Users/cY/.local/bin/codex-switch` to
`/Users/cY/.local/share/codex-switch/current/scripts/codex-switch`.

Ordinary command without `--skip-self-update`:

```bash
codex-switch check-update internal
```

Expected result after reinstall: the installed `codex-switch` implementation
remains local `0.1.13-dev`; the command reports internal Codex latest `0.142.5`
as blocked and keeps internal `0.142.4`.

Actual result:

```text
codex-switch self-update: checking latest release...
codex-switch self-update: already up to date 0.1.13-dev
Internal profile codex: /Users/cY/.local/bin/codex
Current: codex-cli 0.142.4
Latest release tag: internal-rust-v0.142.5
Latest release status: blocked by codex-switch policy
Blocked internal releases: 0.142.5
Pinned fallback version: 0.142.4
Update: skipped (latest 0.142.5 is blocked; keeping 0.142.4)
```

## Regression Suite

```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
```

Result: passed, 123 tests.

```bash
python3 -m py_compile scripts/*.py
bash -n install.sh
bash -n scripts/codex-switch
bash -n scripts/codex_env_setup
bash -n run.sh
```

Result: passed.

```bash
openspec validate always-check-self-update --strict --no-interactive
openspec validate internal-app-protocol-compat --strict --no-interactive
openspec validate --all --strict --no-interactive
```

Result: passed, 11 items.

```bash
git diff --check
scripts/package-release.sh
```

Result: passed, generated `/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz`.

## DevFlow Migration Check

```bash
python3 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/plugin_project_migration.py \
  --repo /Users/cY/dev/codex-switch --json
```

Result: `ok=true`, control plane `current`, status `migration_pending`.
Existing skill layout duplicate/conflict findings remain between
`.codex/skills` and `.agents/skills`; they were not introduced by this repair
and were left untouched.

## Current Workstation State

- Active profile was not switched by this verification and is expected to
  remain `openai-official`.
- Internal profile `codex_bin` and `app_cli_path` point to
  `/Users/cY/.local/bin/codex`.
- `/Users/cY/.local/bin/codex` reports `codex-cli 0.142.4`.
- `codex-switch check-update internal` should continue to report latest
  `0.142.5` as blocked and keep `0.142.4`.
