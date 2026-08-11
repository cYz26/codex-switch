# Generated Artifact Contract: SPLIT-DEPLOY-20260806T123605+0800

## Binding

- Owner: current serialized main Codex deployment task.
- OpenSpec change: `independent-app-cli-profiles`, task 10.3.
- Approved by: user request `部署生效一下` on 2026-08-06.
- Durable root:
  `.planning/devflow/deployments/20260806T123605+0800/`.
- Physical package root:
  `/private/tmp/codex-switch-deploy-20260806T123605+0800`.
- Physical root state at contract seal: absent.
- Owner command: `scripts/package-release.sh` with
  `CODEX_SWITCH_DIST_DIR` bound to the exact physical root.

## Lifecycle

- Creation: the owner may create only the exact physical root, its release
  outputs, and package-script staging/backup paths beneath that root.
- Owner exit: after package validation and live installation complete, or on
  the first package, identity, promotion, or install failure.
- Terminal success disposition: `RETAIN` as deployment and rollback evidence.
- Terminal failure disposition: `HUMAN_GATE`; retain evidence and do not
  improvise cleanup.
- Physical purge, wildcard deletion, recursive cleanup after owner exit, and
  cleanup of any installed release are forbidden without a separate Human
  Gate.

## Expected Terminal Outputs

```text
/private/tmp/codex-switch-deploy-20260806T123605+0800/codex-switch
/private/tmp/codex-switch-deploy-20260806T123605+0800/run.sh
/private/tmp/codex-switch-deploy-20260806T123605+0800/codex-switch.tar.gz
```

The package manifest, validator result, archive digest, installed immutable
payload digest, `current`/`rollback` references, and source/package identity
must be recorded in the deployment verification receipt. No cleanup authority
is inferred from successful verification.
