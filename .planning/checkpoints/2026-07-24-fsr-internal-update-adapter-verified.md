# Fail-Safe Internal Update Adapter Verified Checkpoint

## Status

`fail-safe-update-release` task 3.4 is complete at 15/38. Task 4.1 is the next
dependency-ready item.

## Implemented Contract

- Standalone and one-key internal updates use ordered policy targets.
- Helper and version-probe failures propagate without success output.
- The installed binary must report the exact intended semantic version.
- App-server compatibility must pass before update completion.
- Complete helper value-option parsing prevents `--dry-run` from becoming an
  option value.
- Malformed existing internal manifests fail closed instead of selecting the
  default install path.
- Plugin-repair failure after update still permits mandatory compatibility
  verification before the original repair failure is returned.

## Verification

- Python 3.12.13 focused profile adapter: 26/26 passed.
- System Python 3.9.6 shell/adapter subset: 20/20 passed.
- Python 3.12.13 complete update/release: 64/64 passed.
- System Python 3.9.6 complete update/release: 64/64 passed.
- Strict FSR OpenSpec: passed.
- Bash syntax: passed.
- `git diff --check`: passed.
- Wrapper SHA-256:
  `28e8a2ec2fe13bd33db0f27d4937ac939efcaec55603365c500ece177ad23798`.

## Safety Boundary

No live update, install/self-update, profile/App switch, plugin mutation,
network release, commit, push, tag, or OpenSpec archive action ran.

## Next Action

Add task 4.1 RED catalog-result contracts before changing plugin repair.
