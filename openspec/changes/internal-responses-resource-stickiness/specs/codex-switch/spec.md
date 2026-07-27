# Specification Delta: codex-switch

## ADDED Requirements

### Requirement: Internal Azure Responses tool-follow-up smoke

The system SHALL provide an explicit verification option that exercises an
internal Azure Responses shell-tool call followed by the tool-result follow-up.

#### Scenario: Responses tool smoke uses target profile runtime

- GIVEN the requested profile has a configured `codex_bin`
- AND the requested profile has a resolved `CODEX_HOME`
- WHEN the user runs `codex-switch verify <profile> --responses-tool-smoke`
- THEN verification runs the profile `codex_bin` with `CODEX_HOME` set to that
  profile home
- AND the command uses `codex exec --json` with an ephemeral read-only prompt
  that requires a harmless shell tool call and a final response.

#### Scenario: Azure resource mismatch is diagnosed

- GIVEN a Responses tool-follow-up smoke fails with the service message
  `The requested item was created under a different Azure OpenAI resource`
- WHEN verification reports the failure
- THEN the output identifies it as an internal Responses resource-stickiness
  failure
- AND the output explains that the Responses context follow-up must stay on the
  same Azure OpenAI resource.

#### Scenario: Missing reasoning item is diagnosed

- GIVEN a Responses continuation fails with `Item with id 'rs_…' not found`
- WHEN verification reports the failure
- THEN the output identifies an internal Responses reasoning continuity failure
- AND the JSON report records only the unavailable reasoning item ID and known
  safe routing headers
- AND the output explains that stateless continuation requires encrypted
  reasoning content or stable upstream item routing.

#### Scenario: Resource mismatch diagnostics are sanitized in reports

- GIVEN a Responses tool-follow-up smoke output includes safe routing headers
  such as `x-account-id`, `x-account-deployment`, `x-model-request-id`, or
  `x-tt-logid`
- AND the user runs verification with `--report`
- WHEN codex-switch writes the JSON verification report
- THEN the report records those known safe routing fields as structured
  diagnostics
- AND the report does not record credentials, authorization headers, bearer
  tokens, API keys, or raw query strings.

#### Scenario: One-key switches can request Responses tool smoke

- GIVEN a one-key `codex-switch internal` or `codex-switch official` command
  completes the profile switch and reaches verification
- WHEN the command includes `--responses-tool-smoke`
- THEN the post-switch verification command includes
  `--responses-tool-smoke`
- AND existing `--runtime-smoke`, `--exec-smoke`, and
  `--verification-report` behavior remains unchanged.

#### Scenario: Ordinary verification remains local by default

- GIVEN the user runs `codex-switch verify <profile>` without
  `--responses-tool-smoke` and without `--exec-smoke`
- WHEN verification runs
- THEN no model-backed exec smoke is performed
- AND existing active-state, runtime config, plugin support, and optional local
  runtime smoke behavior remains unchanged.
