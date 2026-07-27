# Fail-Safe Remote Tag Identity Verified Checkpoint

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `6.6`
Progress: `32/38`

## Result

Manual release recovery now:

- checks out trusted tooling from `main`;
- stages that tooling under `RUNNER_TEMP`;
- resolves only an exact semantic tag against the configured remote;
- checks out the resolved commit before target code runs;
- disables persisted checkout credentials for both checkouts.

Release reconciliation rechecks remote tag identity immediately before release
creation, every asset upload, publication, final release inspection, and after
downloaded asset verification. Tag movement or disappearance stops all later
mutations.

## RED / GREEN

The RED contracts were recorded before this continuation for the missing
remote semantic-tag resolver, missing mutation identity guards, unsafe manual
checkout order, persisted credentials, and target-owned tooling.

Fresh GREEN:

- Python 3.12.13 focused release/tag/workflow group: 4/4 passed.
- System Python 3.9.6 focused release/tag/workflow group: 4/4 passed.

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or OpenSpec archive action ran.

## Next Action

Execute task 6.7 by validating the trusted `v0.1.12` and `v0.1.13` historical
layouts and proving deterministic canonical archive hashes for supported retry
inputs.
