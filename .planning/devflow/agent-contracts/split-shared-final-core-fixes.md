# Agent Task Contract

## Goal
Close the independent final-review blockers in the shared desired-state core so App/CLI Plugin and Skill synchronization is secret-safe, cache-attested, target-CAS protected, stopped-App safe, deterministic with retained versions, and recoverable across every persistent commit boundary.

## Worker ID
`split-shared-final-core-fixes`

## Stable Input Snapshot
- `scripts/codex_switch_shared_configuration.py`: `06c5c144919241b80d0bfdd4782016bf88a2490c2cb751f98ca6d06cafb5f1d3`
- `scripts/test_codex_shared_configuration.py`: `e2753072906ff693289790a88e4cc3cf48e4d85f0645ac6cc1d6e5af264c94ac`
- `scripts/test_codex_shared_materialization.py`: `e18d66108e73f181876e4b9028564b8f1867be51dd83c3befca807d4ba3fe74b`
- OpenSpec design: `19b0a6c8b85c840ecb5ae63f10a58959b4785cd82b19272548fbdc50b5f4a43e`
- OpenSpec spec: `6b507cfc85f2c3db0ce73da69425fa7159227df51862e174457b194666533089`
- OpenSpec tasks: `a66f0d4d9ae300b2a96382d918f424090398bd3538153ceb53caac99041210ab`

Stop before editing if the production hash differs. Tests and OpenSpec are read-only inputs for this worker; report if their hashes drift. Main may independently edit other disjoint files only.

## Scope
Allowed write set for worker `split-shared-final-core-fixes` only:
- `scripts/codex_switch_shared_configuration.py`

Read adjacent store, IO, process-inventory, plugin-attestation, transaction-lock, config-document, and tests as needed. Forbidden: every other write, including tests, OpenSpec, control plane, docs, release files, live homes/caches/App/processes, network/backend/plugin commands, dependencies, cleanup, Git, release, or archive.

## Constraints
Read `.agents/skills/diagnosing-bugs/SKILL.md` and `.agents/skills/tdd/SKILL.md` fully. Use only standard-library code and preserve existing public seams. Treat the new failing tests as canonical RED; do not weaken them. Preserve unrelated WIP and exact physical cache retention.

Implement the updated OpenSpec systemically:

1. Screen marketplace values as well as names. URL-like source values reject userinfo, credential-like query keys, and fragments with `shared_configuration.secret_value`; rejected bytes never enter store state/generations. Avoid broad false positives for ordinary local paths and refs.
2. Normalize Plugin-Skill paths by resolving existing source routes, rejecting `..`, special files, and symlink escape. Target remapping must resolve inside the attested target artifact/cache and reject missing/escaped roots.
3. Re-attest every stored materialization receipt against actual target manifest/version/tree/Skill roots before `cli_ready`. Missing/corrupt cache makes report non-ready; apply creates a same-generation repair plan and re-materializes. Never reuse an unattested retained receipt in `_local_materializations`.
4. Validate state schema deeply enough to bind `projection_sha256`, immutable generation payload, baselines, and receipts. Missing state still checks unsafe cache/personal-Skill ownership before returning bootstrap-required.
5. Make App-stopped proof fail closed on process-inventory failure and on a recognized Desktop or any relevant app-server, including mismatched binding. Recheck stopped state at commit after materialization. Keep the injectable adapter seam.
6. Add target raw-config CAS from the locked plan through commit. A concurrent target change returns `shared_configuration.target_changed_during_plan`, preserves the foreign edit, and writes no shared state/config/link/generation.
7. Multiple retained local versions without a deterministic configured Skill path or attested active identity return `shared_configuration.materialization.ambiguous_cache`; never silently downgrade `portable_exact`. Preserve a stored target `backend_managed` policy on later observations so identical semantic changes do not become false conflicts merely because the target cache now exists.
8. Add one prepared journal at `shared-configuration/pending-commit.json`. Before the first config/link/generation/state effect, bind predecessor state, source/target CAS, exact target file kind/bytes/mode, Skill-link predecessor, planned projection, receipts, collision-safe generation payload, and expected commit identity. `state.json` is the only commit point. Use checkpoint callbacks named `prepared`, `target_config_written`, `personal_skills_link_created`, `generation_published`, and `state_published` after each durable boundary.
9. At the start of every apply under the store lock, classify/recover the journal before planning. If committed state matches, complete cleanup; otherwise rollback only an expected transaction-produced config/link state. Foreign drift blocks. Retain orphan immutable generation files and allocate the next unused monotonic generation so a different retry cannot collide. Plan/report modes are read-only and return `shared_configuration.pending_recovery` while a journal exists.
10. Reject symlink/non-regular target config before materializer snapshot or publication; never follow and mutate an external target through a config symlink. Normal exceptions rollback; BaseException checkpoint interruptions deliberately leave recoverable journal evidence.

