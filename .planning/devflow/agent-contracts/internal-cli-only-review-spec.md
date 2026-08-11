# Agent Task Contract: INTERNAL-CLI-ONLY-REVIEW-SPEC

- Goal: independently compare the current CLI-only implementation with
  `openspec/changes/internal-cli-only-runtime/specs/codex-switch/spec.md`.
- Scope: missing/partial requirements, incorrect behavior, and scope creep in
  the target change only; unrelated dirty-worktree changes are excluded.
- Constraints: read-only; no source, test, control-plane, cache, install, App,
  provider, Git, release, or archive mutation.
- Write set: none.
- Verification: trace every requirement scenario to current code and focused
  tests, citing exact files/lines or symbols.
- Evidence: return a concise findings list to the main agent; explicitly state
  if all scenarios are covered.
- Human Gate: any proposed scope expansion or mutation returns to the main
  agent; the reviewer never applies a fix.
