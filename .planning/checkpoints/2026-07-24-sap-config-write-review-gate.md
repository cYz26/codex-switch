# Checkpoint: SAP Config-Write Receipt Review Gate

Date: 2026-07-24

## Active Goal

Continue goal `019f8f8f-e64c-7093-af73-2c0247cf2891`. TPS and CRB are complete.
SAP is active. FSR, integration, and final verification remain pending.

## Current Outcome

SAP tasks 2.1-2.5 have an implementation candidate and focused validation, but
are not complete until the main change-review gate closes.

The candidate:

- creates a backend/schema-digest-bound schema-v2 capability receipt;
- generates the receipt from isolated schema generation and a temporary-home
  behavioral config-write probe;
- persists only sanitized capability state and digests;
- supplies the receipt and expected schema digest through the managed launcher;
- blocks every unproven config write before backend or filesystem mutation;
- forwards a proven write once and returns the backend response/version;
- removes the proxy's former post-response compensating config write.

## Fresh Evidence

- Python 3.12 protocol suite: 23/23 passed.
- Python 3.9 protocol suite: 23/23 passed.
- Strict `schema-scoped-app-proxy` OpenSpec validation: passed.
- Python 3.12 compile for adapter, proxy, and wrapper: passed.
- `git diff --check`: passed.

No ChatGPT restart, live profile switch, install/update, plugin mutation,
release, commit, tag, push, or rollout edit ran.

## Open Review Gate

Review the tasks 2.1-2.5 diff against:

- `openspec/changes/schema-scoped-app-proxy/`;
- `.planning/devflow/agent-contracts/schema-config-write-receipt.md`;
- repository policy in `AGENTS.md` and `ENGINEERING_POLICY.md`.

The review must cover process cleanup/timeouts, receipt and launcher promotion,
backend/schema digest authority, request ordering, fail-closed behavior, stable
diagnostics, and proof that no post-response config repair remains. Fix all
actionable findings and rerun focused plus adjacent regressions before checking
the OpenSpec tasks.

## New Request Boundary

The user separately requested a comparison hint against the latest official
`openai/codex` release, especially during an internal switch. Current evidence
on 2026-07-24:

- latest official stable release: `rust-v0.145.0`;
- latest official prerelease observed: `rust-v0.146.0-alpha.5`;
- current internal profile CLI: `codex-cli 0.144.6`;
- current ChatGPT bundled CLI: `codex-cli 0.145.0-alpha.30`.

This is public CLI behavior outside the active Goal. No implementation or
OpenSpec artifact has been created. Recommended design: compare against the
latest stable release as a read-only, non-blocking advisory; label prerelease
information separately or keep it opt-in; never use the official comparison to
drive the internal installer. Obtain user design approval and resolve Goal
sequencing before starting the dedicated Full OpenSpec change.

## Exact Resume Point

1. Complete the SAP 2.1-2.5 main change review.
2. Fix findings and rerun dual-runtime focused and adjacent suites.
3. Mark tasks 2.1-2.5 complete only after the review gate is green.
4. Continue SAP tasks 3.x-5.x, then FSR and final integration.
5. Handle the official-version advisory only through its separate approved
   Full OpenSpec change.
