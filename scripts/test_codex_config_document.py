#!/usr/bin/env python3

from __future__ import annotations

import importlib
import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from codex_switch_config import (
    merge_missing_non_usage_shared_config_defaults,
    merge_missing_shared_config_defaults,
    replace_plugin_skill_usage_state,
    merge_shared_config_overlay,
)
from codex_switch_constants import SwitchError
from codex_switch_home_sync import (
    merge_shared_with_profile_seed,
    strip_managed_comments,
)


WRAPPER = Path(__file__).with_name("codex-switch")
PROFILE_SWITCH = Path(__file__).with_name("codex_profile_switch.py")


def config_document_module():
    try:
        return importlib.import_module("codex_switch_config_document")
    except ModuleNotFoundError as exc:
        raise AssertionError("ConfigDocument module is required") from exc


def recover_missing(document, snapshot, *, protected_paths):
    method = getattr(document, "recover_missing_from", None)
    if not callable(method):
        raise AssertionError("ConfigDocument.recover_missing_from is required")
    return method(snapshot, protected_paths=protected_paths)


def remove_exact_scalar_assignment(
    document,
    *,
    path,
    table_path,
    label,
):
    method = getattr(document, "remove_exact_scalar_assignment", None)
    if not callable(method):
        raise AssertionError(
            "ConfigDocument.remove_exact_scalar_assignment is required"
        )
    return method(path=path, table_path=table_path, label=label)