## Verification
Run and return exact results for:

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest scripts.test_codex_shared_configuration
PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=scripts python3.12 -m unittest scripts.test_codex_shared_configuration scripts.test_codex_shared_materialization scripts.test_codex_shared_lifecycle
PYTHONDONTWRITEBYTECODE=1 python3.12 -m py_compile scripts/codex_switch_shared_configuration.py
openspec validate independent-app-cli-profiles --strict --no-interactive
git diff --check -- scripts/codex_switch_shared_configuration.py
```

Also report named results for each new final-review regression, journal recovery checkpoint, and the formerly regressed identical-semantic coalescing test. Do not run live backend/plugin commands.

## Evidence
Return `DONE`, `DONE_WITH_CONCERNS`, or `BLOCKED` and report:
- changed files and final hashes;
- commands run;
- complete test logs or validation results with exact RED/GREEN counts;
- mapping of every numbered constraint to code and named tests;
- journal ordering and recovery behavior;
- unverified areas;
- risk notes and incidental-finding classification.

## Human Gate
The worker must wait for human review and report `BLOCKED_AWAITING_HUMAN` before any scope/write-set expansion, changing a public API or profile compatibility contract, adding a dependency, touching a forbidden path, weakening fail-closed behavior, skipping required validation, continuing with failing tests or unverified severe risk, mutating live state, executing a backend/plugin/network operation, deleting retained cache/generation evidence, or performing Git/install/release/archive/cleanup effects.

## Follow-up Amendment 2026-08-05

Stable inputs for this follow-up replace the original snapshot:

- `scripts/codex_switch_shared_configuration.py`: `a87afb7ecd338247efb4cb1e06c43d8cfbb2abc3daa9cbbddd663b7dd29f5ec3`
- `scripts/test_codex_shared_configuration.py`: `bdd3d1591b422f5ada65bc7561c6c92396d183114e18bc0dda785bbe755e047a`
- `scripts/test_codex_shared_materialization.py`: `8cbef96c486fd9310a1f8852c6a43bc6f18cf4f2d46055d7eeb7f61329f3358d`
- OpenSpec design: `211a9898509ccb3ec5b9834a3c0caa08c93b086eedbd35f4ab1cc42b9fa4eebe`
- OpenSpec spec: `390b86a3a51b2a4c0a0eb4e2c8ec29ffbfd7ee0ff85319443df7b4da5ba073a6`
- OpenSpec tasks: `48f64f5e8ff2ff6728c228c26c05a5158dcf20bec3af1cfdabd9aafb1748c6be`

Close these additional canonical REDs without editing tests:

1. Re-attestation must compare actual manifest version, tree digest, and Skill
   roots to the supplied committed/materializer receipt for every policy.
   Backend cache drift must enter same-generation internal repair, never become
   a CLI-originated generation pending to the App.
2. `_materialize_plan` must not blindly restore target config bytes. Any adapter
   that returns with a changed target config must yield
   `shared_configuration.target_changed_during_plan` while preserving the
   foreign bytes. Production-native expected config isolation belongs to the
   disjoint plugin worker.
3. Before first journal publication, create the shared and generations
   directories privately and durably: fsync each newly created directory's
   parent so power loss cannot lose the journal's directory entry after later
   target effects.

Named REDs:

- `test_backend_managed_tree_drift_repairs_without_promoting_cli_state`
- `test_target_config_change_during_materialization_is_preserved`
- `test_first_prepared_journal_durably_publishes_new_directory_entries`
