---
checkpoint_id: 2026-07-27-parity-exact-source-install-red
created_at: 2026-07-27T12:20:00+08:00
boundary: live_acceptance_red
project_mode: brownfield
change_id: internal-official-feature-parity
compact_recommended: false
compact_status: skipped
next_stage: Add one focused historical-manifest installer RED, then implement the minimal compatibility fix
---

# Checkpoint: Exact-Source Install RED

Date: 2026-07-27 12:20:00 +0800
Goal: `internal-official-feature-parity`
Change: `internal-official-feature-parity`
Status: `RED_SAFE`

## Result

The authorized task-8.2 command ran once and exited 2:

```text
reason: candidate_invalid
message: Promotion candidate failed bundle validation:
         Release manifest required paths mismatch
OpenSpec progress: 69/79
```

The current source candidate independently builds and validates with payload
SHA-256 `5cb103bb9f454b2767a9ae3f2e7dbd7cd9ed6a291b53cbeddc99b4a14746758d`.
A fresh isolated installer layout promotes it successfully.

## Root Cause

The new promotion code uses current-version required-path equality when reading
an existing immutable `current` reference. Installed 0.1.13 is a valid
manifest-v1 release with the historical 16-path requirement, while the new
candidate requires 20 paths after parity, Runtime Binding, App Proxy, and
home-sync became package requirements. The old release is valid rollback input,
but the shared strict candidate validator rejects it before publication.

## Safety Proof

```text
current: ed5d74c14feae71533eb0fac7d5de39bd4a74e10b59a2a02311d82c5286828ab
rollback: 9eb07bbc327b5f02a4f91d75d2aad902e58d9682e3d09802d898850cc4053f33
promotion-state SHA-256:
  ad51285c922e8ce03943c4a2e26297c1cbc7da20c0f186112d3a0b50d5abc85e
candidate release in live layout: absent
ChatGPT/proxy/backend pids: 95489/95838/95842
```

No live reference, state, release, profile, App, provider, backend, dependency,
Git, release/archive, or cleanup mutation occurred. Task 8.3 did not begin.

## Next Action

Add exactly one installer-adapter RED for upgrading from the supported
historical manifest-v1 16-path set. Then make the smallest validation change
that keeps new candidates strict while accepting that exact historical set
only for existing immutable `current`/`rollback` references. Run focused
dual-runtime verification before any second live install attempt.
