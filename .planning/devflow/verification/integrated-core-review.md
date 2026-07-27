# Integrated Core Review Verification

Date: 2026-07-25
Task: `INT-001`
Status: complete; `VER-001` and `ROLLOUT-001` remain pending

## Review Findings Closed

- Capability receipts are refreshed or reused through one digest-bound artifact
  seam and are committed with the internal manifest and managed wrapper in the
  same transaction.
- Internal Desktop AppServer smoke uses the managed launcher/proxy/backend
  chain in a temporary home and rejects manifest, payload, schema, backend,
  wrapper-path, child-backend, or child-argument drift.
- Canonical official advisory and switching resolve the ChatGPT bundle binding;
  stale canonical manifest fields are repaired in the switch transaction rather
  than rejected or used as runtime authority.
- Catalog command stderr makes the result unverified and authorizes no plugin or
  config writes.
- Automatic release checkout does not persist credentials. Remote Git actions
  receive only transient step-scoped authentication without duplicate headers.

## Fresh Verification

- `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_protocol_config.py -v`
  passed 37/37.
- `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_protocol_config.py -v`
  passed 37/37.
- `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_runtime_binding.py -v`
  passed 55/55.
- `PYTHONDONTWRITEBYTECODE=1 /usr/bin/python3 scripts/test_codex_runtime_binding.py -v`
  passed 55/55.
- `PYTHONDONTWRITEBYTECODE=1 python3.12 scripts/test_codex_verify.py -v`
  passed 22/22.
- `CODEX_SWITCH_PYTHON="$(command -v python3.12)" PYTHONDONTWRITEBYTECODE=1
  /usr/bin/python3 scripts/test_codex_verify.py -v` passed 22/22.
- `scripts/test_codex_official_release.py -v` passed 6/6 on Python 3.12 and
  system Python 3.9.
- The two catalog fail-closed regressions passed 2/2 on both runtimes.
- The transient release-auth regression passed 1/1 on both runtimes.
- `git diff --check` passed.

## Static Integration Proof

The call-map check found exactly one production definition for each of:

- `resolve_store_runtime_binding`
- `ProtocolAdapter`
- `CapabilityReceipt`
- `CatalogResult`
- `run_bounded_process`

No production definition or path remains for the retired recursive proxy
helpers, canonical-manifest hard rejection, or AppServer post-response config
repair.

## Boundary

The prior FSR full profile result predates these integrated edits and is not
final evidence. Full transaction/profile/update-release/OpenSpec/static/package
verification must run under `VER-001` before installation or a completion
claim. No live workstation mutation ran for this task.
