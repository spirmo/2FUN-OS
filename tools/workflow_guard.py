#!/usr/bin/env python3
"""Read-only workflow control for the 2FUN project."""

import argparse
import json
import os
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MISSION_FILE = ROOT / "PROJECT_MISSION.md"
STATE_FILE = ROOT / "WORKFLOW_STATE.json"
HISTORY_FILE = ROOT / "WORKFLOW_HISTORY.jsonl"
CATALOG_FILE = ROOT / "MISSION_CATALOG.json"


def load_state():
    with STATE_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def load_catalog():
    with CATALOG_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def load_history():
    events = []
    with HISTORY_FILE.open(encoding="utf-8") as file:
        for number, line in enumerate(file, 1):
            if not line.strip():
                continue
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid history JSON at line {number}: {exc}"
                ) from exc
    return events


def verify():
    errors = []

    for path in (MISSION_FILE, STATE_FILE, HISTORY_FILE, CATALOG_FILE):
        if not path.is_file():
            errors.append(f"Missing required file: {path.name}")

    if errors:
        return errors, None, []

    try:
        state = load_state()
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Cannot read workflow state: {exc}")
        return errors, None, []

    try:
        events = load_history()
    except (OSError, ValueError) as exc:
        errors.append(f"Cannot read workflow history: {exc}")
        return errors, state, []

    try:
        catalog = load_catalog()
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"Cannot read mission catalog: {exc}")
        return errors, state, events

    mission = state.get("active_mission", {})
    catalog_missions = catalog.get("missions", [])
    catalog_active_id = catalog.get("active_mission_id")
    catalog_active = next(
        (item for item in catalog_missions
         if str(item.get("id")) == str(catalog_active_id)),
        None,
    )
    if str(catalog_active_id) != str(mission.get("id")):
        errors.append("Catalog active mission ID does not match workflow state.")
    if catalog_active is None:
        errors.append("Active mission is missing from mission catalog.")
    elif catalog_active.get("status") != "ACTIVE":
        errors.append("Catalog active mission status is not ACTIVE.")
    if mission.get("status") != "ACTIVE":
        errors.append("Active mission status is not ACTIVE.")

    if mission.get("closure_approved") is not False:
        errors.append("Unexpected mission closure approval state.")

    if not any(
        event.get("event") == "MISSION_BASELINE_APPROVED"
        and event.get("mission_id") == mission.get("id")
        for event in events
    ):
        errors.append("Mission baseline approval event is missing.")

    if not MISSION_FILE.read_text(encoding="utf-8").strip():
        errors.append("Mission document is empty.")

    return errors, state, events


def command_status(_args):
    errors, state, events = verify()
    if state is None:
        print("WORKFLOW STATUS: INVALID")
        for error in errors:
            print("ERROR:", error)
        return 1

    mission = state["active_mission"]
    print("PROJECT:", state.get("project"))
    print("MISSION:", mission.get("id"), "-", mission.get("title"))
    print("STATUS:", mission.get("status"))
    print("CURRENT STAGE:", mission.get("current_stage"))
    print("CLOSURE APPROVED:", mission.get("closure_approved"))
    print("HISTORY EVENTS:", len(events))
    print("ACCEPTANCE CRITERIA:")

    for name, status in mission.get("acceptance_criteria", {}).items():
        print(f"  {name}: {status}")

    print("WORKFLOW CHECK:", "FAILED" if errors else "OK")
    for error in errors:
        print("ERROR:", error)

    return 1 if errors else 0


def command_next(_args):
    errors, state, _events = verify()
    if errors or state is None:
        print("NEXT ACTION: BLOCKED")
        for error in errors:
            print("ERROR:", error)
        return 1

    action = state.get("next_action", {})
    print("ACTIVE MISSION:", state["active_mission"].get("id"))
    print("CURRENT STAGE:", state["active_mission"].get("current_stage"))
    print("NEXT ACTION:", action.get("id"))
    print("DESCRIPTION:", action.get("description"))
    print("ACTION STATUS:", action.get("status"))
    return 0


def command_history(_args):
    errors, _state, events = verify()
    if errors:
        print("HISTORY CHECK: FAILED")
        for error in errors:
            print("ERROR:", error)
        return 1

    for index, event in enumerate(events, 1):
        print(
            f"{index}. {event.get('timestamp', 'NO_TIMESTAMP')} | "
            f"{event.get('event', 'UNKNOWN_EVENT')} | "
            f"mission={event.get('mission_id', 'UNKNOWN')}"
        )

    print("TOTAL EVENTS:", len(events))
    return 0


