# Package Verification: INTERNAL-CLI-REPAIR-20260810T202906+0800

## Boundary

This is the retained, uninstalled release counterpart for
`internal-cli-only-runtime` task 6.5. It does not authorize or claim an
installation, internal update, split, App stop/restart, live cache mutation,
release, archive, Git operation, migration, cleanup, or destructive effect.

## Package and Identity

The owner command completed inside the exact absent-at-seal physical root:

```text
/private/tmp/codex-switch-internal-cli-repair-20260810T202906+0800
```

`validate_release_outputs` accepted the final package, runner, archive,
allowlist, modes, required paths, and manifest. Final identity:

```text
version: 0.1.13
files: 71
directories: 5
payload SHA-256: 7b278e90df47e512aeebfcd8ce18d87a67ed193c325acc26e7aed9b787663ab7
archive SHA-256: 1d1fa06fc383cebaac7d5955c8a35bed9bb78e33bbeba3d58f71b1d565430e9e
manifest SHA-256: c5c2c281c843a26a734a3e7c63710b257cba05552ebf717b1581c057b6b96bd6
README SHA-256: e036ca396f9147c2f986ccb80252041de887a83a47db0c3ebc09f208d54d6ff2
SKILL SHA-256: 76f07959108d7554cedff8ef0441e97f94e5e1be736a4cbec42b4f9c8473f4d9
```

README, SKILL, wrapper, three production Python seams, and four focused test
files are byte-exact between source and package. Nine package-local focused
promotion, managed-shell, streaming-size, verifier, progress, and conditional
restart tests passed in 6.279 seconds.

## Release-Counterpart Plugin Eval

The installed Plugin Eval entrypoint analyzed the isolated package root:

```text
score: 58/100
grade: D
risk: high
checks: 2 fail, 3 warn, 2 info
active budget: 4,283 tokens
```

The findings remain the existing INC-012 classes: invoke/deferred static token
budgets, top-level README layout, historical Python complexity and long lines,
and unavailable coverage artifacts. No new finding class was introduced. A
benchmark-backed Skill/package architecture refactor is outside this runtime
repair and remains `DEFER_AND_CONTINUE`.

## Terminal Receipt

- Owner exit: package validation, source/package identity, focused tests, and
  release-counterpart Plugin Eval completed.
- Terminal disposition: `RETAIN`.
- Cleanup complete: false; cleanup was not authorized.
- Installation/promotion/live activation: not run.
