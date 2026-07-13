# Evidence: dev-flow-refresh-20260713

## Claim

The current repository completed the safe DevFlow refresh scope: the release
asset and installed plugin cache match, project-local DevFlow skills are
current, the six OpenSpec 1.6 skills were refreshed transactionally, and the
latest durable AGENTS guidance was merged without applying the blocked provider
migration or deleting legacy skills.

## Commands Run

| Command | Exit | Evidence File / Output Summary |
|---|---:|---|
| `sync_release_assets.py --repo /Users/cY/dev/skills/cy-codex-skills --target dev-flow --json` | 0 | DevFlow release asset status `current`; no stale or changed outputs. |
| `codex_auto_update_plugins_skills.py --json` | 0 | Installed `dev-flow@cy-codex-skills` cache `matches-source`. |
| `activate_project_dependencies.py --repo /Users/cY/dev/codex-switch --codex-home /Users/cY/.codex --refresh-project-skills --apply --json` | 0 | DevFlow links current; exact six OpenSpec 1.6 skills copied transactionally. |
| `validate_workflow_state.py --repo /Users/cY/dev/codex-switch --json` | 0 | `ok=true`, no issues; only legacy root-state migration warning remains. |
| `doctor_workflow.py --repo /Users/cY/dev/codex-switch --check-cache-drift --json` | 0 | No DevFlow cache drift; repair status is solely the deferred legacy root-state migration. |
| `plugin_project_migration.py --repo /Users/cY/dev/codex-switch --json` | 1 | Expected diagnostic block: provider migration remains blocked; 18 legacy duplicates remain and no migration apply ran. |
| `scaffold_workflow.py --repo /Users/cY/dev/codex-switch --mode auto --dry-run --json` | 0 | Brownfield dry-run completed; `AGENTS.md.generated` candidate reviewed and no generated file remains. |
| `git diff --check` | 0 | No whitespace errors. |

## TDD Evidence

- RED: not applicable; this is workflow configuration and documentation maintenance.
- GREEN: not applicable.
- Regression check: workflow validation, doctor, migration sync, scaffold dry-run, and diff check above.

## Changed Files

- `AGENTS.md`: merged durable control-plane, capability-routing, intake/planning, goal, workflow-mode, and refresh guidance while preserving codex-switch-specific rules.
- `.planning/STATE.md`: recorded that the narrow refresh did not require Goal Mode.
- `.planning/phases/01-foundation/VERIFICATION.md`: linked refresh verification evidence.
- `.planning/verification/20260708074052-dev-flow-refresh-scoped-validation-project-skill-refresh-agents-.md`: preserved the earlier refresh record.
- `.planning/verification/20260713123254-dev-flow-refresh-final-verification.md`: recorded current final verification and deferred migration boundaries.

## Risks / Gaps

- Provider-state migration is blocked by an unauthoritative legacy Superpowers link identity, an invalid inferred core provider configuration, active phase `01-foundation`, and active change `always-check-self-update`.
- Eighteen legacy `.codex/skills` duplicates remain; cleanup requires separate approval.
- The official codex-switch shim still points to the removed `/Applications/Codex.app`; this refresh used `/Applications/ChatGPT.app/Contents/Resources/codex` directly and did not rebind the profile.
- `.planning/devflow/context-health/events.jsonl` is a local hook event stream and is intentionally excluded from the commit.

## Reviewer Notes

- No product code, public API, persistence, or dependency contract changed.
- A new Codex session is required to load the refreshed project-local OpenSpec skills.
