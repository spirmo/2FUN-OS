import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from argparse import Namespace
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "project_manager.py"

SPEC = importlib.util.spec_from_file_location(
    "project_manager_under_test", MODULE_PATH
)
project_manager = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(project_manager)


class ProjectManagerSelectionTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.control = self.root / "project_control"
        self.subprojects_dir = self.control / "subprojects"
        self.subprojects_dir.mkdir(parents=True)

        self.parent_file = self.control / "parent_project.json"
        self.registry_file = self.control / "registry.json"
        self.active_file = self.control / "active_subproject.json"
        self.global_history_file = self.control / "global_history.jsonl"

        self.parent_file.write_text(
            json.dumps({"project_id": "2FUN"}),
            encoding="utf-8",
        )

        self.registry = {
            "parent_project_id": "2FUN",
            "subprojects": [
                {"id": "2FUNC", "status": "ACTIVE"},
                {"id": "UVI", "status": "ACTIVE"},
                {"id": "DRAFT_PART", "status": "DRAFT"},
            ],
        }
        self.registry_file.write_text(
            json.dumps(self.registry),
            encoding="utf-8",
        )

        self.active = {
            "parent_project_id": "2FUN",
            "active_subproject_id": "2FUNC",
        }
        self.active_file.write_text(
            json.dumps(self.active),
            encoding="utf-8",
        )

        for subproject_id in ("2FUNC", "UVI"):
            self.create_subproject(subproject_id)

        self.patches = [
            patch.object(project_manager, "ROOT", self.root),
            patch.object(project_manager, "CONTROL", self.control),
            patch.object(project_manager, "PARENT_FILE", self.parent_file),
            patch.object(project_manager, "REGISTRY_FILE", self.registry_file),
            patch.object(project_manager, "ACTIVE_FILE", self.active_file),
            patch.object(
                project_manager, "GLOBAL_HISTORY_FILE",
                self.global_history_file,
            ),
            patch.object(
                project_manager, "SUBPROJECTS_DIR", self.subprojects_dir
            ),
        ]
        for item in self.patches:
            item.start()

    def tearDown(self):
        for item in reversed(self.patches):
            item.stop()
        self.temp_dir.cleanup()

    def create_subproject(self, subproject_id):
        directory = self.subprojects_dir / subproject_id
        directory.mkdir(parents=True)

        paths = {}
        for key in (
            "workflow_engine",
            "mission_catalog",
            "mission_document",
            "workflow_state",
            "workflow_history",
        ):
            filename = f"{key}.txt"
            (directory / filename).write_text(
                "temporary test data\n",
                encoding="utf-8",
            )
            paths[key] = str(
                Path("project_control")
                / "subprojects"
                / subproject_id
                / filename
            )

        metadata = {
            "parent_project_id": "2FUN",
            "subproject_id": subproject_id,
            "status": "ACTIVE",
            **paths,
        }
        (directory / "subproject.json").write_text(
            json.dumps(metadata),
            encoding="utf-8",
        )

    def read_active_id(self):
        return json.loads(
            self.active_file.read_text(encoding="utf-8")
        )["active_subproject_id"]

    def test_select_changes_active_and_reports_previous_id(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = project_manager.command_select_subproject(
                Namespace(id="UVI")
            )

        self.assertEqual(result, 0)
        self.assertEqual(self.read_active_id(), "UVI")
        self.assertIn("ACTIVE SUBPROJECT: UVI", output.getvalue())
        self.assertIn("PREVIOUS SUBPROJECT: 2FUNC", output.getvalue())

    def test_selecting_current_subproject_does_not_rewrite_file(self):
        with patch.object(
            project_manager,
            "write_json_atomic",
            wraps=project_manager.write_json_atomic,
        ) as writer:
            result = project_manager.command_select_subproject(
                Namespace(id="2FUNC")
            )

        self.assertEqual(result, 0)
        self.assertEqual(self.read_active_id(), "2FUNC")
        writer.assert_not_called()

    def test_draft_subproject_is_rejected_without_changing_active(self):
        with self.assertRaises(project_manager.ManagerError):
            project_manager.command_select_subproject(
                Namespace(id="DRAFT_PART")
            )

        self.assertEqual(self.read_active_id(), "2FUNC")


    def test_add_subproject_creates_draft_without_changing_active(self):
        output = io.StringIO()

        with contextlib.redirect_stdout(output):
            result = project_manager.command_add_subproject(
                Namespace(
                    id="NEW_PART",
                    name="New Part",
                    description="Temporary test subproject",
                )
            )

        directory = self.subprojects_dir / "NEW_PART"
        metadata = json.loads(
            (directory / "subproject.json").read_text(encoding="utf-8")
        )
        registry = json.loads(
            self.registry_file.read_text(encoding="utf-8")
        )

        self.assertEqual(result, 0)
        self.assertTrue((directory / "evidence").is_dir())
        self.assertTrue((directory / "context").is_dir())
        self.assertEqual(metadata["status"], "DRAFT")
        self.assertEqual(metadata["name"], "New Part")
        self.assertIsNone(metadata["mission_catalog"])
        self.assertTrue(
            (directory / "subproject.json").read_bytes().endswith(b"\n")
        )
        self.assertIn(
            {"id": "NEW_PART", "name": "New Part", "status": "DRAFT"},
            registry["subprojects"],
        )
        self.assertEqual(self.read_active_id(), "2FUNC")
        self.assertIn("MISSION: NOT CREATED", output.getvalue())

    def test_add_duplicate_subproject_preserves_existing_data(self):
        original_registry = self.registry_file.read_bytes()
        existing_metadata = (
            self.subprojects_dir / "2FUNC" / "subproject.json"
        ).read_bytes()

        with self.assertRaises(project_manager.ManagerError):
            project_manager.command_add_subproject(
                Namespace(
                    id="2FUNC",
                    name="Duplicate",
                    description="Must not overwrite",
                )
            )

        self.assertEqual(self.registry_file.read_bytes(), original_registry)
        self.assertEqual(
            (self.subprojects_dir / "2FUNC" / "subproject.json").read_bytes(),
            existing_metadata,
        )
        self.assertEqual(self.read_active_id(), "2FUNC")

    def test_add_subproject_rolls_back_directory_if_registry_write_fails(self):
        original_registry = self.registry_file.read_bytes()
        directory = self.subprojects_dir / "NEW_PART"

        with patch.object(
            project_manager,
            "write_json_atomic",
            side_effect=OSError("simulated registry write failure"),
        ):
            with self.assertRaisesRegex(
                OSError, "simulated registry write failure"
            ):
                project_manager.command_add_subproject(
                    Namespace(
                        id="NEW_PART",
                        name="New Part",
                        description="Rollback test",
                    )
                )

        self.assertFalse(directory.exists())
        self.assertEqual(self.registry_file.read_bytes(), original_registry)
        self.assertEqual(self.read_active_id(), "2FUNC")


    def read_registry(self):
        return json.loads(self.registry_file.read_text(encoding="utf-8"))

    def read_metadata(self, subproject_id):
        path = self.subprojects_dir / subproject_id / "subproject.json"
        return json.loads(path.read_text(encoding="utf-8"))

    def set_status(self, subproject_id, status):
        registry = self.read_registry()
        entry = next(
            item for item in registry["subprojects"]
            if item["id"] == subproject_id
        )
        entry["status"] = status
        self.registry_file.write_text(json.dumps(registry), encoding="utf-8")

        metadata_path = (
            self.subprojects_dir / subproject_id / "subproject.json"
        )
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        metadata["status"] = status
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")

    def test_pause_rejects_selected_subproject(self):
        registry_before = self.registry_file.read_bytes()
        metadata_path = (
            self.subprojects_dir / "2FUNC" / "subproject.json"
        )
        metadata_before = metadata_path.read_bytes()

        with self.assertRaisesRegex(
            project_manager.ManagerError, "selected subproject"
        ):
            project_manager.command_pause_subproject(Namespace(id="2FUNC"))

        self.assertEqual(self.registry_file.read_bytes(), registry_before)
        self.assertEqual(metadata_path.read_bytes(), metadata_before)
        self.assertFalse(project_manager.GLOBAL_HISTORY_FILE.exists())
        self.assertEqual(self.read_active_id(), "2FUNC")

    def test_pause_non_selected_subproject_records_history(self):
        project_manager.command_select_subproject(Namespace(id="UVI"))

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = project_manager.command_pause_subproject(
                Namespace(id="2FUNC")
            )

        self.assertEqual(result, 0)
        self.assertEqual(
            next(
                item["status"]
                for item in self.read_registry()["subprojects"]
                if item["id"] == "2FUNC"
            ),
            "PAUSED",
        )
        self.assertEqual(self.read_metadata("2FUNC")["status"], "PAUSED")
        self.assertEqual(self.read_active_id(), "UVI")

        history = project_manager.GLOBAL_HISTORY_FILE.read_text(
            encoding="utf-8"
        ).splitlines()
        self.assertEqual(len(history), 1)
        event = json.loads(history[0])
        self.assertEqual(event["event"], "SUBPROJECT_PAUSED")
        self.assertEqual(event["subproject_id"], "2FUNC")
        self.assertEqual(event["selected_subproject_id"], "UVI")
        self.assertIn("GLOBAL HISTORY: APPENDED", output.getvalue())

    def test_resume_does_not_change_selected_subproject(self):
        project_manager.command_select_subproject(Namespace(id="UVI"))
        self.set_status("2FUNC", "PAUSED")

        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = project_manager.command_resume_subproject(
                Namespace(id="2FUNC")
            )

        self.assertEqual(result, 0)
        self.assertEqual(
            next(
                item["status"]
                for item in self.read_registry()["subprojects"]
                if item["id"] == "2FUNC"
            ),
            "ACTIVE",
        )
        self.assertEqual(self.read_metadata("2FUNC")["status"], "ACTIVE")
        self.assertEqual(self.read_active_id(), "UVI")

        event = json.loads(
            project_manager.GLOBAL_HISTORY_FILE.read_text(
                encoding="utf-8"
            ).splitlines()[0]
        )
        self.assertEqual(event["event"], "SUBPROJECT_RESUMED")
        self.assertEqual(event["subproject_id"], "2FUNC")
        self.assertEqual(event["selected_subproject_id"], "UVI")
        self.assertIn("SELECTED SUBPROJECT: UNCHANGED", output.getvalue())

    def test_pause_rolls_back_all_files_if_history_write_fails(self):
        project_manager.command_select_subproject(Namespace(id="UVI"))

        registry_before = self.registry_file.read_bytes()
        metadata_path = (
            self.subprojects_dir / "2FUNC" / "subproject.json"
        )
        metadata_before = metadata_path.read_bytes()
        history_path = project_manager.GLOBAL_HISTORY_FILE

        with patch.object(
            project_manager,
            "append_global_history",
            side_effect=OSError("simulated history failure"),
        ):
            with self.assertRaisesRegex(
                OSError, "simulated history failure"
            ):
                project_manager.command_pause_subproject(
                    Namespace(id="2FUNC")
                )

        self.assertEqual(self.registry_file.read_bytes(), registry_before)
        self.assertEqual(metadata_path.read_bytes(), metadata_before)
        self.assertFalse(history_path.exists())
        self.assertEqual(self.read_active_id(), "UVI")


if __name__ == "__main__":
    unittest.main()
