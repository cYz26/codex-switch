#!/usr/bin/env python3

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path


SCRIPTS_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPTS_DIR))

from codex_switch_official_release import (
    compare_to_official_stable,
    resolve_profile_advisory_cli,
)
from codex_switch_runtime_binding import (
    ChatGPTDesktopHost,
    DesktopInventory,
)
from codex_switch_store import Store


def write_executable(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("#!/bin/sh\nexit 0\n")
    path.chmod(0o755)
    return path


class CodexOfficialStableComparisonTests(unittest.TestCase):
    def assert_comparison(
        self,
        current_output: str,
        stable_tag: str,
        *,
        outcome: str,
        current_version: str | None,
        stable_version: str | None,
        current_is_prerelease: bool = False,
    ) -> None:
        result = compare_to_official_stable(current_output, stable_tag)

        self.assertEqual(outcome, result.outcome)
        self.assertEqual(current_version, result.current_version)
        self.assertEqual(stable_version, result.stable_version)
        self.assertEqual(current_is_prerelease, result.current_is_prerelease)
        self.assertTrue(result.reason)
        self.assertFalse(hasattr(result, "target_version"))

    def test_compares_behind_matching_and_ahead_versions(self) -> None:
        cases = (
            ("codex-cli 0.144.6", "behind"),
            ("codex-cli 0.145.0", "matches"),
            ("codex-cli 0.146.0", "ahead"),
        )
        for current_output, outcome in cases:
            with self.subTest(current_output=current_output):
                self.assert_comparison(
                    current_output,
                    "rust-v0.145.0",
                    outcome=outcome,
                    current_version=current_output.removeprefix("codex-cli "),
                    stable_version="0.145.0",
                )

    def test_current_prerelease_uses_semantic_order_against_stable(self) -> None:
        self.assert_comparison(
            "codex-cli 0.145.0-alpha.30",
            "rust-v0.145.0",
            outcome="behind",
            current_version="0.145.0-alpha.30",
            stable_version="0.145.0",
            current_is_prerelease=True,
        )
        self.assert_comparison(
            "codex-cli 0.146.0-alpha.3",
            "rust-v0.145.0",
            outcome="ahead",
            current_version="0.146.0-alpha.3",
            stable_version="0.145.0",
            current_is_prerelease=True,
        )

    def test_invalid_current_output_is_unknown(self) -> None:
        self.assert_comparison(
            "codex-cli unknown",
            "rust-v0.145.0",
            outcome="unknown",
            current_version=None,
            stable_version="0.145.0",
        )

    def test_invalid_or_prerelease_stable_tag_is_unknown(self) -> None:
        for stable_tag in (
            "",
            "v0.145.0",
            "rust-v0.145.0-alpha.6",
            "rust-vlatest",
            "https://github.com/openai/codex/releases/tag/rust-v0.145.0",
        ):
            with self.subTest(stable_tag=stable_tag):
                self.assert_comparison(
                    "codex-cli 0.144.6",
                    stable_tag,
                    outcome="unknown",
                    current_version="0.144.6",
                    stable_version=None,
                )

    def test_canonical_official_advisory_ignores_manifest_drift(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")
            profile = store.profile_dir("openai-official")
            profile.mkdir(parents=True)
            stale = write_executable(root / "stale" / "codex")
            bundled = write_executable(
                root / "ChatGPT.app" / "Contents" / "Resources" / "codex"
            )
            main = write_executable(
                root / "ChatGPT.app" / "Contents" / "MacOS" / "ChatGPT"
            )
            store.manifest_path("openai-official").write_text(
                (
                    '{"name":"openai-official","runtime_binding":"canonical",'
                    f'"codex_bin":"{stale}","app_cli_path":"{stale}"}}'
                )
            )
            inventory = DesktopInventory(
                current=ChatGPTDesktopHost(
                    kind="chatgpt",
                    bundle_root=root / "ChatGPT.app",
                    bundle_id="com.openai.codex",
                    main_executable=main,
                    bundled_cli=bundled,
                    healthy=True,
                )
            )

            resolved = resolve_profile_advisory_cli(
                store,
                "openai-official",
                inventory=inventory,
            )

            self.assertEqual(bundled, resolved)

    def test_explicit_official_advisory_preserves_manifest_binding(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            live = root / "live"
            live.mkdir()
            store = Store(root / "store", live, root / "agent.plist")
            profile = store.profile_dir("openai-official")
            profile.mkdir(parents=True)
            explicit = write_executable(root / "explicit" / "codex")
            bundled = write_executable(
                root / "ChatGPT.app" / "Contents" / "Resources" / "codex"
            )
            main = write_executable(
                root / "ChatGPT.app" / "Contents" / "MacOS" / "ChatGPT"
            )
            store.manifest_path("openai-official").write_text(
                (
                    '{"name":"openai-official",'
                    '"runtime_binding":"explicit-compatibility",'
                    f'"codex_bin":"{explicit}","app_cli_path":"{explicit}"}}'
                )
            )
            inventory = DesktopInventory(
                current=ChatGPTDesktopHost(
                    kind="chatgpt",
                    bundle_root=root / "ChatGPT.app",
                    bundle_id="com.openai.codex",
                    main_executable=main,
                    bundled_cli=bundled,
                    healthy=True,
                )
            )

            resolved = resolve_profile_advisory_cli(
                store,
                "openai-official",
                inventory=inventory,
            )

            self.assertEqual(explicit, resolved)


if __name__ == "__main__":
    unittest.main()