class ConfigDocumentTests(unittest.TestCase):
    def test_managed_runtime_render_is_byte_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shared_config = root / "shared.toml"
            runtime_config = root / "runtime.toml"
            canonical_config = root / "profile.toml"
            shared_config.write_text(
                "# user-owned shared comment\n"
                "\n"
                "[features]\n"
                "hooks = true\n"
            )
            canonical_config.write_text(
                'model = "internal-model"\n'
                'model_provider = "azure"\n'
                "\n"
                "[model_providers.azure]\n"
                'name = "Azure"\n'
                "\n"
                "[model_providers.azure.query_params]\n"
                'api-version = "v1"\n'
            )

            first = merge_shared_with_profile_seed(
                shared_config,
                "internal",
                runtime_config,
                canonical_config,
            )
            runtime_config.write_text(first)
            second = merge_shared_with_profile_seed(
                shared_config,
                "internal",
                runtime_config,
                canonical_config,
            )
            runtime_config.write_text(second)
            third = merge_shared_with_profile_seed(
                shared_config,
                "internal",
                runtime_config,
                canonical_config,
            )

            self.assertEqual(second, third)

    def test_managed_comment_cleanup_preserves_unrelated_user_spacing(self) -> None:
        text = (
            "# codex-switch: generated heading\n"
            "\n"
            "[features]\n"
            "hooks = true\n"
            "\n"
            "\n"
            "# user-owned separator\n"
            "[desktop]\n"
            'theme = "dark"\n'
        )

        cleaned = strip_managed_comments(text)

        self.assertIn(
            "hooks = true\n\n\n# user-owned separator\n[desktop]",
            cleaned,
        )

    def test_parse_preserves_valid_text_and_reports_semantic_paths(self) -> None:
        module = config_document_module()
        text = (
            '# heading\n'
            'top.level = "value"\n'
            '\n'
            '["desktop.settings"]\n'
            '"theme.mode" = "dark"\n'
            'nested.value = "old"\n'
        )

        document = module.ConfigDocument.parse(text, "valid fixture")

        self.assertEqual(text, document.text)
        self.assertEqual(
            {
                ("top", "level"),
                ("desktop.settings", "theme.mode"),
                ("desktop.settings", "nested", "value"),
            },
            set(document.assignment_paths),
        )

    def test_parse_rejects_invalid_toml_with_label(self) -> None:
        module = config_document_module()

        with self.assertRaisesRegex(
            SwitchError,
            "Invalid TOML.*invalid fixture",
        ):
            module.ConfigDocument.parse('value = "unterminated\n', "invalid fixture")

    def test_parse_requires_real_toml_parser(self) -> None:
        module = config_document_module()

        with mock.patch.object(module, "tomllib", None):
            with self.assertRaisesRegex(
                SwitchError,
                "Python 3\\.11\\+.*missing parser fixture",
            ):
                module.ConfigDocument.parse('value = "ok"\n', "missing parser fixture")

    def test_legacy_toml_validator_requires_real_parser(self) -> None:
        validator = importlib.import_module("codex_switch_toml_validate")

        with mock.patch.object(validator, "tomllib", None):
            with self.assertRaisesRegex(
                SwitchError,
                "Python 3\\.11\\+.*legacy validator fixture",
            ):
                validator.validate_toml_text(
                    'value = "accepted by the old basic scanner"\n',
                    "legacy validator fixture",
                )

    def test_parse_records_complete_regular_and_array_table_spans(self) -> None:
        module = config_document_module()
        text = (
            "[desktop]\n"
            "queue = [\n"
            '  "one",\n'
            "]\n"
            "# belongs to the desktop block\n"
            "\n"
            "[[skills.config]]\n"
            'path = "/skills/one/SKILL.md"\n'
            "enabled = false\n"
            "\n"
            "[[skills.config]]\n"
            'path = "/skills/two/SKILL.md"\n'
        )

        document = module.ConfigDocument.parse(text, "table spans")

        self.assertEqual(3, len(document.tables))
        self.assertEqual(("desktop",), document.tables[0].path)
        self.assertFalse(document.tables[0].is_array)
        self.assertEqual(
            (
                "[desktop]\n"
                "queue = [\n"
                '  "one",\n'
                "]\n"
                "# belongs to the desktop block\n"
                "\n"
            ),
            document.tables[0].text,
        )
        self.assertEqual(("skills", "config"), document.tables[1].path)
        self.assertTrue(document.tables[1].is_array)
        self.assertEqual(0, document.tables[1].array_index)
        self.assertEqual(("skills", "config"), document.tables[2].path)
        self.assertEqual(1, document.tables[2].array_index)

    def test_replace_values_from_handles_quoted_and_dotted_keys(self) -> None:
        module = config_document_module()
        current = module.ConfigDocument.parse(
            (
                '["desktop.settings"]\n'
                '"theme.mode" = "dark"\n'
                'nested.value = "old"\n'
                'untouched = "keep"\n'
            ),
            "current",
        )
        overlay = module.ConfigDocument.parse(
            (
                '["desktop.settings"]\n'
                '"theme.mode" = "light"\n'
                'nested.value = "new"\n'
            ),
            "overlay",
        )

        result = current.replace_values_from(overlay)

        self.assertEqual(
            (
                '["desktop.settings"]\n'
                '"theme.mode" = "light"\n'
                'nested.value = "new"\n'
                'untouched = "keep"\n'
            ),
            result.text,
        )

    def test_replace_values_from_preserves_crlf_comments_and_array_span(self) -> None:
        module = config_document_module()
        current_text = (
            "# keep heading\r\n"
            "[desktop]\r\n"
            "queue = [\r\n"
            '  "old-a", # old item\r\n'
            '  "old-b",\r\n'
            "] # keep target comment\r\n"
            'mode = "keep"\r\n'
        )
        current = module.ConfigDocument.parse(current_text, "current CRLF")
        overlay = module.ConfigDocument.parse(
            (
                "[desktop]\r\n"
                "queue = [\r\n"
                '  "new",\r\n'
                "]\r\n"
            ),
            "overlay CRLF",
        )

        result = current.replace_values_from(overlay)

        self.assertEqual(
            (
                "# keep heading\r\n"
                "[desktop]\r\n"
                "queue = [\r\n"
                '  "new",\r\n'
                "] # keep target comment\r\n"
                'mode = "keep"\r\n'
            ),
            result.text,
        )

    def test_replace_values_from_replaces_complete_multiline_string(self) -> None:
        module = config_document_module()
        current = module.ConfigDocument.parse(
            (
                "[message]\n"
                'body = """old line\n'
                'stale line"""\n'
                'tail = "keep"\n'
            ),
            "current string",
        )
        overlay = module.ConfigDocument.parse(
            (
                "[message]\n"
                'body = """new line\n'
                'new tail"""\n'
            ),
            "overlay string",
        )

        result = current.replace_values_from(overlay)

        self.assertEqual(
            (
                "[message]\n"
                'body = """new line\n'
                'new tail"""\n'
                'tail = "keep"\n'
            ),
            result.text,
        )
        self.assertNotIn("stale line", result.text)

    def test_replace_values_from_replaces_inline_tables_in_reverse_order(self) -> None:
        module = config_document_module()
        current = module.ConfigDocument.parse(
            (
                "[first]\n"
                'value = { old = "one", keep = true } # first comment\n'
                "\n"
                "[second]\n"
                'value = { old = "two" } # second comment\n'
            ),
            "current inline tables",
        )
        overlay = module.ConfigDocument.parse(
            (
                "[first]\n"
                'value = { new = "a-much-longer-value" }\n'
                "\n"
                "[second]\n"
                'value = { new = "x" }\n'
            ),
            "overlay inline tables",
        )

        result = current.replace_values_from(overlay)

        self.assertEqual(
            (
                "[first]\n"
                'value = { new = "a-much-longer-value" } # first comment\n'
                "\n"
                "[second]\n"
                'value = { new = "x" } # second comment\n'
            ),
            result.text,
        )

    def test_semantically_equal_overlay_is_byte_identical(self) -> None:
        module = config_document_module()
        current_text = (
            "# preserve exact bytes\r\n"
            "value = [1, 2] # target comment\r\n"
        )
        current = module.ConfigDocument.parse(current_text, "current no-op")
        overlay = module.ConfigDocument.parse(
            "value = [ 1, 2 ]\n",
            "overlay no-op",
        )

        result = current.replace_values_from(overlay)

        self.assertIs(current, result)
        self.assertEqual(current_text, result.text)

    def test_remove_exact_scalar_assignment_preserves_section_and_siblings(
        self,
    ) -> None:
        module = config_document_module()
        document = module.ConfigDocument.parse(
            (
                "# keep heading\n"
                "[agents]\n"
                "# keep tuning comment\n"
                "max_threads = 6 # remove only this assignment\n"
                "max_depth = 3\n"
                'role = "explorer"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
            ),
            "max threads source",
        )

        result = remove_exact_scalar_assignment(
            document,
            path=("agents", "max_threads"),
            table_path=("agents",),
            label="max threads removed",
        )

        self.assertEqual(
            (
                "# keep heading\n"
                "[agents]\n"
                "# keep tuning comment\n"
                "max_depth = 3\n"
                'role = "explorer"\n'
                "\n"
                "[features]\n"
                "memory = true\n"
            ),
            result.text,
        )
        self.assertEqual(3, result.data["agents"]["max_depth"])
        self.assertEqual("explorer", result.data["agents"]["role"])
        self.assertNotIn("max_threads", result.data["agents"])

    def test_remove_exact_scalar_assignment_is_idempotent_when_absent(
        self,
    ) -> None:
        module = config_document_module()
        text = (
            "[agents]\n"
            "max_depth = 3\n"
            'role = "explorer"\n'
        )
        document = module.ConfigDocument.parse(text, "already clean agents")

        result = remove_exact_scalar_assignment(
            document,
            path=("agents", "max_threads"),
            table_path=("agents",),
            label="still clean agents",
        )

        self.assertIs(document, result)
        self.assertEqual(text, result.text)

    def test_remove_exact_scalar_assignment_rejects_dotted_form(
        self,
    ) -> None:
        module = config_document_module()
        document = module.ConfigDocument.parse(
            (
                "agents.max_threads = 6\n"
                'mode = "keep"\n'
            ),
            "dotted max threads",
        )

        with self.assertRaisesRegex(
            SwitchError,
            "config_exact_assignment_ambiguous",
        ):
            remove_exact_scalar_assignment(
                document,
                path=("agents", "max_threads"),
                table_path=("agents",),
                label="dotted max threads rejected",
            )

    def test_remove_exact_scalar_assignment_rejects_non_scalar_value(
        self,
    ) -> None:
        module = config_document_module()
        document = module.ConfigDocument.parse(
            (
                "[agents]\n"
                "max_threads = [6]\n"
                "max_depth = 3\n"
            ),
            "non-scalar max threads",
        )

        with self.assertRaisesRegex(
            SwitchError,
            "config_exact_assignment_ambiguous",
        ):
            remove_exact_scalar_assignment(
                document,
                path=("agents", "max_threads"),
                table_path=("agents",),
                label="non-scalar max threads rejected",
            )

    def test_remove_exact_scalar_assignment_rejects_inline_parent_table(
        self,
    ) -> None:
        module = config_document_module()
        document = module.ConfigDocument.parse(
            (
                "agents = { max_threads = 6, max_depth = 3 }\n"
                'mode = "keep"\n'
            ),
            "inline agents table",
        )

        with self.assertRaisesRegex(
            SwitchError,
            "config_exact_assignment_ambiguous",
        ):
            remove_exact_scalar_assignment(
                document,
                path=("agents", "max_threads"),
                table_path=("agents",),
                label="inline agents table rejected",
            )

    def test_recovery_keeps_current_disabled_skill_and_restores_missing_once(
        self,
    ) -> None:
        module = config_document_module()
        current_text = (
            "[[skills.config]]\n"
            'path = "/skills/current/SKILL.md"\n'
            "enabled = false\n"
        )
        current = module.ConfigDocument.parse(current_text, "current skills")
        snapshot = module.ConfigDocument.parse(
            (
                "[[skills.config]]\n"
                'path = "/skills/current/SKILL.md"\n'
                "enabled = true\n"
                "\n"
                "[[skills.config]]\n"
                'path = "/skills/missing/SKILL.md"\n'
                "enabled = true\n"
            ),
            "snapshot skills",
        )

        result = recover_missing(
            current,
            snapshot,
            protected_paths=frozenset(),
        )

        self.assertIn(current_text, result.text)
        self.assertNotIn(
            'path = "/skills/current/SKILL.md"\nenabled = true',
            result.text,
        )
        self.assertEqual(
            1,
            result.text.count('path = "/skills/missing/SKILL.md"'),
        )
        self.assertEqual(
            (("skills", "config", "/skills/missing/SKILL.md"),),
            result.restored_paths,
        )
        self.assertEqual((), result.diagnostics)

    def test_recovery_skips_ambiguous_snapshot_skill_identities(self) -> None:
        module = config_document_module()
        current = module.ConfigDocument.parse("", "empty current")
        snapshot = module.ConfigDocument.parse(
            (
                "[[skills.config]]\n"
                "enabled = true\n"
                "\n"
                "[[skills.config]]\n"
                'path = ["/skills/non-scalar/SKILL.md"]\n'
                "\n"
                "[[skills.config]]\n"
                'path = "/skills/duplicate/SKILL.md"\n'
                "\n"
                "[[skills.config]]\n"
                'path = "/skills/duplicate/SKILL.md"\n'
            ),
            "ambiguous snapshot",
        )

        result = recover_missing(
            current,
            snapshot,
            protected_paths=frozenset(),
        )

        self.assertEqual("", result.text)
        self.assertEqual(
            {
                "skills_config_missing_identity",
                "skills_config_non_string_identity",
                "skills_config_duplicate_identity",
            },
            {diagnostic.code for diagnostic in result.diagnostics},
        )

    def test_recovery_skips_identity_duplicated_in_current_document(self) -> None:
        module = config_document_module()
        current_text = (
            "[[skills.config]]\n"
            'path = "/skills/duplicate/SKILL.md"\n'
            "enabled = false\n"
            "\n"
            "[[skills.config]]\n"
            'path = "/skills/duplicate/SKILL.md"\n'
            "enabled = true\n"
        )
        current = module.ConfigDocument.parse(current_text, "duplicate current")
        snapshot = module.ConfigDocument.parse(
            (
                "[[skills.config]]\n"
                'path = "/skills/duplicate/SKILL.md"\n'
                "enabled = true\n"
            ),
            "snapshot duplicate current",
        )

        result = recover_missing(
            current,
            snapshot,
            protected_paths=frozenset(),
        )

        self.assertEqual(current_text, result.text)
        self.assertEqual(
            ["skills_config_duplicate_identity"],
            [diagnostic.code for diagnostic in result.diagnostics],
        )

    def test_recovery_does_not_normalize_skill_identity_paths(self) -> None:
        module = config_document_module()
        current = module.ConfigDocument.parse(
            (
                "[[skills.config]]\n"
                'path = "/skills/team/../shared/SKILL.md"\n'
            ),
            "lexical current",
        )
        snapshot = module.ConfigDocument.parse(
            (
                "[[skills.config]]\n"
                'path = "/skills/shared/SKILL.md"\n'
            ),
            "normalized-looking snapshot",
        )

        result = recover_missing(
            current,
            snapshot,
            protected_paths=frozenset(),
        )

        self.assertIn(
            'path = "/skills/team/../shared/SKILL.md"',
            result.text,
        )
        self.assertIn('path = "/skills/shared/SKILL.md"', result.text)

    def test_recovery_blocks_protected_ancestor_equal_and_descendant_paths(
        self,
    ) -> None:
        module = config_document_module()
        current = module.ConfigDocument.parse("", "protected current")
        snapshot = module.ConfigDocument.parse(
            (
                'ancestor = { child = "blocked" }\n'
                'equal.key = "blocked"\n'
                'descendant.child = "blocked"\n'
                'allowed.key = "restored"\n'
            ),
            "protected snapshot",
        )

        result = recover_missing(
            current,
            snapshot,
            protected_paths=frozenset(
                {
                    ("ancestor", "child"),
                    ("equal", "key"),
                    ("descendant",),
                }
            ),
        )

        self.assertNotIn("ancestor", result.text)
        self.assertNotIn("equal", result.text)
        self.assertNotIn("descendant", result.text)
        self.assertIn('allowed.key = "restored"', result.text)

    def test_recovery_honors_exact_plugin_removal_and_skips_unknown_arrays(
        self,
    ) -> None:
        module = config_document_module()
        current = module.ConfigDocument.parse("", "plugin removal current")
        snapshot = module.ConfigDocument.parse(
            (
                '[plugins."removed@market"]\n'
                "enabled = true\n"
                "\n"
                '[plugins."removed@market-extra"]\n'
                "enabled = true\n"
                "\n"
                "[[unknown.items]]\n"
                'id = "do-not-guess"\n'
            ),
            "plugin removal snapshot",
        )

        result = recover_missing(
            current,
            snapshot,
            protected_paths=frozenset({("plugins", "removed@market")}),
        )

        self.assertNotIn('[plugins."removed@market"]', result.text)
        self.assertIn('[plugins."removed@market-extra"]', result.text)
        self.assertNotIn("[[unknown.items]]", result.text)
        self.assertIn(
            "unknown_array_table",
            {diagnostic.code for diagnostic in result.diagnostics},
        )

    def test_shared_overlay_replaces_complete_multiline_values(self) -> None:
        current = (
            'model = "internal-model"\n'
            "\n"
            "[desktop]\n"
            "queue = [\n"
            '  "old-a",\n'
            '  "old-b",\n'
            "] # keep target comment\n"
            'mode = "keep"\n'
        )
        overlay = (
            'model = "must-not-overlay-profile-state"\n'
            "\n"
            "[desktop]\n"
            "queue = [\n"
            '  "new",\n'
            "]\n"
        )

        merged = merge_shared_config_overlay(current, overlay)

        self.assertIn('model = "internal-model"', merged)
        self.assertNotIn("must-not-overlay-profile-state", merged)
        self.assertIn('  "new",', merged)
        self.assertNotIn("old-a", merged)
        self.assertNotIn("old-b", merged)
        self.assertIn("] # keep target comment", merged)
        self.assertIn('mode = "keep"', merged)

    def test_missing_defaults_restore_complete_multiline_assignment(self) -> None:
        current = "[desktop]\nexisting = true\n"
        defaults = (
            "[desktop]\n"
            "queue = [\n"
            '  "one",\n'
            '  "two",\n'
            "]\n"
        )

        merged = merge_missing_shared_config_defaults(current, defaults)

        self.assertIn("existing = true", merged)
        self.assertIn('  "one",', merged)
        self.assertIn('  "two",', merged)
        config_document_module().ConfigDocument.parse(merged, "merged defaults")

    def test_missing_defaults_use_skill_identity_instead_of_block_bytes(self) -> None:
        current = (
            "[[skills.config]]\n"
            'path = "/skills/current/SKILL.md"\n'
            "enabled = false\n"
        )
        defaults = (
            "[[skills.config]]\n"
            'path = "/skills/current/SKILL.md"\n'
            "enabled = true\n"
            "\n"
            "[[skills.config]]\n"
            'path = "/skills/missing/SKILL.md"\n'
            "enabled = true\n"
        )

        merged = merge_missing_shared_config_defaults(current, defaults)

        self.assertEqual(
            1,
            merged.count('path = "/skills/current/SKILL.md"'),
        )
        self.assertIn(
            'path = "/skills/current/SKILL.md"\nenabled = false',
            merged,
        )
        self.assertEqual(
            1,
            merged.count('path = "/skills/missing/SKILL.md"'),
        )

    def test_non_usage_defaults_never_restore_plugin_or_skill_usage(self) -> None:
        defaults = (
            "[marketplaces.team]\n"
            'source = "team/repo"\n'
            "\n"
            '[plugins."removed@team"]\n'
            "enabled = true\n"
            "\n"
            "[[skills.config]]\n"
            'path = "/skills/removed/SKILL.md"\n'
            "\n"
            '[hooks.state."removed@team:hooks.json:stop:0:0"]\n'
            "enabled = true\n"
        )

        merged = merge_missing_non_usage_shared_config_defaults("", defaults)

        self.assertIn("[marketplaces.team]", merged)
        self.assertIn('[hooks.state."removed@team:hooks.json:stop:0:0"]', merged)
        self.assertNotIn('[plugins."removed@team"]', merged)
        self.assertNotIn("[[skills.config]]", merged)

    def test_exact_usage_replacement_fails_closed_on_ambiguous_skill_identity(
        self,
    ) -> None:
        authoritative = (
            "[[skills.config]]\n"
            'path = "/skills/duplicate/SKILL.md"\n'
            "\n"
            "[[skills.config]]\n"
            'path = "/skills/duplicate/SKILL.md"\n'
        )

        with self.assertRaisesRegex(
            SwitchError,
            "skills_config_duplicate_identity",
        ):
            replace_plugin_skill_usage_state(
                '[plugins."existing@team"]\nenabled = true\n',
                authoritative,
                "ambiguous authoritative usage",
            )

    def test_shell_wrapper_selects_available_python_with_tomllib(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            old_python = bin_dir / "python3"
            old_python.write_text("#!/bin/sh\nexit 1\n")
            old_python.chmod(0o755)
            modern_python = bin_dir / "python3.12"
            modern_python.write_text(
                "#!/bin/sh\n"
                f"exec {shlex.quote(sys.executable)} \"$@\"\n"
            )
            modern_python.chmod(0o755)
            switch_script = root / "selected_python.py"
            switch_script.write_text(
                "import sys\n"
                "print(f'selected:{sys.version_info.major}.{sys.version_info.minor}')\n"
            )
            env = os.environ.copy()
            env["PATH"] = f"{bin_dir}:/usr/bin:/bin"
            env["CODEX_SWITCH_SCRIPT"] = str(switch_script)
            env["CODEX_SWITCH_SKIP_SELF_UPDATE"] = "1"
            env.pop("CODEX_SWITCH_PYTHON", None)

            result = subprocess.run(
                [str(WRAPPER), "raw", "probe"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )

        self.assertEqual(0, result.returncode, result.stderr)
        self.assertIn(
            f"selected:{sys.version_info.major}.{sys.version_info.minor}",
            result.stdout,
        )

    def test_shell_wrapper_rejects_explicit_old_python_before_switch_script(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            marker = root / "switch-script-ran"
            old_python = root / "python3-old"
            old_python.write_text(
                "#!/bin/sh\n"
                'if [ "${1:-}" = "-c" ]; then exit 1; fi\n'
                f"touch {shlex.quote(str(marker))}\n"
            )
            old_python.chmod(0o755)
            switch_script = root / "must_not_run.py"
            switch_script.write_text(
                f"from pathlib import Path\nPath({str(marker)!r}).touch()\n"
            )
            env = os.environ.copy()
            env["CODEX_SWITCH_PYTHON"] = str(old_python)
            env["CODEX_SWITCH_SCRIPT"] = str(switch_script)
            env["CODEX_SWITCH_SKIP_SELF_UPDATE"] = "1"

            result = subprocess.run(
                [str(WRAPPER), "raw", "probe"],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env,
            )
            marker_exists = marker.exists()

        self.assertNotEqual(0, result.returncode)
        self.assertFalse(marker_exists)
        self.assertIn("Python 3.11+", result.stderr)

    def test_direct_profile_switch_rejects_old_python_before_store_write(
        self,
    ) -> None:
        old_python = Path("/usr/bin/python3")
        version = subprocess.run(
            [
                str(old_python),
                "-c",
                "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')",
            ],
            check=True,
            text=True,
            stdout=subprocess.PIPE,
        ).stdout.strip()
        if tuple(int(part) for part in version.split(".")) >= (3, 11):
            self.skipTest("/usr/bin/python3 already provides tomllib")

        with tempfile.TemporaryDirectory() as temp:
            store = Path(temp) / "store"
            result = subprocess.run(
                [
                    str(old_python),
                    str(PROFILE_SWITCH),
                    "--store-dir",
                    str(store),
                    "init",
                ],
                check=False,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            store_exists = store.exists()

        self.assertEqual(2, result.returncode)
        self.assertFalse(store_exists)
        self.assertIn("Python 3.11+", result.stderr)


if __name__ == "__main__":
    unittest.main()
