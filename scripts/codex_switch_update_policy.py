#!/usr/bin/env python3

from __future__ import annotations

import re
from dataclasses import dataclass
from functools import total_ordering
from typing import Iterable, Optional, Tuple, Union


_SEMVER_PATTERN = re.compile(
    r"""
    ^
    (?P<major>0|[1-9][0-9]*)
    \.
    (?P<minor>0|[1-9][0-9]*)
    \.
    (?P<patch>0|[1-9][0-9]*)
    (?:
        -
        (?P<prerelease>
            [0-9A-Za-z-]+
            (?:\.[0-9A-Za-z-]+)*
        )
    )?
    (?:
        \+
        (?P<build>
            [0-9A-Za-z-]+
            (?:\.[0-9A-Za-z-]+)*
        )
    )?
    $
    """,
    re.VERBOSE,
)
_SEMVER_SEARCH_PATTERN = re.compile(
    r"""
    (?<![0-9])
    (?P<version>
        (?:0|[1-9][0-9]*)
        \.
        (?:0|[1-9][0-9]*)
        \.
        (?:0|[1-9][0-9]*)
        (?:
            -
            [0-9A-Za-z-]+
            (?:\.[0-9A-Za-z-]+)*
        )?
        (?:
            \+
            [0-9A-Za-z-]+
            (?:\.[0-9A-Za-z-]+)*
        )?
    )
    (?![0-9A-Za-z.+-])
    """,
    re.VERBOSE,
)

PrereleasePart = Union[int, str]


@total_ordering
@dataclass(frozen=True)
class SemanticVersion:
    major: int
    minor: int
    patch: int
    prerelease: Tuple[PrereleasePart, ...] = ()

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, SemanticVersion):
            return NotImplemented

        core = (self.major, self.minor, self.patch)
        other_core = (other.major, other.minor, other.patch)
        if core != other_core:
            return core < other_core

        if not self.prerelease:
            return False
        if not other.prerelease:
            return True

        for left, right in zip(self.prerelease, other.prerelease):
            if left == right:
                continue
            if isinstance(left, int) and isinstance(right, str):
                return True
            if isinstance(left, str) and isinstance(right, int):
                return False
            return left < right
        return len(self.prerelease) < len(other.prerelease)


@dataclass(frozen=True)
class InternalUpdateDecision:
    outcome: str
    target_version: Optional[str]
    current_version: Optional[str]
    latest_version: Optional[str]
    reason: str


def parse_semantic_version(value: Optional[str]) -> Optional[SemanticVersion]:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    match = _SEMVER_PATTERN.fullmatch(normalized)
    if match is None:
        return None

    prerelease_parts = []
    prerelease = match.group("prerelease")
    if prerelease is not None:
        for part in prerelease.split("."):
            if part.isdigit():
                if len(part) > 1 and part.startswith("0"):
                    return None
                prerelease_parts.append(int(part))
            else:
                prerelease_parts.append(part)

    return SemanticVersion(
        major=int(match.group("major")),
        minor=int(match.group("minor")),
        patch=int(match.group("patch")),
        prerelease=tuple(prerelease_parts),
    )


def extract_semantic_version(text: str) -> Optional[str]:
    for match in _SEMVER_SEARCH_PATTERN.finditer(text):
        candidate = match.group("version")
        if parse_semantic_version(candidate) is not None:
            return candidate
    return None


def _parsed_blocked_versions(
    blocked_versions: Iterable[str],
) -> Optional[Tuple[SemanticVersion, ...]]:
    parsed = []
    for value in blocked_versions:
        if not isinstance(value, str):
            return None
        version = parse_semantic_version(value)
        if version is None:
            return None
        parsed.append(version)
    return tuple(parsed)


def decide_internal_update(
    *,
    current_version: Optional[str],
    latest_version: Optional[str],
    blocked_versions: Iterable[str] = (),
    fallback_version: Optional[str] = None,
) -> InternalUpdateDecision:
    blocked = _parsed_blocked_versions(blocked_versions)
    if blocked is None:
        return InternalUpdateDecision(
            outcome="failed",
            target_version=None,
            current_version=current_version,
            latest_version=latest_version,
            reason="blocked versions must all be valid semantic versions",
        )

    current = parse_semantic_version(current_version)
    if current is None:
        return InternalUpdateDecision(
            outcome="failed",
            target_version=None,
            current_version=current_version,
            latest_version=latest_version,
            reason="current version must be a valid semantic version",
        )

    current_is_blocked = current in blocked

    if current_is_blocked:
        fallback = parse_semantic_version(fallback_version)
        if fallback is None or fallback in blocked:
            return InternalUpdateDecision(
                outcome="failed",
                target_version=None,
                current_version=current_version,
                latest_version=latest_version,
                reason="blocked current version requires a valid unblocked fallback",
            )
        return InternalUpdateDecision(
            outcome="blocked_fallback",
            target_version=fallback_version.strip()
            if fallback_version is not None
            else None,
            current_version=current_version,
            latest_version=latest_version,
            reason="current version is explicitly blocked",
        )

    latest = parse_semantic_version(latest_version)
    if latest is None:
        return InternalUpdateDecision(
            outcome="failed",
            target_version=None,
            current_version=current_version,
            latest_version=latest_version,
            reason="latest version must be a valid semantic version",
        )

    latest_is_blocked = latest in blocked

    if current > latest:
        return InternalUpdateDecision(
            outcome="newer_current",
            target_version=None,
            current_version=current_version,
            latest_version=latest_version,
            reason="healthy current version is newer than the reported latest",
        )

    if current == latest:
        return InternalUpdateDecision(
            outcome="up_to_date",
            target_version=None,
            current_version=current_version,
            latest_version=latest_version,
            reason="current version matches the reported latest",
        )

    if latest_is_blocked:
        return InternalUpdateDecision(
            outcome="failed",
            target_version=None,
            current_version=current_version,
            latest_version=latest_version,
            reason="reported latest is blocked and healthy current cannot be downgraded",
        )

    return InternalUpdateDecision(
        outcome="upgrade",
        target_version=latest_version.strip()
        if latest_version is not None
        else None,
        current_version=current_version,
        latest_version=latest_version,
        reason="healthy current version is older than the reported latest",
    )
