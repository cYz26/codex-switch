# Design: Internal Responses Resource Stickiness Verification

## Skill Routing Ledger

- Request kind: bug repair and scenario documentation for internal Azure
  Responses tool-follow-up failures.
- Workflow mode: brownfield, OpenSpec-required compatibility and error
  handling change.
- `plugin-project-migration`: used as a sync-only DevFlow drift check; apply
  was not run.
- `capability-research`: used during diagnosis. Microsoft Azure Responses docs
  and local traces establish that Responses is stateful and that reasoning
  context must carry across turns.
- `superpowers:systematic-debugging`: used during diagnosis to isolate plain
  text success from tool-follow-up failure.
- `superpowers:writing-plans`: used; canonical plan content is recorded in
  this OpenSpec change.
- `superpowers:test-driven-development`: required for implementation.
- OpenSpec routing: new change `internal-responses-resource-stickiness`.
- GSD routing: not required; this is a narrow repair, not phase planning.

## Target State

`codex-switch verify <profile> --responses-tool-smoke` performs the existing
local verification and additionally runs a deterministic model-backed smoke
that forces Codex to call the shell tool and then submit the result back to the
Responses API. The smoke uses the target profile `CODEX_HOME`, the configured
profile `codex_bin`, an ephemeral exec session, read-only sandboxing, and a
fixed prompt with a harmless `printf` command.

If the smoke fails with the Azure resource mismatch message, codex-switch
reports a named internal Responses resource-stickiness problem. When debug
headers are present in the output, codex-switch extracts only sanitized routing
fields and records them in the JSON report.

## Boundary

The local repair is diagnostic and preventative. It prevents internal mode from
being considered healthy when the Responses tool-follow-up path is broken, and
it produces a clear upstream handoff. The durable service repair remains with
AIDP/internal backend routing: every request that shares a Responses context
must stay on the same Azure OpenAI resource, or the service must provide a
supported sticky routing key for clients.

codex-switch currently proxies Desktop app-server JSON-RPC only. It does not
sit in the model HTTP `/responses` path and should not add an unsupported local
HTTP proxy in this change.

## CLI Design

- Add `--responses-tool-smoke` to `codex-switch verify <profile>`.
- Add the same flag to one-key `codex-switch internal` / `official` forwarding,
  parallel to existing `--runtime-smoke`, `--exec-smoke`, and
  `--verification-report`.
- Keep `--runtime-smoke` unchanged: it remains local runtime startup and plugin
  listing only.
- Keep `--exec-smoke <prompt>` unchanged for caller-provided model smoke.

## Diagnostic Model

Add a small structured diagnostic object for smoke failures:

- `kind`: currently `azure_responses_resource_mismatch` when detected.
- `message`: stable user-facing diagnosis.
- `accounts`: unique `x-account-id` values found in output.
- `deployments`: unique `x-account-deployment` values found in output.
- `model_request_ids`: unique `x-model-request-id` values found in output.
- `tt_log_ids`: unique `x-tt-logid` values found in output.

The diagnostic also recognizes `Item with id 'rs_…' not found`:

- `kind`: `responses_reasoning_item_unavailable`;
- `item_ids`: unique unavailable `rs_` identifiers;
- `message`: stateless continuation requires encrypted reasoning content or
  stable upstream item routing;
- the same allowlisted routing headers remain available for upstream triage.

The parser must be conservative:

- It recognizes the exact resource mismatch service message.
- It recognizes only `rs_` IDs from the exact item-not-found service message.
- It extracts only known safe header fields.
- It must not expose query parameters, API keys, authorization headers, bearer
  tokens, or arbitrary large raw output in structured report fields.

## Documentation

Create `docs/troubleshooting/internal-azure-responses-resource-stickiness.md`.
The document records:

- Symptoms and the exact service message.
- Why fresh threads still fail.
- The local command to run.
- How to interpret mismatched `x-account-id` values.
- The upstream owner contract for AIDP/internal backend routing.
- Why codex-switch verification is the local repair boundary.

## Capability Slices

### Slice 1: OpenSpec and troubleshooting contract

Record the behavior and scenario documentation before implementation.

### Slice 2: Failing verifier tests

Add regression tests for:

- The new CLI flag runs a deterministic tool-follow-up `codex exec --json`.
- Azure resource mismatch output produces the stable diagnostic.
- JSON reports include sanitized structured diagnostics.
- One-key switch forwarding passes the new flag to `verify`.

### Slice 3: Verifier implementation

Implement the smallest helpers in `scripts/codex_switch_verify.py`, register
CLI flags in `scripts/codex_profile_switch.py`, and update
`scripts/codex-switch` forwarding.

### Slice 4: Documentation and verification

Add troubleshooting docs, run focused and broad validation, update OpenSpec
tasks, record verification evidence, and update `.planning/STATE.md`.

## Acceptance Criteria

- [ ] A fake Codex binary proves the tool-follow-up smoke command runs with
      target profile `CODEX_HOME`.
- [ ] A fake Azure resource mismatch output causes verification to fail with a
      stable internal Responses resource-stickiness diagnosis.
- [ ] JSON verification report contains sanitized diagnostics and does not
      contain secrets from arbitrary output.
- [ ] One-key switch commands forward `--responses-tool-smoke` to target
      verification.
- [ ] Troubleshooting docs explain the scenario and upstream repair contract.

## Validation Commands

```bash
PYTHONPATH=scripts python3 -m unittest \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_runs_profile_codex_with_target_home \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_responses_tool_smoke_reports_azure_resource_mismatch \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_report_includes_sanitized_responses_tool_smoke_diagnostics \
  scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_one_key_switch_forwards_responses_tool_smoke_to_verify
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests
python3 -m py_compile scripts/*.py
openspec validate internal-responses-resource-stickiness --strict --no-interactive
openspec validate --all --strict --no-interactive
git diff --check
```

## Risks / Rollback

The new smoke is service-backed and can fail because of external service
health, credentials, or model availability. Keeping it opt-in avoids changing
ordinary switch behavior. Rollback removes the flag, helper, tests, and
troubleshooting doc; existing runtime and exec smoke behavior remains intact.
