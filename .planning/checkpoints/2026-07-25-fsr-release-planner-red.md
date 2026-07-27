# Fail-Safe Release Planner RED Checkpoint

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `6.1`
Progress: `27/38`

## RED Contract

Seven planner and fake-GitHub contracts now cover:

- latest semantic tag not being an ancestor of the source commit;
- an existing release tag pointing at another commit;
- latest-tag reconciliation when one required asset is missing;
- no action for a matching, complete, published latest tag;
- remote `main` moving before release ref creation;
- local asset checksum drift after manifest validation;
- publish failure followed by an idempotent rerun that reuses matching assets.

Python 3.12.13 and system Python 3.9.6 each produced the same single expected
failure: `build_plan(...)` returned `release_action="reconcile"` for a complete,
published latest tag at `HEAD`, instead of `release_action="none"`. The other
six contracts passed, so the RED is isolated to planner action selection rather
than Git fixtures, checksum evidence, or fake publication behavior.

## Recovered Pre-Checkpoint Work

The previously written but unexecuted historical-release tests first failed
because manifest-less packages were accepted implicitly and no explicit
versioned layout/canonicalization seam existed. The bounded repair now:

- rejects a missing manifest outside explicit historical reconciliation;
- accepts only trusted `v0.1.12` and `v0.1.13` layouts;
- validates legacy package, runner, archive, symlink, special-file, and mode
  boundaries;
- accepts bounded AppleDouble metadata only when it maps to a real archive
  member for those trusted historical layouts;
- removes metadata and rewrites the historical archive deterministically.

The focused historical group passes 10/10 on Python 3.12. This is partial
evidence for later tasks 6.5 and 6.7; neither task is marked complete.

## Validation

- `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_update_release.py CodexReleasePlannerTests -v`
  - result: 7 run, 1 expected RED failure.
- `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_update_release.py CodexReleasePlannerTests -v`
  - result: 7 run, the same 1 expected RED failure.
- dual-runtime `py_compile` for the release test, planner, and bundle module:
  passed.
- focused `git diff --check`: passed.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

## Next Action

Execute task 6.2: make the planner select `none` for a complete published latest
tag while preserving ancestry, missing-asset reconciliation, remote race,
checksum, and rerun contracts. Then run all seven planner tests GREEN on both
supported Python interpreters.
