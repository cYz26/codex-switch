# Preflight: DEVFLOW-PROVIDER-MIGRATION-20260804T165042+0800

## Status

- Observation: complete and read-only.
- Physical quarantine root: absent.
- Provider moves: zero.
- Current outcome: `CONTINUE_NEXT_ITEM`; the continuation instruction consumed
  `DEVFLOW-MATT-TRIGGERED-SET-CORRECTION` before task 1.3.

## Characterization RED

The mandated command was run exactly:

```text
python3 .../scripts/devflow_runtime.pyz/activate_project_dependencies.py ...
exit: 1
error: can't find '__main__' module in '.../devflow_runtime.pyz/activate_project_dependencies.py'
```

The adjacent installed launcher is operational:

```text
python3.12 .../scripts/activate_project_dependencies.py ... --dry-run --json
exit: 0
workflowReady: true
DevFlow official items: 16
OpenSpec official items: 6
skill_layout_migration.status: legacy_duplicate
legacy_duplicate: 12
manual_review_required: 19
```

The invalid generated zipapp-subpath recommendation is non-blocking for the
local migration because the adjacent launcher is installed, current, and
produces the complete diagnostic report. Repairing DevFlow source remains out
of scope.

## Sealed Contract

```text
contract sha256: 419a9e3febe6265f1b7971dec9f91514303b91cfe215b16479d65a427b935ffe
physical root: .codex/provider-migration-quarantine/20260804T165042+0800
physical root state: absent
AGENTS.md sha256: 267fdbc0d4d6f9845559957f7c24f8442daabb2d5fa7c648df5b4874f1aa4993
.dev-flow.json state: absent
HEAD: 8e8e21b8f9e951ce84eb96bc7f245ae31f513279
branch: main
```

## GSD Ownership Evidence

```text
gsd manifest sha256: f44c284df8570074598efae168fde7de41ca93cac191d98249ebc29fbe26a9d2
manifest files: 391
matching files: 391
mismatch: 0
missing: 0
.codex/config.toml sha256: 591db9ff2e4728f84370b75317fe7b7819d96640d25c797988104785932ce83e
.codex/hooks.json sha256: 2ed8b4bd0fcee2349a2302aa70584d5c2ac6073833e238cd1c03c6cd1a8a5d9b
```

Whole-root inventories:

| Root | Files | Directories | Content digest |
|---|---:|---:|---|
| `.codex/agents` | 12 | 1 | `3f47afedd67c03269e1f247dd964b584a9566ccd3aac8290fdce0d94786c9f0d` |
| `.codex/gsd-core` | 332 | 20 | `caaca18004340a7d63d9089ec298bb5f348887ab3c5b14db5b3ed5e5f0ef72ed` |
| `.codex/hooks` | 12 | 1 | `5090cf19de0c0a7beb7e5f7e97b38baf7ec50f4297bd60d80b102f52a03f4010` |
| `.codex/get-shit-done` | 0 | 17 | empty |

All twelve hooks are named `gsd-*`; all four commands in `hooks.json` target
those hooks and zero commands target another provider. `config.toml` contains
only `[features] hooks = true` and six `[agents.gsd-*]` sections, with both
ownership comments identifying the GSD installers.

The nineteen `.codex/skills/gsd-*` directories contain the 38 manifest-owned
skill files. The six `.agents/skills/gsd-*` directories contain 12 files and
each directory is byte-identical to its matching legacy GSD directory.

## Symlink Evidence

Legacy DevFlow links are valid and resolve as follows:

```text
capability-research -> installed DevFlow cache
change-plan -> installed DevFlow cache
checkpoint-compact -> DevFlow development source
claude-code-delegate -> installed DevFlow cache
context-tool-audit -> DevFlow development source
execute-task -> DevFlow development source
feature-intake -> DevFlow development source
plugin-project-migration -> DevFlow development source
project-orchestrator -> installed DevFlow cache
project-setup -> DevFlow development source
verify-and-archive -> DevFlow development source
workflow-doctor -> DevFlow development source
```

The four legacy `.codex/skills` Superpowers links are broken and target the
retired `openai-curated/superpowers/e2d08a2e` cache. The four active
`.agents/skills` Superpowers links are valid and target the internal
`superpowers-upstream-v6-0-3/superpowers/6.0.3` cache.

## Active Skill Inventory Finding

```text
total .agents/skills entries: 37
DevFlow links: 16
OpenSpec 1.7 directories: 6
approved Matt directories present: 5
GSD directories: 6
Superpowers links: 4
```

