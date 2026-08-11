# Internal 0.145 Native-Resume Source Verified

Timestamp: 2026-07-28T18:14:46+08:00

Active change: `internal-official-feature-parity`

Status: `SOURCE_VERIFIED_LIVE_RETRY_READY`

## Scope

The consumed gate was `PARITY-0.145-NATIVE-RESUME-IMPLEMENT`. Production/test
writes remained exactly:

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`

Canonical OpenSpec, ledger, state, verification, and checkpoint evidence remain
main-owned. No installer, profile, App, candidate, plugin, proxy, provider,
dependency, Git, release, archive, or cleanup effect occurred during source
implementation.

## TDD Result

The named native-compatible resume test was first RED because current policy
required adapter coverage. The minimal implementation now accepts the sole
`thread/resume.params.history` dependency only when:

1. exact current `client_request:thread/resume` official and internal schemas
   are both present, `compatible=true`, and reason codes are empty; or
2. the existing exact schema/rule-bound adapter coverage is accepted.

Missing either side, contradictory compatible/reason-coded evidence,
incompatible resume without exact coverage, wrong direction, wrong method, an
extra dependency, and absence of the exact comparison all remain feature-level
`parity.feature.core_drift`.

The read-only Standards and Spec review axes reported no remaining actionable
findings after the fail-closed guard and exactness tests were added.

## Fresh Verification

```text
Python 3.12 ParityMethodCoverageTests: 7/7
system Python 3.9 ParityMethodCoverageTests: 7/7
Python 3.12 complete parity: 95/95 in 2.217s
system Python 3.9 complete parity: 95/95 in 37.239s
Python 3.12 update/release: 132/132 in 284.472s
system Python 3.9 update/release: 132/132 in 348.351s
Python 3.12 AST/import: passed
system Python 3.9 AST/import: passed
active strict OpenSpec: valid
all strict OpenSpec: 18/18
AI-native plan lint: passed
pinned workflow: ok=true, issues=[]
known workflow warning: legacy DevFlow root state is read-only
git diff --check and untracked checkpoint diff check: passed
new bytecode after gate consumption: none
```

The first static harness attempt omitted `scripts` from `sys.path`, and its
first untracked-diff shell used zsh's read-only `status` name. Those diagnostic
commands failed before evaluating production. Corrected commands used an
explicit scripts import path and task-specific shell variable and passed on
both runtimes.

## Isolated Package

Root:
`/private/tmp/codex-switch-native-resume-final.P5dgvY`

```text
manifest files: 66
manifest directories: 5
required paths: 20
source/package parity module SHA-256:
  f1d5928c7e6f9f2dbdb40018c6a06a108d64003d6ca142f7a3df04dd467f027e
source/package parity test SHA-256:
  1fc2abf1b40eddbeaf209e49d01de218396b1862f99f4998e93ba0aab121271c
archive SHA-256:
  2fe6ec94004a39f5815dba880b139063bf49d4db5a7fbb0b91e792d4908b4558
bundle-manifest SHA-256:
  c54123584f25c6f0adeeab6107d4f993a226c84abb6bd6bbe9abcc3eb0505cd3
```

The package builder validated manifest, modes, digests, imports, and archive.
Both changed files are byte-identical between source and package.

## Next Action

Use the already authorized supported source install, verify the new immutable
payload, and then freshly re-attest the retained internal 0.145.0 candidate and
every live input. Retry promotion with that retained candidate only. Do not run
`update-internal`, download another candidate, or reuse the earlier live hashes
as current evidence. Stop on any candidate, official bundle, config, manifest,
launcher, active-record, shell, or transaction-marker drift.
