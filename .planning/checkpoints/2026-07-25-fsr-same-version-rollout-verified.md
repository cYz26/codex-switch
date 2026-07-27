# Same-Version Self-Update Rollout Repair Verified

Date: 2026-07-25 20:39:32 +0800
Change: `fail-safe-update-release`
Tasks: `FSR-002`, `INC-011`, `ROLLOUT-001`
Status: complete

## Root Cause And Repair

Installed strict `0.1.13` downloaded and validated historical latest
`v0.1.13` before comparing versions. That asset predates the strict release
modules, so normal commands emitted `source_invalid` and a non-blocking sync
warning. Trusted explicit/default-latest metadata is now compared before any
download or staging. Same-version and older releases stop cleanly; newer
malformed candidates still fail closed.

The earlier Python traceback came from Python 3.9 lacking `tomllib`. The shell
wrapper selects Python 3.11+ before dispatch, and explicit old Python fails
before the switch script or store can mutate.

The repeated ChatGPT restart came from a temporary `launchctl submit` job,
which is keepalive-capable after failure. The job was removed, and future
one-shot restart procedures must not use that mechanism.

## Verification

- update/release: 113/113 passed serially;
- profile: 198/198 passed;
- system Python focused self-update: 5/5 passed;
- Python selection/fail-before-write: 3/3 passed;
- strict OpenSpec: 17/17 passed;
- Bash syntax: 5/5 passed;
- Python 3.12.13 and 3.9.6: AST 54/54 and imports 46/46;
- workflow YAML: 2/2; release static contracts: 7/7;
- isolated package: version 0.1.13, 64 files, mode 0755, payload
  `9e9c9cd4bce6fd0efcc8dacd8a04e75221f7e64b4a7a3a2864423ea24fcecbd3`;
- `git diff --check`: passed.

The first concurrent full update/release run hit one one-second fixture smoke
timeout. The exact test passed alone, and the authoritative complete serial
rerun passed 113/113.

## Live Receipt

The supported local-source installer completed. Normal `codex-switch status`
printed `already up to date 0.1.13` and emitted neither `source_invalid` nor
`sync failed`. Active ownership remained `internal`.

`current` points to
`releases/9e9c9cd4bce6fd0efcc8dacd8a04e75221f7e64b4a7a3a2864423ea24fcecbd3`;
`rollback` points to
`releases/db85a38c2bc18fcb7d63f9bbca4dcbef898d5fcb0857646690075dd4418a2550`.

ChatGPT pid 4983 and proxy/backend pids 5332/5346 retained their existing
uptime. Launchd contains only the normal ChatGPT application job and
`com.openai.codex-cli-path`; no temporary restart job remains.

## Boundaries

No App restart, profile switch, plugin mutation, commit, push, tag, release,
OpenSpec archive, dependency change, destructive cleanup, or parity
implementation ran during this closure.