def command_missions(_args):
    errors, state, _events = verify()
    if errors or state is None:
        print("MISSION CATALOG: INVALID")
        for error in errors:
            print("ERROR:", error)
        return 1

    catalog = load_catalog()
    print("PROJECT:", catalog.get("project"))
    print("ACTIVE MISSION ID:", catalog.get("active_mission_id"))
    print("MISSIONS:")
    for mission in catalog.get("missions", []):
        marker = " [ACTIVE]" if str(mission.get("id")) == str(catalog.get("active_mission_id")) else ""
        print(f"  {mission.get(chr(105)+chr(100))}: {mission.get(chr(116)+chr(105)+chr(116)+chr(108)+chr(101))} | "
              f"status={mission.get(chr(115)+chr(116)+chr(97)+chr(116)+chr(117)+chr(115))}{marker}")
    return 0


def command_show_mission(args):
    errors, state, _events = verify()
    if errors or state is None:
        print("MISSION LOOKUP: BLOCKED")
        for error in errors:
            print("ERROR:", error)
        return 1

    catalog = load_catalog()
    mission = next(
        (item for item in catalog.get("missions", [])
         if str(item.get("id")) == str(args.mission_id)),
        None,
    )
    if mission is None:
        print(f"MISSION NOT FOUND: {args.mission_id}")
        return 1
    print(json.dumps(mission, ensure_ascii=False, indent=2))
    return 0




def command_record_stage_evidence(args):
    errors, state, events = verify()
    if errors or state is None:
        print("EVIDENCE RECORDING: BLOCKED")
        for error in errors:
            print("ERROR:", error)
        return 1

    try:
        evidence = json.loads(args.evidence)
    except (json.JSONDecodeError, TypeError) as exc:
        print(f"INVALID EVIDENCE JSON: {exc}")
        return 1

    if not isinstance(evidence, list):
        print("INVALID EVIDENCE: expected a JSON list")
        return 1

    catalog = load_catalog()
    mission = state["active_mission"]
    mission_id = mission.get("id")

    catalog_mission = next(
        (
            item for item in catalog.get("missions", [])
            if str(item.get("id")) == str(mission_id)
        ),
        None,
    )
    if catalog_mission is None:
        print("EVIDENCE RECORDING: active mission missing from catalog")
        return 1

    stage_id = args.stage_id
    if stage_id != mission.get("current_stage"):
        print("EVIDENCE RECORDING: stage is not the current active stage")
        return 1

    stage = next(
        (
            item for item in catalog_mission.get("stages", [])
            if item.get("id") == stage_id
        ),
        None,
    )
    if stage is None or stage.get("status") != "ACTIVE":
        print("EVIDENCE RECORDING: unknown or inactive stage")
        return 1

    criteria = stage.get("acceptance")
    if (
        not isinstance(criteria, list)
        or not criteria
        or any(not isinstance(item, str) or not item.strip()
               for item in criteria)
    ):
        print("EVIDENCE RECORDING: invalid stage acceptance criteria")
        return 1

    if len(evidence) != len(criteria):
        print(
            "INCOMPLETE EVIDENCE: expected "
            f"{len(criteria)} items, received {len(evidence)}"
        )
        return 1

    if any(
        not isinstance(item, str) or not item.strip()
        for item in evidence
    ):
        print("INVALID EVIDENCE: every item must be a non-empty string")
        return 1

    if any(
        event.get("event") == "WORKFLOW_STAGE_ACCEPTANCE_EVIDENCE_RECORDED"
        and str(event.get("mission_id")) == str(mission_id)
        and event.get("stage_id") == stage_id
        for event in events
    ):
        print("EVIDENCE RECORDING: evidence already recorded for this stage")
        return 1

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "WORKFLOW_STAGE_ACCEPTANCE_EVIDENCE_RECORDED",
        "mission_id": mission_id,
        "stage_id": stage_id,
        "stage_status": "EVIDENCE_RECORDED_PENDING_USER_ACCEPTANCE",
        "acceptance_evidence": [
            {
                "criterion": criterion,
                "evidence": item.strip(),
            }
            for criterion, item in zip(criteria, evidence)
        ],
    }

    try:
        original = HISTORY_FILE.read_bytes()
        if original and not original.endswith(b"\n"):
            print("EVIDENCE RECORDING: history has an incomplete final line")
            return 1

        updated = original + (
            json.dumps(event, ensure_ascii=False) + "\n"
        ).encode("utf-8")

        _write_files_transactionally({
            HISTORY_FILE: updated,
        })
    except (OSError, RuntimeError) as exc:
        print(f"EVIDENCE RECORDING FAILED: {exc}")
        return 1

    print("EVIDENCE RECORDING: SUCCESS")
    print("MISSION:", mission_id)
    print("STAGE:", stage_id)
    print("STATUS: EVIDENCE_RECORDED_PENDING_USER_ACCEPTANCE")
    print("CRITERIA RECORDED:", len(criteria))
    return 0



