# Checkpoint: SAP Launcher Preparation Verified

Date: 2026-07-24

## Active Goal

Continue goal `019f8f8f-e64c-7093-af73-2c0247cf2891`. TPS and CRB are complete.
SAP tasks 1.1-4.4 are complete. SAP 5.x, FSR, integration, and final
verification remain pending.

## Completed Slice

SAP tasks 4.1-4.3 passed main review and are checked complete.

The source implementation:

- adds `codex_switch_home_sync.py prepare-launch`;
- precomputes canonical profile, live, target, snapshot, and Desktop state
  before the first managed mutation;
- removes every runtime/non-shareable symlink from the internal app home;
- rejects relative, dangling, self-referential, source-home, target-home, and
  resolved target-home-alias shareable symlinks;
- retains absolute external shareable symlinks;
- uses the same classifier in launcher sync, transaction planning, and the
  pinned transaction filesystem adapter;
- preserves current internal Plugin/Skill usage state across Desktop restart;
- generates a thin wrapper pinned to validated Python 3.11+ without embedded
  `find`, copy/link, TOML, or auth-deletion policy;
- preserves complete app-server argv and the backend's original `PYTHONPATH`.

## RED / GREEN

- Initial launcher RED: 4/4 failed for duplicate wrapper policy, incomplete
  isolated-link removal, unsafe shareable propagation, and mutation before TOML
  failure.
- Initial launcher GREEN: 4/4 passed.
- Main-review RED: 2/2 failed for a target-home symlink alias and malformed
  canonical profile config.
- Main-review GREEN: 2/2 passed after resolved-target classification and
  explicit profile-config preflight.

## Fresh Evidence

- Launcher-focused profile tests: 10/10 passed.
- Shared support tests: 3/3 passed.
- Complete profile suite Python 3.12: 139/139 passed.
- Transaction Python 3.12: 211/211 passed.
- Config Document Python 3.12: 24/24 passed.
- Runtime binding Python 3.12: 55/55 passed.
- Protocol Python 3.12: 27/27 passed.
- Python 3.9.6 and 3.12 syntax compile: passed.
- Strict `schema-scoped-app-proxy` OpenSpec validation: passed.
- Bash syntax and `git diff --check`: passed.

## Remaining SAP Work

- Task 5.1: generated-wrapper/proxy/fake-backend real-chain E2E.
- Task 5.2: remove superseded helpers only after caller proof.
- Tasks 5.3-5.5: final focused/full checks and evidence closure.

## Safety Boundary

No ChatGPT restart, live profile switch, install/update, plugin mutation,
release, commit, tag, push, or rollout edit ran. Preserve the dirty worktree and
obtain explicit authorization before any external-effect gate.

The official latest-version comparison remains INC-006
`BLOCKED_AWAITING_HUMAN` outside the active Goal.

## Exact Resume Point

Start SAP task 5.1 with one generated-wrapper/fake-backend process-chain RED
covering modern, legacy, unknown, config-write gating, response masking, raw
payload preservation, stderr, EOF, timeout, and nonzero exit behavior.
