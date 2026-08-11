# Generated Artifact Contract: SPLIT-NATIVE-CACHE-LIFECYCLE-20260811T122033+0800

## Binding

- Owner: current serialized main Codex task-13.4 contract closure.
- OpenSpec change: `independent-app-cli-profiles`, task 13.4.
- Approved by: the user's 2026-08-11 explicit confirmation to adopt the native
  Plugin installed-cache lifecycle; repository policy requires an isolated
  release counterpart and Plugin Eval for the changed `SKILL.md`.
- Durable root:
  `.planning/devflow/deployments/20260811T122033+0800/`.
- Physical package root:
  `/private/tmp/codex-switch-native-cache-lifecycle-20260811T122033+0800`.
- Physical root state at contract seal: absent, verified immediately before
  this contract was written.
- Owner command: `scripts/package-release.sh` with `CODEX_SWITCH_DIST_DIR`
  bound to the exact physical root.

## Lifecycle

- Creation: the owner may create only the exact physical root, its release
  outputs, and package-script staging or backup paths beneath that root.
- Owner exit: after package validation, source/package identity, package-local
  shared tests, and release-counterpart Plugin Eval complete, or on the first
  package or identity failure.
- Terminal success disposition: `RETAIN` as task-13.4 verification evidence.
- Terminal failure disposition: `HUMAN_GATE`; retain evidence and do not
  improvise cleanup.
- Physical purge, wildcard deletion, recursive cleanup after owner exit,
  installation, promotion, repository `dist/` changes, and live
  Plugin/App/CLI effects are forbidden without a separate Human Gate.

## Expected Terminal Outputs

```text
/private/tmp/codex-switch-native-cache-lifecycle-20260811T122033+0800/codex-switch
/private/tmp/codex-switch-native-cache-lifecycle-20260811T122033+0800/run.sh
/private/tmp/codex-switch-native-cache-lifecycle-20260811T122033+0800/codex-switch.tar.gz
```

The package manifest and validator result, archive digest, source/package
identity, package-local results, and release-counterpart Plugin Eval must be
recorded in the terminal verification receipt. Success grants no install,
activation, live switch, App action, standalone cache cleanup, or Git authority.
