#!/usr/bin/env python3
"""Plan, prepare, and reconcile automatic codex-switch patch releases."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import urllib.parse
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Mapping, Optional, Sequence, Tuple

try:
    from codex_switch_release_bundle import (
        FIXED_DIRECTORIES,
        FIXED_FILES,
        MANIFEST_NAME,
        BundleError,
        canonicalize_legacy_release_archive,
        validate_legacy_release_outputs,
        validate_release_outputs,
    )
except ModuleNotFoundError:
    from scripts.codex_switch_release_bundle import (
        FIXED_DIRECTORIES,
        FIXED_FILES,
        MANIFEST_NAME,
        BundleError,
        canonicalize_legacy_release_archive,
        validate_legacy_release_outputs,
        validate_release_outputs,
    )


SEMVER_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")
REQUIRED_RELEASE_ASSETS = (
    "install.sh",
    "run.sh",
    "codex-switch.tar.gz",
)
ASSET_MANIFEST_SCHEMA = "codex-switch.release-assets"
ASSET_MANIFEST_VERSION = 1


@dataclass(frozen=True)
class LegacyReleaseLayout:
    required_files: Tuple[str, ...]
    required_directories: Tuple[str, ...]
    allow_appledouble_archive: bool


LEGACY_RELEASE_LAYOUTS: Mapping[str, LegacyReleaseLayout] = {
    "v0.1.12": LegacyReleaseLayout(
        required_files=tuple(FIXED_FILES),
        required_directories=("agents", "evals", "scripts"),
        allow_appledouble_archive=True,
    ),
    "v0.1.13": LegacyReleaseLayout(
        required_files=tuple(FIXED_FILES),
        required_directories=tuple(FIXED_DIRECTORIES),
        allow_appledouble_archive=True,
    ),
}


class ReleaseError(RuntimeError):
    """Release preparation or reconciliation failed."""


class ReleaseConflict(ReleaseError):
    """Observed release state conflicts with the intended immutable release."""


@dataclass(frozen=True)
class ReleaseAsset:
    name: str
    path: Path
    size: int
    sha256: str


@dataclass(frozen=True)
class ReleaseSnapshot:
    exists: bool
    assets: Tuple[str, ...]
    draft: bool = False


@dataclass(frozen=True)
class CommitFile:
    mode: str
    object_id: str


def _run(
    command: Sequence[str],
    *,
    cwd: Optional[Path] = None,
    check: bool = True,
) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(
        list(command),
        cwd=cwd,
        check=False,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise ReleaseError(
            f"Command failed ({result.returncode}): {' '.join(command)}: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    return result


def run_git(repo: Path, *args: str) -> str:
    return _run(["git", *args], cwd=repo).stdout.strip()


def parse_tag(tag: str) -> Tuple[int, int, int]:
    match = SEMVER_TAG.match(tag)
    if not match:
        raise ValueError(f"Expected semantic release tag like v1.2.3, got {tag!r}")
    return tuple(int(part) for part in match.groups())  # type: ignore[return-value]


def format_tag(version: Tuple[int, int, int]) -> str:
    return f"v{version[0]}.{version[1]}.{version[2]}"


def version_text_from_tag(tag: str) -> str:
    major, minor, patch = parse_tag(tag)
    return f"{major}.{minor}.{patch}"


def latest_release_tag(repo: Path) -> str:
    raw = run_git(repo, "tag", "--list", "v[0-9]*.[0-9]*.[0-9]*")
    tags = [tag for tag in raw.splitlines() if SEMVER_TAG.match(tag)]
    if not tags:
        raise ReleaseError("No semantic release tags found")
    return max(tags, key=parse_tag)


def next_patch_tag(tag: str) -> str:
    major, minor, patch = parse_tag(tag)
    return format_tag((major, minor, patch + 1))


def resolve_commit(repo: Path, ref: str) -> str:
    return run_git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")


def optional_commit(repo: Path, ref: str) -> Optional[str]:
    result = _run(
        ["git", "rev-parse", "--verify", "--quiet", f"{ref}^{{commit}}"],
        cwd=repo,
        check=False,
    )
    if result.returncode == 0:
        return result.stdout.strip()
    if result.returncode == 1:
        return None
    raise ReleaseError(
        f"Could not inspect Git ref {ref}: "
        f"{result.stderr.strip() or result.stdout.strip()}"
    )


def is_ancestor(repo: Path, ancestor: str, descendant: str) -> bool:
    result = _run(
        ["git", "merge-base", "--is-ancestor", ancestor, descendant],
        cwd=repo,
        check=False,
    )
    if result.returncode == 0:
        return True
    if result.returncode == 1:
        return False
    raise ReleaseError(
        f"Could not compare Git ancestry for {ancestor} and {descendant}: "
        f"{result.stderr.strip() or result.stdout.strip()}"
    )


def changed_files(repo: Path, base_tag: str, head: str) -> List[str]:
    raw = run_git(repo, "diff", "--name-only", f"{base_tag}..{head}")
    return [line for line in raw.splitlines() if line]


def is_release_relevant(path: str) -> bool:
    if path in {"install.sh", "run.sh", "SKILL.md"}:
        return True
    if path in {
        ".github/workflows/release.yml",
        ".github/workflows/auto-release.yml",
    }:
        return True
    if path.startswith("scripts/"):
        name = Path(path).name
        return not name.startswith("test_")
    if path.startswith("agents/"):
        return True
    return False


class GitHubCliAdapter:
    def __init__(self, repository: str) -> None:
        if not repository or "/" not in repository:
            raise ReleaseError(
                "GitHub repository must use owner/name form; set "
                "GITHUB_REPOSITORY or pass --github-repo"
            )
        self.repository = repository

    def _gh(self, *args: str, check: bool = True) -> subprocess.CompletedProcess[str]:
        return _run(["gh", *args], check=check)

    def inspect_release(self, tag: str) -> ReleaseSnapshot:
        encoded_tag = urllib.parse.quote(tag, safe="")
        result = self._gh(
            "api",
            f"repos/{self.repository}/releases/tags/{encoded_tag}",
            check=False,
        )
        if result.returncode != 0:
            payload: object = None
            for candidate in (result.stdout, result.stderr):
                try:
                    payload = json.loads(candidate)
                except (TypeError, json.JSONDecodeError):
                    continue
                if isinstance(payload, dict):
                    break
            if (
                isinstance(payload, dict)
                and str(payload.get("status", "")) == "404"
            ) or (
                "Not Found" in result.stderr and "HTTP 404" in result.stderr
            ):
                return ReleaseSnapshot(exists=False, assets=(), draft=False)
            raise ReleaseError(
                f"Could not inspect GitHub release {tag}: "
                f"{result.stderr.strip() or result.stdout.strip()}"
            )

        try:
            payload = json.loads(result.stdout)
        except json.JSONDecodeError as error:
            raise ReleaseError(
                f"GitHub release {tag} returned invalid JSON: {error}"
            ) from error
        if (
            not isinstance(payload, dict)
            or not isinstance(payload.get("assets"), list)
            or type(payload.get("draft")) is not bool
        ):
            raise ReleaseError(f"GitHub release {tag} has an unsupported response")
        names: List[str] = []
        for raw_asset in payload["assets"]:
            if (
                not isinstance(raw_asset, dict)
                or not isinstance(raw_asset.get("name"), str)
                or not raw_asset["name"]
            ):
                raise ReleaseError(f"GitHub release {tag} has an invalid asset")
            names.append(raw_asset["name"])
        if len(names) != len(set(names)):
            raise ReleaseConflict(f"GitHub release {tag} has duplicate asset names")
        return ReleaseSnapshot(
            exists=True,
            assets=tuple(sorted(names)),
            draft=payload["draft"],
        )

    def create_release(self, tag: str) -> None:
        self._gh(
            "release",
            "create",
            tag,
            "--repo",
            self.repository,
            "--title",
            tag,
            "--notes",
            f"Release {tag}",
            "--verify-tag",
            "--draft",
        )

    def download_asset(self, tag: str, name: str, destination: Path) -> None:
        if destination.exists():
            raise ReleaseError(f"Refusing to overwrite downloaded asset: {destination}")
        destination.parent.mkdir(parents=True, exist_ok=True)
        self._gh(
            "release",
            "download",
            tag,
            "--repo",
            self.repository,
            "--pattern",
            name,
            "--dir",
            str(destination.parent),
        )
        downloaded = destination.parent / name
        if downloaded != destination or not destination.is_file():
            raise ReleaseError(f"GitHub release did not download {tag}/{name}")

    def upload_asset(self, tag: str, path: Path) -> None:
        self._gh(
            "release",
            "upload",
            tag,
            str(path),
            "--repo",
            self.repository,
        )

    def publish_release(self, tag: str) -> None:
        self._gh(
            "release",
            "edit",
            tag,
            "--repo",
            self.repository,
            "--draft=false",
        )


def build_plan(
    repo: Path,
    head: str,
    *,
    github: Optional[object] = None,
) -> Dict[str, Any]:
    latest_tag = latest_release_tag(repo)
    head_commit = resolve_commit(repo, head)
    latest_commit = resolve_commit(repo, latest_tag)
    if not is_ancestor(repo, latest_commit, head_commit):
        raise ReleaseConflict(
            f"Latest semantic tag {latest_tag} ({latest_commit}) is not an "
            f"ancestor of {head_commit}"
        )

    files = changed_files(repo, latest_tag, head_commit)
    relevant = [path for path in files if is_release_relevant(path)]
    snapshot: Optional[ReleaseSnapshot] = None
    if github is not None:
        raw_snapshot = github.inspect_release(latest_tag)
        if not isinstance(raw_snapshot, ReleaseSnapshot):
            raise ReleaseError("GitHub adapter returned an invalid release snapshot")
        snapshot = raw_snapshot

    missing_assets: List[str] = []
    if snapshot is not None:
        present = set(snapshot.assets) if snapshot.exists else set()
        missing_assets = [
            name for name in REQUIRED_RELEASE_ASSETS if name not in present
        ]

    reconcile_required = bool(
        snapshot is not None and (snapshot.draft or missing_assets)
    )
    prepare_required = bool(relevant)
    if reconcile_required and prepare_required:
        action = "reconcile_then_prepare"
    elif reconcile_required:
        action = "reconcile"
    elif prepare_required:
        action = "prepare"
    else:
        action = "none"
    target_tag = latest_tag if reconcile_required else ""
    target_commit = latest_commit if reconcile_required else ""
    proposed_tag = next_patch_tag(latest_tag) if prepare_required else ""
    if prepare_required and not reconcile_required:
        target_tag = proposed_tag

    required = reconcile_required or prepare_required
    return {
        "latest_tag": latest_tag,
        "latest_commit": latest_commit,
        "head": run_git(repo, "rev-parse", "--short", head_commit),
        "head_commit": head_commit,
        "source_commit": head_commit,
        "changed_files": files,
        "release_relevant_files": relevant,
        "release_required": required,
        "release_action": action,
        "reconcile_required": reconcile_required,
        "prepare_required": prepare_required,
        "target_tag": target_tag,
        "target_commit": target_commit,
        "missing_assets": missing_assets,
        "next_tag": proposed_tag,
        "next_version": (
            version_text_from_tag(proposed_tag) if proposed_tag else ""
        ),
    }


def write_github_output(path: Path, plan: Mapping[str, Any]) -> None:
    release_files = ",".join(plan["release_relevant_files"])
    missing_assets = ",".join(plan["missing_assets"])
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"release_required={str(plan['release_required']).lower()}\n")
        handle.write(f"release_action={plan['release_action']}\n")
        handle.write(
            f"reconcile_required={str(plan['reconcile_required']).lower()}\n"
        )
        handle.write(f"prepare_required={str(plan['prepare_required']).lower()}\n")
        handle.write(f"latest_tag={plan['latest_tag']}\n")
        handle.write(f"source_commit={plan['source_commit']}\n")
        handle.write(f"target_tag={plan['target_tag']}\n")
        handle.write(f"target_commit={plan['target_commit']}\n")
        handle.write(f"missing_assets={missing_assets}\n")
        handle.write(f"next_tag={plan['next_tag']}\n")
        handle.write(f"next_version={plan['next_version']}\n")
        handle.write(f"release_files={release_files}\n")


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_asset_evidence(name: str, path: Path) -> ReleaseAsset:
    if name not in REQUIRED_RELEASE_ASSETS:
        raise ReleaseError(f"Unsupported release asset name: {name}")
    raw_path = Path(os.path.abspath(os.path.expanduser(os.fspath(path))))
    if raw_path.is_symlink() or not raw_path.is_file():
        raise ReleaseError(f"Release asset is missing or not regular: {raw_path}")
    return ReleaseAsset(
        name=name,
        path=raw_path,
        size=raw_path.stat().st_size,
        sha256=_sha256_file(raw_path),
    )


def _commit_release_files(
    repo: Path,
    commit: str,
    *,
    required_files: Sequence[str],
    required_directories: Sequence[str],
) -> Dict[str, CommitFile]:
    source_paths = ["install.sh", *required_files, *required_directories]
    result = subprocess.run(
        ["git", "ls-tree", "-r", "-z", commit, "--", *source_paths],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ReleaseError(
            f"Could not inspect release tree {commit}: "
            f"{os.fsdecode(result.stderr).strip()}"
        )
    files: Dict[str, CommitFile] = {}
    for record in result.stdout.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, raw_kind, raw_object = metadata.split(b" ", 2)
        except ValueError as error:
            raise ReleaseError(
                f"Invalid Git tree record for release commit {commit}"
            ) from error
        path = os.fsdecode(raw_path)
        mode = raw_mode.decode("ascii")
        kind = raw_kind.decode("ascii")
        object_id = raw_object.decode("ascii")
        if (
            kind != "blob"
            or mode not in {"100644", "100755"}
            or path in files
        ):
            raise ReleaseConflict(
                f"Unsupported release tree entry at {commit}: {path}"
            )
        files[path] = CommitFile(mode=mode, object_id=object_id)
    for required in ("install.sh", *required_files):
        if required not in files:
            raise ReleaseConflict(
                f"Release commit {commit} is missing required file: {required}"
            )
    for required in required_directories:
        prefix = f"{required}/"
        if not any(path.startswith(prefix) for path in files):
            raise ReleaseConflict(
                f"Release commit {commit} is missing required directory: {required}"
            )
    return files


def _git_blob(repo: Path, object_id: str) -> bytes:
    result = subprocess.run(
        ["git", "cat-file", "blob", object_id],
        cwd=repo,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if result.returncode != 0:
        raise ReleaseError(
            f"Could not read release blob {object_id}: "
            f"{os.fsdecode(result.stderr).strip()}"
        )
    return result.stdout


def _git_mode(path: Path) -> str:
    return "100755" if stat.S_IMODE(path.stat().st_mode) & 0o111 else "100644"


def assert_release_source_matches_commit(
    repo: Path,
    commit: str,
    *,
    required_files: Sequence[str] = FIXED_FILES,
    required_directories: Sequence[str] = FIXED_DIRECTORIES,
) -> None:
    repo = repo.resolve()
    expected_commit = resolve_commit(repo, commit)
    head_commit = resolve_commit(repo, "HEAD")
    if head_commit != expected_commit:
        raise ReleaseConflict(
            f"Release source HEAD {head_commit} is not bound to commit "
            f"{expected_commit}"
        )
    commit_files = _commit_release_files(
        repo,
        expected_commit,
        required_files=required_files,
        required_directories=required_directories,
    )
    source_files, _source_directories = _release_source_entries(
        repo,
        required_files=required_files,
        required_directories=required_directories,
    )
    source_files = {"install.sh": repo / "install.sh", **source_files}
    if set(source_files) != set(commit_files):
        missing = sorted(set(commit_files) - set(source_files))
        extra = sorted(set(source_files) - set(commit_files))
        raise ReleaseConflict(
            f"Release source file set differs from commit tree: "
            f"missing={missing}; extra={extra}"
        )
    for relative, path in source_files.items():
        commit_file = commit_files[relative]
        if _git_mode(path) != commit_file.mode:
            raise ReleaseConflict(
                f"Release source mode differs from commit tree: {relative}"
            )
        if path.read_bytes() != _git_blob(repo, commit_file.object_id):
            raise ReleaseConflict(
                f"Release source differs from commit tree: {relative}"
            )


def _release_source_entries(
    repo: Path,
    *,
    required_files: Sequence[str] = FIXED_FILES,
    required_directories: Sequence[str] = FIXED_DIRECTORIES,
) -> Tuple[Dict[str, Path], Dict[str, Path]]:
    files: Dict[str, Path] = {}
    directories: Dict[str, Path] = {}
    for relative in required_files:
        path = repo / relative
        if path.is_symlink() or not path.is_file():
            raise ReleaseError(f"Release source file is missing or invalid: {path}")
        files[relative] = path
    for relative in required_directories:
        root = repo / relative
        if root.is_symlink() or not root.is_dir():
            raise ReleaseError(
                f"Release source directory is missing or invalid: {root}"
            )
        directories[relative] = root
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ReleaseError(f"Release source contains a symlink: {path}")
            if path.is_file():
                files[path.relative_to(repo).as_posix()] = path
            elif path.is_dir():
                directories[path.relative_to(repo).as_posix()] = path
            else:
                raise ReleaseError(
                    f"Release source contains a special file: {path}"
                )
    return files, directories


def validate_bundle_matches_source(
    repo: Path,
    package_dir: Path,
    *,
    required_files: Sequence[str] = FIXED_FILES,
    required_directories: Sequence[str] = FIXED_DIRECTORIES,
) -> None:
    source_files, source_directories = _release_source_entries(
        repo,
        required_files=required_files,
        required_directories=required_directories,
    )
    package_files: Dict[str, Path] = {}
    package_directories: Dict[str, Path] = {}
    root_manifest = package_dir / MANIFEST_NAME
    for path in package_dir.rglob("*"):
        if path.is_symlink():
            raise ReleaseConflict(f"Release bundle contains a symlink: {path}")
        relative = path.relative_to(package_dir).as_posix()
        if path.is_file() and path != root_manifest:
            package_files[relative] = path
        elif path.is_dir():
            package_directories[relative] = path
        elif path != root_manifest:
            raise ReleaseConflict(
                f"Release bundle contains a special file: {path}"
            )
    if set(package_files) != set(source_files):
        missing = sorted(set(source_files) - set(package_files))
        extra = sorted(set(package_files) - set(source_files))
        raise ReleaseConflict(
            "Release bundle does not match commit-bound source files: "
            f"missing={missing}; extra={extra}"
        )
    if set(package_directories) != set(source_directories):
        missing = sorted(set(source_directories) - set(package_directories))
        extra = sorted(set(package_directories) - set(source_directories))
        raise ReleaseConflict(
            "Release bundle does not match commit-bound source directories: "
            f"missing={missing}; extra={extra}"
        )
    for relative, source in source_files.items():
        packaged = package_files[relative]
        if _sha256_file(source) != _sha256_file(packaged):
            raise ReleaseConflict(
                f"Release bundle differs from commit-bound source: {relative}"
            )


def collect_release_assets(
    repo: Path,
    dist_dir: Path,
    tag: str,
    commit: str,
    *,
    allow_legacy: bool = False,
) -> Tuple[ReleaseAsset, ...]:
    repo = repo.resolve()
    dist = dist_dir if dist_dir.is_absolute() else repo / dist_dir
    dist = dist.resolve()
    expected_version = version_text_from_tag(tag)
    legacy_layout: Optional[LegacyReleaseLayout] = None
    package_dir = dist / "codex-switch"
    runner = dist / "run.sh"
    archive = dist / "codex-switch.tar.gz"
    manifest_path = package_dir / MANIFEST_NAME
    if not os.path.lexists(str(manifest_path)) and allow_legacy:
        legacy_layout = LEGACY_RELEASE_LAYOUTS.get(tag)
        if legacy_layout is None:
            raise ReleaseError(f"Unsupported historical release layout: {tag}")
    authority_files = (
        legacy_layout.required_files
        if legacy_layout is not None
        else FIXED_FILES
    )
    authority_directories = (
        legacy_layout.required_directories
        if legacy_layout is not None
        else FIXED_DIRECTORIES
    )
    assert_release_source_matches_commit(
        repo,
        commit,
        required_files=authority_files,
        required_directories=authority_directories,
    )
    try:
        if os.path.lexists(str(manifest_path)):
            manifest = validate_release_outputs(
                package_dir,
                runner,
                archive,
                allow_historical_required_paths=allow_legacy,
            )
        else:
            if not allow_legacy:
                raise ReleaseError(
                    "Release bundle manifest is required outside explicit "
                    "historical reconciliation"
                )
            if legacy_layout is None:
                raise ReleaseError(f"Unsupported historical release layout: {tag}")
            manifest = validate_legacy_release_outputs(
                package_dir,
                runner,
                archive,
                expected_version=expected_version,
                required_files=legacy_layout.required_files,
                required_directories=legacy_layout.required_directories,
                strict_executable_modes=False,
                allow_appledouble_archive=(
                    legacy_layout.allow_appledouble_archive
                ),
            )
            canonicalize_legacy_release_archive(package_dir, archive)
    except BundleError as error:
        raise ReleaseError(f"Release bundle validation failed: {error}") from error
    if manifest.get("version") != expected_version:
        raise ReleaseConflict(
            f"Release bundle version {manifest.get('version')!r} does not match "
            f"{tag} ({expected_version})"
        )
    validate_bundle_matches_source(
        repo,
        package_dir,
        required_files=(
            authority_files
        ),
        required_directories=(
            authority_directories
        ),
    )
    version = (repo / "VERSION").read_text().strip()
    if version != expected_version:
        raise ReleaseConflict(
            f"Repository VERSION {version!r} does not match {tag} "
            f"({expected_version})"
        )
    install = repo / "install.sh"
    if (
        install.is_symlink()
        or not install.is_file()
        or not install.stat().st_mode & 0o111
    ):
        raise ReleaseError(f"Release installer is missing or not executable: {install}")
    locations = {
        "install.sh": install,
        "run.sh": dist / "run.sh",
        "codex-switch.tar.gz": dist / "codex-switch.tar.gz",
    }
    return tuple(
        build_asset_evidence(name, locations[name])
        for name in REQUIRED_RELEASE_ASSETS
    )


def _asset_payload(asset: ReleaseAsset) -> Dict[str, Any]:
    return {
        "name": asset.name,
        "path": str(asset.path),
        "size": asset.size,
        "sha256": asset.sha256,
    }


def write_asset_manifest(
    path: Path,
    *,
    tag: str,
    commit: str,
    assets: Sequence[ReleaseAsset],
) -> None:
    names = [asset.name for asset in assets]
    if names != list(REQUIRED_RELEASE_ASSETS):
        raise ReleaseError("Release asset manifest requires the canonical asset order")
    payload = {
        "schema": ASSET_MANIFEST_SCHEMA,
        "schema_version": ASSET_MANIFEST_VERSION,
        "tag": tag,
        "commit": commit,
        "assets": [_asset_payload(asset) for asset in assets],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        with path.open("x", encoding="utf-8") as handle:
            json.dump(payload, handle, sort_keys=True, indent=2)
            handle.write("\n")
    except FileExistsError as error:
        raise ReleaseError(f"Refusing to overwrite release asset manifest: {path}") from error


def load_asset_manifest(
    path: Path,
    *,
    expected_tag: str,
    expected_commit: str,
) -> Tuple[ReleaseAsset, ...]:
    try:
        payload = json.loads(path.read_text())
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ReleaseError(f"Invalid release asset manifest {path}: {error}") from error
    if (
        not isinstance(payload, dict)
        or payload.get("schema") != ASSET_MANIFEST_SCHEMA
        or type(payload.get("schema_version")) is not int
        or payload.get("schema_version") != ASSET_MANIFEST_VERSION
        or payload.get("tag") != expected_tag
        or payload.get("commit") != expected_commit
        or not isinstance(payload.get("assets"), list)
    ):
        raise ReleaseError(f"Unsupported release asset manifest: {path}")

    assets: List[ReleaseAsset] = []
    for raw in payload["assets"]:
        if (
            not isinstance(raw, dict)
            or not isinstance(raw.get("name"), str)
            or not isinstance(raw.get("path"), str)
            or type(raw.get("size")) is not int
            or not isinstance(raw.get("sha256"), str)
        ):
            raise ReleaseError(f"Invalid release asset entry in {path}")
        observed = build_asset_evidence(raw["name"], Path(raw["path"]))
        if observed.size != raw["size"] or observed.sha256 != raw["sha256"]:
            raise ReleaseConflict(
                f"Release asset changed after validation: {observed.name}"
            )
        assets.append(observed)
    if [asset.name for asset in assets] != list(REQUIRED_RELEASE_ASSETS):
        raise ReleaseError("Release asset manifest has an incomplete or reordered set")
    return tuple(assets)


def validate_prepare_state(
    *,
    source_commit: str,
    remote_main_commit: str,
    candidate_commit: str,
    existing_tag_commit: Optional[str],
) -> None:
    if remote_main_commit != source_commit:
        raise ReleaseConflict(
            f"remote main moved from {source_commit} to {remote_main_commit}"
        )
    if existing_tag_commit is not None:
        if existing_tag_commit != candidate_commit:
            raise ReleaseConflict(
                "release tag points at a different commit: "
                f"{existing_tag_commit} != {candidate_commit}"
            )
        raise ReleaseConflict(
            f"release tag already exists at {existing_tag_commit}; "
            f"candidate is {candidate_commit}"
        )


def remote_tag_commit(repo: Path, remote: str, tag: str) -> Optional[str]:
    result = _run(
        [
            "git",
            "ls-remote",
            "--tags",
            remote,
            f"refs/tags/{tag}",
            f"refs/tags/{tag}^{{}}",
        ],
        cwd=repo,
        check=False,
    )
    if result.returncode != 0:
        raise ReleaseError(
            f"Could not inspect remote tag {tag}: "
            f"{result.stderr.strip() or result.stdout.strip()}"
        )
    direct: Optional[str] = None
    peeled: Optional[str] = None
    for line in result.stdout.splitlines():
        parts = line.split()
        if len(parts) != 2:
            raise ReleaseError(f"Invalid ls-remote response for tag {tag}")
        commit, ref = parts
        if ref.endswith("^{}"):
            peeled = commit
        else:
            direct = commit
    return peeled or direct


def resolve_remote_semantic_tag(repo: Path, remote: str, tag: str) -> str:
    parse_tag(tag)
    commit = remote_tag_commit(repo, remote, tag)
    if commit is None:
        raise ReleaseConflict(f"Remote tag is missing: {tag}")
    return commit


def reconcile_release_assets(
    *,
    tag: str,
    release_commit: str,
    tag_commit: str,
    assets: Sequence[ReleaseAsset],
    github: object,
    tag_identity_check: Optional[Callable[[], None]] = None,
) -> Dict[str, Any]:
    if tag_commit != release_commit:
        raise ReleaseConflict(
            f"release tag {tag} points at a different commit: "
            f"{tag_commit} != {release_commit}"
        )
    asset_map = {asset.name: asset for asset in assets}
    if (
        len(asset_map) != len(assets)
        or tuple(asset_map) != REQUIRED_RELEASE_ASSETS
    ):
        raise ReleaseError("Reconciliation requires the canonical release asset set")
    for asset in assets:
        observed = build_asset_evidence(asset.name, asset.path)
        if observed.size != asset.size or observed.sha256 != asset.sha256:
            raise ReleaseConflict(f"Release asset changed before publish: {asset.name}")

    snapshot = github.inspect_release(tag)
    if not isinstance(snapshot, ReleaseSnapshot):
        raise ReleaseError("GitHub adapter returned an invalid release snapshot")
    existing = set(snapshot.assets) if snapshot.exists else set()
    required = set(REQUIRED_RELEASE_ASSETS)

    with tempfile.TemporaryDirectory(prefix="codex-switch-release-existing-") as raw:
        download_root = Path(raw)
        for name in REQUIRED_RELEASE_ASSETS:
            if name not in existing:
                continue
            destination = download_root / name
            github.download_asset(tag, name, destination)
            downloaded = build_asset_evidence(name, destination)
            expected = asset_map[name]
            if (
                downloaded.size != expected.size
                or downloaded.sha256 != expected.sha256
            ):
                raise ReleaseConflict(
                    f"Existing release asset checksum mismatch: {tag}/{name}"
                )

    if not snapshot.exists:
        if tag_identity_check is not None:
            tag_identity_check()
        github.create_release(tag)
        snapshot = ReleaseSnapshot(exists=True, assets=(), draft=True)

    missing = [name for name in REQUIRED_RELEASE_ASSETS if name not in existing]
    uploaded: List[str] = []
    for name in missing:
        if tag_identity_check is not None:
            tag_identity_check()
        github.upload_asset(tag, asset_map[name].path)
        uploaded.append(name)

    uploaded_snapshot = github.inspect_release(tag)
    if (
        not isinstance(uploaded_snapshot, ReleaseSnapshot)
        or not uploaded_snapshot.exists
    ):
        raise ReleaseError(f"GitHub release {tag} is missing after publication")
    uploaded_names = set(uploaded_snapshot.assets)
    still_missing = [
        name for name in REQUIRED_RELEASE_ASSETS if name not in uploaded_names
    ]
    if still_missing:
        raise ReleaseError(
            f"GitHub release {tag} is missing assets after publication: "
            f"{', '.join(still_missing)}"
        )

    with tempfile.TemporaryDirectory(
        prefix="codex-switch-release-prepublish-"
    ) as raw:
        download_root = Path(raw)
        for name in REQUIRED_RELEASE_ASSETS:
            destination = download_root / name
            github.download_asset(tag, name, destination)
            downloaded = build_asset_evidence(name, destination)
            expected = asset_map[name]
            if (
                downloaded.size != expected.size
                or downloaded.sha256 != expected.sha256
            ):
                raise ReleaseConflict(
                    f"Uploaded release asset checksum mismatch: {tag}/{name}"
                )

    published_now = False
    if uploaded_snapshot.draft:
        if tag_identity_check is not None:
            tag_identity_check()
        github.publish_release(tag)
        published_now = True

    if tag_identity_check is not None:
        tag_identity_check()
    final_snapshot = github.inspect_release(tag)
    if (
        not isinstance(final_snapshot, ReleaseSnapshot)
        or not final_snapshot.exists
        or final_snapshot.draft
    ):
        raise ReleaseError(f"GitHub release {tag} is not published")
    final_names = set(final_snapshot.assets)
    still_missing = [
        name for name in REQUIRED_RELEASE_ASSETS if name not in final_names
    ]
    if still_missing:
        raise ReleaseError(
            f"GitHub release {tag} is missing published assets: "
            f"{', '.join(still_missing)}"
        )

    verified: List[str] = []
    with tempfile.TemporaryDirectory(prefix="codex-switch-release-verify-") as raw:
        download_root = Path(raw)
        for name in REQUIRED_RELEASE_ASSETS:
            destination = download_root / name
            github.download_asset(tag, name, destination)
            downloaded = build_asset_evidence(name, destination)
            expected = asset_map[name]
            if (
                downloaded.size != expected.size
                or downloaded.sha256 != expected.sha256
            ):
                raise ReleaseConflict(
                    f"Published release asset checksum mismatch: {tag}/{name}"
                )
            verified.append(name)

    if tag_identity_check is not None:
        tag_identity_check()
    return {
        "outcome": (
            "published"
            if published_now
            else "reconciled"
            if uploaded
            else "complete"
        ),
        "tag": tag,
        "commit": release_commit,
        "uploaded_assets": sorted(uploaded),
        "verified_assets": verified,
        "asset_sha256": {
            name: asset_map[name].sha256 for name in REQUIRED_RELEASE_ASSETS
        },
    }


def _github_repository(value: Optional[str]) -> str:
    repository = value or os.environ.get("GITHUB_REPOSITORY") or os.environ.get(
        "GH_REPO"
    )
    if not repository:
        raise ReleaseError(
            "GitHub repository is required; pass --github-repo or set "
            "GITHUB_REPOSITORY"
        )
    return repository


def cmd_plan(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    github = (
        GitHubCliAdapter(_github_repository(args.github_repo))
        if args.github_repo
        else None
    )
    plan = build_plan(repo, args.head, github=github)
    if args.github_output:
        write_github_output(args.github_output, plan)
    if args.json:
        print(json.dumps(plan, indent=2, sort_keys=True))
    elif not args.github_output:
        print(f"latest_tag: {plan['latest_tag']}")
        print(f"release_action: {plan['release_action']}")
        print(f"release_required: {str(plan['release_required']).lower()}")
        if plan["target_tag"]:
            print(f"target_tag: {plan['target_tag']}")
        if plan["release_relevant_files"]:
            print("release_relevant_files:")
            for path in plan["release_relevant_files"]:
                print(f"- {path}")
    return 0


def cmd_bump(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    version_path = repo / "VERSION"
    version_path.write_text(f"{version_text_from_tag(args.tag)}\n")
    return 0


def cmd_assets(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    commit = resolve_commit(repo, args.commit)
    if args.require_tag:
        tag_commit = resolve_commit(repo, args.tag)
        if tag_commit != commit:
            raise ReleaseConflict(
                f"release tag {args.tag} points at a different commit: "
                f"{tag_commit} != {commit}"
            )
    assets = collect_release_assets(
        repo,
        args.dist_dir,
        args.tag,
        commit,
        allow_legacy=args.allow_legacy,
    )
    write_asset_manifest(
        args.manifest,
        tag=args.tag,
        commit=commit,
        assets=assets,
    )
    receipt = {
        "outcome": "assets_validated",
        "tag": args.tag,
        "commit": commit,
        "manifest": str(args.manifest),
        "assets": [_asset_payload(asset) for asset in assets],
    }
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


def cmd_prepare(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    source_commit = resolve_commit(repo, args.source_commit)
    candidate_commit = resolve_commit(repo, args.candidate_commit)
    remote_main_commit = resolve_commit(repo, args.remote_ref)
    if not is_ancestor(repo, source_commit, candidate_commit):
        raise ReleaseConflict(
            f"release candidate {candidate_commit} does not descend from "
            f"source {source_commit}"
        )
    assets = load_asset_manifest(
        args.manifest,
        expected_tag=args.tag,
        expected_commit=candidate_commit,
    )
    assert_release_source_matches_commit(repo, candidate_commit)
    local_tag_commit = optional_commit(repo, f"refs/tags/{args.tag}")
    observed_remote_tag = remote_tag_commit(repo, args.remote, args.tag)
    if (
        local_tag_commit is not None
        and observed_remote_tag is not None
        and local_tag_commit != observed_remote_tag
    ):
        raise ReleaseConflict(
            f"local and remote tag {args.tag} point at different commits"
        )
    existing_tag_commit = observed_remote_tag or local_tag_commit
    validate_prepare_state(
        source_commit=source_commit,
        remote_main_commit=remote_main_commit,
        candidate_commit=candidate_commit,
        existing_tag_commit=existing_tag_commit,
    )
    receipt = {
        "outcome": "prepared",
        "tag": args.tag,
        "source_commit": source_commit,
        "candidate_commit": candidate_commit,
        "remote_main_commit": remote_main_commit,
        "existing_tag_commit": existing_tag_commit or "",
        "assets": [_asset_payload(asset) for asset in assets],
    }
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


def cmd_reconcile(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    release_commit = resolve_commit(repo, args.commit)
    local_tag_commit = resolve_commit(repo, args.tag)
    observed_remote_tag = resolve_remote_semantic_tag(
        repo,
        args.remote,
        args.tag,
    )
    if local_tag_commit != observed_remote_tag:
        raise ReleaseConflict(
            f"local and remote tag {args.tag} point at different commits"
        )
    assets = load_asset_manifest(
        args.manifest,
        expected_tag=args.tag,
        expected_commit=release_commit,
    )
    assert_release_source_matches_commit(repo, release_commit)
    github = GitHubCliAdapter(_github_repository(args.github_repo))

    def check_remote_tag_identity() -> None:
        current_remote_tag = resolve_remote_semantic_tag(
            repo,
            args.remote,
            args.tag,
        )
        if current_remote_tag != release_commit:
            raise ReleaseConflict(
                f"remote tag {args.tag} moved from {release_commit} "
                f"to {current_remote_tag}"
            )

    receipt = reconcile_release_assets(
        tag=args.tag,
        release_commit=release_commit,
        tag_commit=observed_remote_tag,
        assets=assets,
        github=github,
        tag_identity_check=check_remote_tag_identity,
    )
    if args.json:
        print(json.dumps(receipt, indent=2, sort_keys=True))
    return 0


def cmd_resolve_tag(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    commit = resolve_remote_semantic_tag(repo, args.remote, args.tag)
    payload = {
        "outcome": "resolved",
        "tag": args.tag,
        "commit": commit,
    }
    if args.github_output:
        with args.github_output.open("a", encoding="utf-8") as handle:
            handle.write(f"tag={args.tag}\n")
            handle.write(f"commit={commit}\n")
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif not args.github_output:
        print(f"{args.tag} {commit}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--repo",
        type=Path,
        default=Path.cwd(),
        help="Repository to inspect. Default: current directory.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    plan = sub.add_parser("plan", help="Plan or resume an automatic release.")
    plan.add_argument("--head", default="HEAD")
    plan.add_argument("--github-repo")
    plan.add_argument("--json", action="store_true")
    plan.add_argument("--github-output", type=Path)
    plan.set_defaults(func=cmd_plan)

    bump = sub.add_parser("bump", help="Update VERSION to match a release tag.")
    bump.add_argument("--tag", required=True)
    bump.set_defaults(func=cmd_bump)

    assets = sub.add_parser(
        "assets",
        help="Validate deterministic local release assets and write a manifest.",
    )
    assets.add_argument("--tag", required=True)
    assets.add_argument("--commit", default="HEAD")
    assets.add_argument("--dist-dir", type=Path, default=Path("dist"))
    assets.add_argument("--manifest", type=Path, required=True)
    assets.add_argument("--require-tag", action="store_true")
    assets.add_argument(
        "--allow-legacy",
        action="store_true",
        help=(
            "Allow trusted version-scoped layouts without manifests and exact "
            "supported historical required-path manifests."
        ),
    )
    assets.add_argument("--json", action="store_true")
    assets.set_defaults(func=cmd_assets)

    prepare = sub.add_parser(
        "prepare",
        help="Validate assets and remote refs immediately before atomic push.",
    )
    prepare.add_argument("--tag", required=True)
    prepare.add_argument("--source-commit", required=True)
    prepare.add_argument("--candidate-commit", default="HEAD")
    prepare.add_argument(
        "--remote-ref",
        default="refs/remotes/origin/main",
    )
    prepare.add_argument("--remote", default="origin")
    prepare.add_argument("--manifest", type=Path, required=True)
    prepare.add_argument("--json", action="store_true")
    prepare.set_defaults(func=cmd_prepare)

    reconcile = sub.add_parser(
        "reconcile",
        help="Publish only missing assets and verify all downloaded checksums.",
    )
    reconcile.add_argument("--tag", required=True)
    reconcile.add_argument("--commit", default="HEAD")
    reconcile.add_argument("--remote", default="origin")
    reconcile.add_argument("--manifest", type=Path, required=True)
    reconcile.add_argument("--github-repo")
    reconcile.add_argument("--json", action="store_true")
    reconcile.set_defaults(func=cmd_reconcile)

    resolve_tag = sub.add_parser(
        "resolve-tag",
        help="Resolve an exact semantic tag from the configured remote.",
    )
    resolve_tag.add_argument("--tag", required=True)
    resolve_tag.add_argument("--remote", default="origin")
    resolve_tag.add_argument("--github-output", type=Path)
    resolve_tag.add_argument("--json", action="store_true")
    resolve_tag.set_defaults(func=cmd_resolve_tag)
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (
        ReleaseError,
        ValueError,
        OSError,
        subprocess.CalledProcessError,
    ) as exc:
        print(f"release_auto: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
