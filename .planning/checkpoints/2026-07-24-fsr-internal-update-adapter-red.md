# Fail-Safe Internal Update Adapter RED Checkpoint

## Status

`fail-safe-update-release` task 3.3 is complete at 13/38. Task 3.4 is the next
dependency-ready item.

## Public Contracts

- Helper exit 17 must be returned by the one-key wrapper.
- Helper success with the wrong installed version must fail.
- Blocked-current fallback repair failure must not report success.
- App-server compatibility-smoke failure must prevent update completion.

## RED Evidence

- Python 3.12.13: 4/4 expected behavior failures.
- System Python 3.9.6: 4/4 expected behavior failures.
- The 3.9 test process used Python 3.12 only for the existing Config Document
  initialization prerequisite.
- Helper exits 17 and 23 were swallowed.
- Unchanged `1.0.0` after targeting `1.1.0` was accepted.
- Normal upgrade omitted its explicit `--version 1.1.0` target.
- Completion was printed before compatibility-smoke failure.
- Dual test compile and `git diff --check`: passed.

An earlier package-style unittest command failed before collection because
`scripts/` was not on `sys.path`; it is excluded from RED evidence.

## Scope

No production adapter, live update, install/self-update, profile/App switch,
plugin mutation, network release, commit, push, tag, or archive action ran.

## Next Action

Route update checks through the structured policy, bind every helper call to
the intended target, propagate helper status, require an exact after-version,
and defer completion until the app-server compatibility boundary passes.
