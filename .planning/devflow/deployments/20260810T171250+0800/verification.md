# Package Verification: SHARED-SWITCH-OPT-APP-PRESERVE-20260810T171250+0800

## Outcome

- Status: `VERIFIED_NOT_INSTALLED`.
- Generated-artifact disposition: `RETAIN`.
- Physical root:
  `/private/tmp/codex-switch-shared-opt-app-preserve-20260810T171250+0800`.
- Live profile/App/install effect: not performed.
- Cleanup: not authorized and not performed.

## Package Identity

```text
version: 0.1.13
archive SHA-256:
  d6fd3c95cdeb1a113809a195276f071841d2b70153ded4db24b1aa3c9bcbfc83
manifest SHA-256:
  9268efa71afe254be804bc7c8bf672d709c2ff908e8c1f9b79c12b6839d595b8
payload SHA-256:
  d62dd967bb23c60851088c3f4dc621c1273a5ea648130036071551c29001252e
required paths: 22
files: 72
directories: 5
```

The package builder exited zero and passed its built-in manifest, mode,
archive, required-path, and runtime-import validation. README, SKILL,
transaction source, complete transaction test, and complete profile test are
byte-exact with source. Fresh package-local results are conditional transaction
10/10 and profile shortcut/rebind 4/4.

## Release-Counterpart Plugin Eval

Both JSON source-of-truth and required Markdown analysis completed against the
isolated release target. Final result: 58/100, grade D, high static risk, with
2 failures, 3 warnings, and 2 informational checks. Static budgets are trigger
43, invoke 3,837, active 3,880, and deferred 1,038,218 tokens. The finding
classes are unchanged from INC-012: invoke/deferred static budgets, top-level
README placement, historical Python complexity, seven long lines, and missing
coverage artifacts.

These findings predate and materially exceed the conditional split guidance.
Resolving them requires a separately approved benchmark-backed Skill/package
architecture change; this behavior repair retains deterministic 545-test
source proof plus package-local tests. No benchmark/provider run, package
rewrite, install, release, cache refresh, or cleanup was performed.
