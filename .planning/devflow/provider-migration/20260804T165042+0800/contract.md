# Generated Artifact Contract: DEVFLOW-PROVIDER-MIGRATION-20260804T165042+0800

## Binding

- Owner: main Codex task `019fcbba-6d43-7903-815e-a82d609816eb`.
- OpenSpec change: `refresh-devflow-provider-ownership`.
- Approved by: user approval of方案 A on 2026-08-04.
- Durable root:
  `.planning/devflow/provider-migration/20260804T165042+0800/`.
- Physical quarantine root:
  `.codex/provider-migration-quarantine/20260804T165042+0800/`.
- Physical root state at contract seal: absent.
- Execution mode: serialized main-agent exact-path moves; no subagent, hook,
  updater, Doctor, or validator owns mutation.

## Lifecycle

- Before creation: every source MUST pass the preflight in `preflight.md` and
  the physical root MUST remain absent.
- Creation: create only the physical root and the explicit parent directories
  required for the mappings below.
- Owner exit: after final verification, or immediately on the first source,
  destination, ownership, type, content, or inventory mismatch.
- Terminal success disposition: `RETAIN` for rollback evidence.
- Terminal failure disposition: `HUMAN_GATE`; do not improvise cleanup or
  overwrite an active source.
- Physical purge: forbidden by this contract and requires a separate Human
  Gate after owner exit.
- Deletion: no recursive deletion, wildcard deletion, or physical purge is
  authorized.

## Destination Rule

Every source maps to one exact destination by removing its leading dot and
placing the result below the physical root:

```text
.codex/<relative>  -> .codex/provider-migration-quarantine/20260804T165042+0800/codex/<relative>
.agents/<relative> -> .codex/provider-migration-quarantine/20260804T165042+0800/agents/<relative>
```

The destination MUST be absent before each move. This rule and the exact
source inventory below form the immutable rollback mapping.

## Exact Source Inventory

### Legacy DevFlow symlinks

```text
.codex/skills/capability-research
.codex/skills/change-plan
.codex/skills/checkpoint-compact
.codex/skills/claude-code-delegate
.codex/skills/context-tool-audit
.codex/skills/execute-task
.codex/skills/feature-intake
.codex/skills/plugin-project-migration
.codex/skills/project-orchestrator
.codex/skills/project-setup
.codex/skills/verify-and-archive
.codex/skills/workflow-doctor
```

### Legacy GSD skill directories

```text
.codex/skills/gsd-code-review
.codex/skills/gsd-config
.codex/skills/gsd-discuss-phase
.codex/skills/gsd-execute-phase
.codex/skills/gsd-help
.codex/skills/gsd-import
.codex/skills/gsd-new-project
.codex/skills/gsd-pause-work
.codex/skills/gsd-phase
.codex/skills/gsd-plan-phase
.codex/skills/gsd-progress
.codex/skills/gsd-quick
.codex/skills/gsd-resume-work
.codex/skills/gsd-review
.codex/skills/gsd-settings
.codex/skills/gsd-surface
.codex/skills/gsd-update
.codex/skills/gsd-verify-work
.codex/skills/gsd-workspace
```

### Legacy broken Superpowers symlinks

```text
.codex/skills/brainstorming
.codex/skills/test-driven-development
.codex/skills/verification-before-completion
.codex/skills/writing-plans
```

### Active `.agents/skills` GSD directories

```text
.agents/skills/gsd-discuss-phase
.agents/skills/gsd-execute-phase
.agents/skills/gsd-new-project
.agents/skills/gsd-plan-phase
.agents/skills/gsd-progress
.agents/skills/gsd-verify-work
```

### Active `.agents/skills` Superpowers symlinks

```text
.agents/skills/brainstorming
.agents/skills/test-driven-development
.agents/skills/verification-before-completion
.agents/skills/writing-plans
```

### Whole provider-owned paths

```text
.codex/.gsd-profile
.codex/agents
.codex/config.toml
.codex/get-shit-done
.codex/gsd-core
.codex/gsd-file-manifest.json
.codex/gsd-install-state.json
.codex/hooks
.codex/hooks.json
```

### Manifest-owned GSD script files

```text
.codex/scripts/changeset/cli.cjs
.codex/scripts/changeset/github-release-notes.cjs
.codex/scripts/changeset/lint.cjs
.codex/scripts/changeset/new.cjs
.codex/scripts/changeset/parse.cjs
.codex/scripts/changeset/render.cjs
.codex/scripts/changeset/serialize.cjs
.codex/scripts/lib/allowlist-ratchet.cjs
.codex/scripts/lib/cli-exit.cjs
```

## Exact Retained Inventory

```text
.codex/gsd-migration-journal
.codex/scripts/changeset/README.md
.planning/**
TASK_LEDGER.md
openspec/changes/internal-official-feature-parity/**
scripts/codex_env_setup
scripts/codex_switch_parity.py
scripts/test_codex_parity.py
scripts/test_codex_update_release.py
```

The `.planning/**` notation is retention-only and grants no cleanup authority.
No file under it may be moved by this contract except the new provider-migration
and verification records explicitly owned by the active OpenSpec change.

## Preflight Requirements

1. Installed DevFlow cache remains
   `0.3.0+codex.20260529145038` and `matches-source`.
2. The adjacent migration launcher reproduces 12 `legacy_duplicate` and 19
   `manual_review_required` items.
3. All 391 paths in `.codex/gsd-file-manifest.json` exist and match SHA-256.
4. Every named symlink has the recorded target and valid/broken state.
5. Whole-directory targets contain only the approved inventory; GSD config and
   hook files contain no non-GSD configuration.
6. `.codex/get-shit-done` contains zero files.
7. The physical root and every destination are absent.
8. The unrelated dirty-work fingerprint is durable before mutation.

## Rollback Contract

Rollback is destination-to-source for the exact mappings above and only when:

1. the destination still matches the terminal receipt;
2. the original source is absent;
3. no unexpected destination child exists; and
4. rollback is explicitly selected after a failed migration or later approved
   as a separate action.

Rollback MUST stop rather than overwrite a newly created source. `AGENTS.md`
and `.dev-flow.json` use their recorded pre-change hashes/diff for rollback;
no automatic rollback is exercised after successful verification.
