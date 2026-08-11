# Agent Task Contract: SPLIT-BACKEND-MANAGED-REVIEW-STANDARDS

- Goal: independently review task 13 implementation for repository standards,
  safety, regressions, and deep-module locality.
- Scope: read only `AGENTS.md`, `ENGINEERING_POLICY.md`,
  `scripts/codex_switch_plugins.py`, focused shared tests, README, and SKILL;
  inspect path/link safety, error taxonomy, config restoration, lease/CAS,
  batching, compatibility, and code smells.
- Constraints: no writes, no live Codex/Plugin/App commands, no network, no
  dependency/Git/release/archive/cleanup effects; preserve unrelated dirty work.
- Verification: reason from current source and focused tests; cite exact
  file/line evidence for every hard finding and label judgement-call smells.
- Evidence: concise PASS or findings ordered by severity, plus residual risks.
- Human Gate: stop if a fix requires a public contract, persistence schema,
  dependency, App mutation, cache copy/delete, or scope beyond task 13.
