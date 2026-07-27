## Why

Several supported maintenance paths can delete the wrong directory, remove the last working install before validation, report a failed internal update as successful, downgrade a newer healthy binary, mass-disable plugins after catalog parse failure, publish a tag without an asset, or persist secret-bearing verification output. These paths need one fail-safe promotion and evidence contract.

## What Changes

- Canonically contain package output, build in a temporary staging directory, and reject repository roots, ancestors, and unrelated existing destinations before any recursive removal.
- Stage and validate installer/self-update candidates for structure, version, syntax/import, and command smoke; atomically promote them while retaining last-known-good until a successful re-exec handshake.
- Resolve trusted self-update release metadata before candidate materialization so a same-version or older legacy asset is reported as already current instead of entering strict bundle validation.
- Return explicit internal-update outcomes, propagate helper failures, verify the installed target version, and use ordered comparison that never downgrades a healthy newer binary.
- Keep plugin catalog stdout/stderr separate, validate response schema, distinguish verified-empty from unknown/invalid, and forbid `--disable-unavailable` writes when availability is unproven; validate real installed cache markers.
- Bind release inputs and package contents to exact Git commit trees, build and
  validate release assets before pushing release refs, reconcile an existing
  tag whose required assets are missing, and continue to a pending new release
  in the same run.
- Model verification smokes as structured `passed`/`failed`/`not_run` outcomes with timeouts, bounded capture, global sanitization, unique reports, and no persisted raw prompt or credentials.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: package/install/self-update/internal-update/plugin-repair/release-promotion and verification-report safety requirements are changed.

## Impact

Primary impact is in shell orchestration, installer/packager/release workflow, plugin and verify modules, plus isolated regression tests. Existing release/source fallback behavior remains; remote publication, installation into the user's live location, plugin disable writes, commit, tag, and push are outside implementation verification.
