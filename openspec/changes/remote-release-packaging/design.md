# Design: Remote Release Packaging

## Release Workflow

Add `.github/workflows/release.yml` with:

- `on.push.tags: ["v*"]` for normal release publication.
- `workflow_dispatch` with a `tag` input for manual re-runs against an existing
  tag.
- `permissions.contents: write` so `GITHUB_TOKEN` can create releases and upload
  assets.
- Verification steps that mirror local release readiness:
  `python3 scripts/test_codex_profile_switch.py`, `python3 -m py_compile
  scripts/*.py`, shell syntax checks, OpenSpec validation, and
  `scripts/package-release.sh`.
- A publish step that creates the release if needed, then uploads
  `install.sh`, `dist/run.sh`, and `dist/codex-switch.tar.gz` with
  `gh release upload --clobber`.

This keeps publication tied to the immutable tag content. Re-running the
workflow for the same tag replaces assets without rewriting the tag.

## Source Archive Fallback

The primary path remains the release bundle:

- explicit `CODEX_SWITCH_TARBALL_URL`;
- versioned release asset when `CODEX_SWITCH_VERSION` is set;
- latest release asset otherwise.

When that download or validation fails and a fallback source archive URL can be
resolved, the shell scripts stage from the source archive:

- explicit `CODEX_SWITCH_SOURCE_TARBALL_URL`;
- versioned source archive when `CODEX_SWITCH_VERSION` or the self-update
  version is set;
- main branch source archive for installer/runner latest fallback.

After extracting source, scripts prefer to run `scripts/package-release.sh` into
a temporary dist directory and copy `dist/codex-switch` into the target. If the
source archive lacks the package script but directly contains executable
`scripts/codex-switch`, the scripts copy the source root as a compatibility
fallback.

## Self-Update Behavior

Local self-update keeps its existing non-blocking contract. If the release
bundle is unavailable and source fallback also fails, ordinary commands warn and
continue with the current implementation. If source fallback succeeds and the
staged bundle has the same `VERSION`, the wrapper treats it as no-op and does
not re-exec.

## Compatibility

- Existing `CODEX_SWITCH_TARBALL_URL`, `CODEX_SWITCH_VERSION`,
  `CODEX_SWITCH_SOURCE_DIR`, `CODEX_SWITCH_LIB_DIR`, and proxy overrides keep
  their current meaning.
- New `CODEX_SWITCH_SOURCE_TARBALL_URL` only affects fallback behavior.
- `run.sh` still does not install or update the public PATH symlink.
- Source checkout wrapper invocations still do not self-modify.

## Validation Strategy

- Add failing Python regressions for installer fallback, runner fallback, and
  self-update fallback.
- Add a static workflow contract test for required workflow permissions,
  packaging, and release-upload assets.
- Run existing full Python tests, shell syntax checks, packaging, OpenSpec
  validation, and `git diff --check`.
- After pushing a release tag, verify direct remote invocation through the
  published `run.sh` release asset.