def command_accept_stage(args):
    errors, state, events = verify()
    if errors or state is None:
        print("STAGE ACCEPTANCE: BLOCKED")
        for error in errors:
            print("ERROR:", error)
        return 1

    approval = args.approval
    if not isinstance(approval, str) or not approval.strip():
        print("STAGE ACCEPTANCE: explicit approval is required")
        return 1

    mission = state.get("active_mission", {})
    mission_id = mission.get("id")
    stage_id = args.stage_id

    if stage_id != mission.get("current_stage"):
        print("STAGE ACCEPTANCE: stage is not current")
        return 1

    catalog = load_catalog()
    matches = [
        item for item in catalog.get("missions", [])
        if isinstance(item, dict)
        and str(item.get("id")) == str(mission_id)
    ]
    if len(matches) != 1:
        print("STAGE ACCEPTANCE: active mission missing or ambiguous")
        return 1

    stages = matches[0].get("stages")
    if not isinstance(stages, list):
        print("STAGE ACCEPTANCE: invalid stage list")
        return 1

    indexes = [
        i for i, item in enumerate(stages)
        if isinstance(item, dict) and item.get("id") == stage_id
    ]
    if len(indexes) != 1:
        print("STAGE ACCEPTANCE: stage missing or ambiguous")
        return 1

    index = indexes[0]
    stage = stages[index]
    if stage.get("status") != "ACTIVE" or index + 1 >= len(stages):
        print("STAGE ACCEPTANCE: stage inactive or has no successor")
        return 1

    next_stage = stages[index + 1]
    if (
        not isinstance(next_stage, dict)
        or next_stage.get("status") != "PENDING"
        or not isinstance(next_stage.get("id"), str)
        or not next_stage["id"].strip()
    ):
        print("STAGE ACCEPTANCE: next stage is not pending")
        return 1

    criteria = stage.get("acceptance")
    if (
        not isinstance(criteria, list)
        or not criteria
        or any(not isinstance(x, str) or not x.strip() for x in criteria)
    ):
        print("STAGE ACCEPTANCE: invalid acceptance criteria")
        return 1

    relevant = [
        event for event in events
        if isinstance(event, dict)
        and str(event.get("mission_id")) == str(mission_id)
        and event.get("stage_id") == stage_id
    ]
    if any(
        event.get("event") == "WORKFLOW_STAGE_ACCEPTED"
        for event in relevant
    ):
        print("STAGE ACCEPTANCE: stage was already accepted")
        return 1

    evidence_events = [
        event for event in relevant
        if event.get("event")
        == "WORKFLOW_STAGE_ACCEPTANCE_EVIDENCE_RECORDED"
    ]
    if len(evidence_events) != 1:
        print("STAGE ACCEPTANCE: exactly one evidence record is required")
        return 1

    evidence = evidence_events[0].get("acceptance_evidence")
    if (
        not isinstance(evidence, list)
        or len(evidence) != len(criteria)
        or any(
            not isinstance(item, dict)
            or item.get("criterion") != criterion
            or not isinstance(item.get("evidence"), str)
            or not item["evidence"].strip()
            for criterion, item in zip(criteria, evidence)
        )
    ):
        print("STAGE ACCEPTANCE: evidence is incomplete or invalid")
        return 1

    try:
        original_history = HISTORY_FILE.read_bytes()
        if original_history and not original_history.endswith(b"\n"):
            print("STAGE ACCEPTANCE: history has an incomplete final line")
            return 1

        updated_catalog = json.loads(json.dumps(catalog))
        updated_state = json.loads(json.dumps(state))
        updated_mission = next(
            item for item in updated_catalog["missions"]
            if str(item.get("id")) == str(mission_id)
        )
        updated_stages = updated_mission["stages"]
        updated_stages[index]["status"] = "COMPLETED"
        updated_stages[index + 1]["status"] = "ACTIVE"

        next_stage_id = updated_stages[index + 1]["id"]
        updated_state["active_mission"]["current_stage"] = next_stage_id
        updated_state["next_action"] = {
            "id": "BUILD_EVIDENCE_BASED_TECHNICAL_STAGE_PLAN",
            "description": (
                "Distinguish completed and unfinished 2FUNC work using "
                "actual evidence, then define remaining stages and dependencies"
            ),
            "status": "IN_PROGRESS",
        }

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "WORKFLOW_STAGE_ACCEPTED",
            "mission_id": mission_id,
            "stage_id": stage_id,
            "next_stage_id": next_stage_id,
            "stage_status": "COMPLETED",
            "approval": "USER_EXPLICIT_APPROVAL",
            "approval_text": approval.strip(),
        }
        updated_history = original_history + (
            json.dumps(event, ensure_ascii=False) + "\n"
        ).encode("utf-8")

        _write_files_transactionally({
            HISTORY_FILE: updated_history,
            CATALOG_FILE: (
                json.dumps(updated_catalog, ensure_ascii=False, indent=2)
                + "\n"
            ).encode("utf-8"),
            STATE_FILE: (
                json.dumps(updated_state, ensure_ascii=False, indent=2)
                + "\n"
            ).encode("utf-8"),
        })
    except (OSError, RuntimeError, TypeError, ValueError, KeyError) as exc:
        print(f"STAGE ACCEPTANCE FAILED: {exc}")
        return 1

    print("STAGE ACCEPTANCE: SUCCESS")
    print("MISSION:", mission_id)
    print("COMPLETED STAGE:", stage_id)
    print("ACTIVE STAGE:", next_stage_id)
    print("APPROVAL: USER_EXPLICIT_APPROVAL")
    return 0



