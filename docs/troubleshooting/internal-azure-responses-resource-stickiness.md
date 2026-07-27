# Internal Azure Responses Resource Stickiness

## Symptom

Internal Azure Responses requests can complete for plain text prompts but fail
after Codex calls a tool and submits the tool result back to the model.

The service error is:

```text
The requested item was created under a different Azure OpenAI resource. Use the same resource that created the item to access it.
```

The same upstream continuity defect can also surface as:

```text
Item with id 'rs_...' not found.
```

When the request uses `store=false`, reasoning items must carry returned
`reasoning.encrypted_content` for stateless continuation. A bare `rs_` ID is a
remote reference and can fail after resource rerouting or loss of upstream item
state.

Fresh threads can reproduce the same failure. That means the problem is not
necessarily stale local conversation state or an old Desktop thread.

## Why This Happens

Responses tool workflows are multi-step:

1. Codex sends an initial `/responses` request.
2. The model asks Codex to run a tool.
3. Codex submits the tool result as a follow-up request in the same Responses
   context.

The follow-up must reach the same Azure OpenAI resource that created the
context items in the initial request. If AIDP routes the initial request to one
Azure resource and the follow-up to another, Azure cannot access the
resource-bound item and returns the mismatch error.

The clearest evidence is a single smoke run where safe routing headers differ
between the initial request and the follow-up, for example:

```text
x-account-id: globalttswedencentral010
...
x-account-id: globalttswedencentral053
```

Do not record API keys, authorization headers, bearer tokens, query-string
secrets, or raw credential-bearing URLs in issue notes.

## Local Verification

Run the explicit Responses tool-follow-up smoke after internal backend updates
or when internal Desktop fails after a tool call:

```bash
codex-switch --skip-self-update verify internal --responses-tool-smoke --report
```

For a full post-switch check:

```bash
codex-switch internal --responses-tool-smoke --verification-report
```

This smoke is opt-in because it uses the configured model service. Ordinary
`--runtime-smoke` remains a local runtime startup and plugin-listing check; it
does not exercise the model tool-result follow-up path.

## Expected Failure Diagnosis

When the Azure resource mismatch is detected, codex-switch reports an internal
Responses resource-stickiness failure and records sanitized fields in the JSON
verification report:

- `accounts` from `x-account-id`
- `deployments` from `x-account-deployment`
- `model_request_ids` from `x-model-request-id`
- `tt_log_ids` from `x-tt-logid`

These fields are enough to hand the failure to the AIDP/internal backend owner
without exposing credentials.

## Ownership Boundary

codex-switch cannot directly repair AIDP resource routing. The Desktop app
proxy only handles app-server JSON-RPC between Desktop and the configured
profile backend; it does not proxy model HTTP `/responses` traffic.

For Desktop memory-history resume, codex-switch can prevent a known-bad replay
from blocking the whole thread: it removes server-owned item IDs and omits only
reasoning entries that have no encrypted content, content, or summary. This is
a degraded-continuity fallback, not a substitute for the upstream fix; prior
hidden reasoning is unavailable, while visible messages and tool history remain.

The durable upstream repair is one of:

- AIDP routes every request that shares a Responses context to the same Azure
  OpenAI resource.
- The internal backend/AIDP service provides a supported sticky routing key
  that clients can send on follow-up and retry requests.

The local codex-switch repair is to make the failure visible during
verification and to preserve sanitized evidence for the upstream owner.
