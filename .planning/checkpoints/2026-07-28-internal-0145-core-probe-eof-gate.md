# Internal 0.145 Core-Probe EOF Gate

Timestamp: 2026-07-28T18:25:22+08:00

Active change: `internal-official-feature-parity`

Status: `BLOCKED_AWAITING_HUMAN`

Gate: `PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT`

## Safe Promotion Result

The exact installed hidden promotion seam reused the retained candidate and
returned 2 after 5.009 seconds:

```text
codex-profile-switch:
  Parity preparation is unhealthy: parity.probe.missing_response
```

The failure occurred before executable swap or runtime-bundle transaction.
Immediate post-failure attestation proves:

```text
bound: codex-cli 0.144.6
bound inode/SHA-256:
  43110921 /
  410ebcd3bf469f01bca78ba479e72964eb761653edea35574abba76e1f88e8b6
candidate: codex-cli 0.145.0
candidate inode/SHA-256:
  57343496 /
  a34c872ccaaa02b6823bdf75138826a17177b91117a1920cedec9834772197b8
fixed executable backup: absent
runtime rebind marker: absent
runtime rebind temporary directories: zero
installer scratch roots: zero
```

`.zshrc`, official config, internal managed config, internal manifest,
launcher, and active-record hashes remain exactly equal to preflight. No
profile, App, plugin, proxy, provider, Git, release, archive, or cleanup effect
occurred.

## Tight Feedback Loop and Minimal Reproduction

The production core probe starts app-server, writes initialize, initialized,
`collaborationMode/list`, and `thread/start`, immediately closes stdin, then
waits. A credential-free isolated differential ran this exact sequence against:

- official bundled 0.146.0-alpha.3.1;
- bound internal 0.144.6; and
- retained internal 0.145.0.

All three returned only `parity-probe-initialize` before clean exit 0. This
falsifies candidate-only protocol drift.

A second isolated diagnostic used the same candidate and messages but waited
for each request ID before sending the next message and closed stdin only after
all expected responses. It returned, in order:

```text
parity-probe-initialize
parity-probe-collaboration
parity-probe-thread
returncode: 0
```

The loop is credential-free, deterministic, sub-second, and exercises the real
app-server process. It proves premature stdin EOF is the load-bearing cause.

## Ranked Hypotheses

1. **Confirmed:** immediate stdin close makes app-server stop after the first
   response instead of draining queued requests. Response-paced writes make
   all three versions return all IDs.
2. **Falsified:** internal 0.145 removed or broke the core methods. The same
   immediate-EOF behavior occurs in official and bound binaries, while 0.145
   returns every method under response pacing.
3. **Falsified for the core probe:** provider/auth/config failure. The minimal
   credential-free core process returns every required response interactively.
4. **Falsified:** the native-resume policy correction caused this failure. The
   policy gate passes and execution reaches the independent probe runner.

## Design Options

### A. Response-paced single app-server session (recommended)

Keep one candidate app-server process and one shared deadline. Send messages in
the specified order. Notifications are flushed immediately; after every
request with an ID, wait until the bounded stdout capture contains the matching
complete JSON response before sending the next message. Close stdin only after
all expected IDs arrive or after an existing terminal condition.

This models the real stateful protocol, has no timing sleep, preserves one total
timeout/output bound and process-group termination, and leaves semantic
evaluation/sanitized receipt evidence unchanged.

### B. Fixed grace period before EOF

Write everything, sleep, then close stdin. It is smaller but timing-dependent
and flaky under load. Reject.

### C. One app-server process per request

Each request would get EOF only after its response, but initialize/session state
would not carry across requests. It does not model Desktop behavior. Reject.

## Proposed Completion Contract

After approval:

1. Update the existing OpenSpec proposal/design/spec/tasks so they require
   response-paced stateful core probing and one shared deadline.
2. Add a RED default-runner regression whose fake app-server returns only
   initialize if stdin closes early and all IDs only when the caller waits.
3. Add fail-closed negatives for wrong/unmatched response ID, early exit,
   malformed/oversized output, shared-deadline timeout, and descendant
   termination.
4. Implement the smallest runner change in
   `scripts/codex_switch_parity.py`; keep raw output in bounded memory and
   persist only the existing sanitized digest.
5. Re-run focused/full parity and update/release on Python 3.12/system Python
   3.9, strict/static/workflow/package/source identity, and two-axis review.
6. Reinstall exact verified source, re-attest the same retained candidate and
   live inputs, and make one further promotion attempt using that candidate
   only.

Implementation/test writes remain exactly:

- `scripts/codex_switch_parity.py`
- `scripts/test_codex_parity.py`

No dependency, provider/model/auth/config contract, public CLI, proxy/plugin
behavior, second candidate/download, destructive cleanup, Git, release, or
archive change is proposed.

## Stop Condition

Do not revise the OpenSpec behavior artifacts, edit the runner/tests, rerun
promotion, switch internal, or restart ChatGPT until the user explicitly
approves `PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT`.