def _validate_draft_data(data, existing_ids):
    if not isinstance(data, dict):
        raise ValueError("Mission data must be a JSON object.")

    mission_id = data.get("id")
    if isinstance(mission_id, bool) or not isinstance(mission_id, int) or mission_id < 1:
        raise ValueError("Mission id must be a positive integer.")

    if str(mission_id) in existing_ids:
        raise ValueError(f"Mission ID already exists: {mission_id}")

    title = data.get("title")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("Mission title is required.")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        raise ValueError("Mission scope must be an object.")

    for key in ("in_scope", "out_of_scope"):
        values = scope.get(key)
        if not isinstance(values, list) or not values:
            raise ValueError(f"scope.{key} must be a non-empty list.")
        if any(not isinstance(item, str) or not item.strip() for item in values):
            raise ValueError(f"Every scope.{key} item must be non-empty text.")

    depends_on = data.get("depends_on")
    if not isinstance(depends_on, list):
        raise ValueError("depends_on must be a list.")
    if any(
        isinstance(item, bool) or not isinstance(item, int) or item < 1
        for item in depends_on
    ):
        raise ValueError("Every dependency ID must be a positive integer.")
    if mission_id in depends_on:
        raise ValueError("A mission cannot depend on itself.")

    stages = data.get("stages")
    if not isinstance(stages, list) or not stages:
        raise ValueError("At least one stage is required.")

    stage_ids = set()
    for stage in stages:
        if not isinstance(stage, dict):
            raise ValueError("Every stage must be an object.")

        stage_id = stage.get("id")
        if not isinstance(stage_id, str) or not stage_id.strip():
            raise ValueError("Every stage requires a non-empty id.")
        if stage_id in stage_ids:
            raise ValueError(f"Duplicate stage ID: {stage_id}")
        stage_ids.add(stage_id)

        if not isinstance(stage.get("title"), str) or not stage["title"].strip():
            raise ValueError(f"Stage {stage_id} requires a title.")

        acceptance = stage.get("acceptance")
        if not isinstance(acceptance, list) or not acceptance:
            raise ValueError(f"Stage {stage_id} requires acceptance criteria.")
        if any(not isinstance(item, str) or not item.strip() for item in acceptance):
            raise ValueError(f"Stage {stage_id} has invalid acceptance criteria.")

    plan = data.get("technical_stage_plan")
    if not isinstance(plan, dict):
        raise ValueError("technical_stage_plan must be an object.")
    if not isinstance(plan.get("stages"), list):
        raise ValueError("technical_stage_plan.stages must be a list.")

    if data.get("closure_approval_required") is not True:
        raise ValueError("closure_approval_required must be true.")

    return {
        "id": mission_id,
        "title": title.strip(),
        "status": "DRAFT",
        "approval": "PENDING",
        "depends_on": depends_on,
        "scope": {
            "in_scope": scope["in_scope"],
            "out_of_scope": scope["out_of_scope"],
        },
        "stages": stages,
        "technical_stage_plan": {
            "status": "PENDING_APPROVAL",
            "stages": plan["stages"],
        },
        "closure_approval_required": True,
    }


