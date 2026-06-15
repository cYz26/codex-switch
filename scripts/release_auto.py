#!/usr/bin/env python3
"""Plan and prepare automatic codex-switch patch releases."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SEMVER_TAG = re.compile(r"^v(\d+)\.(\d+)\.(\d+)$")


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=repo,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return result.stdout.strip()


def parse_tag(tag: str) -> tuple[int, int, int]:
    match = SEMVER_TAG.match(tag)
    if not match:
        raise ValueError(f"Expected semantic release tag like v1.2.3, got {tag!r}")
    return tuple(int(part) for part in match.groups())


def format_tag(version: tuple[int, int, int]) -> str:
    return f"v{version[0]}.{version[1]}.{version[2]}"


def version_text_from_tag(tag: str) -> str:
    major, minor, patch = parse_tag(tag)
    return f"{major}.{minor}.{patch}"


def latest_release_tag(repo: Path) -> str:
    raw = run_git(repo, "tag", "--list", "v[0-9]*.[0-9]*.[0-9]*")
    tags = [tag for tag in raw.splitlines() if SEMVER_TAG.match(tag)]
    if not tags:
        raise RuntimeError("No semantic release tags found")
    return max(tags, key=parse_tag)


def next_patch_tag(tag: str) -> str:
    major, minor, patch = parse_tag(tag)
    return format_tag((major, minor, patch + 1))


def changed_files(repo: Path, base_tag: str, head: str) -> list[str]:
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


def build_plan(repo: Path, head: str) -> dict[str, Any]:
    latest_tag = latest_release_tag(repo)
    files = changed_files(repo, latest_tag, head)
    relevant = [path for path in files if is_release_relevant(path)]
    required = bool(relevant)
    proposed_tag = next_patch_tag(latest_tag) if required else ""
    return {
        "latest_tag": latest_tag,
        "head": run_git(repo, "rev-parse", "--short", head),
        "changed_files": files,
        "release_relevant_files": relevant,
        "release_required": required,
        "next_tag": proposed_tag,
        "next_version": version_text_from_tag(proposed_tag) if proposed_tag else "",
    }


def write_github_output(path: Path, plan: dict[str, Any]) -> None:
    release_files = ",".join(plan["release_relevant_files"])
    with path.open("a", encoding="utf-8") as handle:
        handle.write(f"release_required={str(plan['release_required']).lower()}\n")
        handle.write(f"latest_tag={plan['latest_tag']}\n")
        handle.write(f"next_tag={plan['next_tag']}\n")
        handle.write(f"next_version={plan['next_version']}\n")
        handle.write(f"release_files={release_files}\n")


def cmd_plan(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    plan = build_plan(repo, args.head)
    if args.github_output:
        write_github_output(args.github_output, plan)
    if args.json:
        print(json.dumps(plan, indent=2, sort_keys=True))
    elif not args.github_output:
        print(f"latest_tag: {plan['latest_tag']}")
        print(f"release_required: {str(plan['release_required']).lower()}")
        if plan["release_required"]:
            print(f"next_tag: {plan['next_tag']}")
            print("release_relevant_files:")
            for path in plan["release_relevant_files"]:
                print(f"- {path}")
    return 0


def cmd_bump(args: argparse.Namespace) -> int:
    repo = args.repo.resolve()
    version_path = repo / "VERSION"
    version_path.write_text(f"{version_text_from_tag(args.tag)}\n")
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

    plan = sub.add_parser("plan", help="Plan whether HEAD needs an automatic release.")
    plan.add_argument("--head", default="HEAD")
    plan.add_argument("--json", action="store_true")
    plan.add_argument("--github-output", type=Path)
    plan.set_defaults(func=cmd_plan)

    bump = sub.add_parser("bump", help="Update VERSION to match a release tag.")
    bump.add_argument("--tag", required=True)
    bump.set_defaults(func=cmd_bump)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except (RuntimeError, ValueError, subprocess.CalledProcessError) as exc:
        print(f"release_auto: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
