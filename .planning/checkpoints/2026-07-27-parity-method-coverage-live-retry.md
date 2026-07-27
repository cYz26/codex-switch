# Task 8.3 Live Retry Gate

Recorded: 2026-07-27T19:23:50+08:00
Change: `internal-official-feature-parity`
Task: 8.3
Progress: 70/79
Status: `BLOCKED_AWAITING_HUMAN`
Milestone: `OFFICIAL_FIRST_PAUSE_READY`
Required authorization: `PARITY-8.3-LIVE-RETRY`

## Why Work Pauses Here

The method-coverage repair is source/package verified, but the user expects to
use the official profile as the primary runtime and assigns low priority to
repeated profile switching. The remaining work is live acceptance, not an
unresolved source implementation defect.

Task 8.3 stays unchecked until a future authorized run promotes a healthy
receipt-v2 generation and clean status, Doctor, and
`verify internal --repair=none` evidence. Tasks 8.4-8.7 and change closure
remain unavailable.

## Resume Contract

After explicit `PARITY-8.3-LIVE-RETRY` authorization:

1. Re-read this checkpoint, the active OpenSpec task 8.3, the verified source
   checkpoint, and the parity verification record.
2. Re-attest current shell PATH, active profile, ChatGPT bundle binary,
   configured internal `codex_bin`, generated wrapper, running app-server
   ownership, official/internal schema pair, and every mutable config/catalog/
   capability input.
3. Re-run source/package verification if any source, package, binary, schema,
   acceptance trace, adapter rule, or mutable input digest changed. Do not
   treat `/private/tmp/codex-switch-parity-83.HLiOjw` as current authority.
4. Install the exact verified source only if the installed payload is not
   already byte-exact.
5. Run one supported same-backend preparation/rebind and its bounded
   provider-backed typed-v2 probe.
6. Record promoted manifest, capability receipt, parity receipt-v2, method
   coverage, acceptance trace, overlay, and config digests; require clean
   status, Doctor, and `verify internal --repair=none`.
7. Stop again before task 8.4.

## Still Excluded

This gate does not authorize ChatGPT restart, task 8.4 or later Desktop
acceptance, provider/model/API/auth migration, dependencies, Git actions,
release/publication, OpenSpec archive, destructive cleanup, legacy skill
migration, or retained-evidence cleanup.

The historical internal-mode pid/config snapshot is stale and must not be
reused. Preparation or revalidation failure leaves the existing official-first
workstation ownership unchanged and records a new safe RED before any scope
change.
