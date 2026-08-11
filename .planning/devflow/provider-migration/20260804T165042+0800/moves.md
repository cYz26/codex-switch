# Move Receipt: DEVFLOW-PROVIDER-MIGRATION-20260804T165042+0800

## Root Creation

The immutable contract existed with SHA-256
`419a9e3febe6265f1b7971dec9f91514303b91cfe215b16479d65a427b935ffe`
before either physical directory was created.

```text
parent: .codex/provider-migration-quarantine
parent device: 16777233
parent inode: 58202761
parent mode: 0700
parent uid: 502
parent gid: 20

root: .codex/provider-migration-quarantine/20260804T165042+0800
root device: 16777233
root inode: 58202762
root mode: 0700
root uid: 502
root gid: 20
```

Immediate pre-creation re-attestation passed 391/391 GSD manifest hashes and
all provider source path-type checks. No source had moved at root creation.

## Move Groups

- Group 3.2 legacy DevFlow/Superpowers links: complete; 16 exact symlinks moved
  under `codex/skills`, mapping digest
  `13768fbe6c44862361707c6a4b3a07b7db2709cb36d6e8f937747c77e44c8121`.
  The active legacy root now contains exactly nineteen GSD directories, and
  all sixteen official DevFlow links remain valid.
- Group 3.3 GSD/Superpowers skills: complete; nineteen legacy GSD directories,
  six active GSD directories, and four active Superpowers links moved. The
  combined quarantine tree digest is
  `1d4f4e1b2c55c54a220396c86340f2d0a5fb2a73dfaa27f282a1fbce6e563add`;
  all 38 manifest-owned GSD skill files match. Active discovery is exactly 16
  DevFlow + 6 OpenSpec + 5 triggered Matt, and `domain-modeling` is absent.
- Group 3.4 GSD runtime/config/scripts: complete. The combined pre-move active
  plus quarantine manifest and the terminal quarantine manifest both pass
  391/391. Relative content digests are agents
  `4e177d842f5d3ce7c4a25e631fcb401ab5539a27060698725542896f7449095f`,
  core `be203138d59e8021eae3d6aebb83df167509d610663904ce356b9989121f6dbb`,
  and hooks `59cacf00e921e7b552a2256f442a8ae32b05ad17f9b3d44a30eee2dec9855685`.
  The complete current quarantine digest is
  `a309f4e4c32f1fdff5337be1b2d17a51e7d1566e8c250dd705f77591c0721d91`.
  `.codex/gsd-migration-journal` remains present; the retained unowned README
  remains byte-identical at
  `86ff89331dfd94b2afd9ff9974883f137f3f0c3652e4687fecb216c0eee9e9ea`.

Each completed group will preserve the contract's source-relative destination
mapping and record focused post-move validation here. No deletion or physical
purge is authorized.

## Post-Move Verification

```text
source/destination mapping: complete
quarantine GSD manifest: 391/391
active skills: 16 DevFlow + 6 OpenSpec + 5 triggered Matt
active GSD/Superpowers: 0
domain-modeling: absent by skipped capability
retained GSD journal: present
retained unowned README: byte-identical
unrelated dirty fingerprint: 4cd5ca825d9a182ef5feb09b1c70b344fce25a3e4d120f586d34ad36e3bff61f
physical deletion/purge: none
```

The physical quarantine remains mode 0700 on device `16777233`, inode
`58202762`. Final diagnostics passed and the terminal disposition is `RETAIN`;
the canonical inventory digest and rollback boundary are recorded in
`terminal-receipt.md`. Physical purge remains unauthorized.
