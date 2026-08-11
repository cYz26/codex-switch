# Evidence: DEVFLOW-REFRESH-20260804

## Claim

The installed `dev-flow@cy-codex-skills` cache and the safe project-local
workflow surfaces were refreshed from DevFlow
`0.3.0+codex.20260529145038`. The active project now uses the refreshed
DevFlow links, verified OpenSpec 1.7 skills, a namespaced DevFlow state, and a
current plugin-project migration receipt. Existing parity work and legacy
workflow artifacts were preserved.

This receipt does not claim that legacy skill-layout cleanup or provider-state
migration is complete. Those remain separate Human Gates.

## Commands Run

| Command | Exit | Evidence File / Output Summary |
|---|---:|---|
| `python3 .../scripts/devflow_runtime.pyz/activate_project_dependencies.py --repo /Users/cY/dev/codex-switch --skip-official-installs --migrate-official-skill-layout --dry-run --json` | 1 | The generated recommendation incorrectly treated the zipapp as a directory and reproduced `can't find '__main__' module`. |
| `python3 .../scripts/activate_project_dependencies.py --repo /Users/cY/dev/codex-switch --skip-official-installs --migrate-official-skill-layout --dry-run --json` | 0 | Correct adjacent launcher completed read-only preflight and exposed project skill-source conflicts plus OpenSpec 1.6 to 1.7 drift. |
| `CODEX_HOME=/Users/cY/.codex /Applications/ChatGPT.app/Contents/Resources/codex plugin add dev-flow@cy-codex-skills --json` | 0 | Installed/refreshed DevFlow `0.3.0+codex.20260529145038` under `/Users/cY/.codex/plugins/cache/...`. |
| `python3.12 /Users/cY/dev/skills/cy-codex-skills/dev/scripts/codex_auto_update_plugins_skills.py --json` | 0 | Final `plugin-cache-verify` status for DevFlow is `matches-source`. |
| `python3.12 .../activate_project_dependencies.py --repo /Users/cY/dev/codex-switch --codex-home /Users/cY/.codex --refresh-project-skills --dry-run --json` | 0 | Planned 16 DevFlow link refreshes and six isolated OpenSpec 1.7 copy refreshes. |
| `python3.12 .../activate_project_dependencies.py --repo /Users/cY/dev/codex-switch --codex-home /Users/cY/.codex --refresh-project-skills --apply --json` | 0 | Applied 16 `refreshed-link` and six `refreshed-copy` actions; isolated OpenSpec generation reported no version or inventory mismatches. |
| `python3.12 .../plugin_project_migration.py --repo /Users/cY/dev/codex-switch --codex-home /Users/cY/.codex --apply --json` | 0 | Wrote migration state/history/report; no stale project skill, missing skill, or conflict remained in the ordinary migration surface. |
| `cp -p .planning/STATE.md .planning/devflow/STATE.md` plus `cmp` and SHA-256 | 0 | Added the canonical namespaced state without modifying or deleting the legacy state; both source snapshots initially had SHA-256 `c3d7119b3166c45f010f68701be70a523be23e1cb0f0afa8375b99fcbb1dfb60`. |
| `python3.12 .../validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json` | 0 | `ok: true`, zero issues, zero warnings; active parity stage and Human Gate preserved. |
| `python3.12 .../doctor_workflow.py --repo /Users/cY/dev/codex-switch --check-cache-drift --json` | 0 | `diagnosis: healthy`, zero issues, `No workflow repair needed.` |
| `python3.12 .../activate_project_dependencies.py --repo /Users/cY/dev/codex-switch --skip-official-installs --migrate-official-skill-layout --dry-run --json` | 0 | Final read-only layout plan: 16 DevFlow skills `already-linked`, six OpenSpec skills `already-present`, 12 `legacy_duplicate`, and 19 unmanaged GSD skills `manual_review_required`. |
| `openspec --version` and `openspec validate internal-official-feature-parity --strict --json` | 0 | OpenSpec `1.7.0`; one change passed, zero failed. |
| `git diff --check` | 0 | Existing tracked diff has no whitespace error. |
| `python3.12 .../scaffold_workflow.py --repo /Users/cY/dev/codex-switch --mode auto --dry-run --json` | 0 | Brownfield dry-run only; no scaffold plan was applied. |

## TDD Evidence

- RED: not applicable; this was a plugin/cache and project workflow refresh,
  not a production behavior implementation.
- GREEN: dependency transaction verification, workflow validation, Doctor,
  OpenSpec strict validation, JSON validation, SHA-256, and `cmp` are recorded
  above.
- Regression check: active OpenSpec change remains valid under OpenSpec 1.7.0,
  and the current parity Human Gate remains unchanged.

## Changed Files

- `.agents/skills/`: 16 DevFlow links refreshed to the installed cache and six
  OpenSpec skill copies refreshed from verified isolated OpenSpec 1.7 output.
- `.planning/devflow/STATE.md`: canonical namespaced state created from the
  current root state, then this refresh checkpoint appended.
- `.planning/devflow/plugin-project-migration/state.json`: installed runtime
  version receipt.
- `.planning/devflow/plugin-project-migration/migration-history.jsonl`: apply
  history receipt.
- `.planning/devflow/plugin-project-migration/reports/latest.json`: latest
  migration report.
- `.planning/devflow/verification/20260804T155336-devflow-refresh.md`: this
  verification receipt.
- `/Users/cY/.codex/plugins/cache/cy-codex-skills/dev-flow/0.3.0+codex.20260529145038`:
  refreshed global cache outside the repository.

No existing parity source, test, OpenSpec, ledger, checkpoint, or legacy
workflow file was modified by this refresh.

## Risks / Gaps

- Migration sync remains `migration_pending` because 12 matching
  `.codex/skills` entries are `legacy_duplicate`; the final layout dry-run also
  retained 19 unmanaged GSD skills as `manual_review_required`. Cleanup was
  not authorized and none was performed.
- The read-only legacy inspector also found four broken legacy Superpowers
  links and several ownership-ambiguous GSD/runtime paths. All were preserved
  for a separately approved exact-path cleanup review.
- `AGENTS` status is `conflict`: the latest generated template changes workflow
  ownership to the newer OpenSpec/DevFlow/Matt contract, while the active
  project rules require a separate provider-state migration apply gate. Active
  `AGENTS.md` was not overwritten.
- `.dev-flow.json` remains absent and the validated default is
  `full-openspec`; no provider selection or lock was synthesized from the
  missing file.
- A new Codex task/session is recommended before relying on newly refreshed
  project skills, because already-running tasks may retain the old skill
  inventory.

## Reviewer Notes

- Existing uncommitted parity work was preserved and remains outside this
  refresh write set.
- No commit, push, release, archive, App restart, profile mutation, provider
  migration, or legacy cleanup was performed.
- The active `PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT` Human Gate remains the
  next parity-development decision and was not broadened by this maintenance.
