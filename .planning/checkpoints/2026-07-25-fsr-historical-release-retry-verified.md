# Fail-Safe Historical Release Retry Verified Checkpoint

Date: 2026-07-25
Change: `fail-safe-update-release`
Task: `6.7`
Progress: `33/38`

## Result

Historical asset recovery is now explicit at the CLI/workflow boundary:

- `release_auto.py assets --allow-legacy` enables the historical route;
- the manual exact-tag workflow passes that flag;
- missing manifests remain rejected without the flag;
- only `v0.1.12` and `v0.1.13` use trusted version-scoped layouts;
- unsupported historical tags fail closed.

Trusted tooling validates package/source identity, executable modes, archive
members, top-level runner identity, and exact VERSION before rewriting the
archive deterministically.

## RED / GREEN

RED:

- `assets` rejected the explicit historical flag as unknown;
- the manual workflow did not request the historical route.

GREEN:

- historical/CLI/workflow group: 13/13 on Python 3.12.13;
- historical/CLI/workflow group: 13/13 on system Python 3.9.6;
- exact `v0.1.12` and `v0.1.13` retry archives canonicalized to stable hashes;
- strict FSR OpenSpec, dual-runtime compile, and focused diff check passed.

No live install, profile/App switch, plugin mutation, network release, commit,
push, tag, or OpenSpec archive action ran.

## Next Action

Execute task 6.8: reconcile the latest historical release and preserve pending
release-relevant source work in the same automatic workflow run.
