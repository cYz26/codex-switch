# Internal 0.145 Native-Resume Compatibility Gate

Timestamp: 2026-07-28T16:31:00+08:00

Active change: `internal-official-feature-parity`

Progress: 74/84

Status: `BLOCKED_AWAITING_HUMAN`

Gate: `PARITY-0.145-NATIVE-RESUME-IMPLEMENT`

## Safe Live Result

Exact source payload
`275ad2e2fda95c0d2591fe95aa4d9e7075988da286851f6584e51c3bad771dab`
is installed and strictly validates. The one authorized update staged and
signed internal 0.145.0 at
`/Users/cY/.local/bin/.codex-internal-update-6efc91d3f6359549077f8a00`
and stopped before promotion with `parity.feature.core_drift`.

The bound internal backend remains 0.144.6. `.zshrc`, official config, internal
config, manifest, launcher, and active official profile are unchanged.
Installer scratch is absent. The retained candidate is a non-symlink
mode-0700 sibling and is not on live PATH.

## Exact Diagnosis

The only error is `item_ids`. Its only observed dependency is
`thread/resume.params.history`. For internal 0.145.0, current
`client_request:thread/resume` has both schemas, is direction-aware
`compatible=true`, and has no reason codes. Because the method is compatible,
there is correctly no adapter method-coverage record.

Current policy requires an adapter record even for a natively compatible
method. This is a false negative at the binary-upgrade compatibility boundary.

## Planned Correction

Accept the exact observed resume dependency only if either:

1. the exact current `client_request:thread/resume` comparison contains both
   schemas and is natively compatible; or
2. the exact existing adapter rule and schema-bound coverage record pass.

Missing methods, incompatible methods without exact accepted coverage,
absence of coverage without exact native compatibility, stale/broader
coverage, and any additional observed dependency remain unhealthy.

RED test:

`ParityMethodCoverageTests.test_item_ids_accepts_exact_native_resume_compatibility_without_adapter_coverage`

Write-set expansion:

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`

Focused/full parity must pass on Python 3.12 and system Python 3.9, followed by
dual-runtime update/release adjacency, strict/static/package/source identity,
exact-source reinstall, fresh candidate/live fingerprint validation, and one
promotion retry using the retained candidate.

## Planning Validation

```text
active strict OpenSpec: valid
all strict OpenSpec: 18/18
AI-native plan lint: passed
pinned workflow validation: ok=true, issues=[]
known warning: legacy DevFlow root state remains read-only
git diff --check: passed
```

Final zero-side-effect attestation still reports:

```text
.zshrc SHA-256:
  8a144f4d2221437b65119b343b356958fb3155a63e3037956c0ce8aa9da224b4
official config SHA-256:
  ca02832ff0a2b8829f976e3dcb13a18b725fd61be8eeffd0a1f0d10ee52d2ca3
internal config SHA-256:
  59a14e0e108e17b3488871d8880255bae78c85d9cad1a05778093ba638db31f1
bound backend: codex-cli 0.144.6
retained candidate: codex-cli 0.145.0, mode 0700
runtime rebind marker/temp: absent
installer scratch: absent
```

## Stop Condition

The narrower Scheme A incident write set does not include these two files.
Do not implement, retry promotion, switch internal, restart ChatGPT, download a
second candidate, or broaden policy until the user explicitly approves
`PARITY-0.145-NATIVE-RESUME-IMPLEMENT`.

## Approval Consumed

At 2026-07-28T17:41:14+08:00 the user explicitly approved
`PARITY-0.145-NATIVE-RESUME-IMPLEMENT`. The gate is consumed for the exact
two-file TDD correction and recorded source/package validation. The retained
candidate may be retried only after fresh identity/live-state attestation; no
second download or scope expansion is authorized.

## RED Evidence

Python 3.12 ran the named native-resume test alone. It failed at the expected
healthy assertion: 1 test, 1 failure, 0.002 seconds. The input had both current
resume schemas, `compatible=true`, no reason codes, no coverage record, and the
sole exact observed dependency. Production remained unchanged.

## Source GREEN

The exact two-file correction is GREEN. The named regression passes on Python
3.12 and system Python 3.9, the method-coverage class passes 6/6 on both, and
the complete parity suite passes 94/94 on both. Missing schema sides,
incompatible resume without exact coverage, extra dependency, and no exact
comparison remain unhealthy. Update/release adjacency and source/package
review are still required before live retry.

## Review Guard RED

Read-only Standards review identified contradictory native evidence as an
in-scope fail-closed guard: `compatible=true` with non-empty incompatibility
reasons must not pass. Spec review also tightened both-side and exact
direction/method negatives. After the tests reached the production seam, the
focused Python 3.12 test failed only at the contradictory entry: 1 test, 1
failure, 0.005 seconds. Production had not yet been tightened.
