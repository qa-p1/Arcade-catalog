from __future__ import annotations

import copy
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from typing import Any, Callable


REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO / "scripts"))

from build_index import build_index, write_index  # noqa: E402
from validate import parse_key_sequence, validate_repository  # noqa: E402


FIXTURES = REPO / "tests" / "fixtures"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def sample_catalog() -> dict[str, Any]:
    return {
        "schema": 1,
        "updated": "2026-10-11",
        "apps": [
            {
                "id": "arcade.alpha",
                "name": "Arcade Alpha",
                "repo": "qa-p1/Arcade-Alpha",
                "pitch": "Search and preview files",
                "description": "Find a file by name or metadata. Open a quick preview when you need more detail.",
                "category": "files",
                "icon": "icons/arcade.alpha.svg",
                "screenshots": [],
                "platforms": {"linux": "ci", "windows": "ci", "macos": "ci"},
                "linkProtocol": [1],
                "minTools": "0.2.0",
                "docs": "README.md",
                "resident": False,
                "homepage": "https://github.com/qa-p1/Arcade-Alpha",
            }
        ],
        "tools": {
            "id": "arcade.tools",
            "name": "Arcade Tools",
            "repo": "qa-p1/Arcade-tools",
            "minTools": "0.2.0",
            "icon": "icons/arcade.tools.svg",
        },
        "bundles": [
            {
                "id": "starter",
                "title": "Starter",
                "description": "A small starter bundle.",
                "apps": ["arcade.alpha"],
            }
        ],
    }


def sample_engines() -> dict[str, Any]:
    return {
        "schema": 1,
        "engines": [
            {
                "id": "ripgrep",
                "name": "ripgrep",
                "homepage": "https://github.com/BurntSushi/ripgrep",
                "detect": {"binaries": ["rg"], "versionArgs": ["--version"]},
                "usedBy": [{"app": "arcade.alpha", "for": "Search inside files."}],
                "install": {"debian": "sudo apt install ripgrep"},
                "linkDownload": False,
            }
        ],
    }


def sample_sheet() -> dict[str, Any]:
    return {
        "schema": 1,
        "id": "sample",
        "name": "Sample App",
        "checkedVersion": "1.2",
        "sources": ["https://example.org/keyboard-shortcuts"],
        "match": {"linux": {"class": ["sample-app"]}},
        "groups": [
            {
                "title": "General",
                "context": "app",
                "shortcuts": [
                    {"id": "open", "title": "Open", "keys": {"default": "Ctrl+K"}}
                ],
            }
        ],
    }


