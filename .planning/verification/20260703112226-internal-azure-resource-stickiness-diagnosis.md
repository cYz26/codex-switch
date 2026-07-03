# Internal Azure Resource Stickiness Diagnosis

Date: 2026-07-03

## Symptom

The internal profile can complete a plain text `codex exec --json` request, but
fails after a shell tool call when Codex submits the tool-result follow-up to
the Responses API.

Observed service error:

```text
The requested item was created under a different Azure OpenAI resource. Use the same resource that created the item to access it.
```

## Evidence

Fresh-thread failures were found in the internal Codex state database for
threads created on 2026-07-02 around 18:39-18:41 local time, including
`019f2269-4973-7c11-b32f-413e3936acab` and
`019f226a-39bf-71a3-b522-9ae952421731`. These were internal-profile threads
using provider `azure` and model `gpt-5.5-2026-04-24`, so the symptom is not
limited to an old conversation context.

Local smoke checks on 2026-07-03 showed:

- Plain text smoke with the internal profile completed successfully.
- Tool-result smoke with the same profile reproduced the Azure resource error.
- Lowering reasoning effort to `low` or `none` did not avoid the error.
- Switching `wire_api` to `chat` is not supported by the current internal
  Codex binary.
- Overriding the model to the returned deployment name failed model/product
  validation.
- Enabling `responses_websockets` or `responses_websockets_v2` did not avoid
  the error.

The low-noise client trace for the failing tool-result smoke showed the first
`/responses` request succeeded with:

- `x-account-deployment: deployment-gpt-5.5-2026-04-24-platform-global`
- `x-account-id: globalttswedencentral010`
- `x-model-request-id: b1ce23f9-e838-47c5-a705-afa2564e4409`
- `x-tt-logid: 20260703112009D6B58AAAD12F032ED7AB`

The follow-up `/responses` request after the tool result failed with 400 and:

- `x-account-deployment: deployment-gpt-5.5-2026-04-24-platform-global`
- `x-account-id: globalttswedencentral053`
- `x-model-request-id: 741c1f3e-fad4-48be-abe0-d0c2e99b3506`
- `x-tt-logid: 202607031120158DCF6A7C87F2A6AF4908`

No credentials or query secrets are recorded in this evidence.

## Diagnosis

The failing request pair stays within the same local Codex invocation and the
same returned deployment, but AIDP routes the initial Responses request and the
tool-result follow-up to different Azure OpenAI resource/account IDs. The
Responses context contains service-owned response/reasoning items created under
the first resource. The follow-up request then lands on a different resource,
which cannot access those items and returns the observed resource mismatch
error.

The current `scripts/codex_switch_app_proxy.py` only proxies Desktop app-server
JSON-RPC and model/config/thread messages. It does not sit in the model HTTP
`/responses` path, so codex-switch cannot directly repair AIDP resource
routing without adding a new HTTP proxy or receiving a supported sticky routing
mechanism from the internal backend/AIDP side.

## Current Local Gap

The existing `--runtime-smoke` verification checks `codex --version` and
`codex plugin list --json`; it does not exercise a Responses tool-result
follow-up. This allowed internal mode to look healthy even though the real
Desktop/tool-call path was broken. The existing `--exec-smoke <prompt>` is
model-backed, but it only catches this failure when the provided prompt forces
a tool call and follow-up.

## Local Verification

Baseline verification command:

```bash
PYTHONPATH=scripts python3 -m unittest scripts.test_codex_profile_switch.CodexProfileSwitchTests.test_verify_runtime_smoke_runs_profile_codex_with_target_home
```

Result: pass, 1 test.

DevFlow migration sync command:

```bash
python3 /Users/cY/dev/skills/cy-codex-skills/dev/plugins/dev-flow/scripts/plugin_project_migration.py --repo /Users/cY/dev/codex-switch --json
```

Result: sync succeeded with `status: migration_pending`. Runtime and stored
DevFlow versions both remain `0.3.0+codex.20260529145038`; the pending work is
official skill-layout migration involving legacy duplicates and conflicts under
`.codex/skills` and `.agents/skills`. No migration apply command was run
because this repair does not require project skill-layout mutation.

## Repair Direction

The durable upstream repair is for AIDP/Azure routing to keep all requests that
share a Responses context on the same Azure OpenAI resource, or to expose a
supported sticky routing key that Codex can send on follow-up requests.

The local codex-switch repair should harden verification so internal Azure
Responses profiles have an explicit tool-follow-up smoke that fails with a
clear, sanitized resource-stickiness diagnosis instead of reporting internal
mode healthy.

Archive remains closed. No archive action was taken.
