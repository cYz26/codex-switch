# Generated Artifact Contract: INTERNAL-CLI-REPAIR-20260810T202906+0800

## Binding

- Owner: current serialized main Codex internal-CLI live-acceptance repair.
- OpenSpec change: `internal-cli-only-runtime`, task 6.5.
- Approved by: user confirmation on 2026-08-10 to implement the combined
  binary-size, managed-smoke, and conditional App-guidance repair; repository
  policy requires isolated release-counterpart evaluation for changed Skill
  guidance.
- Durable root:
  `.planning/devflow/deployments/20260810T202906+0800/`.
- Physical package root:
  `/private/tmp/codex-switch-internal-cli-repair-20260810T202906+0800`.
- Physical root state at contract seal: absent.
- Owner command: `scripts/package-release.sh` with
  `CODEX_SWITCH_DIST_DIR` bound to the exact physical root.

## Lifecycle

- Creation: the owner may create only the exact physical root, its release
  outputs, and package-script staging or backup paths beneath that root.
- Owner exit: after package validation, source/package identity, focused
  package checks, and release-counterpart Plugin Eval complete, or on the first
  package or identity failure.
- Terminal success disposition: `RETAIN` as implementation verification
  evidence.
- Terminal failure disposition: `HUMAN_GATE`; retain evidence and do not
  improvise cleanup.
- Physical purge, wildcard deletion, recursive cleanup after owner exit,
  installation, promotion, and repository `dist/` changes are forbidden
  without a separate Human Gate.

## Expected Terminal Outputs

```text
/private/tmp/codex-switch-internal-cli-repair-20260810T202906+0800/codex-switch
/private/tmp/codex-switch-internal-cli-repair-20260810T202906+0800/run.sh
/private/tmp/codex-switch-internal-cli-repair-20260810T202906+0800/codex-switch.tar.gz
```

The package manifest and validator result, archive digest, source/package
identity, focused package results, and release-counterpart Plugin Eval must be
recorded in the terminal verification receipt. No install, activation, live
switch, App action, release, or cleanup authority is inferred from success.
