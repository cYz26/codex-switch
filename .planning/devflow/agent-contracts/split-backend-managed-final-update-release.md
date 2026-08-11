# Agent Task Contract: SPLIT-BACKEND-MANAGED-FINAL-UPDATE-RELEASE

- Goal: run the final read-only update/release regression suite against the
  current task-13 source bytes.
- Scope: execute `scripts/test_codex_update_release.py -v` only; inspect
  failures without edits.
- Write set: none; test-owned temporary directories outside the repository are
  permitted and must be left to the test harness.
- Constraints: no repository writes, no live Codex/Plugin/App commands, no
  network, no dependency, Git, release, archive, cleanup, or workstation
  mutation; preserve unrelated dirty work.
- Verification: report exact command, Python version, count, duration, and
  complete failure details if any.
- Evidence: concise PASS/FAIL with terminal summary.
- Human Gate: stop on any test requiring live state, source edits, or expanded
  effects and report the blocker to main.
