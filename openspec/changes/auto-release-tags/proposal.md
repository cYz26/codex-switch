# Automatic release tags and packaging

## Why

`codex-switch` already publishes release assets from `v*` tags, but merging
release-relevant changes to `main` still depends on a manual decision to bump
`VERSION`, create a tag, and publish the release. That leaves `main` ahead of
`releases/latest`, so install, run, and self-update users can remain on stale
code after user-visible behavior ships.

## What Changes

- Add an automatic release gate for `main` pushes.
- Detect whether changes since the latest `vX.Y.Z` tag are release-relevant.
- Skip pure planning, OpenSpec, verification, and docs-only changes.
- For release-relevant changes, run release-equivalent verification, bump
  `VERSION` to the next patch version, commit that bump, create the matching
  `vX.Y.Z` tag, push the commit and tag, then publish release assets.
- Keep the existing `v*` tag release workflow for manually pushed tags and
  manual reruns.

## Target State

After a release-relevant change lands on `main`, GitHub Actions automatically
publishes a new patch release without a separate human tag step. If a `main`
push contains only planning/spec verification/docs-only work, no tag is
created. Release assets continue to come from immutable tag content and include
`install.sh`, `run.sh`, and `codex-switch.tar.gz`.

## Scope

- Project mode: brownfield
- Change type: workflow-repair / behavior-change

## Capability Evidence

- authoritative/current: GitHub Actions supports `push` branch/tag triggers
  and `workflow_dispatch`. GitHub documents that events created by a workflow's
  `GITHUB_TOKEN` do not trigger new workflow runs except
  `workflow_dispatch` and `repository_dispatch`, so the automatic release
  workflow must publish assets itself after creating a tag instead of relying
  on the tag push to trigger the existing release workflow.
- local scan: `.github/workflows/release.yml` currently publishes assets for
  `v*` tag pushes and manual dispatch only. `install.sh`, `run.sh`, and local
  self-update read `releases/latest` by default. `VERSION` remains `0.1.3`
  while `main` contains release-relevant changes after `v0.1.3`.

## Non-Goals

- Do not archive any existing OpenSpec changes.
- Do not require a personal access token or external secret for normal release
  publication.
- Do not infer minor or major versions automatically; automatic releases use
  the next patch version.
- Do not publish for pure `.planning/**`, `openspec/**`, or docs-only changes.

## Completion Contract

- [ ] Automatic release planning classifies release-relevant and non-release
      changes deterministically.
- [ ] `main` push workflow creates and publishes a patch release only when
      release-relevant changes exist.
- [ ] Existing manual `v*` tag publishing still works.
- [ ] Tests cover release-required detection, skip detection, version bumping,
      and workflow contract.
- [ ] README and OpenSpec describe the automatic release boundary.
- [ ] Verification evidence and workflow state are recorded.

## Risks

- A bot-created tag push will not reliably trigger another workflow when using
  `GITHUB_TOKEN`; the auto-release workflow must publish assets in the same
  run.
- Release detection can be too broad or too narrow. Keep the first version
  conservative: runtime, installer, packaging, workflow, skill/agent assets,
  and non-test scripts are release-relevant; planning/spec/docs-only files are
  not.
