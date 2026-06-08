# Code Review: 01-foundation

## Scope

Reviewed the verified `codex-switch` runtime-state isolation and workflow
closure changes, plus the remote script runner change:

- `run.sh`
- `scripts/codex_switch_app_wrapper.py`
- `scripts/codex_switch_switching.py`
- `scripts/codex_switch_config.py`
- `scripts/codex_switch_plan.py`
- `scripts/package-release.sh`
- `scripts/test_codex_profile_switch.py`
- `README.md`
- `SKILL.md`
- OpenSpec, planning, and release artifacts

## Findings

No blocking code findings.

## Notes

- The internal Desktop wrapper removes only app-home symlinks that point into
  live `CODEX_HOME`; profile-local runtime state is preserved.
- Runtime-state names are excluded before live-home support assets are linked,
  so future launches do not recreate live runtime symlinks.
- Shared non-auth config overlay behavior remains covered by regression tests.
- The remote runner keeps PATH installation separate from direct invocation:
  it installs the release bundle under a stable implementation directory and
  delegates to bundled `scripts/codex-switch` with forwarded arguments.
- Plugin Eval release-package findings are recorded as justified deferrals in
  `.planning/verification/20260608115159-remote-script-runner-verification.md`.

## Verification

- `python3 scripts/test_codex_profile_switch.py`: passed, 22 tests OK.
- `openspec validate --all --strict --json`: passed, 2 specs valid and 0 active
  changes.
- `git diff --check`: passed.