def _write_files_transactionally(updates):
    originals = {}
    temporary = {}
    replaced = []

    try:
        for target, content in updates.items():
            originals[target] = target.read_bytes()
            fd, temp_name = tempfile.mkstemp(
                prefix=f".{target.name}.",
                suffix=".tmp",
                dir=str(target.parent),
            )
            temp_path = Path(temp_name)
            temporary[target] = temp_path

            with os.fdopen(fd, "wb") as file:
                file.write(content)
                file.flush()
                os.fsync(file.fileno())

        for target, temp_path in temporary.items():
            os.replace(temp_path, target)
            replaced.append(target)

    except Exception as exc:
        rollback_errors = []
        for target in reversed(replaced):
            try:
                fd, temp_name = tempfile.mkstemp(
                    prefix=f".{target.name}.rollback.",
                    suffix=".tmp",
                    dir=str(target.parent),
                )
                with os.fdopen(fd, "wb") as file:
                    file.write(originals[target])
                    file.flush()
                    os.fsync(file.fileno())
                os.replace(temp_name, target)
            except Exception as rollback_exc:
                rollback_errors.append(f"{target.name}: {rollback_exc}")

        detail = f"Write failed: {exc}"
        if rollback_errors:
            detail += "; ROLLBACK FAILED: " + "; ".join(rollback_errors)
        raise RuntimeError(detail) from exc

    finally:
        for temp_path in temporary.values():
            try:
                temp_path.unlink(missing_ok=True)
            except OSError:
                pass


def command_add_mission(args):
    errors, _state, events = verify()
    if errors:
        print("ADD MISSION: BLOCKED")
        for error in errors:
            print("ERROR:", error)
        return 1

    try:
        data = json.loads(args.data)
        catalog = load_catalog()
        existing_ids = {
            str(item.get("id"))
            for item in catalog.get("missions", [])
            if isinstance(item, dict)
        }

        mission = _validate_draft_data(data, existing_ids)

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "MISSION_DRAFT_CREATED",
            "mission_id": mission["id"],
            "title": mission["title"],
        }

        updated_catalog = dict(catalog)
        updated_catalog["missions"] = [
            *catalog["missions"],
            mission,
        ]

        history_text = HISTORY_FILE.read_text(encoding="utf-8")
        if history_text and not history_text.endswith("\n"):
            history_text += "\n"
        history_text += json.dumps(event, ensure_ascii=False) + "\n"

        updates = {
            CATALOG_FILE: (
                json.dumps(updated_catalog, ensure_ascii=False, indent=2) + "\n"
            ).encode("utf-8"),
            HISTORY_FILE: history_text.encode("utf-8"),
        }
        _write_files_transactionally(updates)

    except (OSError, json.JSONDecodeError, TypeError, ValueError, RuntimeError) as exc:
        print(f"ADD MISSION: REJECTED - {exc}")
        return 1

    print("MISSION DRAFT CREATED:", mission["id"])
    print("STATUS: DRAFT")
    print("APPROVAL: PENDING")
    print("ACTIVE MISSION UNCHANGED:", catalog.get("active_mission_id"))
    print("HISTORY EVENT: MISSION_DRAFT_CREATED")
    return 0


