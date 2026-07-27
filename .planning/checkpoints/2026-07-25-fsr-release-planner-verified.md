# Fail-Safe Release Planner Verified Checkpoint

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `6.2`
Progress: `28/38`

## Result

`build_plan(...)` now selects reconciliation only when the latest release is
missing, remains draft, or lacks required assets. A matching, complete,
published latest tag at `HEAD` selects no action. Existing ancestry, tag
identity, remote-base, checksum, and idempotent publish-rerun behavior remains
unchanged.

The release planner already exposes explicit `prepare`, `reconcile`, and `none`
decisions; validates an exact asset manifest; rejects a moved remote base or
conflicting tag; requires atomic main+tag publication at the workflow adapter;
and downloads/hashes every required asset before and after publication.

The release-bundle module changed while recovering historical-layout tests, so
the trusted bootstrap SHA-256 in `install.sh` and `run.sh` was refreshed to:

`bf6d221ff937cb9d66e9a4c8cd0705c9f76f37333982d2989b399e9d8a226228`

## Verification

- Python 3.12.13 planner plus piped-bootstrap regressions: 8/8 passed.
- System Python 3.9.6 planner plus piped-bootstrap regressions: 8/8 passed.
- Full Python 3.12 update/release suite: 87 run, 82 passed, 5 failed before the
  bootstrap hash refresh. The two bootstrap failures are now GREEN; the
  remaining three failures are the intentionally pending task 6.5 RED
  contracts for nested manifest handling, special files, and package-root
  mode.
- strict `fail-safe-update-release` OpenSpec validation: passed.
- dual-runtime `py_compile`, Bash syntax, trusted-hash equality, and
  `git diff --check`: passed.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

## Next Action

Execute task 6.3 by adding static workflow-order tests before changing the
workflow adapters.
