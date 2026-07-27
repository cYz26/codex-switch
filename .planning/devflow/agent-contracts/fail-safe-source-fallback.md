# Agent Task Contract

## Goal
Complete `fail-safe-update-release` task 1.3 by strict TDD: a downloaded source
archive may be copied only through the currently trusted fixed-allowlist
implementation and must never execute its `scripts/package-release.sh` during
installer, remote-runner, or self-update fallback.

## Worker ID
`fail-safe-source-fallback`

## Stable Input Snapshot
- `install.sh`: `7b71e586d8d3ea1561525dfe51eb8529936bd02dbb39e325c54fe5503eabb8db`
- `run.sh`: `ac8bd542e8a7a3b66b52e821136cee7e452ad5fb08d0c8cbddaa6ded375e5419`
- `scripts/codex-switch`: `c8d5e88f154fba2ee351ce8908101a6cce74c53dab65775bf7da68a10aa676c1`
- `scripts/test_codex_update_release.py`: `bbb4b64eea78f874e9d723647c5d6fe848df3fd65668cb3ee9a792369a5a1b55`
- `scripts/test_codex_profile_switch.py`: `6e75ff589201a4fb19f0e5de491b5dbdf0f3ae44e7a7cdc71395ec37d3722d78`
- `README.md`: `a05fec80ad6ded3088304cfe5c5ed0ac8a61f29ce7f84d9ed41333f23e5e726b`
- `SKILL.md`: `a4cbebb18be478ab8b7c8cc51290ba5374e7589ce0e1a3f8d578d184b8a8278f`
- read-only bundle module:
  `eaba9e7e3d0b2a447057e3a084d59ae7b78408ff7827f88ac6db2dd676e8f671`
- canonical OpenSpec tasks:
  `1132200279b312cc25b25a930e6e77bb85f35c6b8946bd0faae6ec122b6d961e`

Stop before editing if any listed hash differs. OpenSpec, control-plane, bundle
module, and package adapter files are main-owned and read-only.

## Scope
Allowed write set for worker `fail-safe-source-fallback` only:
- `install.sh`
- `run.sh`
- `scripts/codex-switch`
- `scripts/test_codex_update_release.py`
- `scripts/test_codex_profile_switch.py`
- `README.md`
- `SKILL.md`

Read-only inputs include the approved `fail-safe-update-release` artifacts,
`scripts/codex_switch_release_bundle.py`, `scripts/package-release.sh`, and the
current installer/runner/self-update tests. Forbidden: every other path,
especially OpenSpec, `.planning/`, `TASK_LEDGER.md`, installed release trees,
live profile stores, App bundles, plugin caches, rollout/session files, network
URLs other than local `file://` fixtures, Git staging/commit/push/tag/release,
live install/update/profile-switch commands, or dependency changes. The worker
is not alone in the worktree; preserve all unrelated edits and make only narrow
changes inside the listed files.

## Constraints
The pre-agreed public seams are `install.sh`, `run.sh`, and the existing
`scripts/codex-switch` self-update entrypoint, observed through temporary
install/library roots, command output, and filesystem side effects. Use
standard Bash and Python `unittest`; record a real RED before production edits.

Add source archives containing the complete fixed release allowlist plus:
- a `scripts/package-release.sh` that writes an external sentinel if executed;
- a working raw `scripts/codex-switch` identifying the source path;
- an extra top-level file and cache residue that must not be copied.

Exercise all three downloaded-source fallback paths with missing release-bundle
`file://` URLs. Assert the malicious sentinel is absent, the raw source wrapper
is used, only `README.md`, `SKILL.md`, `VERSION`, `run.sh`, `agents/`, `docs/`,
`evals/`, and `scripts/` are copied, root `scripts/__pycache__` is removed, and
the extra top-level file is absent. Tests must use only temporary install,
library, archive, and marker paths.

Replace archive-owned packaging-script execution with a trusted fixed-allowlist
copy implemented by the currently running installer, runner, or wrapper.
Validate every required file/directory before copying, preserve executable
modes for `run.sh`, `scripts/codex-switch`, and
`scripts/package-release.sh`, and keep the existing release-bundle and explicit
local `CODEX_SWITCH_SOURCE_DIR` behavior unchanged. It is acceptable and
expected that the archive's `scripts/package-release.sh` is copied as inert
data inside the allowlisted `scripts/` tree; it must never run during fallback.

Update the narrow existing source-fallback assertions from archive-packaged
behavior to trusted raw allowlist behavior. Update README/SKILL wording so it
states that downloaded source scripts are not executed. Do not implement
immutable promotion, install rollback, self-update handshake, update policy,
plugin catalog, verification, or release workflow tasks.

## Verification
Capture exact RED and GREEN output, then run:

```bash
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py -v
PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_installer_falls_back_to_source_archive_and_installs_path_command \
  CodexProfileSwitchTests.test_remote_runner_falls_back_to_source_archive_and_execs_command \
  CodexProfileSwitchTests.test_local_wrapper_self_update_falls_back_to_source_archive -v
PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_profile_switch.py \
  CodexProfileSwitchTests.test_installer_falls_back_to_source_archive_and_installs_path_command \
  CodexProfileSwitchTests.test_remote_runner_falls_back_to_source_archive_and_execs_command \
  CodexProfileSwitchTests.test_local_wrapper_self_update_falls_back_to_source_archive -v
bash -n install.sh run.sh scripts/codex-switch scripts/package-release.sh
openspec validate fail-safe-update-release --strict --no-interactive
git diff --check
```

Also run `rg` proving no supported downloaded-source fallback invokes
`package-release.sh`; the release packager itself remains an expected caller.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` with exact changed files and
final hashes; all commands run; added/updated test names; complete test logs
and exact RED/GREEN validation results; installer/runner/self-update sentinel
and allowlist matrix; the trusted copy algorithm and required-path validation;
focused dual-runtime results; shell/OpenSpec/diff/`rg` results; docs changes;
residual risks and unverified areas; incidental finding disposition; and review
needs. Do not mark task checkboxes or edit verification, ledger, state,
OpenSpec, bundle module, or package adapter files.

## Human Gate
Stop and report `BLOCKED_AWAITING_HUMAN` before changing the public distribution
layout, adding a dependency, executing any downloaded script, expanding beyond
task 1.3, changing explicit local-source behavior, editing outside the write
set, touching live workstation/install/plugin/App state, bypassing a failing
required test, or performing Git/network/release actions. If a required fix
needs another file or contract change, report the exact seam and reason without
editing it.
