## Why

Profile switching currently reports only the profile-specific CLI/update source.
An internal switch can therefore complete without showing that its CLI trails
the latest stable upstream `openai/codex` release, leaving compatibility drift
easy to miss.

## What Changes

- Add a read-only comparison against the latest stable release published by
  `openai/codex`.
- Show the comparison during update checks and one-key profile switches,
  especially for `internal`.
- Keep the advisory non-blocking when GitHub or version parsing is unavailable.
- Keep prereleases outside the default comparison baseline and label the stable
  channel explicitly.
- Never use the upstream comparison to select or install an internal release.

## Capabilities

### New Capabilities

None.

### Modified Capabilities

- `codex-switch`: update-check and profile-switch output gains a bounded,
  profile-aware upstream stable-version advisory.

## Impact

The Bash wrapper, one small Python comparison policy module, the release-bundle
required-module manifest, focused profile switch tests, and user documentation
are affected. No profile state, authentication, update source, release
workflow behavior, dependency, or live App binding changes are required.
