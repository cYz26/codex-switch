# Generated Artifact Contract: SPLIT-SHORTCUT-20260810T120157+0800

## Binding

- Owner: current serialized main Codex shortcut implementation task.
- OpenSpec change: `independent-app-cli-profiles`, task 11.4.
- Approved by: user confirmation on 2026-08-10 to implement the concise
  command and update the local installation.
- Durable root:
  `.planning/devflow/deployments/20260810T120157+0800/`.
- Physical package root:
  `/private/tmp/codex-switch-shortcut-20260810T120157+0800`.
- Physical root state at contract seal: absent.
- Owner command: `scripts/package-release.sh` with
  `CODEX_SWITCH_DIST_DIR` bound to the exact physical root.

## Lifecycle

- Creation: the owner may create only the exact physical root, its release
  outputs, and package-script staging/backup paths beneath that root.
- Owner exit: after package validation and immutable local installation
  complete, or on the first package, identity, promotion, or install failure.
- Terminal success disposition: `RETAIN` as implementation, install, and
  rollback evidence.
- Terminal failure disposition: `HUMAN_GATE`; retain evidence and do not
  improvise cleanup.
- Physical purge, wildcard deletion, recursive cleanup after owner exit, and
  cleanup of any installed release are forbidden without a separate Human
  Gate.

## Expected Terminal Outputs

```text
/private/tmp/codex-switch-shortcut-20260810T120157+0800/codex-switch
/private/tmp/codex-switch-shortcut-20260810T120157+0800/run.sh
/private/tmp/codex-switch-shortcut-20260810T120157+0800/codex-switch.tar.gz
```

The package manifest, validator result, archive digest, installed immutable
payload digest, `current`/`rollback` references, source/package identity,
Plugin Eval result, and installed shortcut help/isolated-preview evidence must
be recorded in the deployment verification receipt. No cleanup authority is
inferred from successful verification.
