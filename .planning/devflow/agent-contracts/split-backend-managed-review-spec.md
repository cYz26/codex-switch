# Agent Task Contract: SPLIT-BACKEND-MANAGED-REVIEW-SPEC

- Goal: independently review task 13 implementation against the active
  `independent-app-cli-profiles` proposal/design/spec/tasks.
- Scope: read only `scripts/codex_switch_plugins.py`,
  `scripts/test_codex_shared_materialization.py`, README, SKILL, and the active
  OpenSpec change; focus on installed/available provenance, source/target
  independence, post-add proof, precise findings, and functional-CLI contract.
- Constraints: no writes, no live Codex/Plugin/App commands, no network, no
  dependency/Git/release/archive/cleanup effects; preserve unrelated dirty work.
- Verification: map every task-13 scenario to production behavior and a public
  test; identify missing, incorrect, or extra behavior with file/line evidence.
- Evidence: concise PASS or actionable findings, separating blockers from
  non-blocking observations.
- Human Gate: stop if resolution would require persistence schema, dependency,
  App mutation, cache copy/delete, or scope beyond task 13.
