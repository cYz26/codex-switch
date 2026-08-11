# Terminal Receipt: DEVFLOW-PROVIDER-MIGRATION-20260804T165042+0800

## Disposition

- Completed at: `2026-08-04T17:23:03+08:00`.
- Owner exit: successful after final provider/content attestation.
- Physical quarantine disposition: `RETAIN`.
- Physical purge: not authorized; a separate Human Gate is still required.
- Archive, commit, push, restart, release, dependency, profile, credential, and
  product-code effects: not performed.

## Identity

```text
root: .codex/provider-migration-quarantine/20260804T165042+0800
device: 16777233
inode: 58202762
mode: 0700
canonical terminal inventory sha256: bb43aeadceae9e5d9337ac3680b65a93f4ec4ab6ba708b0691ff17da0be971ad
files: 420
directories: 96
symlinks: 20
```

The canonical digest is SHA-256 over sorted root-relative inventory rows. Each
row binds entry kind, path, mode, and either file SHA-256 or symlink target.

## Exact Mapping Attestation

The immutable exact source list and destination rule remain in `contract.md`,
whose SHA-256 remains
`419a9e3febe6265f1b7971dec9f91514303b91cfe215b16479d65a427b935ffe`.

```text
expected mappings: 63
verified original sources absent: 63
verified quarantine destinations and types: 63
GSD manifest entries: 391
GSD manifest content matches: 391
active legacy .codex/skills entries: 0
```

All destination paths still use the source-relative mapping specified by the
contract. No wildcard move, recursive deletion, overwrite, or physical purge
occurred.

## Active Discovery Attestation

```text
active .agents/skills entries: 27
DevFlow installed-cache links: 16
OpenSpec 1.7 skills: 6
triggered Matt skills: 5
domain-modeling: absent
active GSD/Superpowers providers: 0
official layout: current
legacy_duplicate: 0
manual_review_required: 0
```

The installed DevFlow cache is byte-identical to the local marketplace source
and reports `matches-source`. The installed-cache migration route reports
`current`, zero stale/missing/conflicting skills, and stored/runtime version
`0.3.0+codex.20260529145038`.

## Retained History

```text
.codex/gsd-migration-journal: present
.codex/scripts/changeset/README.md: present
README sha256: 86ff89331dfd94b2afd9ff9974883f137f3f0c3652e4687fecb216c0eee9e9ea
unrelated dirty-work sha256: 4cd5ca825d9a182ef5feb09b1c70b344fce25a3e4d120f586d34ad36e3bff61f
HEAD: 8e8e21b8f9e951ce84eb96bc7f245ae31f513279
branch: main
```

## Rollback

Rollback remains destination-to-source for only the 63 contract mappings.
Before each reverse move, revalidate the terminal inventory row and prove the
original source is absent. Stop on a newly created source, type/content drift,
or unexpected destination child; never overwrite. Restoring `AGENTS.md` or
removing `.dev-flow.json` is a separate explicit rollback decision. Successful
migration does not authorize automatic rollback or quarantine purge.
