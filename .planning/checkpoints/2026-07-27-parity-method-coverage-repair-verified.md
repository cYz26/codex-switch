# Task 8.3 Method-Coverage Repair Verified

Recorded: 2026-07-27T19:23:50+08:00
Change: `internal-official-feature-parity`
Task: 8.3 source implementation only
Progress: 70/79
Status: `OFFICIAL_FIRST_PAUSE_READY`
Next gate: `PARITY-8.3-LIVE-RETRY`

## Milestone

The complete task-8.3 source repair and its isolated release package are
verified. The user is prioritizing the official profile, so development pauses
here rather than performing another live same-backend rebind. Task 8.3 remains
unchecked because no receipt-v2 candidate has been promoted and no live clean
status/Doctor/verify evidence exists.

## Implemented Contract

- The Protocol Adapter exposes one canonical structured 21-rule manifest and
  derives its global rule-set digest from it.
- The exact `thread/resume` ID and opaque-reasoning transform consumes the same
  named rule object bound by method coverage.
- Nullable `anyOf(null,string)` and `type:[null,string]` forms normalize as
  native semantic equivalents.
- Seven retained incompatible method pairs receive exact adapter or
  optional-extension dispositions; changed schema/rule evidence and observed
  optional use fail closed.
- `item_ids` requires the exact observed resume dependency.
- `multi_agent_v2` stays provisional until overlay/config proof, exact bounded
  probes, and post-probe fingerprint revalidation pass.
- Receipt schema v2 binds sorted method coverage, the versioned
  `official-desktop-core-v1` acceptance trace, and exactly passed
  `core_protocol` plus `typed_subagent_v2` results. Schema v1 is unsupported
  and regenerated through staged repair.

## Immutable Evidence

```text
fixture:
  testdata/parity/current-method-coverage-redacted.json
  sha256 529f746ef6370413cf1f18299f93a089f74076939242edd9579827ede65b1b5f
adapter rule set:
  sha256 1332cb0f29d32c0c5d3dc17b1cfe30ac7fb33bbe2d1fff7c9580fe2249ac9308
acceptance trace:
  id official-desktop-core-v1
  sha256 1c8a577e2847e604f9e80f7b55452058250f7ca449adf7d5b65ca82ef41e2c26
production:
  scripts/codex_switch_protocol_adapter.py
  sha256 8d1d45d762eeb7b4a3ffba2681e2691815f773341bd234aeb3bd6a10792ef4ed
  scripts/codex_switch_parity.py
  sha256 e1a2e934d2374d421cc89cf7943571c57661d5035112f5f9d437025c3a16bfd5
tests:
  scripts/test_codex_protocol_config.py
  sha256 8ac80bbaa4502ad2599555d1a7e9d7e17d0a4292a10d9475c1616adb2687e5ef
  scripts/test_codex_parity.py
  sha256 0a8422171ca2f1ba29c9ada9a2e3b189e55a461a522048730fa9bc27cd5aa658
```

## Fresh Test Evidence

```text
11 named task-8.3 tests:
  Python 3.12: passed
  system Python 3.9: passed
Protocol Adapter:
  Python 3.12: 41/41
  system Python 3.9: 41/41
Parity:
  Python 3.12: 93/93
  system Python 3.9: 93/93
Verifier receipt consumers:
  Python 3.12: 30/30
  system Python 3.9: 30/30
Runtime Binding receipt consumers:
  Python 3.12: 75/75
  system Python 3.9: 75/75
```

Two read-only reviewers reported no task-8.3 specification or
engineering-policy blocker. They retained two non-blocking maintenance notes:
some non-resume adapter transforms still duplicate manifest/implementation
metadata, and the explicit preparation-order regression intentionally uses
source marker ordering.

The DevFlow legacy-layout dry-run made no writes. The hook-provided nested
`.pyz/activate_project_dependencies.py` path is not directly executable
(`__main__` missing); the supported sibling launcher completed the dry-run and
reported the known 16 source conflicts with migration
`blocked_by_dependency_preflight`. OpenSpec 1.6 and methodology provenance
remain ready. This is `DEFER_AND_CONTINUE`; legacy migration/cleanup remains
unauthorized.

## Isolated Package

```text
root:
  /private/tmp/codex-switch-parity-83.HLiOjw
payload sha256:
  12c60c7e74a24b7e6b6b32f3b68443bdae6e0467666f5a400b897604d2a967fb
archive file sha256:
  2bbcb66b4f100c87686abdbc4fd4ba4e7d77250524f19ca6d3aaeff5c887c270
validate_release_outputs:
  passed
task source/package identity:
  6/6 byte-exact
retained fixture packaged:
  false
```

The package is validation evidence only. It is not installed and is not
standing authority for a later live retry; any changed source or runtime
fingerprint requires a new package and full revalidation.

## Mutation Boundary

No installed release, live receipt, overlay, config, manifest, launcher,
active record, profile, App, process, provider, dependency, Git state, public
release, archive, or retained evidence was mutated. No ChatGPT restart or
provider-backed task ran.
