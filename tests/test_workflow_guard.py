import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
MODULE_PATH = ROOT / "tools" / "workflow_guard.py"

SPEC = importlib.util.spec_from_file_location(
    "workflow_guard_under_test", MODULE_PATH
)
workflow_guard = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow_guard)


class WorkflowGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)

        self.mission_file = self.root / "PROJECT_MISSION.md"
        self.state_file = self.root / "WORKFLOW_STATE.json"
        self.history_file = self.root / "WORKFLOW_HISTORY.jsonl"
        self.catalog_file = self.root / "MISSION_CATALOG.json"

        self.mission_file.write_text(
            "2FUN mission baseline\n", encoding="utf-8"
        )

        self.state = {
            "project": "2FUN",
            "active_mission": {
                "id": 1,
                "title": "Complete the 2FUNC core",
                "status": "ACTIVE",
                "current_stage": "WORKFLOW_CONTROL_SETUP",
                "closure_approved": False,
                "acceptance_criteria": {
                    "core_components_implemented": "UNVERIFIED"
                },
            },
            "next_action": {
                "id": "VALIDATE_WORKFLOW",
                "description": "Validate workflow commands",
                "status": "IN_PROGRESS",
            },
        }

        self.acceptance_criteria = [
            "Mission document exists and its content is checked",
            "Machine-readable workflow state is valid",
            "Append-only workflow history exists",
            "Workflow guard read-only inspection commands and controlled mission-management commands are implemented and validated",
            "Mission catalog and mission-management controls are implemented",
        ]
        self.mission = {
            "id": 1,
            "title": "Complete the 2FUNC core",
            "status": "ACTIVE",
            "approval": "APPROVED",
            "scope": {
                "in_scope": ["2FUNC core"],
                "out_of_scope": ["Exchange"],
            },
            "stages": [
                {
                    "id": "WORKFLOW_CONTROL_SETUP",
                    "title": "Build and validate the project workflow control system",
                    "status": "ACTIVE",
                    "acceptance": self.acceptance_criteria,
                },
                {
                    "id": "MISSION_TECHNICAL_PLAN",
                    "title": "Define and approve the evidence-based technical stage plan for 2FUNC",
                    "status": "PENDING",
                    "acceptance": [
                        "Existing completed work is distinguished from unfinished work using actual evidence",
                        "Remaining technical stages and dependencies are explicitly defined",
                        "User approves the technical stage plan",
                    ],
                },
            ],
        }
        self.catalog = {
            "schema_version": 1,
            "project": "2FUN",
            "active_mission_id": 1,
            "missions": [self.mission],
        }

        self.history_file.write_text(
            json.dumps({
                "timestamp": "2026-11-05T00:00:00+00:00",
                "event": "MISSION_BASELINE_APPROVED",
                "mission_id": 1,
            }) + "\n",
            encoding="utf-8",
        )

        self.write_json(self.state_file, self.state)
        self.write_json(self.catalog_file, self.catalog)

        self.patches = [
            patch.object(workflow_guard, "MISSION_FILE", self.mission_file),
            patch.object(workflow_guard, "STATE_FILE", self.state_file),
            patch.object(workflow_guard, "HISTORY_FILE", self.history_file),
            patch.object(workflow_guard, "CATALOG_FILE", self.catalog_file),
        ]

        for item in self.patches:
            item.start()
            self.addCleanup(item.stop)

    def tearDown(self):
        self.temp_dir.cleanup()

    @staticmethod
    def write_json(path, value):
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def capture(self, function, args=None):
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            result = function(args)
        return result, output.getvalue()

    def test_verify_accepts_matching_active_mission(self):
        errors, state, events = workflow_guard.verify()

        self.assertEqual(errors, [])
        self.assertIsNotNone(state)
        self.assertEqual(len(events), 1)

    def test_missions_lists_active_mission(self):
        result, output = self.capture(workflow_guard.command_missions)

        self.assertEqual(result, 0)
        self.assertIn("ACTIVE MISSION ID: 1", output)
        self.assertIn("Complete the 2FUNC core", output)
        self.assertIn("[ACTIVE]", output)

    def test_show_mission_displays_existing_mission(self):
        args = type("Args", (), {"mission_id": "1"})()
        result, output = self.capture(
            workflow_guard.command_show_mission, args
        )

        self.assertEqual(result, 0)
        displayed = json.loads(output)
        self.assertEqual(displayed["id"], 1)
        self.assertEqual(displayed["approval"], "APPROVED")

    def test_show_mission_reports_missing_id(self):
        args = type("Args", (), {"mission_id": "999"})()
        result, output = self.capture(
            workflow_guard.command_show_mission, args
        )

        self.assertEqual(result, 1)
        self.assertIn("MISSION NOT FOUND: 999", output)

    def test_verify_rejects_catalog_active_id_mismatch(self):
        invalid_catalog = dict(self.catalog)
        invalid_catalog["active_mission_id"] = 999
        self.write_json(self.catalog_file, invalid_catalog)

        errors, state, events = workflow_guard.verify()

        self.assertIsNotNone(state)
        self.assertTrue(
            any("does not match workflow state" in error for error in errors)
        )



    def draft_data(self, mission_id=2):
        return json.dumps({
            "id": mission_id,
            "title": "Future mission draft",
            "scope": {
                "in_scope": ["Defined future work"],
                "out_of_scope": ["Unrelated work"]
            },
            "depends_on": [],
            "stages": [
                {
                    "id": "INITIAL_STAGE",
                    "title": "Initial stage",
                    "status": "PENDING",
                    "acceptance": ["Evidence is recorded"]
                }
            ],
            "technical_stage_plan": {
                "status": "PENDING_APPROVAL",
                "stages": []
            },
            "closure_approval_required": True
        })

    def test_add_mission_creates_draft(self):
        args = type("Args", (), {"data": self.draft_data()})()
        result, output = self.capture(
            workflow_guard.command_add_mission, args
        )

        self.assertEqual(result, 0, output)
        catalog = json.loads(self.catalog_file.read_text(encoding="utf-8"))
        created = next(
            item for item in catalog["missions"] if item["id"] == 2
        )
        self.assertEqual(created["status"], "DRAFT")
        self.assertEqual(created["approval"], "PENDING")
        self.assertEqual(catalog["active_mission_id"], 1)

        events = workflow_guard.load_history()
        self.assertEqual(len(events), 2)
        self.assertEqual(events[-1]["event"], "MISSION_DRAFT_CREATED")
        self.assertEqual(events[-1]["mission_id"], 2)

    def test_add_mission_rejects_duplicate_id(self):
        original_catalog = self.catalog_file.read_text(encoding="utf-8")
        original_history = self.history_file.read_text(encoding="utf-8")
        args = type("Args", (), {"data": self.draft_data(1)})()

        result, output = self.capture(
            workflow_guard.command_add_mission, args
        )

        self.assertEqual(result, 1)
        self.assertIn("already exists", output.lower())
        self.assertEqual(
            self.catalog_file.read_text(encoding="utf-8"),
            original_catalog
        )
        self.assertEqual(
            self.history_file.read_text(encoding="utf-8"),
            original_history
        )

    def test_add_mission_rejects_incomplete_data(self):
        original_catalog = self.catalog_file.read_text(encoding="utf-8")
        original_history = self.history_file.read_text(encoding="utf-8")
        args = type("Args", (), {
            "data": json.dumps({"id": 2, "title": "Incomplete"})
        })()

        result, output = self.capture(
            workflow_guard.command_add_mission, args
        )

        self.assertEqual(result, 1)
        self.assertEqual(
            self.catalog_file.read_text(encoding="utf-8"),
            original_catalog
        )
        self.assertEqual(
            self.history_file.read_text(encoding="utf-8"),
            original_history
        )

    def test_add_mission_preserves_active_mission_and_state(self):
        original_state = self.state_file.read_text(encoding="utf-8")
        args = type("Args", (), {"data": self.draft_data()})()

        self.capture(workflow_guard.command_add_mission, args)

        state = json.loads(self.state_file.read_text(encoding="utf-8"))
        catalog = json.loads(self.catalog_file.read_text(encoding="utf-8"))
        self.assertEqual(state, self.state)
        self.assertEqual(catalog["active_mission_id"], 1)
        self.assertEqual(
            self.catalog["missions"][0]["status"], "ACTIVE"
        )
        self.assertEqual(
            original_state,
            self.state_file.read_text(encoding="utf-8")
        )


    def test_approve_mission_approves_draft(self):
        create_args = type("Args", (), {"data": self.draft_data()})()
        create_result, create_output = self.capture(
            workflow_guard.command_add_mission, create_args
        )
        self.assertEqual(create_result, 0, create_output)

        args = type("Args", (), {"mission_id": "2"})()
        result, output = self.capture(
            workflow_guard.command_approve_mission, args
        )

        self.assertEqual(result, 0, output)
        catalog = json.loads(
            self.catalog_file.read_text(encoding="utf-8")
        )
        approved = next(
            item for item in catalog["missions"] if item["id"] == 2
        )
        self.assertEqual(approved["status"], "APPROVED")
        self.assertEqual(approved["approval"], "APPROVED")
        self.assertEqual(catalog["active_mission_id"], 1)

        events = workflow_guard.load_history()
        self.assertEqual(events[-1]["event"], "MISSION_APPROVED")
        self.assertEqual(events[-1]["mission_id"], 2)

    def test_approve_mission_rejects_missing_id(self):
        original_catalog = self.catalog_file.read_text(encoding="utf-8")
        original_history = self.history_file.read_text(encoding="utf-8")

        args = type("Args", (), {"mission_id": "999"})()
        result, output = self.capture(
            workflow_guard.command_approve_mission, args
        )

        self.assertEqual(result, 1)
        self.assertIn("MISSION NOT FOUND", output)
        self.assertEqual(
            self.catalog_file.read_text(encoding="utf-8"),
            original_catalog,
        )
        self.assertEqual(
            self.history_file.read_text(encoding="utf-8"),
            original_history,
        )

    def test_approve_mission_rejects_active_mission(self):
        original_catalog = self.catalog_file.read_text(encoding="utf-8")
        original_history = self.history_file.read_text(encoding="utf-8")

        args = type("Args", (), {"mission_id": "1"})()
        result, output = self.capture(
            workflow_guard.command_approve_mission, args
        )

        self.assertEqual(result, 1)
        self.assertIn("not a pending draft", output.lower())
        self.assertEqual(
            self.catalog_file.read_text(encoding="utf-8"),
            original_catalog,
        )
        self.assertEqual(
            self.history_file.read_text(encoding="utf-8"),
            original_history,
        )

    def test_approve_mission_rejects_repeated_approval(self):
        create_args = type("Args", (), {"data": self.draft_data()})()
        create_result, create_output = self.capture(
            workflow_guard.command_add_mission, create_args
        )
        self.assertEqual(create_result, 0, create_output)

        args = type("Args", (), {"mission_id": "2"})()
        first_result, first_output = self.capture(
            workflow_guard.command_approve_mission, args
        )
        self.assertEqual(first_result, 0, first_output)

        history_after_first = self.history_file.read_text(encoding="utf-8")
        second_result, second_output = self.capture(
            workflow_guard.command_approve_mission, args
        )

        self.assertEqual(second_result, 1)
        self.assertIn("not a pending draft", second_output.lower())
        self.assertEqual(
            self.history_file.read_text(encoding="utf-8"),
            history_after_first,
        )



    def evidence_data(self):
        return json.dumps([
            "Mission document reviewed",
            "Workflow state JSON validated",
            "Existing history JSONL inspected",
            "Workflow commands and their tests inspected",
            "Mission catalog and management commands inspected",
        ])

    def test_record_stage_evidence_appends_all_criteria_without_state_changes(self):
        catalog_before = self.catalog_file.read_bytes()
        state_before = self.state_file.read_bytes()
        history_before = self.history_file.read_text(encoding="utf-8")

        args = type("Args", (), {
            "stage_id": "WORKFLOW_CONTROL_SETUP",
            "evidence": self.evidence_data(),
        })()

        result, output = self.capture(
            workflow_guard.command_record_stage_evidence, args
        )

        self.assertEqual(result, 0, output)
        events = [
            json.loads(line)
            for line in self.history_file.read_text(encoding="utf-8").splitlines()
        ]
        event = events[-1]

        self.assertEqual(event["event"], "WORKFLOW_STAGE_ACCEPTANCE_EVIDENCE_RECORDED")
        self.assertEqual(event["mission_id"], 1)
        self.assertEqual(event["stage_id"], "WORKFLOW_CONTROL_SETUP")
        self.assertEqual(
            event["stage_status"],
            "EVIDENCE_RECORDED_PENDING_USER_ACCEPTANCE",
        )
        self.assertEqual(
            [item["criterion"] for item in event["acceptance_evidence"]],
            self.acceptance_criteria,
        )
        self.assertEqual(
            [item["evidence"] for item in event["acceptance_evidence"]],
            json.loads(self.evidence_data()),
        )
        self.assertTrue(
            self.history_file.read_text(encoding="utf-8").startswith(history_before)
        )
        self.assertEqual(self.catalog_file.read_bytes(), catalog_before)
        self.assertEqual(self.state_file.read_bytes(), state_before)

        catalog_after = json.loads(self.catalog_file.read_text(encoding="utf-8"))
        stages = catalog_after["missions"][0]["stages"]
        self.assertEqual(stages[0]["status"], "ACTIVE")
        self.assertEqual(stages[1]["status"], "PENDING")

    def test_record_stage_evidence_rejects_incomplete_evidence(self):
        history_before = self.history_file.read_bytes()
        args = type("Args", (), {
            "stage_id": "WORKFLOW_CONTROL_SETUP",
            "evidence": json.dumps(["only one evidence"]),
        })()

        result, output = self.capture(
            workflow_guard.command_record_stage_evidence, args
        )

        self.assertEqual(result, 1)
        self.assertEqual(self.history_file.read_bytes(), history_before)

    def test_record_stage_evidence_rejects_unknown_or_inactive_stage(self):
        history_before = self.history_file.read_bytes()
        evidence = self.evidence_data()

        unknown_args = type("Args", (), {
            "stage_id": "UNKNOWN_STAGE",
            "evidence": evidence,
        })()
        result, _ = self.capture(
            workflow_guard.command_record_stage_evidence, unknown_args
        )
        self.assertEqual(result, 1)
        self.assertEqual(self.history_file.read_bytes(), history_before)

        self.mission["stages"][1]["status"] = "PENDING"
        inactive_args = type("Args", (), {
            "stage_id": "MISSION_TECHNICAL_PLAN",
            "evidence": evidence,
        })()
        result, _ = self.capture(
            workflow_guard.command_record_stage_evidence, inactive_args
        )
        self.assertEqual(result, 1)
        self.assertEqual(self.history_file.read_bytes(), history_before)

    def test_record_stage_evidence_rejects_duplicate_event(self):
        args = type("Args", (), {
            "stage_id": "WORKFLOW_CONTROL_SETUP",
            "evidence": self.evidence_data(),
        })()

        first_result, first_output = self.capture(
            workflow_guard.command_record_stage_evidence, args
        )
        self.assertEqual(first_result, 0, first_output)
        history_after_first = self.history_file.read_bytes()

        second_result, second_output = self.capture(
            workflow_guard.command_record_stage_evidence, args
        )

        self.assertEqual(second_result, 1)
        self.assertEqual(self.history_file.read_bytes(), history_after_first)


    def record_current_stage_evidence(self):
        args = type("Args", (), {
            "stage_id": "WORKFLOW_CONTROL_SETUP",
            "evidence": self.evidence_data(),
        })()
        result, output = self.capture(
            workflow_guard.command_record_stage_evidence, args
        )
        self.assertEqual(result, 0, output)

    def accept_current_stage(self, approval="I explicitly approve this stage."):
        args = type("Args", (), {
            "stage_id": "WORKFLOW_CONTROL_SETUP",
            "approval": approval,
        })()
        return self.capture(workflow_guard.command_accept_stage, args)

    def test_accept_stage_updates_catalog_state_and_history_after_evidence(self):
        self.record_current_stage_evidence()
        approval = (
            "مرحلهٔ WORKFLOW_CONTROL_SETUP را تأیید می‌کنم و "
            "اجازهٔ ورود به MISSION_TECHNICAL_PLAN را می‌دهم."
        )

        result, output = self.accept_current_stage(approval)

        self.assertEqual(result, 0, output)

        state = json.loads(self.state_file.read_text(encoding="utf-8"))
        catalog = json.loads(self.catalog_file.read_text(encoding="utf-8"))
        events = [
            json.loads(line)
            for line in self.history_file.read_text(encoding="utf-8").splitlines()
        ]

        stages = catalog["missions"][0]["stages"]
        self.assertEqual(stages[0]["status"], "COMPLETED")
        self.assertEqual(stages[1]["status"], "ACTIVE")
        self.assertEqual(
            state["active_mission"]["current_stage"],
            "MISSION_TECHNICAL_PLAN",
        )
        self.assertEqual(
            state["next_action"]["id"],
            "BUILD_EVIDENCE_BASED_TECHNICAL_STAGE_PLAN",
        )
        self.assertEqual(state["active_mission"]["status"], "ACTIVE")
        self.assertFalse(state["active_mission"]["closure_approved"])
        self.assertEqual(events[-1]["event"], "WORKFLOW_STAGE_ACCEPTED")
        self.assertEqual(events[-1]["approval_text"], approval)

    def test_accept_stage_rejects_missing_evidence_without_changes(self):
        before = (
            self.state_file.read_bytes(),
            self.catalog_file.read_bytes(),
            self.history_file.read_bytes(),
        )

        result, output = self.accept_current_stage()

        self.assertEqual(result, 1, output)
        self.assertEqual(
            before,
            (
                self.state_file.read_bytes(),
                self.catalog_file.read_bytes(),
                self.history_file.read_bytes(),
            ),
        )

    def test_accept_stage_rejects_blank_approval_without_changes(self):
        self.record_current_stage_evidence()
        before = (
            self.state_file.read_bytes(),
            self.catalog_file.read_bytes(),
            self.history_file.read_bytes(),
        )

        result, output = self.accept_current_stage("   ")

        self.assertEqual(result, 1, output)
        self.assertEqual(
            before,
            (
                self.state_file.read_bytes(),
                self.catalog_file.read_bytes(),
                self.history_file.read_bytes(),
            ),
        )

    def test_accept_stage_rejects_duplicate_acceptance_without_changes(self):
        self.record_current_stage_evidence()
        first_result, first_output = self.accept_current_stage()
        self.assertEqual(first_result, 0, first_output)

        before = (
            self.state_file.read_bytes(),
            self.catalog_file.read_bytes(),
            self.history_file.read_bytes(),
        )
        second_result, second_output = self.accept_current_stage()

        self.assertEqual(second_result, 1)
        self.assertEqual(
            before,
            (
                self.state_file.read_bytes(),
                self.catalog_file.read_bytes(),
                self.history_file.read_bytes(),
            ),
        )

    def test_accept_stage_rejects_non_pending_next_stage_without_changes(self):
        self.record_current_stage_evidence()
        self.mission["stages"][1]["status"] = "ACTIVE"
        self.write_json(self.catalog_file, self.catalog)

        before = (
            self.state_file.read_bytes(),
            self.catalog_file.read_bytes(),
            self.history_file.read_bytes(),
        )
        result, output = self.accept_current_stage()

        self.assertEqual(result, 1, output)
        self.assertEqual(
            before,
            (
                self.state_file.read_bytes(),
                self.catalog_file.read_bytes(),
                self.history_file.read_bytes(),
            ),
        )

    def test_accept_stage_rolls_back_files_when_transactional_replace_fails(self):
        self.record_current_stage_evidence()
        before = (
            self.state_file.read_bytes(),
            self.catalog_file.read_bytes(),
            self.history_file.read_bytes(),
        )
        original_replace = workflow_guard.os.replace
        injected = {"done": False}

        def fail_catalog_once(source, destination):
            if destination == self.catalog_file and not injected["done"]:
                injected["done"] = True
                raise OSError("simulated catalog replace failure")
            return original_replace(source, destination)

        args = type("Args", (), {
            "stage_id": "WORKFLOW_CONTROL_SETUP",
            "approval": "I explicitly approve this stage.",
        })()

        with patch.object(
            workflow_guard.os, "replace", side_effect=fail_catalog_once
        ):
            result, output = self.capture(
                workflow_guard.command_accept_stage, args
            )

        self.assertTrue(injected["done"])
        self.assertEqual(result, 1)
        self.assertIn("STAGE ACCEPTANCE FAILED", output)
        self.assertEqual(
            before,
            (
                self.state_file.read_bytes(),
                self.catalog_file.read_bytes(),
                self.history_file.read_bytes(),
            ),
        )

if __name__ == "__main__":
    unittest.main()
