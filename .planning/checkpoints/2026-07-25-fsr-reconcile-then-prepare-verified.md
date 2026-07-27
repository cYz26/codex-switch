# Fail-Safe Reconcile-Then-Prepare Verified Checkpoint

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `6.8`
Implementation progress: `30/35`
OpenSpec checkbox progress: `34/42`

## Result

Release planning now preserves both required outcomes:

- `reconcile_required` identifies an incomplete/draft latest release;
- `prepare_required` identifies release-relevant source changes;
- `reconcile_then_prepare` represents both in one run.

The automatic workflow first checks out and verifies the existing release
commit, packages it into a dedicated temporary dist root, validates/reconciles
its assets, then restores the exact original source commit. The pending release
uses a separate dist root and asset manifest before remote-base validation,
atomic main+tag push, publication, and downloaded checksum verification.

## RED / GREEN

RED:

- planner returned `reconcile` and discarded the pending prepare action;
- workflow had no reconciliation-specific package/validate path or source
  restoration step.

GREEN:

- planner/workflow group: 21/21 on Python 3.12.13;
- planner/workflow group: 21/21 on system Python 3.9.6;
- prepare-only regression: passed on both runtimes;
- strict FSR OpenSpec, dual-runtime compile, workflow YAML parse, and focused
  diff check passed.

No live install, profile/App switch, plugin mutation, network release, commit,
push, tag, or OpenSpec archive action ran.

## Next Action

Execute task 7.1 cleanup only after caller scans prove obsolete unsafe paths
are unreferenced.