class ValidatorTests(unittest.TestCase):
    def test_published_repository_names_match_github(self) -> None:
        catalog = json.loads((REPO / "catalog.json").read_text(encoding="utf-8"))
        expected = {
            "arcade.find": "Arcade-Find", "arcade.look": "Arcade-look",
            "arcade.lens": "Arcade-lens", "arcade.box": "Arcade-box",
            "arcade.clipboard": "Arcade-clipboard", "arcade.shelf": "Arcade-Shelf",
            "arcade.wheel": "Arcade-wheel", "arcade.tools": "Arcade-tools",
        }
        for app in catalog["apps"] + [catalog["tools"]]:
            with self.subTest(app=app["id"]):
                self.assertEqual(app["repo"], "qa-p1/" + expected[app["id"]])

    def new_root(self) -> Path:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        (root / "icons").mkdir()
        (root / "icons" / "arcade.alpha.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n')
        (root / "icons" / "arcade.tools.svg").write_text('<svg xmlns="http://www.w3.org/2000/svg"/>\n')
        write_json(root / "catalog.json", sample_catalog())
        write_json(root / "engines.json", sample_engines())
        write_index(root)
        return root

    def errors_for(self, root: Path) -> list[str]:
        errors, _warnings = validate_repository(root)
        return errors

    def assert_error(self, root: Path, fragment: str) -> None:
        errors = self.errors_for(root)
        self.assertTrue(any(fragment in error for error in errors), f"expected {fragment!r} in errors:\n" + "\n".join(errors))

    def test_minimal_repository_is_valid(self) -> None:
        self.assertEqual(self.errors_for(self.new_root()), [])

    def test_every_json_file_is_parsed_and_parse_errors_name_the_file(self) -> None:
        root = self.new_root()
        (root / "extra.json").write_text('{"unfinished":', encoding="utf-8")
        self.assert_error(root, "extra.json:$: invalid JSON")

    def test_duplicate_object_keys_are_rejected(self) -> None:
        root = self.new_root()
        (root / "catalog.json").write_text('{"schema":1,"schema":1}', encoding="utf-8")
        self.assert_error(root, "catalog.json:$: invalid JSON: duplicate object key 'schema'")

    def test_unknown_top_level_fields_warn_without_failing(self) -> None:
        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["futureField"] = {"kept": True}
        write_json(root / "catalog.json", catalog)
        errors, warnings = validate_repository(root)
        self.assertEqual(errors, [])
        self.assertTrue(any("catalog.json:/futureField" in warning for warning in warnings))

    def test_catalog_schema_date_required_fields_and_types(self) -> None:
        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["schema"] = True
        catalog["updated"] = "2026-02-31"
        catalog["apps"] = "not-an-array"
        write_json(root / "catalog.json", catalog)
        errors = self.errors_for(root)
        self.assertTrue(any("/schema" in error and "integer 1" in error for error in errors))
        self.assertTrue(any("/updated" in error for error in errors))
        self.assertTrue(any("/apps" in error and "expected an array" in error for error in errors))

        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        del catalog["bundles"]
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "catalog.json:$/bundles: missing required field")

    def test_app_owner_ids_pitch_description_category_and_platforms(self) -> None:
        cases: list[tuple[str, Callable[[dict[str, Any]], None], str]] = [
            ("owner", lambda app: app.update(repo="other/Arcade-Alpha"), "/apps/0/repo"),
            ("id", lambda app: app.update(id="alpha"), "/apps/0/id"),
            ("pitch", lambda app: app.update(pitch="x" * 61), "/apps/0/pitch"),
            ("description-short", lambda app: app.update(description="Only one sentence."), "/apps/0/description"),
            ("description-long", lambda app: app.update(description="One. Two. Three. Four."), "/apps/0/description"),
            ("category", lambda app: app.update(category="games"), "/apps/0/category"),
            ("platform-value", lambda app: app["platforms"].update(linux="sometimes"), "/apps/0/platforms/linux"),
            ("platform-key", lambda app: app["platforms"].update(android="ci"), "/apps/0/platforms/android"),
            ("protocol", lambda app: app.update(linkProtocol=[2]), "/apps/0/linkProtocol"),
            ("semver", lambda app: app.update(minTools="0.2"), "/apps/0/minTools"),
            ("resident-type", lambda app: app.update(resident="yes"), "/apps/0/resident"),
        ]
        for label, mutate, expected in cases:
            with self.subTest(label=label):
                root = self.new_root()
                catalog = json.loads((root / "catalog.json").read_text())
                mutate(catalog["apps"][0])
                write_json(root / "catalog.json", catalog)
                self.assert_error(root, expected)

    def test_duplicate_and_unsorted_app_ids_are_rejected(self) -> None:
        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["tools"]["id"] = "arcade.alpha"
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "duplicate id")

        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        second = copy.deepcopy(catalog["apps"][0])
        second.update(id="arcade.beta", name="Arcade Beta", repo="qa-p1/Arcade-Beta", icon="icons/arcade.alpha.svg")
        catalog["apps"].insert(0, second)
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "/apps: apps must be sorted alphabetically")

    def test_tools_owner_and_semver_are_checked(self) -> None:
        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["tools"]["repo"] = "someone/Arcade-tools"
        catalog["tools"]["minTools"] = "1.2"
        write_json(root / "catalog.json", catalog)
        errors = self.errors_for(root)
        self.assertTrue(any("/tools/repo" in error for error in errors))
        self.assertTrue(any("/tools/minTools" in error for error in errors))

    def test_icon_files_and_github_urls_are_checked(self) -> None:
        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["apps"][0]["icon"] = "icons/missing.svg"
        catalog["apps"][0]["screenshots"] = ["http://example.org/image.png"]
        catalog["apps"][0]["homepage"] = "https://example.org/project"
        write_json(root / "catalog.json", catalog)
        errors = self.errors_for(root)
        self.assertTrue(any("/apps/0/icon" in error and "does not exist" in error for error in errors))
        self.assertTrue(any("/apps/0/screenshots/0" in error for error in errors))
        self.assertTrue(any("/apps/0/homepage" in error for error in errors))

        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["tools"]["icon"] = "../outside.svg"
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "/tools/icon: icon must be an SVG or PNG path inside icons/")

    def test_png_icons_must_be_256_square(self) -> None:
        root = self.new_root()
        icon = REPO / "icons" / "arcade.lens.png"
        png = bytearray(icon.read_bytes())
        png[16:20] = (128).to_bytes(4, "big")
        png[20:24] = (128).to_bytes(4, "big")
        (root / "icons" / "arcade.test.png").write_bytes(png)
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["apps"][0]["icon"] = "icons/arcade.test.png"
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "PNG icon must be 256x256 pixels (found 128x128)")

    def test_bundle_ids_references_and_wildcard(self) -> None:
        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["bundles"][0]["apps"] = ["arcade.missing"]
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "unknown app id 'arcade.missing'")

        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["bundles"][0]["apps"] = "*"
        write_json(root / "catalog.json", catalog)
        self.assertEqual(self.errors_for(root), [])

        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["bundles"].append(copy.deepcopy(catalog["bundles"][0]))
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "duplicate bundle id")

        root = self.new_root()
        catalog = json.loads((root / "catalog.json").read_text())
        catalog["bundles"][0]["id"] = "Bad Bundle"
        write_json(root / "catalog.json", catalog)
        self.assert_error(root, "bundle id must be kebab-case")

    def test_engine_required_fields_types_ids_and_app_references(self) -> None:
        root = self.new_root()
        engines = json.loads((root / "engines.json").read_text())
        engines["schema"] = 2
        engines["engines"][0]["usedBy"][0]["app"] = "arcade.missing"
        engines["engines"][0]["detect"]["binaries"] = []
        engines["engines"][0]["install"] = {"unknown": "install this"}
        write_json(root / "engines.json", engines)
        errors = self.errors_for(root)
        self.assertTrue(any("engines.json:/schema" in error for error in errors))
        self.assertTrue(any("unknown catalog app" in error for error in errors))
        self.assertTrue(any("/detect/binaries" in error for error in errors))
        self.assertTrue(any("unknown package manager" in error for error in errors))

        root = self.new_root()
        engines = json.loads((root / "engines.json").read_text())
        engines["engines"].append(copy.deepcopy(engines["engines"][0]))
        write_json(root / "engines.json", engines)
        self.assert_error(root, "duplicate engine id")

        root = self.new_root()
        engines = json.loads((root / "engines.json").read_text())
        engines["engines"][0]["homepage"] = "http://example.org"
        engines["engines"][0]["detect"]["minVersion"] = "1.0"
        write_json(root / "engines.json", engines)
        errors = self.errors_for(root)
        self.assertTrue(any("/homepage" in error for error in errors))
        self.assertTrue(any("/detect/minVersion" in error for error in errors))

        root = self.new_root()
        engines = json.loads((root / "engines.json").read_text())
        del engines["engines"][0]["detect"]
        write_json(root / "engines.json", engines)
        self.assert_error(root, "/detect: missing required field")

    def test_only_tesseract_can_have_link_download(self) -> None:
        root = self.new_root()
        engines = json.loads((root / "engines.json").read_text())
        engines["engines"][0]["linkDownload"] = True
        write_json(root / "engines.json", engines)
        self.assert_error(root, "only the Tesseract engine may be downloaded")

    def put_sheet(self, root: Path, sheet: dict[str, Any], filename: str = "sample.json") -> None:
        write_json(root / "shortcuts" / filename, sheet)
        write_index(root)

    def test_sample_sheet_pipeline_build_index_then_validate(self) -> None:
        root = self.new_root()
        sample = json.loads((FIXTURES / "shortcut-sheet.json").read_text(encoding="utf-8"))
        write_json(root / "shortcuts" / "sample.json", sample)

        built = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "build_index.py"), "--root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(built.returncode, 0, built.stdout + built.stderr)
        self.assertEqual(build_index(root)["sheets"][0]["id"], "sample")

        checked = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "validate.py"), "--root", str(root)],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.assertIn("Validation passed", checked.stdout)

    def test_sheet_id_filename_sources_and_match_rules(self) -> None:
        root = self.new_root()
        self.put_sheet(root, sample_sheet(), "wrong-name.json")
        self.assert_error(root, "/id: sheet id must match the file name")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["id"] = "Bad_Name"
        self.put_sheet(root, sheet, "Bad_Name.json")
        self.assert_error(root, "/id: sheet id must be lowercase kebab-case")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["sources"] = ["http://example.org/source"]
        sheet["match"] = {}
        self.put_sheet(root, sheet)
        errors = self.errors_for(root)
        self.assertTrue(any("/sources/0" in error for error in errors))
        self.assertTrue(any("/match" in error and "at least one" in error for error in errors))

        root = self.new_root()
        sheet = sample_sheet()
        sheet["match"] = {"linux": {"class": []}}
        self.put_sheet(root, sheet)
        self.assert_error(root, "/match/linux/class: array must not be empty")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["sources"] = []
        self.put_sheet(root, sheet)
        self.assert_error(root, "/sources: expected a non-empty array")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["schema"] = 2
        self.put_sheet(root, sheet)
        self.assert_error(root, "shortcuts/sample.json:/schema: schema must be the integer 1")

    def test_sheet_required_groups_context_titles_and_unique_ids(self) -> None:
        root = self.new_root()
        sheet = sample_sheet()
        del sheet["checkedVersion"]
        self.put_sheet(root, sheet)
        self.assert_error(root, "shortcuts/sample.json:$/checkedVersion: missing required field")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["context"] = "Bad Context"
        sheet["groups"][0]["shortcuts"][0]["title"] = "x" * 81
        sheet["groups"].append(copy.deepcopy(sheet["groups"][0]))
        self.put_sheet(root, sheet)
        errors = self.errors_for(root)
        self.assertTrue(any("context must be lowercase kebab-case" in error for error in errors))
        self.assertTrue(any("at most 80 characters" in error for error in errors))
        self.assertTrue(any("duplicate shortcut id" in error for error in errors))

        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["shortcuts"] = []
        self.put_sheet(root, sheet)
        self.assert_error(root, "/groups/0/shortcuts: expected a non-empty array")

    def test_pinned_key_notation_accepts_edge_cases(self) -> None:
        valid = [
            "Ctrl+Shift+P",
            "Super+Slash",
            "Ctrl+Alt+Shift+L",
            "Ctrl+K Ctrl+S",
            "Super",
            "Ctrl+Shift+Equal",
            "F24",
            "Numpad9",
            "MouseLeft",
            "WheelDown",
            "MicMute",
            "WheelLeft",
            "WheelRight",
            "Code123",
        ]
        for value in valid:
            with self.subTest(value=value):
                self.assertIsNotNone(parse_key_sequence(value))

        bad = json.loads((FIXTURES / "bad-key-sequences.json").read_text(encoding="utf-8"))
        for label, values in bad.items():
            for value in values:
                with self.subTest(rule=label, value=value):
                    self.assertIsNone(parse_key_sequence(value))

    def test_schema_key_pattern_matches_validator_notation(self) -> None:
        schema = json.loads((REPO / "schema" / "shortcut-sheet.schema.json").read_text(encoding="utf-8"))
        pattern = next(
            branch["pattern"]
            for branch in schema["$defs"]["binding"]["oneOf"]
            if branch.get("type") == "string"
        )
        notation = re.compile(pattern)
        for value in (
            "Ctrl+Shift+P", "Super+Slash", "Ctrl+K Ctrl+S", "Super", "Code42", "F24",
            "MicMute", "WheelLeft", "WheelRight",
        ):
            with self.subTest(valid=value):
                self.assertIsNotNone(parse_key_sequence(value))
                self.assertIsNotNone(notation.fullmatch(value))
        for value in ("Alt+Ctrl+P", "Ctrl+t", "Ctrl++", "Cmd+T", "F25"):
            with self.subTest(invalid=value):
                self.assertIsNone(parse_key_sequence(value))
                self.assertIsNone(notation.fullmatch(value))

    def test_bad_key_notation_and_all_null_bindings_are_rejected(self) -> None:
        for value in ("Alt+Ctrl+P", "Ctrl+t", "Ctrl++", "Cmd+T"):
            with self.subTest(value=value):
                root = self.new_root()
                sheet = sample_sheet()
                sheet["groups"][0]["shortcuts"][0]["keys"]["default"] = value
                self.put_sheet(root, sheet)
                self.assert_error(root, "invalid key sequence")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["shortcuts"][0]["keys"] = {"default": None, "linux": None}
        self.put_sheet(root, sheet)
        self.assert_error(root, "at least one binding must be non-null")

    def test_new_canonical_key_names_validate_in_a_sheet(self) -> None:
        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["shortcuts"][0]["keys"]["default"] = [
            "MicMute", "WheelLeft", "WheelRight"
        ]
        self.put_sheet(root, sheet)
        self.assertEqual(self.errors_for(root), [])

    def test_equal_alternative_and_prefix_conflicts_are_reported_by_context_and_os(self) -> None:
        for second in ("Ctrl+K", "Ctrl+K Ctrl+S"):
            with self.subTest(second=second):
                root = self.new_root()
                sheet = sample_sheet()
                sheet["groups"][0]["shortcuts"].append(
                    {"id": "settings", "title": "Settings", "keys": {"default": second}}
                )
                self.put_sheet(root, sheet)
                self.assert_error(root, "binding conflicts with shortcut 'open'")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["shortcuts"][0]["keys"]["default"] = ["F5", "Ctrl+R"]
        sheet["groups"][0]["shortcuts"].append(
            {"id": "reload", "title": "Reload", "keys": {"default": "Ctrl+R"}}
        )
        self.put_sheet(root, sheet)
        self.assert_error(root, "binding conflicts with shortcut 'open'")

    def test_equal_and_prefix_alternatives_within_one_shortcut_are_rejected(self) -> None:
        for alternatives in (
            ["Ctrl+K", "Ctrl+K"],
            ["Ctrl+K", "Ctrl+K Ctrl+S"],
        ):
            with self.subTest(alternatives=alternatives):
                root = self.new_root()
                sheet = sample_sheet()
                sheet["groups"][0]["shortcuts"][0]["keys"]["default"] = alternatives
                self.put_sheet(root, sheet)
                self.assert_error(root, "alternative bindings conflict with each other")

    def test_os_overrides_and_contexts_are_applied_before_conflict_checks(self) -> None:
        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["shortcuts"][0]["keys"] = {"default": "Ctrl+T", "linux": None}
        sheet["groups"][0]["shortcuts"].append(
            {"id": "other", "title": "Other", "keys": {"default": "Ctrl+T", "linux": "Ctrl+N"}}
        )
        self.put_sheet(root, sheet)
        errors = self.errors_for(root)
        self.assertTrue(any("on windows" in error for error in errors), "Windows should inherit both defaults")
        self.assertFalse(any("on linux" in error for error in errors), "Linux null override should disable the first binding")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["shortcuts"].append(
            {"id": "other", "title": "Other", "keys": {"default": "Ctrl+K"}}
        )
        sheet["groups"].append(
            {
                "title": "Editor",
                "context": "editor",
                "shortcuts": [{"id": "editor-open", "title": "Open", "keys": {"default": "Ctrl+K"}}],
            }
        )
        self.put_sheet(root, sheet)
        errors = self.errors_for(root)
        self.assertTrue(any("on linux" in error for error in errors))
        self.assertFalse(any("editor-open" in error for error in errors))

    def test_rebindable_is_forbidden_anywhere_in_a_sheet(self) -> None:
        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["shortcuts"][0]["rebindable"] = True
        self.put_sheet(root, sheet)
        self.assert_error(root, "rebindable is not allowed in shortcut sheets")

    def test_global_context_is_only_for_system_sheets(self) -> None:
        root = self.new_root()
        sheet = sample_sheet()
        sheet["groups"][0]["context"] = "global"
        self.put_sheet(root, sheet)
        self.assert_error(root, 'context "global" is only for system sheets')

    def test_stale_index_is_rejected_and_unknown_fields_warn(self) -> None:
        root = self.new_root()
        sheet = json.loads((FIXTURES / "shortcut-sheet.json").read_text(encoding="utf-8"))
        write_json(root / "shortcuts" / "sample.json", sheet)
        self.assert_error(root, "shortcuts/index.json:/sheets: index is stale")

        root = self.new_root()
        sheet = sample_sheet()
        sheet["future"] = "allowed"
        self.put_sheet(root, sheet)
        errors, warnings = validate_repository(root)
        self.assertEqual(errors, [])
        self.assertTrue(any("shortcuts/sample.json:/future" in warning for warning in warnings))

        root = self.new_root()
        write_json(root / "shortcuts" / "index.json", {"schema": 1})
        self.assert_error(root, "shortcuts/index.json:$/sheets: missing required field")

        root = self.new_root()
        write_json(root / "shortcuts" / "index.json", {"schema": 2, "sheets": []})
        self.assert_error(root, "shortcuts/index.json:/schema: schema must be the integer 1")

    def test_catalog_and_fixture_top_level_required_keys_match_schema(self) -> None:
        data_schemas = (
            (REPO / "catalog.json", REPO / "schema" / "catalog.schema.json"),
            (REPO / "engines.json", REPO / "schema" / "engines.schema.json"),
            (REPO / "shortcuts" / "index.json", REPO / "schema" / "shortcuts-index.schema.json"),
            (FIXTURES / "shortcut-sheet.json", REPO / "schema" / "shortcut-sheet.schema.json"),
        )
        for data_path, schema_path in data_schemas:
            with self.subTest(data=data_path.name):
                data = json.loads(data_path.read_text(encoding="utf-8"))
                schema = json.loads(schema_path.read_text(encoding="utf-8"))
                self.assertEqual(set(data), set(schema["required"]))


if __name__ == "__main__":
    unittest.main()
