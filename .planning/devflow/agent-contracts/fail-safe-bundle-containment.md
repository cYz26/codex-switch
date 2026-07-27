# Agent Task Contract

## Goal
Complete `fail-safe-update-release` tasks 1.1 and 1.2 through strict TDD:
prove destructive package destinations and unmarked existing bundles are
rejected before mutation, then add the shared release-bundle builder and
migrate `scripts/package-release.sh` to staged, manifest-validated, recoverable
finalization.

## Worker ID
`fail-safe-bundle-containment`

## Stable Input Snapshot
- `scripts/package-release.sh`: `4e7403548dda038c1ec5e7c92e200e143fc10e043b62dff631a8e6b842502312`
- `scripts/test_codex_profile_switch.py`: `6e75ff589201a4fb19f0e5de491b5dbdf0f3ae44e7a7cdc71395ec37d3722d78`
- `scripts/test_codex_update_release.py`: absent
- `scripts/codex_switch_release_bundle.py`: absent
- canonical OpenSpec proposal: `2d21c3f1639723eb3564cb8b6e0a2a51e9c325409f177745e9caed0fd1eefc4d`
- canonical OpenSpec design: `32112285bf93fde1faf59f68697dd39667a228cc0be79bbac33fe00d5800248a`
- canonical OpenSpec spec: `0e7ab1c4c00a31eeaa51802c72ef406ccda1b1ca0eb63277e3aaec9afacd1adf`
- canonical OpenSpec tasks: `08a7a0003679776ddbf43eb9a091c5efd6117e9c9928dc20fb35fa062e18f61e`

Stop before editing if any existing-file hash differs or either absent file now
exists. OpenSpec and control-plane files are main-owned and read-only.

## Scope
Allowed write set for worker `fail-safe-bundle-containment` only:
- `scripts/test_codex_update_release.py`
- `scripts/codex_switch_release_bundle.py`
- `scripts/package-release.sh`

Read-only inputs include the complete approved
`openspec/changes/fail-safe-update-release/` change, existing package/install/
runner/release workflows, and `scripts/test_codex_profile_switch.py`.
Forbidden: every other path, especially OpenSpec, `.planning/`,
`TASK_LEDGER.md`, `.planning/STATE.md`, installed release trees, live profile
stores, App bundles, plugin caches, rollout/session files, network, Git
staging/commit/push/tag/release, install/update/profile-switch commands, or
dependency changes. The worker is not alone in the worktree and must preserve
all unrelated edits without reverting or rewriting them.

## Constraints
The pre-agreed public test seams are the
`codex_switch_release_bundle.py` CLI/library boundary, the
`scripts/package-release.sh` adapter, and filesystem-visible bundle outputs.
Use Python 3.9-compatible standard-library code and `unittest`. Record an
actual RED run after adding the task 1.1 tests and before production edits.

Tests must cover output/package resolution equal to the repository, filesystem
root, and a repository ancestor; output/package symlink redirection; an
unrelated existing destination; an existing destination with no valid build
marker; and an injected or deterministic copy failure. Every failure must
assert byte-identical repository and destination sentinels where applicable.
Missing implementation alone must not satisfy a rejection test: assert stable
typed/error reasons or the direct library exception contract.

The builder must canonically resolve repository, output root, and package
destination before any recursive cleanup. It must reject repository roots,
ancestors, filesystem root, symlink destinations, and unclassified existing
package directories. Copy only the current fixed release allowlist, preserving
the existing inclusion of troubleshooting docs. Build on the target filesystem
inside a unique temporary staging directory carrying a staging marker. Emit a
versioned bundle manifest that classifies the destination and records required
paths, normalized executable expectations, file modes, and SHA-256 digests.
Validate the staged package, top-level runner, and archive before finalization.

Finalization must preserve all prior classified outputs until the complete
candidate validates, use rename/replace operations with rollback for partial
failure, never recursively delete an unclassified path, and clean only
marker-owned temporary/backup paths. The successful public output remains
`<output>/codex-switch`, `<output>/run.sh`, and
`<output>/codex-switch.tar.gz`; `package-release.sh` still prints the tarball
path. Do not implement source-archive fallback, immutable install promotion,
self-update, update policy, plugin catalog, verify, or workflow ordering tasks.
Do not add a production dependency or alter the distribution's public layout.

## Verification
Capture exact RED and GREEN output, then run:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_package_release_includes_troubleshooting_docs -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py CodexProfileSwitchTests.test_package_release_includes_troubleshooting_docs -v
bash -n scripts/package-release.sh
/usr/bin/python3 -m py_compile scripts/codex_switch_release_bundle.py scripts/test_codex_update_release.py
python3.12 -m py_compile scripts/codex_switch_release_bundle.py scripts/test_codex_update_release.py
openspec validate fail-safe-update-release --strict --no-interactive
git diff --check
```

Also run one isolated successful package build into a fresh temporary output
root and inspect the manifest, required executable modes, digest validation,
archive members, and absence of residual staging/backup paths. Do not package
into the repository's real `dist/`.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` with the exact changed files
and final SHA-256 hashes; all added test names; ordered RED and GREEN commands
and complete test logs or exact validation outputs with failure/pass counts;
containment and sentinel-preservation matrix; manifest schema and fixed
allowlist; copy-failure injection seam; finalization/rollback sequence; isolated
package receipt; dual-interpreter focused results; adjacent troubleshooting-doc
regression; shell/compile/OpenSpec/diff results; residual risks and unverified
areas; incidental findings disposition; and review needs. Do not mark task
checkboxes or edit verification, ledger, state, or OpenSpec.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing the public distribution
layout, adding a dependency, deleting or replacing an unclassified destination,
executing downloaded source scripts, expanding beyond tasks 1.1-1.2, editing
outside the exclusive write set, touching live workstation/install/plugin/App
state, bypassing a failing required test, or performing Git/network/release
actions. If a required correction needs another file or contract change,
report the exact seam and reason without editing it.
