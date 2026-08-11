#!/usr/bin/env python3

from __future__ import annotations

import base64
import fcntl
import importlib
import json
import os
import shutil
import signal
import stat
import sys
import tempfile
import time
import unittest
from pathlib import Path
from types import SimpleNamespace
from typing import Any, Iterable
from unittest.mock import patch

from codex_switch_selection import ProfileSelection
from codex_switch_store import Store


SELECTOR = "demo@team"
SECOND_SELECTOR = "second@team"
OFFICIAL_SECRET = "OFFICIAL-MCP-TOKEN-MUST-NOT-BE-SHARED"
INTERNAL_SECRET = "INTERNAL-MCP-TOKEN-MUST-STAY-LOCAL"


class SimulatedSharedCommitCrash(BaseException):
    pass


def shared_configuration_module():
    try:
        return importlib.import_module("codex_switch_shared_configuration")
    except ModuleNotFoundError as exc:
        if exc.name != "codex_switch_shared_configuration":
            raise
        raise AssertionError(
            "codex_switch_shared_configuration public module is required"
        ) from exc


def toml_string(value: str | Path) -> str:
    return json.dumps(str(value))


def finding_codes(result: Any) -> tuple[str, ...]:
    return tuple(
        str(getattr(finding, "code", finding)) for finding in result.findings
    )


def tree_snapshot(*roots: Path) -> dict[str, tuple[Any, ...]]:
    snapshot: dict[str, tuple[Any, ...]] = {}
    for root in roots:
        root_key = str(root)
        if not root.exists() and not root.is_symlink():
            snapshot[root_key] = ("missing",)
            continue
        paths = [root]
        if root.is_dir() and not root.is_symlink():
            paths.extend(sorted(root.rglob("*"), key=lambda path: str(path)))
        for path in paths:
            key = str(path)
            metadata = path.lstat()
            mode = stat.S_IMODE(metadata.st_mode)
            if path.is_symlink():
                snapshot[key] = ("symlink", mode, os.readlink(path))
            elif path.is_file():
                snapshot[key] = ("file", mode, path.read_bytes())
            else:
                snapshot[key] = ("directory", mode)
    return snapshot


class SharedConfigurationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.official_home = self.root / "official-home"
        self.internal_home = self.root / "internal-home"
        self.official_home.mkdir()
        self.internal_home.mkdir()
        (self.official_home / "plugins" / "cache").mkdir(parents=True)
        (self.internal_home / "plugins" / "cache").mkdir(parents=True)
        self.official_skills = self.official_home / "skills"
        self.official_skills.mkdir()
        (self.official_skills / "personal-skill").mkdir()
        (self.official_skills / "personal-skill" / "SKILL.md").write_text(
            "# personal skill\n"
        )
        self.store = Store(
            self.root / "store",
            official_codex_home=self.official_home,
            internal_codex_home=self.internal_home,
            launch_agent_path=self.root / "LaunchAgent.plist",
            launch_agent_label="com.example.codex-switch-tests",
        )
        self.store.ensure()
        self.selection = ProfileSelection(
            cli_profile="internal",
            app_profile="openai-official",
            app_profile_explicit=True,
        )
        self.materialize_calls: list[dict[str, Any]] = []
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True),),
        )
        self._write_config(
            self.internal_home,
            profile_marker="internal",
            plugins=(("legacy@internal-only", False),),
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def _config_text(
        self,
        *,
        profile_marker: str,
        plugins: Iterable[tuple[str, bool]] = (),
        skill_paths: Iterable[Path] = (),
        include_marketplace: bool = True,
        marketplace_extra: str = "",
        shared_comment: str = "",
        reverse_plugins: bool = False,
    ) -> str:
        secret = OFFICIAL_SECRET if profile_marker == "official" else INTERNAL_SECRET
        chunks = [
            f'model = "{profile_marker}-model"\n',
            'model_provider = "profile-local"\n',
            'cli_auth_credentials_store = "keyring"\n',
            "\n",
            f"[mcp_servers.{profile_marker}_private]\n",
            f'command = "{profile_marker}-connector"\n',
            f'env = {{ PRIVATE_TOKEN = "{secret}" }}\n',
            "\n",
        ]
        if include_marketplace:
            chunks.extend(
                [
                    "[marketplaces.team]\n",
                    'source_type = "github"\n',
                    'source = "team/plugins"\n',
                ]
            )
            if marketplace_extra:
                chunks.append(marketplace_extra.rstrip() + "\n")
            chunks.append("\n")
        if shared_comment:
            chunks.append(f"# {shared_comment}\n")
        plugin_entries = list(plugins)
        if reverse_plugins:
            plugin_entries.reverse()
        for selector, enabled in plugin_entries:
            chunks.extend(
                [
                    f'[plugins."{selector}"]\n',
                    f"enabled = {'true' if enabled else 'false'}\n",
                    "\n",
                ]
            )
        for skill_path in skill_paths:
            chunks.extend(
                [
                    "[[skills.config]]\n",
                    f"path = {toml_string(skill_path)}\n",
                    "enabled = true\n",
                    "\n",
                ]
            )
        return "".join(chunks)

    def _write_config(
        self,
        home: Path,
        *,
        profile_marker: str,
        plugins: Iterable[tuple[str, bool]] = (),
        skill_paths: Iterable[Path] = (),
        include_marketplace: bool = True,
        marketplace_extra: str = "",
        shared_comment: str = "",
        reverse_plugins: bool = False,
    ) -> None:
        (home / "config.toml").write_text(
            self._config_text(
                profile_marker=profile_marker,
                plugins=plugins,
                skill_paths=skill_paths,
                include_marketplace=include_marketplace,
                marketplace_extra=marketplace_extra,
                shared_comment=shared_comment,
                reverse_plugins=reverse_plugins,
            )
        )

    def _write_plugin_artifact(
        self,
        home: Path,
        *,
        selector: str = SELECTOR,
        version: str,
        payload: str,
    ) -> Path:
        plugin, marketplace = selector.rsplit("@", 1)
        artifact = home / "plugins" / "cache" / marketplace / plugin / version
        manifest = artifact / ".codex-plugin" / "plugin.json"
        manifest.parent.mkdir(parents=True, exist_ok=True)
        manifest.write_text(
            json.dumps(
                {
                    "name": plugin,
                    "version": version,
                    "skills": "./skills/",
                }
            )
            + "\n"
        )
        (artifact / "payload.txt").write_text(payload)
        skill = artifact / "skills" / "fixture" / "SKILL.md"
        skill.parent.mkdir(parents=True, exist_ok=True)
        skill.write_text("# materialized skill\n")
        return artifact

    def _selector(self, desired: Any) -> str:
        if isinstance(desired, dict):
            return str(desired["selector"])
        selector = getattr(desired, "selector", None)
        if selector is not None:
            return str(selector)
        return str(desired)

    def _materialize_plugins(self, **kwargs: Any) -> tuple[dict[str, Any], ...]:
        module = importlib.import_module("codex_switch_plugins")
        self.materialize_calls.append(dict(kwargs))
        target_profile = str(kwargs["target_profile"])
        target_home = (
            self.internal_home
            if target_profile == "internal"
            else self.official_home
        )
        receipts: list[dict[str, Any]] = []
        for desired in kwargs.get("desired_plugins", ()):
            selector = self._selector(desired)
            plugin, marketplace = selector.rsplit("@", 1)
            policy = str(getattr(desired, "policy", "backend_managed"))
            desired_key = str(getattr(desired, "cache_key", ""))
            cache_key = desired_key if policy == "portable_exact" else "1.0.0"
            artifact = (
                target_home
                / "plugins"
                / "cache"
                / marketplace
                / plugin
                / cache_key
            )
            source_artifact = Path(str(getattr(desired, "source_artifact", "")))
            if policy == "portable_exact" and source_artifact.is_dir():
                shutil.copytree(
                    source_artifact,
                    artifact,
                    dirs_exist_ok=True,
                    symlinks=True,
                )
            skill_root = artifact / "skills"
            skill_root.mkdir(parents=True, exist_ok=True)
            manifest = artifact / ".codex-plugin" / "plugin.json"
            if not manifest.exists():
                manifest.parent.mkdir(parents=True, exist_ok=True)
                manifest.write_text(
                    json.dumps(
                        {
                            "name": plugin,
                            "version": cache_key,
                            "skills": "./skills/",
                        }
                    )
                    + "\n"
                )
            if not (skill_root / "SKILL.md").exists() and policy != "portable_exact":
                (skill_root / "SKILL.md").write_text("# materialized skill\n")
            receipts.append(
                {
                    "selector": selector,
                    "policy": policy,
                    "cache_key": cache_key,
                    "manifest_version": json.loads(manifest.read_text())["version"],
                    "tree_sha256": module.plugin_tree_sha256(artifact),
                    "skill_roots": (str(skill_root),),
                }
            )
        return tuple(receipts)

    def _adapters(
        self,
        *,
        app_running: bool = False,
        before_commit: Any = None,
        read_stable: Any = None,
        app_is_running: Any = None,
        commit_checkpoint: Any = None,
    ) -> SimpleNamespace:
        return SimpleNamespace(
            read_stable=read_stable or (lambda path: path.read_text()),
            app_is_running=(
                app_is_running
                if app_is_running is not None
                else lambda store, selection: app_running
            ),
            materialize_plugins=self._materialize_plugins,
            before_commit=before_commit or (lambda store, selection, plan: None),
            commit_checkpoint=(
                commit_checkpoint
                if commit_checkpoint is not None
                else lambda **_kwargs: None
            ),
        )

    def _reconcile(
        self,
        *,
        boundary: str = "cli-preflight",
        mode: str = "apply",
        adapters: Any = None,
    ) -> Any:
        module = shared_configuration_module()
        return module.reconcile_shared_configuration(
            self.store,
            self.selection,
            boundary=boundary,
            mode=mode,
            adapters=adapters or self._adapters(),
        )

    def _report(self, store: Store | None = None) -> Any:
        module = shared_configuration_module()
        return module.shared_configuration_report(store or self.store, self.selection)

    def _assert_generation(
        self,
        result: Any,
        *,
        status: str,
        before: int,
        after: int,
        cli_ready: bool,
        pending_target: str | None = None,
    ) -> None:
        self.assertEqual(status, result.status)
        self.assertEqual(before, result.generation_before)
        self.assertEqual(after, result.generation_after)
        self.assertEqual(cli_ready, result.cli_ready)
        self.assertEqual(pending_target, result.pending_target)

    def test_official_projection_bootstraps_secret_safe_generation(self) -> None:
        result = self._reconcile()

        self._assert_generation(
            result,
            status="applied",
            before=0,
            after=1,
            cli_ready=True,
        )
        self.assertIn("shared_configuration.bootstrap", finding_codes(result))
        internal_config = (self.internal_home / "config.toml").read_text()
        self.assertIn('model = "internal-model"', internal_config)
        self.assertIn(INTERNAL_SECRET, internal_config)
        self.assertIn('[plugins."demo@team"]', internal_config)
        self.assertNotIn('model = "official-model"', internal_config)
        self.assertNotIn(OFFICIAL_SECRET, internal_config)
        persisted_store_bytes = b"\n".join(
            path.read_bytes()
            for path in sorted(self.store.root.rglob("*"))
            if path.is_file()
        )
        self.assertNotIn(OFFICIAL_SECRET.encode(), persisted_store_bytes)
        self.assertNotIn(b"official-model", persisted_store_bytes)
        reopened_store = Store(
            self.store.root,
            official_codex_home=self.official_home,
            internal_codex_home=self.internal_home,
            launch_agent_path=self.store.launch_agent_path,
            launch_agent_label=self.store.launch_agent_label,
        )
        report = self._report(reopened_store)
        self._assert_generation(
            report,
            status="current",
            before=1,
            after=1,
            cli_ready=True,
        )

    def test_semantic_noop_keeps_generation_and_all_bytes_unchanged(self) -> None:
        self._reconcile()
        before = tree_snapshot(self.store.root, self.official_home, self.internal_home)
        materialize_count = len(self.materialize_calls)

        result = self._reconcile()

        self._assert_generation(
            result,
            status="current",
            before=1,
            after=1,
            cli_ready=True,
        )
        self.assertEqual(materialize_count, len(self.materialize_calls))
        self.assertEqual(
            before,
            tree_snapshot(self.store.root, self.official_home, self.internal_home),
        )

    def test_single_official_change_advances_one_generation(self) -> None:
        self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, False)),
        )

        result = self._reconcile()

        self._assert_generation(
            result,
            status="applied",
            before=1,
            after=2,
            cli_ready=True,
        )
        internal_config = (self.internal_home / "config.toml").read_text()
        self.assertIn(f'[plugins."{SECOND_SELECTOR}"]', internal_config)
        self.assertIn('model = "internal-model"', internal_config)

    def test_single_internal_change_applies_at_explicit_stopped_app_boundary(self) -> None:
        self._reconcile()
        self._write_config(
            self.internal_home,
            profile_marker="internal",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, False)),
        )

        result = self._reconcile(
            boundary="explicit-sync",
            adapters=self._adapters(app_running=False),
        )

        self._assert_generation(
            result,
            status="applied",
            before=1,
            after=2,
            cli_ready=True,
        )
        official_config = (self.official_home / "config.toml").read_text()
        self.assertIn(f'[plugins."{SECOND_SELECTOR}"]', official_config)
        self.assertIn('model = "official-model"', official_config)
        self.assertIn(OFFICIAL_SECRET, official_config)

    def test_internal_change_records_pending_state_while_app_is_running(self) -> None:
        self._reconcile()
        self._write_config(
            self.internal_home,
            profile_marker="internal",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, False)),
        )
        official_before = tree_snapshot(self.official_home)

        result = self._reconcile(
            boundary="cli-preflight",
            adapters=self._adapters(app_running=True),
        )

        self._assert_generation(
            result,
            status="pending",
            before=1,
            after=2,
            cli_ready=True,
            pending_target="openai-official",
        )
        self.assertEqual(official_before, tree_snapshot(self.official_home))
        report = self._report()
        self._assert_generation(
            report,
            status="pending",
            before=2,
            after=2,
            cli_ready=True,
            pending_target="openai-official",
        )

    def test_identical_semantic_changes_coalesce_despite_formatting(self) -> None:
        self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, False)),
            shared_comment="official formatting",
        )
        self._write_config(
            self.internal_home,
            profile_marker="internal",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, False)),
            shared_comment="internal formatting",
            reverse_plugins=True,
        )

        result = self._reconcile()

        self._assert_generation(
            result,
            status="applied",
            before=1,
            after=2,
            cli_ready=True,
        )
        self.assertNotIn("shared_configuration.conflict", finding_codes(result))

    def test_divergent_changes_report_conflict_with_zero_reconcile_writes(self) -> None:
        self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, False),),
        )
        self._write_config(
            self.internal_home,
            profile_marker="internal",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, False)),
        )
        before = tree_snapshot(self.store.root, self.official_home, self.internal_home)

        result = self._reconcile()

        self._assert_generation(
            result,
            status="conflict",
            before=1,
            after=1,
            cli_ready=False,
        )
        self.assertEqual(
            ("shared_configuration.conflict",), finding_codes(result)
        )
        self.assertEqual(
            before,
            tree_snapshot(self.store.root, self.official_home, self.internal_home),
        )

    def test_delete_versus_modify_reports_conflict_with_zero_writes(self) -> None:
        self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=(),
            include_marketplace=False,
        )
        self._write_config(
            self.internal_home,
            profile_marker="internal",
            plugins=((SELECTOR, False),),
        )
        before = tree_snapshot(self.store.root, self.official_home, self.internal_home)

        result = self._reconcile()

        self._assert_generation(
            result,
            status="conflict",
            before=1,
            after=1,
            cli_ready=False,
        )
        self.assertEqual(
            ("shared_configuration.conflict",), finding_codes(result)
        )
        self.assertEqual(
            before,
            tree_snapshot(self.store.root, self.official_home, self.internal_home),
        )

    def test_authoritative_disable_is_not_revived_from_internal_baseline(self) -> None:
        self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, False),),
        )

        first = self._reconcile()
        second = self._reconcile()

        self._assert_generation(
            first,
            status="applied",
            before=1,
            after=2,
            cli_ready=True,
        )
        self._assert_generation(
            second,
            status="current",
            before=2,
            after=2,
            cli_ready=True,
        )
        internal_config = (self.internal_home / "config.toml").read_text()
        self.assertIn(f'[plugins."{SELECTOR}"]\nenabled = false', internal_config)

    def test_authoritative_removal_clears_stale_plugin_marketplace_and_skill(self) -> None:
        removed_skill = self.official_skills / "personal-skill" / "SKILL.md"
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True),),
            skill_paths=(removed_skill,),
        )
        self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=(),
            include_marketplace=False,
        )

        result = self._reconcile()

        self._assert_generation(
            result,
            status="applied",
            before=1,
            after=2,
            cli_ready=True,
        )
        internal_config = (self.internal_home / "config.toml").read_text()
        self.assertNotIn("[marketplaces.team]", internal_config)
        self.assertNotIn(f'[plugins."{SELECTOR}"]', internal_config)
        self.assertNotIn("[[skills.config]]", internal_config)
        self.assertTrue((self.internal_home / "plugins" / "cache").is_dir())

    def test_secret_bearing_marketplace_is_rejected_without_persistence(self) -> None:
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True),),
            marketplace_extra='api_token = "TOP-SECRET-MARKETPLACE-VALUE"',
        )
        before = tree_snapshot(self.store.root, self.official_home, self.internal_home)

        result = self._reconcile()

        self._assert_generation(
            result,
            status="blocked",
            before=0,
            after=0,
            cli_ready=False,
        )
        self.assertEqual(
            ("shared_configuration.secret_field",), finding_codes(result)
        )
        self.assertEqual(
            before,
            tree_snapshot(self.store.root, self.official_home, self.internal_home),
        )
        self.assertNotIn(
            b"TOP-SECRET-MARKETPLACE-VALUE",
            b"\n".join(
                path.read_bytes()
                for path in sorted(self.store.root.rglob("*"))
                if path.is_file()
            ),
        )

    def test_credential_bearing_marketplace_values_are_rejected(self) -> None:
        rejected_values = (
            "https://user:TOP-SECRET@example.invalid/plugins.git",
            "https://example.invalid/plugins.git?api_token=TOP-SECRET",
            "https://example.invalid/plugins.git#TOP-SECRET",
        )
        for value in rejected_values:
            with self.subTest(value=value):
                text = self._config_text(
                    profile_marker="official",
                    plugins=((SELECTOR, True),),
                ).replace(
                    'source = "team/plugins"',
                    "source = { source = \"git\", "
                    f"url = {toml_string(value)} }}",
                )
                (self.official_home / "config.toml").write_text(text)
                result = self._reconcile()

                self.assertEqual("blocked", result.status)
                self.assertFalse(result.cli_ready)
                self.assertEqual(
                    ("shared_configuration.secret_value",),
                    finding_codes(result),
                )
                persisted = b"\n".join(
                    path.read_bytes()
                    for path in sorted(self.store.root.rglob("*"))
                    if path.is_file()
                )
                self.assertNotIn(value.encode(), persisted)

    def test_target_config_change_after_plan_is_not_absorbed_into_baseline(self) -> None:
        bootstrap = self._reconcile()
        self.assertEqual("applied", bootstrap.status)
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, True)),
        )
        store_before = tree_snapshot(self.store.root)

        def mutate_target(store: Store, selection: ProfileSelection, plan: Any) -> None:
            del store, selection, plan
            path = self.internal_home / "config.toml"
            path.write_text(
                path.read_text()
                + '\n[plugins."concurrent@team"]\nenabled = true\n'
            )

        result = self._reconcile(
            adapters=self._adapters(before_commit=mutate_target)
        )

        self.assertEqual("blocked", result.status)
        self.assertFalse(result.cli_ready)
        self.assertEqual(
            ("shared_configuration.target_changed_during_plan",),
            finding_codes(result),
        )
        self.assertEqual(store_before, tree_snapshot(self.store.root))
        self.assertIn(
            '[plugins."concurrent@team"]',
            (self.internal_home / "config.toml").read_text(),
        )

    def test_target_config_change_during_materialization_is_preserved(self) -> None:
        first = self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, True)),
        )
        internal_config = self.internal_home / "config.toml"

        def materialize_with_foreign_edit(**kwargs: Any) -> tuple[dict[str, Any], ...]:
            receipts = self._materialize_plugins(**kwargs)
            internal_config.write_text(
                internal_config.read_text()
                + "\n[foreign_edit]\npreserve_me = true\n"
            )
            return receipts

        adapters = self._adapters()
        adapters.materialize_plugins = materialize_with_foreign_edit

        result = self._reconcile(adapters=adapters)

        self.assertEqual("blocked", result.status)
        self.assertFalse(result.cli_ready)
        self.assertEqual(
            ("shared_configuration.target_changed_during_plan",),
            finding_codes(result),
        )
        self.assertEqual(first.generation_after, result.generation_after)
        self.assertIn("[foreign_edit]", internal_config.read_text())
        self.assertIn("preserve_me = true", internal_config.read_text())

    def test_commit_time_running_app_preserves_pending_official_apply(self) -> None:
        self._reconcile()
        internal_config = self.internal_home / "config.toml"
        internal_config.write_text(
            internal_config.read_text().replace("enabled = true", "enabled = false")
        )
        pending = self._reconcile(adapters=self._adapters(app_running=True))
        self.assertEqual("pending", pending.status)
        official_before = tree_snapshot(self.official_home)
        app_checks: list[int] = []

        def app_is_running(store: Store, selection: ProfileSelection) -> bool:
            del store, selection
            app_checks.append(len(app_checks) + 1)
            return len(app_checks) >= 3

        result = self._reconcile(
            boundary="explicit-sync",
            adapters=self._adapters(app_is_running=app_is_running),
        )

        self.assertGreaterEqual(len(app_checks), 3)
        self.assertEqual("pending", result.status)
        self.assertTrue(result.cli_ready)
        self.assertEqual("openai-official", result.pending_target)
        self.assertIn(
            "shared_configuration.pending_app_apply",
            finding_codes(result),
        )
        self.assertEqual(official_before, tree_snapshot(self.official_home))

    def test_official_app_recheck_blocks_before_target_materialization(self) -> None:
        self._reconcile()
        internal_config = self.internal_home / "config.toml"
        internal_config.write_text(
            internal_config.read_text().replace(
                'source = "team/plugins"',
                'source = "team/plugins-next"',
            )
        )
        pending = self._reconcile(adapters=self._adapters(app_running=True))
        self.assertEqual("pending", pending.status)
        self.materialize_calls.clear()
        official_before = tree_snapshot(self.official_home)
        app_checks: list[int] = []

        def app_is_running(store: Store, selection: ProfileSelection) -> bool:
            del store, selection
            app_checks.append(len(app_checks) + 1)
            return len(app_checks) >= 3

        result = self._reconcile(
            boundary="explicit-sync",
            adapters=self._adapters(app_is_running=app_is_running),
        )

        self.assertEqual("pending", result.status)
        self.assertEqual("openai-official", result.pending_target)
        self.assertEqual([], self.materialize_calls)
        self.assertGreaterEqual(len(app_checks), 3)
        self.assertEqual(official_before, tree_snapshot(self.official_home))
        self.assertFalse(
            (
                self.store.root
                / "shared-configuration"
                / "pending-materialization.json"
            ).exists()
        )

    def test_default_stopped_app_proof_fails_closed_on_inventory_or_any_app_process(self) -> None:
        module = shared_configuration_module()
        runtime = SimpleNamespace(home=self.official_home, binding=None)
        process_cases = (
            ((1, ""), (), "unreadable inventory"),
            (
                (0, "fixture process inventory"),
                (SimpleNamespace(kind="desktop"),),
                "Desktop main process",
            ),
            (
                (0, "fixture process inventory"),
                (SimpleNamespace(kind="app-server"),),
                "mismatched app-server",
            ),
        )
        for ps_result, processes, label in process_cases:
            with self.subTest(label=label):
                with (
                    patch(
                        "codex_switch_plugins.profile_plugin_runtime",
                        return_value=runtime,
                    ),
                    patch(
                        "codex_switch_plugins.running_target_app_server_pids",
                        return_value=[],
                    ),
                    patch.object(
                        module,
                        "run_quiet",
                        return_value=ps_result,
                        create=True,
                    ),
                    patch.object(
                        module,
                        "running_codex_processes",
                        return_value=list(processes),
                        create=True,
                    ),
                ):
                    self.assertTrue(
                        module._default_app_is_running(
                            self.store,
                            self.selection,
                        )
                    )

    def test_source_change_before_commit_fails_without_mixed_generation(self) -> None:
        internal_before = (self.internal_home / "config.toml").read_bytes()
        store_before = tree_snapshot(self.store.root)

        def mutate_source(store: Store, selection: ProfileSelection, plan: Any) -> None:
            del store, selection, plan
            path = self.official_home / "config.toml"
            path.write_text(path.read_text() + "# changed during plan\n")

        result = self._reconcile(
            adapters=self._adapters(before_commit=mutate_source)
        )

        self._assert_generation(
            result,
            status="blocked",
            before=0,
            after=0,
            cli_ready=False,
        )
        self.assertEqual(
            ("shared_configuration.source_changed_during_plan",),
            finding_codes(result),
        )
        self.assertEqual(internal_before, (self.internal_home / "config.toml").read_bytes())
        self.assertEqual(store_before, tree_snapshot(self.store.root))
        self.assertFalse((self.internal_home / "skills").exists())

    def test_missing_internal_personal_skills_entry_creates_canonical_link(self) -> None:
        internal_skills = self.internal_home / "skills"
        self.assertFalse(internal_skills.exists())

        result = self._reconcile()

        self.assertEqual("applied", result.status)
        self.assertTrue(internal_skills.is_symlink())
        self.assertEqual(
            self.official_skills.resolve(),
            internal_skills.resolve(),
        )

    def test_correct_personal_skills_link_is_preserved_and_noop_safe(self) -> None:
        internal_skills = self.internal_home / "skills"
        internal_skills.symlink_to(self.official_skills, target_is_directory=True)
        link_before = os.readlink(internal_skills)

        self._reconcile()
        before = tree_snapshot(internal_skills)
        result = self._reconcile()

        self.assertEqual("current", result.status)
        self.assertEqual(link_before, os.readlink(internal_skills))
        self.assertEqual(before, tree_snapshot(internal_skills))

    def test_real_internal_personal_skills_directory_fails_closed(self) -> None:
        internal_skills = self.internal_home / "skills"
        internal_skills.mkdir()
        marker = internal_skills / "owned-by-internal"
        marker.write_text("keep\n")
        before = tree_snapshot(self.store.root, self.internal_home)

        result = self._reconcile()

        self._assert_generation(
            result,
            status="blocked",
            before=0,
            after=0,
            cli_ready=False,
        )
        self.assertEqual(
            ("shared_configuration.personal_skills.real_directory",),
            finding_codes(result),
        )
        self.assertEqual(before, tree_snapshot(self.store.root, self.internal_home))
        self.assertEqual("keep\n", marker.read_text())

    def test_foreign_personal_skills_link_fails_closed(self) -> None:
        foreign = self.root / "foreign-skills"
        foreign.mkdir()
        internal_skills = self.internal_home / "skills"
        internal_skills.symlink_to(foreign, target_is_directory=True)
        before = tree_snapshot(self.store.root, self.internal_home)

        result = self._reconcile()

        self.assertEqual("blocked", result.status)
        self.assertEqual(
            ("shared_configuration.personal_skills.foreign_link",),
            finding_codes(result),
        )
        self.assertEqual(before, tree_snapshot(self.store.root, self.internal_home))
        self.assertEqual(str(foreign), os.readlink(internal_skills))

    def test_dangling_personal_skills_link_fails_closed(self) -> None:
        missing = self.root / "missing-skills"
        internal_skills = self.internal_home / "skills"
        internal_skills.symlink_to(missing, target_is_directory=True)
        before = tree_snapshot(self.store.root, self.internal_home)

        result = self._reconcile()

        self.assertEqual("blocked", result.status)
        self.assertEqual(
            ("shared_configuration.personal_skills.dangling_link",),
            finding_codes(result),
        )
        self.assertEqual(before, tree_snapshot(self.store.root, self.internal_home))
        self.assertEqual(str(missing), os.readlink(internal_skills))

    def test_self_referential_personal_skills_link_fails_closed(self) -> None:
        internal_skills = self.internal_home / "skills"
        internal_skills.symlink_to("skills", target_is_directory=True)
        before = tree_snapshot(self.store.root, self.internal_home)

        result = self._reconcile()

        self.assertEqual("blocked", result.status)
        self.assertEqual(
            ("shared_configuration.personal_skills.self_link",),
            finding_codes(result),
        )
        self.assertEqual(before, tree_snapshot(self.store.root, self.internal_home))
        self.assertEqual("skills", os.readlink(internal_skills))

    def test_plugin_owned_skill_path_remaps_to_target_cache(self) -> None:
        relative_artifact = Path("team") / "demo" / "1.0.0"
        source_skill = (
            self.official_home
            / "plugins"
            / "cache"
            / relative_artifact
            / "skills"
            / "plugin-skill"
            / "SKILL.md"
        )
        target_skill = (
            self.internal_home
            / "plugins"
            / "cache"
            / relative_artifact
            / "skills"
            / "plugin-skill"
            / "SKILL.md"
        )
        source_skill.parent.mkdir(parents=True)
        target_skill.parent.mkdir(parents=True)
        source_skill.write_text("# official artifact skill\n")
        target_skill.write_text("# internal artifact skill\n")
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True),),
            skill_paths=(source_skill,),
        )

        result = self._reconcile()

        self.assertEqual("applied", result.status)
        target_config = (self.internal_home / "config.toml").read_text()
        self.assertIn(str(target_skill), target_config)
        self.assertNotIn(str(self.official_home / "plugins" / "cache"), target_config)

    def test_plugin_skill_traversal_outside_cache_is_rejected_before_materialize(self) -> None:
        source_escape = self.official_home / "plugins" / "escaped" / "SKILL.md"
        target_escape = self.internal_home / "plugins" / "escaped" / "SKILL.md"
        source_escape.parent.mkdir(parents=True)
        target_escape.parent.mkdir(parents=True)
        source_escape.write_text("# source escape\n")
        target_escape.write_text("# target escape\n")
        configured = (
            self.official_home
            / "plugins"
            / "cache"
            / "team"
            / "demo"
            / "1.0.0"
            / ".."
            / ".."
            / ".."
            / ".."
            / "escaped"
            / "SKILL.md"
        )
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True),),
            skill_paths=(configured,),
        )

        result = self._reconcile()

        self.assertEqual("blocked", result.status)
        self.assertFalse(result.cli_ready)
        self.assertEqual(
            ("shared_configuration.materialization.unsafe_cache",),
            finding_codes(result),
        )
        self.assertEqual([], self.materialize_calls)

    def test_plugin_skill_symlink_escape_is_rejected_before_materialize(self) -> None:
        artifact = self._write_plugin_artifact(
            self.official_home,
            version="1.0.0",
            payload="portable",
        )
        outside = self.official_home / "outside-skill"
        outside.mkdir()
        (outside / "SKILL.md").write_text("# outside\n")
        link = artifact / "skills" / "escaped"
        link.symlink_to(outside, target_is_directory=True)
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True),),
            skill_paths=(link / "SKILL.md",),
        )

        result = self._reconcile()

        self.assertEqual("blocked", result.status)
        self.assertFalse(result.cli_ready)
        self.assertEqual(
            ("shared_configuration.materialization.unsafe_cache",),
            finding_codes(result),
        )
        self.assertEqual([], self.materialize_calls)

    def test_multiple_retained_local_versions_never_downgrade_exact_policy(self) -> None:
        self._write_plugin_artifact(
            self.official_home,
            version="1.0.0",
            payload="version-one",
        )
        first = self._reconcile()
        self.assertEqual("applied", first.status)
        self._write_plugin_artifact(
            self.official_home,
            version="2.0.0",
            payload="version-two",
        )

        result = self._reconcile()

        self.assertEqual("blocked", result.status)
        self.assertFalse(result.cli_ready)
        self.assertEqual(
            ("shared_configuration.materialization.ambiguous_cache",),
            finding_codes(result),
        )

    def test_project_local_skill_path_remains_worktree_owned(self) -> None:
        project_skill = (
            self.root
            / "project"
            / ".agents"
            / "skills"
            / "project-skill"
            / "SKILL.md"
        )
        project_skill.parent.mkdir(parents=True)
        project_skill.write_text("# project-owned skill\n")
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True),),
            skill_paths=(project_skill,),
        )
        project_before = tree_snapshot(self.root / "project")

        result = self._reconcile()

        self.assertEqual("applied", result.status)
        target_config = (self.internal_home / "config.toml").read_text()
        self.assertIn(str(project_skill), target_config)
        self.assertEqual(project_before, tree_snapshot(self.root / "project"))
        self.assertFalse(
            (self.official_skills / "project-skill").exists()
            or (self.official_skills / "project-skill").is_symlink()
        )

    def test_missing_committed_cache_is_not_ready_and_preflight_repairs(self) -> None:
        first = self._reconcile()
        self.assertEqual("applied", first.status)
        target = (
            self.internal_home
            / "plugins"
            / "cache"
            / "team"
            / "demo"
            / "1.0.0"
        )
        shutil.rmtree(target)
        materialize_before = len(self.materialize_calls)

        report = self._report()
        self.assertFalse(report.cli_ready)
        self.assertIn(
            "shared_configuration.materialization.unsafe_cache",
            finding_codes(report),
        )

        repaired = self._reconcile()

        self.assertEqual("applied", repaired.status)
        self.assertTrue(repaired.cli_ready)
        self.assertEqual(first.generation_after, repaired.generation_after)
        self.assertEqual(materialize_before + 1, len(self.materialize_calls))
        self.assertTrue(target.is_dir())
        self.assertEqual("current", self._report().status)

    def test_backend_managed_tree_drift_repairs_without_promoting_cli_state(
        self,
    ) -> None:
        first = self._reconcile()
        target_skill = (
            self.internal_home
            / "plugins"
            / "cache"
            / "team"
            / "demo"
            / "1.0.0"
            / "skills"
            / "SKILL.md"
        )
        target_skill.write_text("# externally drifted skill\n")
        materialize_before = len(self.materialize_calls)

        report = self._report()

        self.assertEqual("blocked", report.status)
        self.assertFalse(report.cli_ready)
        self.assertIn(
            "shared_configuration.materialization.unsafe_cache",
            finding_codes(report),
        )

        repaired = self._reconcile()

        self.assertTrue(repaired.cli_ready)
        self.assertIsNone(repaired.pending_target)
        self.assertEqual(first.generation_after, repaired.generation_after)
        self.assertEqual(materialize_before + 1, len(self.materialize_calls))

    def test_missing_state_does_not_hide_unsafe_cache_ownership(self) -> None:
        internal_cache = self.internal_home / "plugins" / "cache"
        internal_cache.rmdir()
        internal_cache.symlink_to(
            self.official_home / "plugins" / "cache",
            target_is_directory=True,
        )

        report = self._report()

        self.assertEqual("blocked", report.status)
        self.assertFalse(report.cli_ready)
        self.assertEqual(
            ("shared_configuration.cache_not_independent",),
            finding_codes(report),
        )

    def test_target_config_symlink_is_rejected_without_mutation(self) -> None:
        target_config = self.internal_home / "config.toml"
        outside = self.root / "outside-config.toml"
        outside.write_text(target_config.read_text())
        target_config.unlink()
        target_config.symlink_to(outside)
        outside_before = outside.read_bytes()

        blocked = self._reconcile()

        self.assertEqual("blocked", blocked.status)
        self.assertFalse(blocked.cli_ready)
        self.assertIn(
            "shared_configuration.target_config_unsafe",
            finding_codes(blocked),
        )
        self.assertTrue(target_config.is_symlink())
        self.assertEqual(str(outside), os.readlink(target_config))
        self.assertEqual(outside_before, outside.read_bytes())
        self.assertFalse(
            (self.store.root / "shared-configuration" / "state.json").exists()
        )

    def test_corrupt_generation_or_state_integrity_is_not_reported_ready(self) -> None:
        self._reconcile()
        generation = next(
            (self.store.root / "shared-configuration" / "generations").glob("*.toml")
        )
        generation.write_text("[plugins]\ncorrupt = true\n")

        generation_report = self._report()

        self.assertEqual("blocked", generation_report.status)
        self.assertFalse(generation_report.cli_ready)
        self.assertIn(
            "shared_configuration.generation_integrity",
            finding_codes(generation_report),
        )

        fixture = SharedConfigurationTests(methodName="runTest")
        fixture.setUp()
        try:
            fixture._reconcile()
            state_path = fixture.store.root / "shared-configuration" / "state.json"
            state = json.loads(state_path.read_text())
            state["projection_sha256"] = "0" * 64
            state_path.write_text(json.dumps(state) + "\n")

            state_report = fixture._report()

            self.assertEqual("blocked", state_report.status)
            self.assertFalse(state_report.cli_ready)
            self.assertIn(
                "shared_configuration.state_integrity",
                finding_codes(state_report),
            )
        finally:
            fixture.tearDown()

    def test_prepared_commit_recovers_every_persistent_boundary(self) -> None:
        checkpoints = (
            "prepared",
            "target_config_written",
            "personal_skills_link_created",
            "generation_published",
            "state_published",
        )
        for checkpoint in checkpoints:
            with self.subTest(checkpoint=checkpoint):
                fixture = SharedConfigurationTests(methodName="runTest")
                fixture.setUp()
                try:
                    def crash(*, phase: str, **_kwargs: Any) -> None:
                        if phase == checkpoint:
                            raise SimulatedSharedCommitCrash(phase)

                    with self.assertRaises(SimulatedSharedCommitCrash):
                        fixture._reconcile(
                            adapters=fixture._adapters(commit_checkpoint=crash)
                        )

                    journal = (
                        fixture.store.root
                        / "shared-configuration"
                        / "pending-commit.json"
                    )
                    self.assertTrue(journal.is_file())
                    before_report = tree_snapshot(
                        fixture.store.root,
                        fixture.official_home,
                        fixture.internal_home,
                    )
                    pending_report = fixture._report()
                    self.assertEqual("blocked", pending_report.status)
                    self.assertFalse(pending_report.cli_ready)
                    self.assertIn(
                        "shared_configuration.pending_recovery",
                        finding_codes(pending_report),
                    )
                    self.assertEqual(
                        before_report,
                        tree_snapshot(
                            fixture.store.root,
                            fixture.official_home,
                            fixture.internal_home,
                        ),
                    )

                    if checkpoint == "generation_published":
                        fixture._write_config(
                            fixture.official_home,
                            profile_marker="official",
                            plugins=((SELECTOR, True), (SECOND_SELECTOR, True)),
                        )

                    recovered = fixture._reconcile()

                    self.assertTrue(recovered.cli_ready)
                    self.assertFalse(journal.exists())
                    final_report = fixture._report()
                    self.assertEqual("current", final_report.status)
                    self.assertTrue(final_report.cli_ready)
                    if checkpoint == "generation_published":
                        self.assertGreaterEqual(final_report.generation_after, 2)
                finally:
                    fixture.tearDown()

    def test_recovery_journal_is_private_and_canonical_artifacts_are_secret_free(
        self,
    ) -> None:
        self._reconcile()
        self._write_config(
            self.official_home,
            profile_marker="official",
            plugins=((SELECTOR, True), (SECOND_SELECTOR, True)),
        )

        def crash(*, phase: str, **_kwargs: Any) -> None:
            if phase == "prepared":
                raise SimulatedSharedCommitCrash(phase)

        with self.assertRaises(SimulatedSharedCommitCrash):
            self._reconcile(adapters=self._adapters(commit_checkpoint=crash))

        shared_root = self.store.root / "shared-configuration"
        journal_path = shared_root / "pending-commit.json"
        journal = json.loads(journal_path.read_text())
        before_payload = base64.b64decode(journal["target"]["before"]["payload_base64"])
        after_payload = base64.b64decode(journal["target"]["after"]["payload_base64"])

        self.assertEqual(0o700, stat.S_IMODE(self.store.root.stat().st_mode))
        self.assertEqual(0o700, stat.S_IMODE(shared_root.stat().st_mode))
        self.assertEqual(0o600, stat.S_IMODE(journal_path.stat().st_mode))
        self.assertIn(INTERNAL_SECRET.encode(), before_payload)
        self.assertIn(INTERNAL_SECRET.encode(), after_payload)

        canonical_payloads = [
            (shared_root / "state.json").read_bytes(),
            *(path.read_bytes() for path in sorted((shared_root / "generations").glob("*.toml"))),
        ]
        for payload in canonical_payloads:
            self.assertNotIn(OFFICIAL_SECRET.encode(), payload)
            self.assertNotIn(INTERNAL_SECRET.encode(), payload)

        recovered = self._reconcile()

        self.assertTrue(recovered.cli_ready)
        self.assertFalse(journal_path.exists())

    def test_first_prepared_journal_durably_publishes_new_directory_entries(
        self,
    ) -> None:
        module = shared_configuration_module()
        original_fsync_directory = module._fsync_directory
        fsynced: list[Path] = []

        def record_fsync(path: Path) -> None:
            fsynced.append(path)
            original_fsync_directory(path)

        def crash(*, phase: str, **_kwargs: Any) -> None:
            if phase == "prepared":
                raise SimulatedSharedCommitCrash(phase)

        with (
            patch.object(module, "_fsync_directory", side_effect=record_fsync),
            self.assertRaises(SimulatedSharedCommitCrash),
        ):
            self._reconcile(adapters=self._adapters(commit_checkpoint=crash))

        shared_root = self.store.root / "shared-configuration"
        self.assertIn(self.store.root, fsynced)
        self.assertIn(shared_root, fsynced)
        self.assertTrue((shared_root / "pending-commit.json").is_file())

    def test_interrupted_materializer_activation_recovers_before_next_plan(
        self,
    ) -> None:
        intent = (
            self.store.root
            / "shared-configuration"
            / "pending-materialization.json"
        )
        main_journal = (
            self.store.root / "shared-configuration" / "pending-commit.json"
        )
        observed_intent: list[bool] = []

        def crash_after_activation(**kwargs: Any) -> tuple[dict[str, Any], ...]:
            receipts = self._materialize_plugins(**kwargs)
            observed_intent.append(intent.is_file() and not main_journal.exists())
            target_config = self.internal_home / "config.toml"
            target_config.write_text(
                target_config.read_text()
                + f'\n[plugins."{SELECTOR}"]\nenabled = true\n'
            )
            raise SimulatedSharedCommitCrash("native-add")

        adapters = self._adapters()
        adapters.materialize_plugins = crash_after_activation
        with self.assertRaises(SimulatedSharedCommitCrash):
            self._reconcile(adapters=adapters)

        self.assertEqual([True], observed_intent)
        self.assertTrue(intent.is_file())
        self.assertFalse(main_journal.exists())
        self.assertIn(
            f'[plugins."{SELECTOR}"]',
            (self.internal_home / "config.toml").read_text(),
        )
        before_report = tree_snapshot(
            self.store.root,
            self.official_home,
            self.internal_home,
        )
        report = self._report()
        self.assertEqual("blocked", report.status)
        self.assertIn(
            "shared_configuration.pending_recovery",
            finding_codes(report),
        )
        self.assertEqual(
            before_report,
            tree_snapshot(
                self.store.root,
                self.official_home,
                self.internal_home,
            ),
        )

        recovered = self._reconcile()

        self.assertTrue(recovered.cli_ready)
        self.assertFalse(intent.exists())
        rendered = (self.internal_home / "config.toml").read_text()
        self.assertEqual(1, rendered.count(f'[plugins."{SELECTOR}"]'))

    @unittest.skipUnless(hasattr(os, "fork"), "requires fork for SIGKILL isolation")
    def test_sigkill_during_materializer_leaves_recoverable_intent(self) -> None:
        intent = (
            self.store.root
            / "shared-configuration"
            / "pending-materialization.json"
        )

        def kill_after_activation(**kwargs: Any) -> tuple[dict[str, Any], ...]:
            self._materialize_plugins(**kwargs)
            target_config = self.internal_home / "config.toml"
            target_config.write_text(
                target_config.read_text()
                + f'\n[plugins."{SELECTOR}"]\nenabled = true\n'
            )
            os.kill(os.getpid(), signal.SIGKILL)
            raise AssertionError("SIGKILL returned")

        child = os.fork()
        if child == 0:
            adapters = self._adapters()
            adapters.materialize_plugins = kill_after_activation
            self._reconcile(adapters=adapters)
            os._exit(99)

        _pid, status = os.waitpid(child, 0)

        self.assertTrue(os.WIFSIGNALED(status))
        self.assertEqual(signal.SIGKILL, os.WTERMSIG(status))
        self.assertTrue(intent.is_file())
        self.assertEqual(0o600, stat.S_IMODE(intent.stat().st_mode))
        report = self._report()
        self.assertEqual("blocked", report.status)
        self.assertIn(
            "shared_configuration.pending_recovery",
            finding_codes(report),
        )

        recovered = self._reconcile()

        self.assertTrue(recovered.cli_ready)
        self.assertFalse(intent.exists())

    def test_store_lease_private_seam_is_active_and_exact_store_only(self) -> None:
        from codex_switch_constants import SwitchError
        from codex_switch_transaction import locked_store_mutation

        wrong_root = self.root / "wrong-store"
        wrong_root.mkdir()
        wrong_store = Store(
            wrong_root,
            official_codex_home=self.official_home,
            internal_codex_home=self.internal_home,
            launch_agent_path=self.store.launch_agent_path,
            launch_agent_label=self.store.launch_agent_label,
        )
        mutation = locked_store_mutation(
            self.store,
            operation="shared materializer lease test",
        )

        with self.assertRaisesRegex(SwitchError, "not active"):
            mutation._shared_materializer_lease_descriptor(self.store)
        with mutation:
            descriptor = mutation._shared_materializer_lease_descriptor(self.store)
            locked = os.fstat(descriptor)
            current = self.store.root.lstat()
            self.assertTrue(stat.S_ISDIR(locked.st_mode))
            self.assertEqual(
                (current.st_dev, current.st_ino),
                (locked.st_dev, locked.st_ino),
            )
            with self.assertRaisesRegex(SwitchError, "not active for this store"):
                mutation._shared_materializer_lease_descriptor(wrong_store)
        with self.assertRaisesRegex(SwitchError, "not active"):
            mutation._shared_materializer_lease_descriptor(self.store)

    @unittest.skipUnless(hasattr(os, "fork"), "requires fork for SIGKILL isolation")
    def test_sigkill_parent_keeps_backend_store_lease_until_late_write_recovery(
        self,
    ) -> None:
        from codex_switch_constants import SwitchError
        from codex_switch_plugins import PluginMaintenanceRuntime

        source = self._write_plugin_artifact(
            self.official_home,
            version="1.0.0",
            payload="lease-source",
        )
        target = (
            self.internal_home
            / "plugins"
            / "cache"
            / "team"
            / "demo"
            / "1.0.0"
        )
        intent = (
            self.store.root
            / "shared-configuration"
            / "pending-materialization.json"
        )
        target_config = self.internal_home / "config.toml"
        target_before = target_config.read_bytes()
        helper = self.root / "blocking-plugin-backend"
        helper_started = self.root / "backend-started"
        catalog_lease_seen = self.root / "catalog-lease-seen"
        helper_release = self.root / "backend-release"
        helper_done = self.root / "backend-done"
        reconcile_result = self.root / "reconcile-result.json"
        selector_activation = f'\n[plugins."{SELECTOR}"]\nenabled = true\n'
        helper.write_text(
            f"#!{sys.executable}\n"
            "import json\n"
            "import os\n"
            "import shutil\n"
            "import stat\n"
            "import sys\n"
            "import time\n"
            "from pathlib import Path\n"
            f"source = Path({str(source)!r})\n"
            f"target = Path({str(target)!r})\n"
            f"store_root = Path({str(self.store.root)!r})\n"
            f"started = Path({str(helper_started)!r})\n"
            f"catalog_seen = Path({str(catalog_lease_seen)!r})\n"
            f"release = Path({str(helper_release)!r})\n"
            f"done = Path({str(helper_done)!r})\n"
            "expected = store_root.stat()\n"
            "lease_fds = []\n"
            "for descriptor in range(3, 256):\n"
            "    try:\n"
            "        observed = os.fstat(descriptor)\n"
            "    except OSError:\n"
            "        continue\n"
            "    if (stat.S_ISDIR(observed.st_mode) and "
            "(observed.st_dev, observed.st_ino) == "
            "(expected.st_dev, expected.st_ino)):\n"
            "        lease_fds.append(descriptor)\n"
            "if not lease_fds:\n"
            "    raise SystemExit(71)\n"
            "if 'list' in sys.argv:\n"
            "    catalog_seen.write_text(','.join(map(str, lease_fds)))\n"
            "    print(json.dumps({'available': [{"
            f"'selector': {SELECTOR!r}, 'version': '1.0.0', "
            f"'source': {{'source': 'local', 'path': {str(source)!r}}}"
            "}]}))\n"
            "    raise SystemExit(0)\n"
            "started.write_text(str(os.getpid()))\n"
            "deadline = time.monotonic() + 10.0\n"
            "while not release.exists():\n"
            "    if time.monotonic() >= deadline:\n"
            "        raise SystemExit(70)\n"
            "    time.sleep(0.01)\n"
            "config = Path(os.environ['CODEX_HOME']) / 'config.toml'\n"
            "config.write_text(config.read_text() + "
            f"{selector_activation!r})\n"
            "shutil.copytree(source, target, dirs_exist_ok=True, symlinks=True)\n"
            "done.write_text('late-write-complete')\n"
        )
        helper.chmod(0o700)
        runtime = PluginMaintenanceRuntime(
            codex_bin=helper,
            home=self.internal_home,
        )

        def wait_for(predicate: Any, description: str, timeout: float = 5.0) -> None:
            deadline = time.monotonic() + timeout
            while time.monotonic() < deadline:
                if predicate():
                    return
                time.sleep(0.01)
            self.fail(f"timed out waiting for {description}")

        def production_adapters(*, observe_recovery: bool = False) -> SimpleNamespace:
            observations: list[tuple[bool, bool]] = []
            read_paths: list[Path] = []

            def read_stable(path: Path) -> str:
                read_paths.append(path)
                text = path.read_text()
                if observe_recovery and path == target_config:
                    observations.append(
                        (intent.exists(), f'[plugins."{SELECTOR}"]' in text)
                    )
                return text

            adapters = SimpleNamespace(
                read_stable=read_stable,
                app_is_running=lambda store, selection: False,
                before_commit=lambda **_kwargs: None,
                commit_checkpoint=lambda **_kwargs: None,
                recovery_observations=observations,
                read_paths=read_paths,
            )
            return adapters

        reconcile_child: int | None = None
        reconcile_reaped = False
        helper_pid: int | None = None
        try:
            with (
                patch(
                    "codex_switch_plugins.profile_home",
                    side_effect=lambda store, name: (
                        self.internal_home
                        if name == "internal"
                        else self.official_home
                    ),
                ),
                patch(
                    "codex_switch_plugins.profile_plugin_runtime",
                    return_value=runtime,
                ),
                patch(
                    "codex_switch_plugins.running_target_app_server_pids",
                    return_value=[],
                ),
            ):
                reconcile_child = os.fork()
                if reconcile_child == 0:
                    result = self._reconcile(adapters=production_adapters())
                    reconcile_result.write_text(
                        json.dumps(
                            {
                                "status": result.status,
                                "findings": [
                                    {
                                        "code": item.code,
                                        "message": item.message,
                                    }
                                    for item in result.findings
                                ],
                            },
                            sort_keys=True,
                        )
                    )
                    os._exit(99)

                wait_for(
                    lambda: helper_started.is_file() or reconcile_result.is_file(),
                    "external backend start",
                )
                if reconcile_result.is_file():
                    self.fail(
                        "reconcile returned before external backend start: "
                        + reconcile_result.read_text()
                    )
                self.assertTrue(catalog_lease_seen.is_file())
                helper_pid = int(helper_started.read_text())
                os.kill(reconcile_child, signal.SIGKILL)
                _pid, status = os.waitpid(reconcile_child, 0)
                reconcile_reaped = True
                self.assertTrue(os.WIFSIGNALED(status))
                self.assertEqual(signal.SIGKILL, os.WTERMSIG(status))
                os.kill(helper_pid, 0)

                self.assertTrue(intent.is_file())
                intent_before_early_apply = intent.read_bytes()
                early_adapters = production_adapters()
                early_materialize_calls: list[bool] = []

                def fail_if_materialized(**_kwargs: Any) -> tuple[dict[str, Any], ...]:
                    early_materialize_calls.append(True)
                    raise SwitchError("shared_configuration.materialization.failed")

                early_adapters.materialize_plugins = fail_if_materialized
                early = self._reconcile(adapters=early_adapters)

                self.assertEqual("blocked", early.status)
                self.assertTrue(
                    any("profile store is busy" in item.message for item in early.findings)
                )
                self.assertEqual(intent_before_early_apply, intent.read_bytes())
                self.assertEqual(target_before, target_config.read_bytes())
                self.assertEqual([], early_adapters.read_paths)
                self.assertEqual([], early_materialize_calls)
                self.assertFalse(helper_done.exists())

                helper_release.touch()
                wait_for(helper_done.is_file, "external backend late write")
                self.assertIn(
                    f'[plugins."{SELECTOR}"]',
                    target_config.read_text(),
                )
                interrupted_cache = tree_snapshot(target)

                def backend_lease_released() -> bool:
                    descriptor = os.open(
                        self.store.root,
                        os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
                    )
                    try:
                        try:
                            fcntl.flock(
                                descriptor,
                                fcntl.LOCK_EX | fcntl.LOCK_NB,
                            )
                        except BlockingIOError:
                            return False
                        fcntl.flock(descriptor, fcntl.LOCK_UN)
                        return True
                    finally:
                        os.close(descriptor)

                wait_for(backend_lease_released, "external backend lease release")
                final_adapters = production_adapters(observe_recovery=True)
                recovered = self._reconcile(adapters=final_adapters)

                self.assertTrue(
                    recovered.cli_ready,
                    [(item.code, item.message) for item in recovered.findings],
                )
                self.assertFalse(intent.exists())
                self.assertTrue(final_adapters.recovery_observations)
                self.assertEqual(
                    (False, False),
                    final_adapters.recovery_observations[0],
                )
                self.assertEqual(
                    1,
                    target_config.read_text().count(f'[plugins."{SELECTOR}"]'),
                )
                self.assertTrue(target.is_dir())
                self.assertEqual(interrupted_cache, tree_snapshot(target))
        finally:
            helper_release.touch(exist_ok=True)
            if reconcile_child is not None and not reconcile_reaped:
                try:
                    os.kill(reconcile_child, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                try:
                    os.waitpid(reconcile_child, 0)
                except ChildProcessError:
                    pass
            if helper_pid is not None and not helper_done.exists():
                try:
                    os.kill(helper_pid, signal.SIGTERM)
                except ProcessLookupError:
                    pass

    def test_interrupted_materializer_preserves_foreign_edit_and_scrubs_selector(
        self,
    ) -> None:
        intent = (
            self.store.root
            / "shared-configuration"
            / "pending-materialization.json"
        )

        def crash_with_foreign_edit(**kwargs: Any) -> tuple[dict[str, Any], ...]:
            self._materialize_plugins(**kwargs)
            target_config = self.internal_home / "config.toml"
            target_config.write_text(
                target_config.read_text()
                + f'\n[plugins."{SELECTOR}"]\nenabled = true\n'
                + "\n[foreign_edit]\npreserve_me = true\n"
            )
            raise SimulatedSharedCommitCrash("native-add")

        adapters = self._adapters()
        adapters.materialize_plugins = crash_with_foreign_edit
        with self.assertRaises(SimulatedSharedCommitCrash):
            self._reconcile(adapters=adapters)

        blocked = self._reconcile()

        self.assertEqual("blocked", blocked.status)
        self.assertIn(
            "shared_configuration.target_changed_during_plan",
            finding_codes(blocked),
        )
        self.assertFalse(intent.exists())
        rendered = (self.internal_home / "config.toml").read_text()
        self.assertNotIn(f'[plugins."{SELECTOR}"]', rendered)
        self.assertIn("[foreign_edit]", rendered)
        self.assertIn("preserve_me = true", rendered)
        self.assertFalse(
            (self.store.root / "shared-configuration" / "state.json").exists()
        )

    def test_shared_storage_symlink_ancestors_fail_closed_without_external_write(
        self,
    ) -> None:
        shared_root = self.store.root / "shared-configuration"
        external = self.root / "external-shared-state"
        external.mkdir(mode=0o700)
        (external / "pending-commit.json").write_text("{}\n")
        shared_root.symlink_to(external, target_is_directory=True)
        external_before = tree_snapshot(external)
        target_before = tree_snapshot(self.official_home, self.internal_home)

        report = self._report()
        applied = self._reconcile()

        for result in (report, applied):
            self.assertEqual("blocked", result.status)
            self.assertIn(
                "shared_configuration.state_integrity",
                finding_codes(result),
            )
        self.assertEqual(external_before, tree_snapshot(external))
        self.assertEqual(
            target_before,
            tree_snapshot(self.official_home, self.internal_home),
        )

        fixture = SharedConfigurationTests(methodName="runTest")
        fixture.setUp()
        try:
            fixture._reconcile()
            generations = (
                fixture.store.root / "shared-configuration" / "generations"
            )
            external_generations = fixture.root / "external-generations"
            generations.rename(external_generations)
            generations.symlink_to(external_generations, target_is_directory=True)
            generations_before = tree_snapshot(external_generations)
            target_before = tree_snapshot(
                fixture.official_home,
                fixture.internal_home,
            )

            generation_report = fixture._report()
            generation_apply = fixture._reconcile()

            for result in (generation_report, generation_apply):
                self.assertEqual("blocked", result.status)
                self.assertIn(
                    "shared_configuration.state_integrity",
                    finding_codes(result),
                )
            self.assertEqual(
                generations_before,
                tree_snapshot(external_generations),
            )
            self.assertEqual(
                target_before,
                tree_snapshot(fixture.official_home, fixture.internal_home),
            )
        finally:
            fixture.tearDown()

    def test_recovery_foreign_link_drift_blocks_before_partial_rollback(self) -> None:
        def crash(*, phase: str, **_kwargs: Any) -> None:
            if phase == "personal_skills_link_created":
                raise SimulatedSharedCommitCrash(phase)

        with self.assertRaises(SimulatedSharedCommitCrash):
            self._reconcile(adapters=self._adapters(commit_checkpoint=crash))

        journal_path = (
            self.store.root / "shared-configuration" / "pending-commit.json"
        )
        internal_config_after = (self.internal_home / "config.toml").read_bytes()
        foreign = self.root / "foreign-skills"
        foreign.mkdir()
        internal_skills = self.internal_home / "skills"
        internal_skills.unlink()
        internal_skills.symlink_to(foreign, target_is_directory=True)

        blocked = self._reconcile()

        self.assertEqual("blocked", blocked.status)
        self.assertIn(
            "shared_configuration.pending_recovery",
            finding_codes(blocked),
        )
        self.assertEqual(
            internal_config_after,
            (self.internal_home / "config.toml").read_bytes(),
        )
        self.assertEqual(str(foreign), os.readlink(internal_skills))
        self.assertTrue(journal_path.is_file())

    def test_shared_configuration_report_is_read_only_and_stable(self) -> None:
        self._reconcile()
        before = tree_snapshot(self.store.root, self.official_home, self.internal_home)

        first = self._report()
        second = self._report()

        self._assert_generation(
            first,
            status="current",
            before=1,
            after=1,
            cli_ready=True,
        )
        self.assertEqual(first, second)
        self.assertEqual(
            before,
            tree_snapshot(self.store.root, self.official_home, self.internal_home),
        )


if __name__ == "__main__":
    unittest.main()
