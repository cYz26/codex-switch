# DevFlow Provider Migration Verification

## Scope

- OpenSpec change: `refresh-devflow-provider-ownership`.
- Contract: `DEVFLOW-PROVIDER-MIGRATION-20260804T165042+0800`.
- Repository: `/Users/cY/dev/codex-switch` at
  `8e8e21b8f9e951ce84eb96bc7f245ae31f513279` on `main`.
- Execution: serialized main task only; no subagent was authorized.
- Archive, commit, push, restart, release, dependency, profile, credential,
  product/parity source, and quarantine-purge effects remained excluded.

## Characterization RED

Before migration, the adjacent installed launcher reported:

```text
official DevFlow items: 16
official OpenSpec items: 6
layout: legacy_duplicate
legacy_duplicate: 12
manual_review_required: 19
GSD manifest: 391/391 match
```

The generated zipapp-subpath recommendation exited 1 with `can't find
'__main__'`; the adjacent installed launcher remained operational and became
the bounded migration/verification route.

## Applied Migration

- Merged the installed DevFlow `AGENTS.md` template with project mode
  `brownfield`; preserved the original `Codex Internal Binary Upgrade Context`
  byte-for-byte.
- Added exactly `{"workflow":{"mode":"full-openspec"}}` to
  `.dev-flow.json`.
- Moved only the 63 contract-listed sources to the contract-relative
  quarantine destinations: 12 legacy DevFlow links, 19 legacy GSD skills, 4
  broken legacy Superpowers links, 6 active GSD skills, 4 active Superpowers
  links, 9 whole GSD-owned runtime/config paths, and 9 manifest-owned script
  files.
- Retained `.codex/gsd-migration-journal`, the unowned changeset README,
  `.planning/**`, parity OpenSpec/source WIP, Git history, and all excluded
  runtime/profile state.
- Refreshed ordinary migration audit state only; no dependency or provider
  selection persistence changed.

The exact path list, mapping rule, owner exit, and rollback rules are sealed in
`.planning/devflow/provider-migration/20260804T165042+0800/contract.md`. The
terminal disposition is recorded in `terminal-receipt.md` as `RETAIN`.

## GREEN Evidence

| Check | Fresh result |
|---|---|
| Adjacent official-layout dry-run | exit 0; `current`; 16 DevFlow; 6 OpenSpec; 0 `legacy_duplicate`; 0 `manual_review_required` |
| Provider/source mapping audit | 63/63 original sources absent and destinations/type-valid |
| GSD quarantine manifest | 391/391 SHA-256 matches |
| Quarantine identity | device 16777233; inode 58202762; mode 0700; 420 files, 96 directories, 20 symlinks |
| Quarantine canonical digest | `bb43aeadceae9e5d9337ac3680b65a93f4ec4ab6ba708b0691ff17da0be971ad` |
| Active provider inventory | 16 DevFlow + 6 OpenSpec + 5 triggered Matt; `domain-modeling` absent; GSD/Superpowers 0 |
| Installed migration apply/check | `applied`, then `current`; stored/runtime versions equal; 0 stale/missing/conflicts |
| Workflow validator | exit 0; `ok=true`; 0 issues; 0 warnings |
| Doctor with cache drift | exit 0; `diagnosis=healthy`; 0 issues; recommendation `No workflow repair needed.` |
| Scaffold dry-run | exit 0; actual `AGENTS.md.generated` absent; active guidance disposition `merged` |
| AGENTS merge | generic body equals installed template after `brownfield` substitution; project internal-binary section equals `HEAD` |
| DevFlow source/cache | updater exit 0; installed `dev-flow@cy-codex-skills` is `matches-source` |
| Dependency/capability check | exit 0; `workflowReady=true`; change-review and completion-proof ready |
| `.dev-flow.json` | JSON valid and exact one-line value |
| OpenSpec active change | strict valid |
| OpenSpec parity change | strict valid |
| OpenSpec repository | 19 passed, 0 failed |
| Diff integrity | `git diff --check` exit 0 |
| Unrelated parity/control paths | 19 files; aggregate SHA-256 remains `4cd5ca825d9a182ef5feb09b1c70b344fce25a3e4d120f586d34ad36e3bff61f` |
| Retained history | GSD journal present; changeset README hash remains `86ff893...e9e9ea` |

The pre-existing `setup-report.md` remained untouched: inode `29070946`, mtime
`2026-06-05T21:45:11+0800`, size 1498, and SHA-256
`2bd6c7c9ce2acca4aa3094d98448d94694607049f8a55f8997868ed7cdf50571`.
It is not an `AGENTS.md.generated` competitor.

## Review

### Standards

No blocking finding. The change follows the approved Full OpenSpec ledger,
uses exact ownership-proven moves, preserves project-specific guidance, makes
no deletion or external/Git effect, and keeps rollback bytes. No production
code was changed, so code-smell findings are not applicable.

### Spec

No blocking finding. Each requirement scenario maps to tasks 1.1-5.4 and a
fresh validator: canonical providers, durable guidance, recoverable migration,
history/WIP preservation, and completion evidence are all represented. No
unrequested provider, dependency, product, profile, release, or archive change
was introduced.

The approved contract explicitly forbids subagents, so the two axes were
reviewed serially by the main owner rather than delegating the Matt review
primitive.

## Residual Findings

### DF-IF-PM-SOURCE-IDENTITY — DEFER_AND_CONTINUE

The full updater uses the local marketplace source as its migration inspection
root and therefore calls all 16 installed-cache links stale. A minimized
differential ran twice: installed-cache inspection was `current/0 stale`, while
marketplace-source inspection was `migration_pending/16 stale`. Versions were
equal and `diff -qr` between the plugin trees was empty. Active discovery,
Doctor, official layout, installed migration state, and cache bytes are
healthy, so this does not invalidate the Completion Contract. Keep links on the
installed cache; a separate DevFlow source change should accept byte-identical
source/cache identities and add a differential regression.

### DF-IF-PM-ZIPAPP-COMMAND — DEFER_AND_CONTINUE

Migration reports still construct an invalid script-below-zipapp command. The
adjacent launcher is installed, current, and produced all required RED/GREEN
evidence. Repair the generated command in a separately scoped DevFlow source
change; do not change this project's verified provider layout as a workaround.

## Rollback and Retention

Physical quarantine is retained, not deleted. Reverse only the exact contract
mappings after proving each source is absent and each destination still matches
the terminal receipt. Stop rather than overwrite or improvise. AGENTS/config
rollback and physical purge remain separate explicit decisions.

## Continuation

Start a new Codex task before relying on the refreshed project discovery set;
the current task loaded its skill inventory before the provider migration.
The existing parity Human Gate remains `PARITY-CORE-PROBE-INTERACTIVE-IMPLEMENT`.
This maintenance change remains unarchived, and no commit or push was made.
