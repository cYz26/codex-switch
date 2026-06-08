# Remote Release Packaging

## Why

Direct remote invocation currently depends on GitHub release assets being
uploaded by a local publisher. If `run.sh` or `codex-switch.tar.gz` are missing
from the release, users can still work around it with raw GitHub URLs and an
explicit tarball override, but that is not the intended cross-project contract.

The release process should be reproducible from GitHub, and the installer,
runner, and local self-update path should have a source-archive fallback so a
missing release bundle does not make remote use unusable.

## What Changes

- Add a GitHub Actions release workflow that runs the repository verification,
  builds `dist/codex-switch.tar.gz`, and uploads `install.sh`, `run.sh`, and the
  bundle as release assets for `v*` tags.
- Add source archive fallback support to `install.sh`, `run.sh`, and local
  wrapper self-update. The fallback downloads a GitHub source archive, packages
  it locally when `scripts/package-release.sh` is available, and then installs
  or executes the packaged implementation.
- Document the release workflow and source fallback overrides.

## Target State

Users can invoke `codex-switch` from other repositories through the documented
release URLs. Future tags publish the required release assets from GitHub
Actions. If a release bundle URL is unavailable but a source archive is
available, the installer, remote runner, and local self-update path can stage a
valid implementation from that source archive without manual local packaging.

## Capability Evidence

- `authoritative_current`: GitHub documents using `GITHUB_TOKEN` in workflows
  and configuring job permissions; GitHub also documents using GitHub CLI in
  workflows. The workflow can use `permissions: contents: write` with
  `GH_TOKEN: ${{ github.token }}` to create or update releases.
- `local_scan`: `scripts/package-release.sh` already emits
  `dist/codex-switch.tar.gz` and `dist/run.sh`; `install.sh`, `run.sh`, and
  `scripts/codex-switch` already install from a tarball URL but treat download
  failure as terminal for installer/runner and as a non-blocking self-update
  warning for local commands.
- `comparison`: Publishing release assets through GitHub Actions keeps the
  normal path compact and reproducible. Source archive fallback keeps raw-script
  and missing-asset scenarios usable without relying on a developer's local
  machine.
- `assumptions`: Repository GitHub Actions must be enabled for remote
  publication. Local verification can prove workflow syntax and packaging
  commands; end-to-end asset publication is proven after pushing a tag and
  observing the uploaded assets.

## Scope

- In scope: GitHub Actions release packaging, source archive fallback,
  regression tests, docs, version bump, verification evidence, state updates.
- Out of scope: changing profile switching behavior, adding production runtime
  dependencies, replacing the release repository, or changing authentication
  flows.

## Completion Contract

- [ ] Release workflow exists and uploads `install.sh`, `run.sh`, and
      `codex-switch.tar.gz` for `v*` tags.
- [ ] Installer falls back from a missing release bundle to a source archive and
      installs a usable PATH command.
- [ ] Remote runner falls back from a missing release bundle to a source archive
      and executes the requested command without creating the PATH symlink.
- [ ] Local release-installed wrapper self-update can sync from a source archive
      fallback when the primary release bundle is unavailable.
- [ ] README/SKILL/OpenSpec document the source fallback and release workflow.
- [ ] Local verification passes and remote release-link behavior is checked
      after publication, or any external blocker is recorded with evidence.
