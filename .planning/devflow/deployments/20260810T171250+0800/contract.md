# Generated Artifact Contract: SHARED-SWITCH-OPT-APP-PRESERVE-20260810T171250+0800

## Binding

- Owner: current serialized main Codex conditional App-preserving split task.
- OpenSpec change: `optimize-shared-switch-transaction`, task 5.3.
- Approved by: user confirmation on 2026-08-10 to implement the conditional
  App-preserving split; the approved change includes isolated package/source
  validation without installation.
- Durable root:
  `.planning/devflow/deployments/20260810T171250+0800/`.
- Physical package root:
  `/private/tmp/codex-switch-shared-opt-app-preserve-20260810T171250+0800`.
- Physical and durable roots at contract seal: absent.
- Owner command: `scripts/package-release.sh` with
  `CODEX_SWITCH_DIST_DIR` bound to the exact physical root.

## Lifecycle

- Creation: the owner may create only the exact physical root, its release
  outputs, and package-script staging/backup paths beneath that root.
- Owner exit: after package validation, source/package identity, package-local
  focused tests, and release-counterpart Plugin Eval complete, or on the first
  package or identity failure.
- Terminal success disposition: `RETAIN` as implementation verification
  evidence.
- Terminal failure disposition: `HUMAN_GATE`; retain evidence and do not
  improvise cleanup.
- Physical purge, wildcard deletion, recursive cleanup after owner exit,
  installation, promotion, and changes to repository `dist/` are forbidden
  without a separate Human Gate.

## Expected Terminal Outputs

```text
/private/tmp/codex-switch-shared-opt-app-preserve-20260810T171250+0800/codex-switch
/private/tmp/codex-switch-shared-opt-app-preserve-20260810T171250+0800/run.sh
/private/tmp/codex-switch-shared-opt-app-preserve-20260810T171250+0800/codex-switch.tar.gz
```

The package manifest, validator result, archive digest, source/package
identity, packaged focused tests, and release-counterpart Plugin Eval must be
recorded in `verification.md`. No install or cleanup authority is inferred
from successful verification.