def command_approve_mission(args):
    errors, _state, _events = verify()
    if errors:
        print("APPROVE MISSION: BLOCKED")
        for error in errors:
            print("ERROR:", error)
        return 1

    try:
        catalog = load_catalog()
        mission = next(
            (
                item for item in catalog.get("missions", [])
                if isinstance(item, dict)
                and str(item.get("id")) == str(args.mission_id)
            ),
            None,
        )

        if mission is None:
            print(f"MISSION NOT FOUND: {args.mission_id}")
            return 1

        if (
            mission.get("status") != "DRAFT"
            or mission.get("approval") != "PENDING"
        ):
            print(
                f"MISSION {args.mission_id} is not a pending draft."
            )
            return 1

        updated_catalog = dict(catalog)
        updated_missions = []
        for item in catalog["missions"]:
            if item is mission:
                approved = dict(item)
                approved["status"] = "APPROVED"
                approved["approval"] = "APPROVED"
                updated_missions.append(approved)
            else:
                updated_missions.append(item)
        updated_catalog["missions"] = updated_missions

        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event": "MISSION_APPROVED",
            "mission_id": mission["id"],
            "title": mission.get("title"),
        }

        history_text = HISTORY_FILE.read_text(encoding="utf-8")
        if history_text and not history_text.endswith("\n"):
            history_text += "\n"
        history_text += json.dumps(event, ensure_ascii=False) + "\n"

        updates = {
            CATALOG_FILE: (
                json.dumps(updated_catalog, ensure_ascii=False, indent=2)
                + "\n"
            ).encode("utf-8"),
            HISTORY_FILE: history_text.encode("utf-8"),
        }
        _write_files_transactionally(updates)

    except (OSError, json.JSONDecodeError, TypeError, ValueError, RuntimeError) as exc:
        print(f"APPROVE MISSION: REJECTED - {exc}")
        return 1

    print("MISSION APPROVED:", mission["id"])
    print("STATUS: APPROVED")
    print("APPROVAL: APPROVED")
    print("ACTIVE MISSION UNCHANGED:", catalog.get("active_mission_id"))
    print("HISTORY EVENT: MISSION_APPROVED")
    return 0

def command_verify(_args):
    errors, state, events = verify()

    if errors:
        print("VERIFY: FAILED")
        for error in errors:
            print("ERROR:", error)
        return 1

    print("VERIFY: PASSED")
    print("MISSION DOCUMENT: PRESENT")
    print("STATE JSON: VALID")
    print("HISTORY JSONL: VALID")
    print("BASELINE EVENT: PRESENT")
    print("MISSION STATUS:", state["active_mission"]["status"])
    print("HISTORY EVENTS:", len(events))
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="2FUN project workflow guard and mission management"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    for name, handler, help_text in (
        ("status", command_status, "Show mission and acceptance status"),
        ("next", command_next, "Show the recorded next action"),
        ("history", command_history, "Show recorded workflow events"),
        ("verify", command_verify, "Validate workflow files and baseline"),
        ("missions", command_missions, "List catalog missions"),
    ):
        sub = subparsers.add_parser(name, help=help_text)
        sub.set_defaults(handler=handler)

    add_parser = subparsers.add_parser(
        "add-mission", help="Register a mission as an unapproved draft"
    )
    add_parser.add_argument(
        "--data", required=True, help="Mission definition as a JSON object"
    )
    add_parser.set_defaults(handler=command_add_mission)

    approve_parser = subparsers.add_parser(
        "approve-mission", help="Approve a pending mission draft"
    )
    approve_parser.add_argument("mission_id")
    approve_parser.set_defaults(handler=command_approve_mission)

    show_parser = subparsers.add_parser(
        "show-mission", help="Show one mission by ID"
    )
    show_parser.add_argument("mission_id")
    show_parser.set_defaults(handler=command_show_mission)

    evidence_parser = subparsers.add_parser(
        "record-stage-evidence",
        help="Record acceptance evidence without approving the stage",
    )
    evidence_parser.add_argument("--stage-id", required=True)
    evidence_parser.add_argument(
        "--evidence",
        required=True,
        help="JSON list containing one evidence item per acceptance criterion",
    )
    evidence_parser.set_defaults(handler=command_record_stage_evidence)

    accept_parser = subparsers.add_parser(
        "accept-stage",
        help="Accept the current stage using recorded evidence and explicit approval",
    )
    accept_parser.add_argument("--stage-id", required=True)
    accept_parser.add_argument(
        "--approval", required=True, help="Explicit user approval text"
    )
    accept_parser.set_defaults(handler=command_accept_stage)

    args = parser.parse_args()
    try:
        return args.handler(args)
    except (OSError, KeyError, TypeError, ValueError) as exc:
        print(f"WORKFLOW ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
