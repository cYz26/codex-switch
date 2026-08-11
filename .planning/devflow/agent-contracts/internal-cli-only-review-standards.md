# Agent Task Contract: INTERNAL-CLI-ONLY-REVIEW-STANDARDS

- Goal: independently review the current CLI-only implementation for documented
  engineering-standard violations and material code smells.
- Scope: only the `internal-cli-only-runtime` implementation seams named in its
  OpenSpec design/tasks; unrelated dirty-worktree changes are excluded.
- Constraints: read-only; no source, test, control-plane, cache, install, App,
  provider, Git, release, or archive mutation.
- Write set: none.
- Verification: cite exact files/lines or symbols and distinguish blocking
  correctness issues from judgement-call smells.
- Evidence: return a concise findings list to the main agent; "no findings" is
  valid only after inspecting production and test seams.
- Human Gate: any proposed scope expansion or mutation returns to the main
  agent; the reviewer never applies a fix.
