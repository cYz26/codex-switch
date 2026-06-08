# Remote Release Packaging Verification

Timestamp: 2026-06-08T14:40:55+08:00

## Scope

OpenSpec change: `remote-release-packaging`

Verified:

- GitHub Actions release workflow contract exists for tag packaging and asset upload.
- `install.sh`, `run.sh`, and local wrapper self-update can fall back from a
  missing release bundle to a source archive.
- Source archive fallback prefers local package generation through
  `scripts/package-release.sh`.
- Release output still includes executable runner assets.

## TDD Evidence

Initial focused regression run failed before implementation:

```text
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_installer_falls_back_to_source_archive_and_installs_path_command \
  CodexProfileSwitchTests.test_remote_runner_falls_back_to_source_archive_and_execs_command \
  CodexProfileSwitchTests.test_local_wrapper_self_update_falls_back_to_source_archive \
  CodexProfileSwitchTests.test_release_workflow_uploads_required_assets

Result: FAILED
- install.sh exited 37 when the primary bundle was missing.
- run.sh exited 37 when the primary bundle was missing.
- local self-update kept the old wrapper instead of using source fallback.
- .github/workflows/release.yml was missing.
```

After implementation, the same focused tests passed:

```text
python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_installer_falls_back_to_source_archive_and_installs_path_command \
  CodexProfileSwitchTests.test_remote_runner_falls_back_to_source_archive_and_execs_command \
  CodexProfileSwitchTests.test_local_wrapper_self_update_falls_back_to_source_archive \
  CodexProfileSwitchTests.test_release_workflow_uploads_required_assets

Result: OK, 4 tests.
```

## Local Validation

```text
python3 scripts/test_codex_profile_switch.py
Result: OK, 30 tests.

python3 -m py_compile scripts/*.py
Result: passed.

bash -n scripts/codex-switch
Result: passed.

bash -n scripts/codex_env_setup
Result: passed.

bash -n install.sh
Result: passed.

bash -n run.sh
Result: passed.

python3 -m json.tool evals/evals.json
Result: passed.

scripts/package-release.sh
Result: dist/codex-switch.tar.gz generated.

test -x dist/run.sh
Result: passed.

test -x dist/codex-switch/run.sh
Result: passed.

git diff --check
Result: passed.

openspec validate remote-release-packaging --strict --json
Result: valid.

openspec validate --all --strict --json
Result: 3/3 valid.
```

## Remote Source Fallback Probe

```text
CODEX_SWITCH_LIB_DIR="$tmp/lib" \
CODEX_SWITCH_INSTALL_DIR="$tmp/bin" \
CODEX_SWITCH_TARBALL_URL="https://github.com/cYz26/codex-switch/releases/download/v0.1.2/missing-codex-switch.tar.gz" \
CODEX_SWITCH_SOURCE_TARBALL_URL="https://github.com/cYz26/codex-switch/archive/refs/tags/v0.1.2.tar.gz" \
./run.sh version

Result: release bundle 404, source archive fallback succeeded, output 0.1.2.
```

## Pending Remote Publication Check

The release workflow has not run until the implementation commit and `v0.1.3`
tag are pushed. After pushing, verify:

```bash
curl -fsSL "https://github.com/cYz26/codex-switch/releases/download/v0.1.3/run.sh" | bash -s -- version
```

Expected output: `0.1.3`.
