# Internal Responses Resource Stickiness Verification

## Why

The internal profile can complete a plain text Azure Responses request, but
fails when a tool call result is submitted back to the Responses API:

```text
The requested item was created under a different Azure OpenAI resource. Use the same resource that created the item to access it.
```

Fresh internal threads also reproduce the failure, so this is not stale local
conversation state. A local trace showed the initial `/responses` request and
the tool-result follow-up were routed to different Azure resource/account IDs
for the same returned deployment. The Responses context created by the first
resource cannot be continued on the second resource.

Existing `codex-switch verify --runtime-smoke` only checks local runtime
startup and plugin listing. Existing `--exec-smoke <prompt>` can catch the
problem only when the caller already knows to force a tool call. This leaves an
internal backend upgrade path where verification can pass while the real
Desktop/tool-call workflow is broken.

## What Changes

- Add an explicit verification smoke that runs a deterministic
  `codex exec --json` prompt requiring a shell tool call and tool-result
  follow-up.
- Keep the smoke opt-in because it uses the model service.
- Detect the Azure resource mismatch service message in smoke output and report
  it as an internal Responses resource-stickiness failure.
- Detect `Item with id 'rs_…' not found` as a reasoning continuity failure;
  record that `store=false` continuation requires returned encrypted reasoning
  content or stable upstream item routing.
- Extract and report sanitized routing evidence when available, including
  `x-account-id`, `x-account-deployment`, `x-model-request-id`, and
  `x-tt-logid`; never persist or print credentials.
- Include the new smoke result and diagnostic fields in JSON verification
  reports.
- Document this failure mode, local verification command, ownership boundary,
  and upstream AIDP/backend repair contract.

## Target State

After internal Codex backend upgrades, the user can run a single codex-switch
verification command that exercises the same Responses tool-follow-up path that
Desktop work depends on. If AIDP routes follow-up requests to a different Azure
resource, verification fails with a direct diagnosis and enough sanitized
request evidence to hand to the internal backend/AIDP owner.

## Scope

In scope:

- `codex-switch verify` CLI surface.
- Optional one-key switch verification forwarding.
- Runtime smoke command construction and failure diagnosis.
- Regression tests using fake Codex binaries; no tests hit the live model
  service.
- Troubleshooting documentation and planning evidence.

Out of scope:

- Adding a local model HTTP proxy.
- Guessing or injecting unsupported AIDP sticky-routing headers.
- Changing internal profile model, provider, endpoint, credentials, or
  `wire_api`.
- Rebinding internal mode to the Desktop App bundle.
- Running DevFlow project skill-layout migration.
- Archiving this or any other OpenSpec change.

## Completion Contract

- [ ] OpenSpec scenarios cover tool-follow-up smoke, sanitized resource
      mismatch diagnostics, JSON reports, and one-key switch forwarding.
- [ ] Regression tests fail before implementation and pass after.
- [ ] `codex-switch verify <profile> --responses-tool-smoke` runs a
      tool-follow-up `codex exec --json` command with the target profile
      `CODEX_HOME`.
- [ ] Azure resource mismatch output is reported as an internal Responses
      resource-stickiness problem.
- [ ] Reports include structured, sanitized smoke diagnostics.
- [ ] Troubleshooting documentation records the scenario, evidence to capture,
      local command, and upstream fix requirement.
- [ ] Focused tests, full Python regression, syntax checks, OpenSpec
      validation, and diff checks pass or blockers are recorded.