Present Matt primitives are `grilling`, `tdd`, `diagnosing-bugs`,
`code-review`, and `codebase-design`. `domain-modeling` is absent. The current
DevFlow template says the six pinned Matt primitives may be copied only when
their capability is triggered; the active change explicitly skips
`domain-language-modeling`. Therefore the planned requirement for exactly six
installed Matt primitives would incorrectly activate an unrelated capability.

Recommended bounded correction:

```text
Replace "exactly six Matt primitives are installed" with
"only triggered members of the six-item approved Matt allowlist are active;
the current verified set is five and domain-modeling remains absent because
domain-language-modeling is skipped."
```

This correction does not expand the write set or change the approved removal
of GSD/Superpowers providers. The continuation instruction confirmed it, and
`openspec-update-change` reconciled proposal, spec, design, and tasks before
implementation resumed. Strict validation passed afterward.

## Unrelated Dirty-Work Fingerprint

The fingerprint covers nineteen exact parity/control-plane paths and excludes
only hook-generated `.planning/devflow/context-health/events.jsonl` plus the
new refresh-owned paths.

```text
aggregate sha256: 4cd5ca825d9a182ef5feb09b1c70b344fce25a3e4d120f586d34ad36e3bff61f
file count: 19
```

Per-file SHA-256:

```text
0d30ddd02a424239929b804eed78a0c1830f4db27d6ec5be8cbbe769a4c507fa  .planning/devflow/verification/internal-official-feature-parity.md
0e7334481204785517ac68ac4a9086b77cc9b1136718fbc15234459b25c61bd9  scripts/codex_env_setup
1fc2abf1b40eddbeaf209e49d01de218396b1862f99f4998e93ba0aab121271c  scripts/test_codex_parity.py
277a65838330d768f3c9043dd51010811d9e8ff7c30ba1dacb0e9e53d2c4a0a3  openspec/changes/internal-official-feature-parity/specs/codex-switch/spec.md
3c88b32f262027a3683daf133bb230880028ed00dde146bd12b392ff2889a230  .planning/checkpoints/2026-07-28-internal-installer-isolation-source-verified.md
468ceef030fa9906dc01d002a2e491b56edae7771b930879f1b196084c42d0a0  openspec/changes/internal-official-feature-parity/proposal.md
5ca7845a45dff1e02e9d26a2443c8f65512a97ab9afa9602af0291e00992d9c8  scripts/test_codex_update_release.py
61c5020796b81f5011ab9d3e649c4f0973ae07dc80f721394f633ccd75bec958  .planning/checkpoints/2026-07-28-internal-installer-isolation-approved.md
7aa2658226f25e3948eedfaa97399c7845df7fa36ba156f120dd98978303a1ee  .planning/checkpoints/2026-07-28-internal-0145-native-resume-gate.md
7c680ee77fc80c0673dd3c9a2ea83b6803cc200483746eeaecb4eb7e4151b8d0  .planning/checkpoints/2026-07-28-internal-installer-isolation-red.md
8b70eb094e14cf3de2eeb2ead0c051cd050a23f7bf6ee28800838f0a4006a1a3  .planning/checkpoints/2026-07-28-internal-installer-live-recovery.md
ab0c78a163b4866721732a2c3e580c13cc376b2e0d8c13f7b9cfd2fbc447feba  openspec/changes/internal-official-feature-parity/tasks.md
c3d7119b3166c45f010f68701be70a523be23e1cb0f0afa8375b99fcbb1dfb60  .planning/STATE.md
d468e81908a51534eead9c39b7dd2fba19f7aa741b6f7c8446ef438075e7b6cf  .planning/checkpoints/2026-07-28-internal-0145-retained-candidate-preflight.md
e5608076010ad18a18c07a1b63bf0e5255a98786ce65698a20e1fd0c3b1cefe4  .planning/checkpoints/2026-07-28-internal-0145-core-probe-eof-gate.md
f1d5928c7e6f9f2dbdb40018c6a06a108d64003d6ca142f7a3df04dd467f027e  scripts/codex_switch_parity.py
f55fb6f21ddd67bb00cda721b691dc9dab85d5fcebce245b4501d7e7a3952b5c  .planning/checkpoints/2026-07-28-internal-0145-native-resume-source-verified.md
fd033a52de9c5144dd881cfdd30183828d730a04f0354b8d0c502488f6d0ee7f  openspec/changes/internal-official-feature-parity/design.md
fe8c9a0761b5c0a2d156af26265a3d5c3c642f0c0510539b5da14a1dad566ae7  TASK_LEDGER.md
```

## Gate Disposition

The Matt triggered-set correction is confirmed, reconciled across proposal,
spec, design, and tasks, and strictly valid. Continue with task 1.3; all
original ownership, quarantine, and scope-expansion stop conditions remain.
