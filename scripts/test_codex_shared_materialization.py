#!/usr/bin/env python3

from __future__ import annotations

import json
import io
import os
import shutil
import tempfile
import unittest
from contextlib import contextmanager, redirect_stderr
from pathlib import Path
from typing import Iterator
from unittest.mock import patch

from codex_switch_constants import SwitchError
from codex_switch_selection import ProfileSelection
from codex_switch_store import Store


SELECTOR = "review-tools@local-market"
PLUGIN = "review-tools"
MARKETPLACE = "local-market"
SKILL_NAME = "review-helper"


def _field(value: object, name: str, default: object = None) -> object:
    if isinstance(value, dict):
        return value.get(name, default)
    return getattr(value, name, default)


def _shared_api():
    # Keep import at the public seam so the RED suite is collected even before
    # the production module exists.
    from codex_switch_shared_configuration import (
        SharedConfigurationAdapters,
        reconcile_shared_configuration,
    )

    return SharedConfigurationAdapters, reconcile_shared_configuration


def _write_plugin_artifact(
    root: Path,
    *,
    plugin: str = PLUGIN,
    version: str,
    payload: str,
) -> Path:
    manifest = root / ".codex-plugin" / "plugin.json"
    manifest.parent.mkdir(parents=True, exist_ok=True)
    manifest.write_text(
        json.dumps(
            {
                "name": plugin,
                "version": version,
                "skills": "./skills/",
            },
            sort_keys=True,
        )
        + "\n"
    )
    (root / "payload.txt").write_text(payload)
    skill_root = root / "skills" / SKILL_NAME
    skill_root.mkdir(parents=True, exist_ok=True)
    (skill_root / "SKILL.md").write_text(
        f"---\nname: {SKILL_NAME}\ndescription: fixture\n---\n\n{payload}\n"
    )
    return skill_root


def _plugin_cache_root(home: Path) -> Path:
    return home / "plugins" / "cache"


def _plugin_version_root(
    home: Path,
    *,
    cache_key: str,
    marketplace: str = MARKETPLACE,
    plugin: str = PLUGIN,
) -> Path:
    return _plugin_cache_root(home) / marketplace / plugin / cache_key


class FakeMaterializer:
    """A deterministic target-backend adapter; it never reads a live home."""

    def __init__(
        self,
        *,
        internal_home: Path,
        source_roots: dict[str, Path],
        policies: dict[str, str] | None = None,
        target_cache_keys: dict[str, str] | None = None,
        target_versions: dict[str, str] | None = None,
        target_payloads: dict[str, str] | None = None,
        failure_code: str | None = None,
    ) -> None:
        self.internal_home = internal_home
        self.source_roots = source_roots
        self.policies = policies or {}
        self.target_cache_keys = target_cache_keys or {}
        self.target_versions = target_versions or {}
        self.target_payloads = target_payloads or {}
        self.failure_code = failure_code
        self.calls: list[dict[str, object]] = []

    def __call__(
        self,
        *,
        store: Store,
        selection: ProfileSelection,
        source_profile: str,
        target_profile: str,
        desired_plugins: tuple[object, ...],
        generation: int,
        _store_lock_descriptor: int,
    ) -> tuple[dict[str, object], ...]:
        self.calls.append(
            {
                "store": store,
                "selection": selection,
                "source_profile": source_profile,
                "target_profile": target_profile,
                "desired_plugins": desired_plugins,
                "generation": generation,
                "store_lock_descriptor": _store_lock_descriptor,
            }
        )
        if self.failure_code is not None:
            raise SwitchError(self.failure_code)

        receipts: list[dict[str, object]] = []
        for desired in desired_plugins:
            selector = str(_field(desired, "selector", ""))
            if selector not in self.source_roots:
                raise AssertionError(f"unexpected desired selector: {selector}")
            plugin, marketplace = selector.rsplit("@", 1)
            source_root = self.source_roots[selector]
            source_version = json.loads(
                (source_root / ".codex-plugin" / "plugin.json").read_text()
            )["version"]
            policy = self.policies.get(
                selector,
                str(_field(desired, "policy", "portable_exact")),
            )
            cache_key = self.target_cache_keys.get(
                selector,
                str(_field(desired, "cache_key", source_root.name)),
            )
            manifest_version = self.target_versions.get(selector, source_version)
            destination = _plugin_version_root(
                self.internal_home,
                marketplace=marketplace,
                plugin=plugin,
                cache_key=cache_key,
            )
            destination.mkdir(parents=True, exist_ok=True)
            if policy == "portable_exact":
                for source in sorted(source_root.rglob("*")):
                    relative = source.relative_to(source_root)
                    target = destination / relative
                    if source.is_dir():
                        target.mkdir(parents=True, exist_ok=True)
                    elif source.is_file():
                        target.parent.mkdir(parents=True, exist_ok=True)
                        target.write_bytes(source.read_bytes())
            else:
                _write_plugin_artifact(
                    destination,
                    plugin=plugin,
                    version=manifest_version,
                    payload=self.target_payloads.get(
                        selector,
                        f"target-backend-{manifest_version}",
                    ),
                )

            from codex_switch_plugins import plugin_tree_sha256

            tree_sha256 = plugin_tree_sha256(destination)
            skill_root = destination / "skills" / SKILL_NAME
            receipts.append(
                {
                    "selector": selector,
                    "policy": policy,
                    "cache_key": cache_key,
                    "manifest_version": manifest_version,
                    "tree_sha256": tree_sha256,
                    "skill_roots": (str(skill_root),),
                }
            )
        return tuple(receipts)


class SharedMaterializationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.official_home = self.root / "official-home"
        self.internal_home = self.root / "internal-home"
        self.official_home.mkdir()
        self.internal_home.mkdir()
        self.store = Store(
            self.root / "store",
            official_codex_home=self.official_home,
            internal_codex_home=self.internal_home,
            launch_agent_path=self.root / "launch-agent.plist",
        )
        self.store.ensure()
        self.selection = ProfileSelection(
            cli_profile="internal",
            app_profile="openai-official",
            app_profile_explicit=True,
        )
        for profile, home in (
            ("internal", self.internal_home),
            ("openai-official", self.official_home),
        ):
            profile_dir = self.store.profile_dir(profile)
            profile_dir.mkdir(parents=True, exist_ok=True)
            (profile_dir / "manifest.json").write_text(
                json.dumps(
                    {
                        "name": profile,
                        "codex_home": str(home),
                        "home_selection_confirmed": True,
                    },
                    sort_keys=True,
                )
                + "\n"
            )
        self.internal_config = self.internal_home / "config.toml"
        self.official_config = self.official_home / "config.toml"
        self.internal_config.write_text(
            'model = "internal-model"\n'
            'personality = "pragmatic"\n'
            "\n[features]\n"
            "internal_runtime_feature = true\n"
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _official_artifact(
        self,
        *,
        cache_key: str = "1.0.0",
        version: str = "1.0.0",
        payload: str = "official-v1",
        marketplace: str = MARKETPLACE,
        plugin: str = PLUGIN,
    ) -> Path:
        root = _plugin_version_root(
            self.official_home,
            marketplace=marketplace,
            plugin=plugin,
            cache_key=cache_key,
        )
        _write_plugin_artifact(
            root,
            plugin=plugin,
            version=version,
            payload=payload,
        )
        return root

    def _write_official_config(
        self,
        *,
        selector: str | None = SELECTOR,
        enabled: bool = True,
        skill_path: Path | None = None,
        marketplace: str = MARKETPLACE,
        marketplace_path: Path | None = None,
    ) -> None:
        source_path = marketplace_path or (self.root / "marketplace")
        lines = [
            'model = "official-model"',
            'personality = "friendly"',
            "",
            f"[marketplaces.{marketplace}]",
            (
                "source = { source = \"local\", path = "
                f"{json.dumps(str(source_path))} }}"
            ),
        ]
        if selector is not None:
            lines.extend(
                (
                    "",
                    f"[plugins.{json.dumps(selector)}]",
                    f"enabled = {'true' if enabled else 'false'}",
                )
            )
        if skill_path is not None:
            lines.extend(
                (
                    "",
                    "[[skills.config]]",
                    f"path = {json.dumps(str(skill_path))}",
                    "enabled = true",
                )
            )
        self.official_config.write_text("\n".join(lines) + "\n")

    def _adapters(
        self,
        materializer: FakeMaterializer,
        *,
        before_commit=None,
    ):
        SharedConfigurationAdapters, _ = _shared_api()
        return SharedConfigurationAdapters(
            materialize_plugins=materializer,
            before_commit=(
                before_commit
                if before_commit is not None
                else lambda **_kwargs: None
            ),
        )

    def _reconcile(self, adapters):
        _, reconcile = _shared_api()
        return reconcile(
            self.store,
            self.selection,
            boundary="cli-preflight",
            mode="apply",
            adapters=adapters,
        )

    @contextmanager
    def _materializer_lease(self) -> Iterator[int]:
        from codex_switch_transaction import locked_store_mutation

        with locked_store_mutation(
            self.store,
            operation="shared materializer test",
        ) as locked:
            yield locked._shared_materializer_lease_descriptor(self.store)

    def _materialize_with_lease(self, materializer, **kwargs):
        with self._materializer_lease() as descriptor:
            return materializer(
                _store_lock_descriptor=descriptor,
                **kwargs,
            )

    def _backend_desired(
        self,
        source: Path,
        *,
        selector: str = "browser@openai-bundled",
    ) -> dict[str, object]:
        from codex_switch_plugins import plugin_tree_sha256

        plugin, marketplace = selector.rsplit("@", 1)
        manifest = json.loads(
            (source / ".codex-plugin" / "plugin.json").read_text()
        )
        return {
            "selector": selector,
            "enabled": True,
            "policy": "backend_managed",
            "plugin": plugin,
            "marketplace": marketplace,
            "marketplace_config": {"source": {"source": "bundled"}},
            "cache_key": source.name,
            "manifest_version": manifest["version"],
            "tree_sha256": plugin_tree_sha256(source),
        }

    def _raw_catalog(
        self,
        *,
        installed: list[dict[str, object]] | None = None,
        available: list[dict[str, object]] | None = None,
    ):
        from codex_switch_plugins import available_plugin_catalog

        result = available_plugin_catalog(
            json.dumps(
                {
                    "installed": installed or [],
                    "available": available or [],
                }
            )
        )
        self.assertTrue(result.verified, result.detail)
        return result

    def _catalog_record(
        self,
        *,
        selector: str,
        version: str,
        source: Path | None,
        installed: bool | None = None,
        enabled: bool | None = None,
    ) -> dict[str, object]:
        plugin, marketplace = selector.rsplit("@", 1)
        record: dict[str, object] = {
            "pluginId": selector,
            "name": plugin,
            "marketplaceName": marketplace,
            "version": version,
        }
        if source is not None:
            record["source"] = {"source": "local", "path": str(source)}
        if installed is not None:
            record["installed"] = installed
        if enabled is not None:
            record["enabled"] = enabled
        return record

    def test_app_add_portable_exact_materializes_independent_cache_and_skill(self) -> None:
        source = self._official_artifact()
        source_skill = source / "skills" / SKILL_NAME / "SKILL.md"
        self._write_official_config(skill_path=source_skill)
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
            policies={SELECTOR: "portable_exact"},
        )

        receipt = self._reconcile(self._adapters(materializer))

        self.assertEqual("applied", receipt.status)
        self.assertTrue(receipt.cli_ready)
        self.assertGreater(receipt.generation_after, receipt.generation_before)
        self.assertEqual((), receipt.findings)
        self.assertEqual(1, len(materializer.calls))
        call = materializer.calls[0]
        self.assertEqual("openai-official", call["source_profile"])
        self.assertEqual("internal", call["target_profile"])
        self.assertEqual(
            [SELECTOR],
            [str(_field(item, "selector")) for item in call["desired_plugins"]],
        )

        self.assertEqual(1, len(receipt.materializations))
        materialization = receipt.materializations[0]
        self.assertEqual(SELECTOR, materialization.selector)
        self.assertEqual("portable_exact", materialization.policy)
        self.assertEqual("1.0.0", materialization.cache_key)
        self.assertEqual("1.0.0", materialization.manifest_version)
        self.assertTrue(materialization.tree_sha256)

        official_cache = _plugin_cache_root(self.official_home)
        internal_cache = _plugin_cache_root(self.internal_home)
        self.assertNotEqual(official_cache.resolve(), internal_cache.resolve())
        self.assertFalse(official_cache.is_symlink())
        self.assertFalse(internal_cache.is_symlink())
        target_skill = Path(materialization.skill_roots[0]) / "SKILL.md"
        self.assertTrue(target_skill.is_file())
        self.assertTrue(target_skill.is_relative_to(internal_cache))
        rendered = self.internal_config.read_text()
        self.assertIn(f'[plugins."{SELECTOR}"]', rendered)
        self.assertIn(str(target_skill), rendered)
        self.assertNotIn(str(source_skill), rendered)
        self.assertIn('model = "internal-model"', rendered)
        self.assertIn('personality = "pragmatic"', rendered)

    def test_same_selector_same_version_tree_change_advances_and_rematerializes(self) -> None:
        source = self._official_artifact(payload="tree-v1")
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
            policies={SELECTOR: "portable_exact"},
        )
        first = self._reconcile(self._adapters(materializer))
        first_identity = first.materializations[0].tree_sha256
        target_payload = _plugin_version_root(
            self.internal_home,
            cache_key="1.0.0",
        ) / "payload.txt"
        self.assertEqual("tree-v1", target_payload.read_text())

        (source / "payload.txt").write_text("tree-v2")
        (source / "skills" / SKILL_NAME / "SKILL.md").write_text(
            "---\nname: review-helper\ndescription: fixture\n---\n\ntree-v2\n"
        )
        materializer.calls.clear()
        second = self._reconcile(self._adapters(materializer))

        self.assertEqual("applied", second.status)
        self.assertTrue(second.cli_ready)
        self.assertGreater(second.generation_after, first.generation_after)
        self.assertEqual(1, len(materializer.calls))
        self.assertNotEqual(
            first_identity,
            second.materializations[0].tree_sha256,
        )
        self.assertEqual("tree-v2", target_payload.read_text())

    def test_disable_then_remove_updates_usage_without_direct_cache_delete(self) -> None:
        source = self._official_artifact()
        skill = source / "skills" / SKILL_NAME / "SKILL.md"
        self._write_official_config(skill_path=skill)
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
        )
        first = self._reconcile(self._adapters(materializer))
        existing_target = _plugin_version_root(self.internal_home, cache_key="1.0.0")
        self.assertTrue(existing_target.is_dir())

        self._write_official_config(enabled=False)
        materializer.calls.clear()
        disabled = self._reconcile(self._adapters(materializer))
        self.assertEqual("applied", disabled.status)
        self.assertTrue(disabled.cli_ready)
        self.assertGreater(disabled.generation_after, first.generation_after)
        self.assertEqual([], materializer.calls)
        self.assertTrue(existing_target.is_dir())
        self.assertIn(f'[plugins."{SELECTOR}"]', self.internal_config.read_text())
        self.assertIn("enabled = false", self.internal_config.read_text())
        self.assertNotIn("[[skills.config]]", self.internal_config.read_text())

        self._write_official_config(enabled=True, skill_path=skill)
        enabled = self._reconcile(self._adapters(materializer))
        self.assertEqual("applied", enabled.status)
        self.assertTrue(enabled.cli_ready)
        self.assertGreater(enabled.generation_after, disabled.generation_after)
        self.assertTrue(existing_target.is_dir())
        self.assertIn(f'[plugins."{SELECTOR}"]', self.internal_config.read_text())
        self.assertIn("enabled = true", self.internal_config.read_text())

        self._write_official_config(selector=None)
        materializer.calls.clear()
        removed = self._reconcile(self._adapters(materializer))
        self.assertEqual("applied", removed.status)
        self.assertTrue(removed.cli_ready)
        self.assertGreater(removed.generation_after, enabled.generation_after)
        self.assertEqual([], materializer.calls)
        self.assertTrue(existing_target.is_dir())
        self.assertNotIn(SELECTOR, self.internal_config.read_text())
        self.assertNotIn("[[skills.config]]", self.internal_config.read_text())

    def test_backend_managed_receipt_allows_compatible_target_divergence(self) -> None:
        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.730.61639",
            version="26.730.61639",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        self._write_official_config(
            selector=selector,
            skill_path=None,
            marketplace="openai-bundled",
            marketplace_path=self.root / "bundled-marketplace",
        )
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={selector: source},
            policies={selector: "backend_managed"},
            target_cache_keys={selector: "26.721.41059"},
            target_versions={selector: "26.721.41059"},
            target_payloads={selector: "internal-compatible-browser"},
        )

        receipt = self._reconcile(self._adapters(materializer))

        self.assertEqual("applied", receipt.status)
        self.assertTrue(receipt.cli_ready)
        self.assertEqual(1, len(receipt.materializations))
        materialization = receipt.materializations[0]
        self.assertEqual(selector, materialization.selector)
        self.assertEqual("backend_managed", materialization.policy)
        self.assertEqual("26.721.41059", materialization.cache_key)
        self.assertEqual("26.721.41059", materialization.manifest_version)
        self.assertTrue(
            _plugin_version_root(
                self.internal_home,
                marketplace="openai-bundled",
                plugin="browser",
                cache_key="26.721.41059",
            ).is_dir()
        )
        self.assertFalse(
            _plugin_version_root(
                self.internal_home,
                marketplace="openai-bundled",
                plugin="browser",
                cache_key="26.730.61639",
            ).exists()
        )

    def test_portable_exact_receipt_mismatch_blocks_config_commit(self) -> None:
        source = self._official_artifact()
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        before = self.internal_config.read_bytes()
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
            policies={SELECTOR: "portable_exact"},
            target_versions={SELECTOR: "9.9.9-receipt-mismatch"},
        )

        receipt = self._reconcile(self._adapters(materializer))

        self.assertEqual("blocked", receipt.status)
        self.assertFalse(receipt.cli_ready)
        self.assertIn(
            "shared_configuration.materialization.unsafe_cache",
            {finding.code for finding in receipt.findings},
        )
        self.assertEqual(receipt.generation_before, receipt.generation_after)
        self.assertEqual(before, self.internal_config.read_bytes())

    def _assert_materialization_blocked(self, code: str) -> None:
        source = self._official_artifact()
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        before = self.internal_config.read_bytes()
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
            failure_code=code,
        )

        receipt = self._reconcile(self._adapters(materializer))

        self.assertEqual("blocked", receipt.status)
        self.assertFalse(receipt.cli_ready)
        self.assertEqual(receipt.generation_before, receipt.generation_after)
        self.assertIn(code, {finding.code for finding in receipt.findings})
        self.assertEqual((), receipt.materializations)
        self.assertEqual(before, self.internal_config.read_bytes())

    def test_unavailable_selector_blocks_without_config_or_receipt_commit(self) -> None:
        self._assert_materialization_blocked(
            "shared_configuration.materialization.unavailable"
        )

    def test_unverified_catalog_blocks_without_config_or_receipt_commit(self) -> None:
        self._assert_materialization_blocked(
            "shared_configuration.materialization.unverified_catalog"
        )

    def test_running_target_process_blocks_before_config_commit(self) -> None:
        source = self._official_artifact()
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        before = self.internal_config.read_bytes()
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
            failure_code=(
                "shared_configuration.materialization.running_process"
            ),
        )

        receipt = self._reconcile(self._adapters(materializer))

        self.assertEqual("blocked", receipt.status)
        self.assertFalse(receipt.cli_ready)
        self.assertIn(
            "shared_configuration.materialization.running_process",
            {finding.code for finding in receipt.findings},
        )
        self.assertEqual(1, len(materializer.calls))
        self.assertEqual(before, self.internal_config.read_bytes())

    def test_cross_home_cache_symlink_fails_closed(self) -> None:
        source = self._official_artifact()
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        official_cache = _plugin_cache_root(self.official_home)
        internal_plugins = self.internal_home / "plugins"
        internal_plugins.mkdir()
        os.symlink(official_cache, internal_plugins / "cache")
        before = self.internal_config.read_bytes()
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
        )

        receipt = self._reconcile(self._adapters(materializer))

        self.assertEqual("blocked", receipt.status)
        self.assertFalse(receipt.cli_ready)
        self.assertIn(
            "shared_configuration.cache_not_independent",
            {finding.code for finding in receipt.findings},
        )
        self.assertEqual([], materializer.calls)
        self.assertEqual(before, self.internal_config.read_bytes())

    def test_failure_after_materialization_keeps_last_known_good_config(self) -> None:
        source = self._official_artifact(payload="generation-one")
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
        )
        first = self._reconcile(self._adapters(materializer))
        self.assertEqual("applied", first.status)
        last_known_good = self.internal_config.read_bytes()

        second_source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="generation-two",
        )
        self._write_official_config(
            skill_path=second_source / "skills" / SKILL_NAME / "SKILL.md"
        )
        materializer.source_roots[SELECTOR] = second_source
        injected: list[object] = []

        def fail_before_commit(*, store, selection, plan) -> None:
            injected.append(plan)
            raise SwitchError("shared_configuration.materialization.failed")

        blocked = self._reconcile(
            self._adapters(materializer, before_commit=fail_before_commit)
        )

        self.assertEqual("blocked", blocked.status)
        self.assertFalse(blocked.cli_ready)
        self.assertIn(
            "shared_configuration.materialization.failed",
            {finding.code for finding in blocked.findings},
        )
        self.assertEqual(first.generation_after, blocked.generation_after)
        self.assertEqual(1, len(injected))
        self.assertEqual(last_known_good, self.internal_config.read_bytes())
        self.assertTrue(
            _plugin_version_root(self.internal_home, cache_key="1.0.0").is_dir()
        )

    def test_unchanged_generation_is_zero_write_zero_materializer_fast_path(self) -> None:
        source = self._official_artifact()
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
        )
        first = self._reconcile(self._adapters(materializer))
        self.assertEqual("applied", first.status)
        materializer.calls.clear()
        before_bytes = self.internal_config.read_bytes()
        before_stat = self.internal_config.stat()
        commit_calls: list[object] = []

        def record_commit(*, store, selection, plan) -> None:
            commit_calls.append(plan)

        second = self._reconcile(
            self._adapters(materializer, before_commit=record_commit)
        )

        after_stat = self.internal_config.stat()
        self.assertEqual("current", second.status)
        self.assertTrue(second.cli_ready)
        self.assertEqual(first.generation_after, second.generation_after)
        self.assertEqual([], materializer.calls)
        self.assertEqual([], commit_calls)
        self.assertEqual(before_bytes, self.internal_config.read_bytes())
        self.assertEqual(before_stat.st_ino, after_stat.st_ino)
        self.assertEqual(before_stat.st_mtime_ns, after_stat.st_mtime_ns)

    def test_production_materializer_attests_existing_portable_exact_cache(self) -> None:
        from codex_switch_plugins import (
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        source = self._official_artifact(payload="portable-source")
        target = _plugin_version_root(self.internal_home, cache_key="1.0.0")
        _write_plugin_artifact(
            target,
            version="1.0.0",
            payload="portable-source",
        )
        desired = {
            "selector": SELECTOR,
            "enabled": True,
            "policy": "portable_exact",
            "plugin": PLUGIN,
            "marketplace": MARKETPLACE,
            "marketplace_config": {
                "source": {
                    "source": "local",
                    "path": str(self.root / "marketplace"),
                }
            },
            "cache_key": "1.0.0",
            "manifest_version": "1.0.0",
            "tree_sha256": plugin_tree_sha256(source),
        }

        with patch(
            "codex_switch_plugins.profile_plugin_runtime",
            side_effect=AssertionError("existing exact cache must not invoke backend"),
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        self.assertEqual(1, len(receipts))
        receipt = receipts[0]
        self.assertEqual(SELECTOR, receipt["selector"])
        self.assertEqual("portable_exact", receipt["policy"])
        self.assertEqual(plugin_tree_sha256(source), receipt["tree_sha256"])
        self.assertTrue(
            all(
                Path(root).resolve().is_relative_to(
                    _plugin_cache_root(self.internal_home).resolve()
                )
                for root in receipt["skill_roots"]
            )
        )

    def test_portable_exact_uses_exact_source_when_native_replaces_old_installed_version(
        self,
    ) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        desired_source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="portable-v2",
        )
        catalog_source = self.root / "catalog-portable-v2"
        _write_plugin_artifact(
            catalog_source,
            version="2.0.0",
            payload="portable-v2",
        )
        prior_target = _plugin_version_root(
            self.internal_home,
            cache_key="1.0.0",
        )
        _write_plugin_artifact(
            prior_target,
            version="1.0.0",
            payload="portable-v1-prior",
        )
        desired_target = _plugin_version_root(
            self.internal_home,
            cache_key="2.0.0",
        )
        desired = {
            "selector": SELECTOR,
            "enabled": True,
            "policy": "portable_exact",
            "plugin": PLUGIN,
            "marketplace": MARKETPLACE,
            "marketplace_config": {
                "source": {
                    "source": "local",
                    "path": str(self.root / "marketplace"),
                }
            },
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(desired_source),
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                SELECTOR: PluginCatalogEntry(
                    selector=SELECTOR,
                    plugin=PLUGIN,
                    marketplace=MARKETPLACE,
                    version="1.0.0",
                    source_path=catalog_source,
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def install_desired_portable(**_kwargs) -> None:
            shutil.rmtree(prior_target)
            _write_plugin_artifact(
                desired_target,
                version="2.0.0",
                payload="portable-v2",
            )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch("codex_switch_plugins._shared_available_catalog", return_value=catalog),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_desired_portable,
            ) as native_add,
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        native_add.assert_called_once()
        self.assertEqual("2.0.0", receipts[0]["cache_key"])
        self.assertEqual("portable-v2", (desired_target / "payload.txt").read_text())
        self.assertFalse(prior_target.exists())

    def test_portable_exact_reports_safe_source_identity_mismatch(self) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        desired_source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="portable-v2",
        )
        drifted_catalog_source = self.root / "catalog-portable-v2-drifted"
        _write_plugin_artifact(
            drifted_catalog_source,
            version="2.0.0",
            payload="portable-v2-drifted",
        )
        desired = {
            "selector": SELECTOR,
            "enabled": True,
            "policy": "portable_exact",
            "plugin": PLUGIN,
            "marketplace": MARKETPLACE,
            "marketplace_config": {
                "source": {
                    "source": "local",
                    "path": str(self.root / "marketplace"),
                }
            },
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(desired_source),
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                SELECTOR: PluginCatalogEntry(
                    selector=SELECTOR,
                    plugin=PLUGIN,
                    marketplace=MARKETPLACE,
                    version="1.0.0",
                    source_path=drifted_catalog_source,
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch("codex_switch_plugins._shared_available_catalog", return_value=catalog),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.source_mismatch",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        native_add.assert_not_called()

    def test_portable_exact_rejects_catalog_source_root_symlink_before_add(
        self,
    ) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        desired_source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="portable-v2",
        )
        real_catalog_source = self.root / "catalog-portable-v2-real"
        _write_plugin_artifact(
            real_catalog_source,
            version="2.0.0",
            payload="portable-v2",
        )
        linked_catalog_source = self.root / "catalog-portable-v2-linked"
        linked_catalog_source.symlink_to(real_catalog_source, target_is_directory=True)
        desired = {
            "selector": SELECTOR,
            "enabled": True,
            "policy": "portable_exact",
            "plugin": PLUGIN,
            "marketplace": MARKETPLACE,
            "marketplace_config": {
                "source": {
                    "source": "local",
                    "path": str(self.root / "marketplace"),
                }
            },
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(desired_source),
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                SELECTOR: PluginCatalogEntry(
                    selector=SELECTOR,
                    plugin=PLUGIN,
                    marketplace=MARKETPLACE,
                    version="1.0.0",
                    source_path=linked_catalog_source,
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch("codex_switch_plugins._shared_available_catalog", return_value=catalog),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unsafe_cache",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        native_add.assert_not_called()

    def test_functional_preflight_flushes_progress_before_materialization(self) -> None:
        from codex_switch_shared_configuration import (
            preflight_internal_shared_configuration,
        )

        class FlushTrackingStream(io.StringIO):
            def __init__(self) -> None:
                super().__init__()
                self.flush_count = 0

            def flush(self) -> None:
                self.flush_count += 1
                super().flush()

        source = self._official_artifact(payload="bootstrap-source")
        self._write_official_config(
            skill_path=source / "skills" / SKILL_NAME / "SKILL.md"
        )
        self.store.active_path.write_text(
            json.dumps(
                {
                    "profile": "internal",
                    "cli_profile": "internal",
                    "app_profile": "openai-official",
                    "launch_agent_path": str(self.store.launch_agent_path),
                },
                sort_keys=True,
            )
            + "\n"
        )
        materializer = FakeMaterializer(
            internal_home=self.internal_home,
            source_roots={SELECTOR: source},
            policies={SELECTOR: "portable_exact"},
        )
        progress = FlushTrackingStream()
        observed_at_materializer: list[tuple[str, int]] = []

        def materialize_after_progress(**kwargs):
            observed_at_materializer.append(
                (progress.getvalue(), progress.flush_count)
            )
            return materializer(**kwargs)

        with (
            patch(
                "codex_switch_plugins.materialize_shared_plugins",
                side_effect=materialize_after_progress,
            ),
            redirect_stderr(progress),
        ):
            receipt = preflight_internal_shared_configuration(
                store_root=self.store.root,
                internal_home=self.internal_home,
            )

        self.assertTrue(receipt.cli_ready)
        self.assertEqual(1, len(observed_at_materializer))
        output_before_materializer, flushes_before_materializer = (
            observed_at_materializer[0]
        )
        self.assertIn(
            "Shared configuration: attesting source configuration and Plugin identities...",
            output_before_materializer,
        )
        self.assertIn(
            "Shared configuration: materializing 1 Plugin for internal...",
            output_before_materializer,
        )
        self.assertGreaterEqual(flushes_before_materializer, 2)

    def test_production_materializer_rejects_absent_stale_and_wrong_store_lease(
        self,
    ) -> None:
        from codex_switch_plugins import (
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        source = self._official_artifact(payload="lease-source")
        target = _plugin_version_root(self.internal_home, cache_key="1.0.0")
        _write_plugin_artifact(target, version="1.0.0", payload="lease-source")
        desired = {
            "selector": SELECTOR,
            "enabled": True,
            "policy": "portable_exact",
            "plugin": PLUGIN,
            "marketplace": MARKETPLACE,
            "marketplace_config": {
                "source": {
                    "source": "local",
                    "path": str(self.root / "marketplace"),
                }
            },
            "cache_key": "1.0.0",
            "manifest_version": "1.0.0",
            "tree_sha256": plugin_tree_sha256(source),
        }
        common = {
            "store": self.store,
            "selection": self.selection,
            "source_profile": "openai-official",
            "target_profile": "internal",
            "desired_plugins": (desired,),
            "generation": 1,
        }

        with self.assertRaisesRegex(
            SwitchError,
            "shared_configuration.materialization.failed",
        ):
            materialize_shared_plugins(**common)

        stale_descriptor = os.open(
            self.store.root,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        os.close(stale_descriptor)
        with self.assertRaisesRegex(
            SwitchError,
            "shared_configuration.materialization.failed",
        ):
            materialize_shared_plugins(
                **common,
                _store_lock_descriptor=stale_descriptor,
            )

        wrong_root = self.root / "wrong-store"
        wrong_root.mkdir()
        wrong_descriptor = os.open(
            wrong_root,
            os.O_RDONLY | getattr(os, "O_DIRECTORY", 0),
        )
        try:
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.failed",
            ):
                materialize_shared_plugins(
                    **common,
                    _store_lock_descriptor=wrong_descriptor,
                )
        finally:
            os.close(wrong_descriptor)

        file_descriptor = os.open(self.internal_config, os.O_RDONLY)
        try:
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.failed",
            ):
                materialize_shared_plugins(
                    **common,
                    _store_lock_descriptor=file_descriptor,
                )
        finally:
            os.close(file_descriptor)

    def test_production_materializer_uses_target_backend_for_managed_plugin(self) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        desired = {
            "selector": selector,
            "enabled": True,
            "policy": "backend_managed",
            "plugin": "browser",
            "marketplace": "openai-bundled",
            "marketplace_config": {
                "source": {"source": "bundled"},
            },
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(source),
        }
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="1.5.0",
        )
        catalog = CatalogResult(
            status="verified",
            entries={
                selector: PluginCatalogEntry(
                    selector=selector,
                    plugin="browser",
                    marketplace="openai-bundled",
                    version="1.5.0",
                    source_path=source,
                    installed_record_seen=True,
                    installed_versions=("1.5.0",),
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def install_with_target_backend(**_kwargs) -> None:
            _write_plugin_artifact(
                target,
                plugin="browser",
                version="1.5.0",
                payload="internal-compatible-browser",
            )

        with (
            patch(
                "codex_switch_plugins.profile_plugin_runtime",
                return_value=runtime,
            ),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(catalog, catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_with_target_backend,
            ) as native_add,
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        native_add.assert_called_once()
        self.assertEqual(1, len(receipts))
        receipt = receipts[0]
        self.assertEqual(selector, receipt["selector"])
        self.assertEqual("backend_managed", receipt["policy"])
        self.assertEqual("1.5.0", receipt["cache_key"])
        self.assertEqual("1.5.0", receipt["manifest_version"])
        self.assertEqual("internal-compatible-browser", (target / "payload.txt").read_text())
        self.assertNotEqual(plugin_tree_sha256(source), receipt["tree_sha256"])

    def test_production_materializer_rejects_uninspectable_managed_cache(self) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
        )

        selector = "browser@openai-bundled"
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="1.5.0",
        )
        _write_plugin_artifact(
            target,
            plugin="browser",
            version="1.5.0",
            payload="unproved-browser",
        )
        desired = {
            "selector": selector,
            "enabled": True,
            "policy": "backend_managed",
            "plugin": "browser",
            "marketplace": "openai-bundled",
            "marketplace_config": {
                "source": {"source": "bundled"},
            },
            "cache_key": "",
            "manifest_version": "",
            "tree_sha256": "",
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                selector: PluginCatalogEntry(
                    selector=selector,
                    plugin="browser",
                    marketplace="openai-bundled",
                    version="1.5.0",
                    source_path=None,
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch(
                "codex_switch_plugins.profile_plugin_runtime",
                return_value=runtime,
            ),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                return_value=catalog,
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
            ) as native_add,
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unsafe_cache",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        native_add.assert_not_called()

    def test_production_identical_managed_cache_still_requires_inspectable_catalog(
        self,
    ) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="byte-identical-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="2.0.0",
        )
        _write_plugin_artifact(
            target,
            plugin="browser",
            version="2.0.0",
            payload="byte-identical-browser",
        )
        desired = {
            "selector": selector,
            "enabled": True,
            "policy": "backend_managed",
            "plugin": "browser",
            "marketplace": "openai-bundled",
            "marketplace_config": {"source": {"source": "bundled"}},
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(source),
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                selector: PluginCatalogEntry(
                    selector=selector,
                    plugin="browser",
                    marketplace="openai-bundled",
                    version="2.0.0",
                    source_path=None,
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch(
                "codex_switch_plugins.profile_plugin_runtime",
                return_value=runtime,
            ),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                return_value=catalog,
            ) as available_catalog,
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unsafe_cache",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        available_catalog.assert_called_once()
        native_add.assert_not_called()

    def test_production_managed_target_need_not_match_source_after_native_add(
        self,
    ) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        stale_target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="1.5.0",
        )
        _write_plugin_artifact(
            stale_target,
            plugin="browser",
            version="1.5.0",
            payload="stale-browser",
        )
        desired = {
            "selector": selector,
            "enabled": True,
            "policy": "backend_managed",
            "plugin": "browser",
            "marketplace": "openai-bundled",
            "marketplace_config": {"source": {"source": "bundled"}},
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(source),
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                selector: PluginCatalogEntry(
                    selector=selector,
                    plugin="browser",
                    marketplace="openai-bundled",
                    version="1.5.0",
                    source_path=source,
                    installed_record_seen=True,
                    installed_versions=("1.5.0",),
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch(
                "codex_switch_plugins.profile_plugin_runtime",
                return_value=runtime,
            ),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(catalog, catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        native_add.assert_called_once()
        self.assertEqual("stale-browser", (stale_target / "payload.txt").read_text())
        self.assertEqual("1.5.0", receipts[0]["cache_key"])

    def test_production_native_add_restores_only_expected_plugin_config_delta(
        self,
    ) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="1.5.0",
        )
        desired = {
            "selector": selector,
            "enabled": True,
            "policy": "backend_managed",
            "plugin": "browser",
            "marketplace": "openai-bundled",
            "marketplace_config": {"source": {"source": "bundled"}},
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(source),
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                selector: PluginCatalogEntry(
                    selector=selector,
                    plugin="browser",
                    marketplace="openai-bundled",
                    version="1.5.0",
                    source_path=source,
                    installed_record_seen=True,
                    installed_versions=("1.5.0",),
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )
        config_before = self.internal_config.read_bytes()

        def install_with_expected_config_delta(**_kwargs) -> None:
            _write_plugin_artifact(
                target,
                plugin="browser",
                version="1.5.0",
                payload="catalog-current-browser",
            )
            self.internal_config.write_text(
                self.internal_config.read_text()
                + f'\n[plugins."{selector}"]\nenabled = true\n'
            )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(catalog, catalog),
            ),
            patch("codex_switch_plugins.running_target_app_server_pids", return_value=[]),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_with_expected_config_delta,
            ),
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        self.assertEqual(1, len(receipts))
        self.assertEqual(config_before, self.internal_config.read_bytes())

    def test_production_native_add_preserves_unexpected_config_drift(self) -> None:
        from codex_switch_plugins import (
            CatalogResult,
            PluginCatalogEntry,
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="2.0.0",
            version="2.0.0",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="1.5.0",
        )
        desired = {
            "selector": selector,
            "enabled": True,
            "policy": "backend_managed",
            "plugin": "browser",
            "marketplace": "openai-bundled",
            "marketplace_config": {"source": {"source": "bundled"}},
            "cache_key": "2.0.0",
            "manifest_version": "2.0.0",
            "tree_sha256": plugin_tree_sha256(source),
        }
        catalog = CatalogResult(
            status="verified",
            entries={
                selector: PluginCatalogEntry(
                    selector=selector,
                    plugin="browser",
                    marketplace="openai-bundled",
                    version="1.5.0",
                    source_path=source,
                    installed_record_seen=True,
                    installed_versions=("1.5.0",),
                )
            },
            stdout="",
            stderr="",
            returncode=0,
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def install_with_foreign_config_delta(**_kwargs) -> None:
            _write_plugin_artifact(
                target,
                plugin="browser",
                version="1.5.0",
                payload="catalog-current-browser",
            )
            self.internal_config.write_text(
                self.internal_config.read_text()
                + f'\n[plugins."{selector}"]\nenabled = true\n'
                + "\n[foreign_edit]\npreserve_me = true\n"
            )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch("codex_switch_plugins._shared_available_catalog", return_value=catalog),
            patch("codex_switch_plugins.running_target_app_server_pids", return_value=[]),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_with_foreign_config_delta,
            ),
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.target_changed_during_plan",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        self.assertIn("[foreign_edit]", self.internal_config.read_text())
        self.assertIn("preserve_me = true", self.internal_config.read_text())
        self.assertNotIn(f'[plugins."{selector}"]', self.internal_config.read_text())

    def test_catalog_preserves_installed_target_and_available_source_axes(
        self,
    ) -> None:
        selector = "browser@openai-bundled"
        source = self.root / "bundled-browser"
        installed = self._catalog_record(
            selector=selector,
            version="26.721.41059",
            source=source,
            installed=True,
            enabled=True,
        )
        available = self._catalog_record(
            selector=selector,
            version="26.803.61601",
            source=source,
            installed=False,
            enabled=True,
        )

        for payload in (
            {"installed": [installed], "available": [available]},
            {"available": [available], "installed": [installed]},
        ):
            with self.subTest(keys=tuple(payload)):
                from codex_switch_plugins import available_plugin_catalog

                catalog = available_plugin_catalog(json.dumps(payload))
                self.assertTrue(catalog.verified, catalog.detail)
                entry = catalog.entries[selector]
                self.assertEqual("26.803.61601", entry.version)
                self.assertEqual(source, entry.source_path)
                self.assertTrue(entry.installed_record_seen)
                self.assertEqual(("26.721.41059",), entry.installed_versions)

        available_without_source = self._catalog_record(
            selector=selector,
            version="26.803.61601",
            source=None,
            installed=False,
        )
        catalog = self._raw_catalog(
            installed=[installed],
            available=[available_without_source],
        )
        entry = catalog.entries[selector]
        self.assertEqual("26.803.61601", entry.version)
        self.assertEqual(source, entry.source_path)
        self.assertEqual(("26.721.41059",), entry.installed_versions)

    def test_production_managed_live_version_divergence_reconciles_with_fresh_target_proof(
        self,
    ) -> None:
        from codex_switch_plugins import (
            PluginMaintenanceRuntime,
            materialize_shared_plugins,
            plugin_tree_sha256,
        )

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser-current",
            marketplace="openai-bundled",
            plugin="browser",
        )
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="26.721.41059",
        )
        _write_plugin_artifact(
            target,
            plugin="browser",
            version="26.721.41059",
            payload="internal-compatible-browser",
        )
        desired = self._backend_desired(source, selector=selector)
        installed = self._catalog_record(
            selector=selector,
            version="26.721.41059",
            source=source,
            installed=True,
            enabled=True,
        )
        pre_catalog = self._raw_catalog(installed=[installed])
        post_catalog = self._raw_catalog(installed=[installed])
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ) as available_catalog,
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        native_add.assert_called_once()
        self.assertEqual(2, available_catalog.call_count)
        self.assertEqual("26.721.41059", receipts[0]["cache_key"])
        self.assertEqual("26.721.41059", receipts[0]["manifest_version"])
        self.assertNotEqual(plugin_tree_sha256(source), receipts[0]["tree_sha256"])

    def test_production_managed_native_update_may_replace_prior_installed_version(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser-current",
            marketplace="openai-bundled",
            plugin="browser",
        )
        prior_target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="26.721.41059",
        )
        _write_plugin_artifact(
            prior_target,
            plugin="browser",
            version="26.721.41059",
            payload="internal-browser-prior",
        )
        replacement_target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="26.805.10001",
        )
        desired = self._backend_desired(source, selector=selector)
        pre_catalog = self._raw_catalog(
            installed=[
                self._catalog_record(
                    selector=selector,
                    version="26.721.41059",
                    source=source,
                    installed=True,
                )
            ]
        )
        post_catalog = self._raw_catalog(
            installed=[
                self._catalog_record(
                    selector=selector,
                    version="26.805.10001",
                    source=source,
                    installed=True,
                )
            ]
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def replace_prior_version(**_kwargs) -> None:
            shutil.rmtree(prior_target)
            _write_plugin_artifact(
                replacement_target,
                plugin="browser",
                version="26.805.10001",
                payload="internal-browser-replacement",
            )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=replace_prior_version,
            ) as native_add,
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        native_add.assert_called_once()
        self.assertFalse(prior_target.exists())
        self.assertTrue(replacement_target.is_dir())
        self.assertEqual("26.805.10001", receipts[0]["cache_key"])
        self.assertEqual("26.805.10001", receipts[0]["manifest_version"])

    def test_production_managed_post_add_uses_fresh_revision_target(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "figma@openai-curated"
        source = self._official_artifact(
            cache_key="2.0.17",
            version="2.0.17",
            payload="official-figma-current",
            marketplace="openai-curated",
            plugin="figma",
        )
        desired = self._backend_desired(source, selector=selector)
        pre_catalog = self._raw_catalog(
            installed=[
                self._catalog_record(
                    selector=selector,
                    version="oldrev1",
                    source=source,
                    installed=True,
                )
            ]
        )
        post_catalog = self._raw_catalog(
            installed=[
                self._catalog_record(
                    selector=selector,
                    version="11c74d6b",
                    source=source,
                    installed=True,
                )
            ]
        )
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-curated",
            plugin="figma",
            cache_key="11c74d6b",
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def install_revision(**_kwargs) -> None:
            _write_plugin_artifact(
                target,
                plugin="figma",
                version="2.0.13",
                payload="internal-compatible-figma",
            )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ) as available_catalog,
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_revision,
            ),
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=(desired,),
                generation=1,
            )

        self.assertEqual(2, available_catalog.call_count)
        self.assertEqual("11c74d6b", receipts[0]["cache_key"])
        self.assertEqual("2.0.13", receipts[0]["manifest_version"])

    def test_production_managed_batch_uses_one_fresh_post_add_catalog(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selectors = (
            "browser@openai-bundled",
            "pdf@openai-bundled",
        )
        installed_records: list[dict[str, object]] = []
        desired_plugins: list[dict[str, object]] = []
        for index, selector in enumerate(selectors, start=1):
            plugin, marketplace = selector.rsplit("@", 1)
            source_version = f"26.803.6160{index}"
            target_version = f"26.721.4105{index}"
            source = self._official_artifact(
                cache_key=source_version,
                version=source_version,
                payload=f"official-{plugin}",
                marketplace=marketplace,
                plugin=plugin,
            )
            target = _plugin_version_root(
                self.internal_home,
                marketplace=marketplace,
                plugin=plugin,
                cache_key=target_version,
            )
            _write_plugin_artifact(
                target,
                plugin=plugin,
                version=target_version,
                payload=f"internal-{plugin}",
            )
            desired_plugins.append(self._backend_desired(source, selector=selector))
            installed_records.append(
                self._catalog_record(
                    selector=selector,
                    version=target_version,
                    source=source,
                    installed=True,
                )
            )

        pre_catalog = self._raw_catalog(installed=installed_records)
        post_catalog = self._raw_catalog(installed=installed_records)
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ) as available_catalog,
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            receipts = self._materialize_with_lease(
                materialize_shared_plugins,
                store=self.store,
                selection=self.selection,
                source_profile="openai-official",
                target_profile="internal",
                desired_plugins=tuple(desired_plugins),
                generation=1,
            )

        self.assertEqual(2, native_add.call_count)
        self.assertEqual(2, available_catalog.call_count)
        self.assertEqual(selectors, tuple(receipt["selector"] for receipt in receipts))

    def test_production_managed_post_add_without_installed_proof_is_unverified_target(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="shared-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        desired = self._backend_desired(source, selector=selector)
        available = self._catalog_record(
            selector=selector,
            version="26.803.61601",
            source=source,
            installed=False,
        )
        pre_catalog = self._raw_catalog(available=[available])
        post_catalog = self._raw_catalog(available=[available])
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="26.803.61601",
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def install_without_catalog_proof(**_kwargs) -> None:
            _write_plugin_artifact(
                target,
                plugin="browser",
                version="26.803.61601",
                payload="shared-browser",
            )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_without_catalog_proof,
            ),
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unverified_target",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

    def test_production_managed_missing_post_add_cache_is_unverified_target(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        desired = self._backend_desired(source, selector=selector)
        available = self._catalog_record(
            selector=selector,
            version="26.803.61601",
            source=source,
        )
        installed = self._catalog_record(
            selector=selector,
            version="26.721.41059",
            source=source,
            installed=True,
        )
        pre_catalog = self._raw_catalog(available=[available])
        post_catalog = self._raw_catalog(
            installed=[installed],
            available=[available],
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin"),
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unverified_target",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

    def test_production_managed_conflicting_installed_targets_are_unverified(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        desired = self._backend_desired(source, selector=selector)
        available = self._catalog_record(
            selector=selector,
            version="26.803.61601",
            source=source,
        )
        pre_catalog = self._raw_catalog(available=[available])
        post_catalog = self._raw_catalog(
            installed=[
                self._catalog_record(
                    selector=selector,
                    version=version,
                    source=source,
                    installed=True,
                )
                for version in ("26.721.41059", "26.722.00000")
            ],
            available=[available],
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin"),
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unverified_target",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

    def test_production_managed_target_manifest_mismatch_is_unverified(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        desired = self._backend_desired(source, selector=selector)
        available = self._catalog_record(
            selector=selector,
            version="26.803.61601",
            source=source,
        )
        installed = self._catalog_record(
            selector=selector,
            version="26.721.41059",
            source=source,
            installed=True,
        )
        pre_catalog = self._raw_catalog(available=[available])
        post_catalog = self._raw_catalog(
            installed=[installed],
            available=[available],
        )
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="26.721.41059",
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def install_mismatched_manifest(**_kwargs) -> None:
            _write_plugin_artifact(
                target,
                plugin="browser",
                version="26.700.0",
                payload="internal-browser",
            )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_mismatched_manifest,
            ),
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unverified_target",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

    def test_production_managed_dangling_target_link_is_unsafe_cache(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        desired = self._backend_desired(source, selector=selector)
        available = self._catalog_record(
            selector=selector,
            version="26.803.61601",
            source=source,
        )
        installed = self._catalog_record(
            selector=selector,
            version="26.721.41059",
            source=source,
            installed=True,
        )
        pre_catalog = self._raw_catalog(available=[available])
        post_catalog = self._raw_catalog(
            installed=[installed],
            available=[available],
        )
        target = _plugin_version_root(
            self.internal_home,
            marketplace="openai-bundled",
            plugin="browser",
            cache_key="26.721.41059",
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        def install_with_dangling_link(**_kwargs) -> None:
            _write_plugin_artifact(
                target,
                plugin="browser",
                version="26.721.41059",
                payload="internal-browser",
            )
            (target / "dangling").symlink_to(target / "missing")

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                side_effect=(pre_catalog, post_catalog),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch(
                "codex_switch_plugins._native_add_shared_plugin",
                side_effect=install_with_dangling_link,
            ),
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unsafe_cache",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

    def test_production_catalog_spawn_failure_is_unverified_catalog(self) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        desired = self._backend_desired(source, selector=selector)
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "missing-internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._capture_profile_command",
                side_effect=OSError("catalog spawn failed"),
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.unverified_catalog",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        native_add.assert_not_called()

    def test_production_managed_source_drift_is_source_mismatch(self) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        desired_source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        drifted_source = self.root / "drifted-browser"
        _write_plugin_artifact(
            drifted_source,
            plugin="browser",
            version="26.900.0",
            payload="drifted-browser",
        )
        desired = self._backend_desired(desired_source, selector=selector)
        pre_catalog = self._raw_catalog(
            available=[
                self._catalog_record(
                    selector=selector,
                    version="26.900.0",
                    source=drifted_source,
                )
            ]
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                return_value=pre_catalog,
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.source_mismatch",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        native_add.assert_not_called()

    def test_production_managed_missing_source_manifest_is_source_mismatch(
        self,
    ) -> None:
        from codex_switch_plugins import PluginMaintenanceRuntime, materialize_shared_plugins

        selector = "browser@openai-bundled"
        desired_source = self._official_artifact(
            cache_key="26.803.61601",
            version="26.803.61601",
            payload="official-browser",
            marketplace="openai-bundled",
            plugin="browser",
        )
        incomplete_source = self.root / "incomplete-browser-source"
        incomplete_source.mkdir()
        desired = self._backend_desired(desired_source, selector=selector)
        pre_catalog = self._raw_catalog(
            available=[
                self._catalog_record(
                    selector=selector,
                    version="26.803.61601",
                    source=incomplete_source,
                )
            ]
        )
        runtime = PluginMaintenanceRuntime(
            codex_bin=self.root / "internal-codex",
            home=self.internal_home,
        )

        with (
            patch("codex_switch_plugins.profile_plugin_runtime", return_value=runtime),
            patch(
                "codex_switch_plugins._shared_available_catalog",
                return_value=pre_catalog,
            ),
            patch(
                "codex_switch_plugins.running_target_app_server_pids",
                return_value=[],
            ),
            patch("codex_switch_plugins._native_add_shared_plugin") as native_add,
        ):
            with self.assertRaisesRegex(
                SwitchError,
                "shared_configuration.materialization.source_mismatch",
            ):
                self._materialize_with_lease(
                    materialize_shared_plugins,
                    store=self.store,
                    selection=self.selection,
                    source_profile="openai-official",
                    target_profile="internal",
                    desired_plugins=(desired,),
                    generation=1,
                )

        native_add.assert_not_called()


if __name__ == "__main__":
    unittest.main()
