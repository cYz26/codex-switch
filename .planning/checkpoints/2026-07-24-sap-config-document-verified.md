# Checkpoint: SAP Config Document Verified

Date: 2026-07-24

## Active Goal

Continue goal `019f8f8f-e64c-7093-af73-2c0247cf2891`. TPS and CRB are complete.
SAP is active. FSR, integration, and final verification remain pending.

## Completed Slice

SAP tasks 3.1-3.5 passed main review and are checked complete.

The source implementation:

- uses `tomllib` for TOML semantics and a scanner only for complete spans;
- preserves quoted/dotted keys, CRLF, comments, and multiline values;
- reparses every changed document and retains byte-identical no-ops;
- recovers `[[skills.config]]` only by parsed lexical `path` identity;
- skips ambiguous or unknown array entities with stable diagnostics;
- honors protected ancestor, equal, and descendant paths;
- migrates offline merge/overlay callers to the Config Document seam;
- keeps current Plugin/Skill usage state authoritative across switch, restart,
  and snapshot paths;
- removes malformed-TOML fallback acceptance;
- resolves or pins Python 3.11+ with `tomllib` before the affected entrypoints
  mutate profile state.

## Review Closure

The first full transaction run produced two errors because an older adopted-home
authority test used plain sentinel text as `config.toml`. That fixture was
changed to valid TOML while retaining byte-exact restore and directory-mode
assertions. The focused authority test and complete transaction suite then
passed. Main review found no remaining task 3.x blocker.

The old line-only table helper definitions have no supported caller. They remain
only until the explicit task 5.2 cleanup gate.

## Fresh Evidence

- Config Document Python 3.12: 24/24 passed.
- Runtime binding Python 3.12: 55/55 passed.
- Transaction Python 3.12: 211/211 passed.
- Profile Python 3.12: 136/136 passed.
- Protocol Python 3.12: 27/27 passed.
- Protocol Python 3.9: 27/27 passed.
- Strict `schema-scoped-app-proxy` OpenSpec validation: passed.
- Bash syntax: passed.
- Python 3.9 and 3.12 syntax compile for seven affected files: passed.
- `git diff --check`: passed.

## Remaining SAP Work

- Tasks 4.1-4.3: canonical launcher preparation.
- Tasks 5.1-5.5: real-chain integration, cleanup, and final verification.

## Safety Boundary

No ChatGPT restart, live profile switch, install/update, plugin mutation,
release, commit, tag, push, or rollout edit ran. Preserve the dirty worktree and
obtain explicit authorization before any external-effect gate.

The official latest-version comparison remains INC-006
`BLOCKED_AWAITING_HUMAN` outside the active Goal.

## Exact Resume Point

Start SAP task 4.1 with launcher-entrypoint symlink and policy-equivalence RED
tests, then implement tasks 4.2-4.3 through the canonical home-sync seam.
