# Fail-Safe Self-Update Verified Checkpoint

## Status

`fail-safe-update-release` task 2.4 is complete at 10/38. Task 3.1 is the next
dependency-ready item.

## Implemented Contract

- Candidate source is canonicalized through the trusted release-bundle module.
- Expected version, manifest structure, modes, syntax, imports, and smoke are
  validated before promotion.
- Promotion uses immutable `releases/<digest>`, atomic refs, and the structured
  run-id/version/digest/root handshake.
- The promotion receipt is validated before re-exec.
- Re-exec uses the receipt's digest root with recursion disabled.
- Sync failure continues through the prior verified implementation.
- A replayed nonzero user command is returned exactly once and is never retried
  as a self-update failure.

## Review Fixes

- New Bash locals are explicitly initialized for `set -u` failure paths.
- Legacy profile self-update fixtures now use canonical bundles and immutable
  refs with trusted promotion modules.
- Release archives use `tar -p`; an explicit `umask 0077` regression proves
  canonical `0755` executable modes survive extraction.

## Verification

- Python 3.12.13 update/release: 53/53 passed.
- System Python 3.9.6 update/release: 53/53 passed.
- Python 3.12.13 focused profile self-update: 10/10 passed.
- System Python 3.9.6 focused profile self-update: 10/10 passed.
- Task 2.3 self-update contract: 6/6 passed on both interpreters.
- Strict OpenSpec, Bash syntax, dual-runtime AST, obsolete in-place-path scan,
  and `git diff --check`: passed.

One exploratory parallel focused run hit the fixture's one-second candidate
smoke timeout. Sequential reruns and both serial full suites passed.

## Scope

No live install, self-update, profile/App switch, plugin mutation, network
release, commit, push, tag, or archive action ran.

## Next Action

Execute task 3.1 by RED: specify ordered internal-update decisions for
healthy/blocked current and latest versions, missing or unparseable versions,
and prerelease ordering before implementing policy task 3.2.
