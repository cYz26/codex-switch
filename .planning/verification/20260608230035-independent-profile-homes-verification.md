# independent-profile-homes Verification

Verified the independent official/internal home switching change:

- `official` activates against the official Codex home.
- `internal` activates against `~/.codex-switch/homes/internal` by default.
- Non-dry-run switches create a backup manifest before mutation.
- `restore <backup-id> --dry-run|--apply` restores backup entries with post-switch state checks.
- Auth, runtime state, and profile-specific model/provider layers are excluded from cross-home sharing.

## Commands

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: passed, 34 tests OK.

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
scripts/package-release.sh && test -x dist/run.sh && test -x dist/codex-switch/run.sh && tar -tzf dist/codex-switch.tar.gz | rg '(^codex-switch/scripts/codex_switch_home_sync.py$|^codex-switch/scripts/codex_switch_restore.py$|^codex-switch/scripts/codex-switch$)'
```

Result: passed; release tarball includes the new modules and wrapper.

```bash
git diff --check
```

Result: passed.

## Remaining Risks

- Live Codex Desktop behavior is covered by wrapper/LaunchAgent tests with fake binaries; no live Desktop process was launched.
- Backup retention remains intentionally out of scope.
