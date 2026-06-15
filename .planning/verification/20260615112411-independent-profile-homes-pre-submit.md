# Verification: independent profile homes pre-submit

Date: 2026-06-15

## Scope

Pre-submit verification for the `independent-profile-homes` change before
committing and pushing the current branch.

## Submission Scope

- Independent official/internal Codex homes and persisted home bindings.
- Shared support sync exclusions and symlink-loop prevention.
- Backup-gated switching and explicit restore support.
- Runtime-first config merge with canonical fallback.
- Internal Desktop app-server model alias proxy for versioned deployment models.
- README, OpenSpec change artifacts, workflow state, and verification records.

Two untracked root-level minified JavaScript bundles,
`src-BZqs_tzA.js` and `src-GT0gjTeg.js`, were excluded and removed as
unreferenced generated artifacts.

## Commands And Results

```bash
python3 /Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038/scripts/plugin_project_migration.py --repo /Users/cY/dev/codex-switch --json
```

Result: `status` was `current`; no DevFlow project migration action was needed.

```bash
python3 scripts/test_codex_profile_switch.py
```

Result: `Ran 56 tests in 16.374s`, `OK`.

```bash
python3 -m py_compile scripts/*.py
```

Result: exit 0.

```bash
bash -n scripts/codex-switch && bash -n scripts/codex_env_setup && bash -n install.sh && bash -n run.sh
```

Result: exit 0.

```bash
openspec validate --all --strict --no-interactive
```

Result: `Totals: 4 passed, 0 failed (4 items)`.

```bash
git diff --check
```

Result: exit 0.

```bash
scripts/package-release.sh
```

Result: wrote `/Users/cY/dev/codex-switch/dist/codex-switch.tar.gz` and exited
0.

## Remaining Risk

Archive remains closed by gate. Do not archive this OpenSpec change until the
archive gate is explicitly opened. Existing Codex Desktop app-server
connections may still need a restart or reconnect before they load the latest
internal app proxy behavior.
