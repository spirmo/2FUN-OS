#!/usr/bin/env python3
"""Central project manager for the 2FUN parent project."""

import argparse
import json
import os
import re
import shutil
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONTROL = ROOT / "project_control"
PARENT_FILE = CONTROL / "parent_project.json"
REGISTRY_FILE = CONTROL / "registry.json"
ACTIVE_FILE = CONTROL / "active_subproject.json"
GLOBAL_HISTORY_FILE = CONTROL / "global_history.jsonl"
SUBPROJECTS_DIR = CONTROL / "subprojects"


class ManagerError(Exception):
    pass


def load_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise ManagerError(f"Required file is missing: {path.relative_to(ROOT)}")
    except (OSError, ValueError) as exc:
        raise ManagerError(f"Cannot read {path.relative_to(ROOT)}: {exc}")


def write_json_atomic(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(data, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def load_control():
    parent = load_json(PARENT_FILE)
    registry = load_json(REGISTRY_FILE)
    active = load_json(ACTIVE_FILE)

    if parent.get("project_id") != "2FUN":
        raise ManagerError("Parent project ID must be 2FUN.")
    if registry.get("parent_project_id") != "2FUN":
        raise ManagerError("Registry parent project ID mismatch.")
    if active.get("parent_project_id") != "2FUN":
        raise ManagerError("Active-subproject parent project ID mismatch.")

    entries = registry.get("subprojects")
    if not isinstance(entries, list):
        raise ManagerError("Registry subprojects must be a list.")

    ids = [item.get("id") for item in entries]
    if any(not isinstance(item, str) or not item for item in ids):
        raise ManagerError("Every subproject must have a non-empty string ID.")
    if len(ids) != len(set(ids)):
        raise ManagerError("Duplicate subproject IDs found.")

    active_id = active.get("active_subproject_id")
    if active_id not in ids:
        raise ManagerError("Active subproject is not registered.")

    return parent, registry, active, entries


def load_subproject(subproject_id):
    path = SUBPROJECTS_DIR / subproject_id / "subproject.json"
    data = load_json(path)
    if data.get("parent_project_id") != "2FUN":
        raise ManagerError(f"{subproject_id}: parent project mismatch.")
    if data.get("subproject_id") != subproject_id:
        raise ManagerError(f"{subproject_id}: metadata ID mismatch.")
    return data


def workflow_paths_ready(metadata):
    keys = (
        "workflow_engine",
        "mission_catalog",
        "mission_document",
        "workflow_state",
        "workflow_history",
    )
    for key in keys:
        value = metadata.get(key)
        if not isinstance(value, str) or not value.strip():
            return False, f"Workflow path is not configured: {key}"
        path = (ROOT / value).resolve()
        if not path.is_relative_to(ROOT.resolve()) or not path.is_file():
            return False, f"Workflow file is missing or outside project: {key}"
    return True, ""


def command_verify(_args):
    _parent, _registry, active, entries = load_control()
    by_id = {item["id"]: item for item in entries}

    for item in entries:
        if item.get("status") in ("ACTIVE", "PAUSED"):
            metadata = load_subproject(item["id"])
            if metadata.get("status") != item.get("status"):
                raise ManagerError(
                    f"{item['id']}: registry and metadata status mismatch."
                )
            if item.get("status") == "ACTIVE":
                ready, reason = workflow_paths_ready(metadata)
                if not ready:
                    raise ManagerError(f"{item['id']}: {reason}")

    active_id = active["active_subproject_id"]
    if by_id[active_id].get("status") != "ACTIVE":
        raise ManagerError("Selected subproject is not marked ACTIVE.")

    metadata = load_subproject(active_id)
    ready, reason = workflow_paths_ready(metadata)
    if not ready:
        raise ManagerError(f"{active_id}: {reason}")

    print("PROJECT CONTROL: VALID")
    print("PARENT PROJECT: 2FUN")
    print("REGISTERED SUBPROJECTS:", len(entries))
    print("ACTIVE SUBPROJECT:", active_id)
    print("ACTIVE WORKFLOW FILES: VALID")
    return 0


def command_list(_args):
    _parent, _registry, active, entries = load_control()
    print("PARENT PROJECT: 2FUN")
    print("SUBPROJECTS:")
    for item in entries:
        marker = " [SELECTED]" if item["id"] == active["active_subproject_id"] else ""
        print(
            f"  {item['id']} | {item.get('name')} | "
            f"{item.get('status', 'UNKNOWN')}{marker}"
        )
    return 0


def command_status(_args):
    _parent, _registry, active, _entries = load_control()
    subproject_id = active["active_subproject_id"]
    metadata = load_subproject(subproject_id)

    print("PARENT PROJECT: 2FUN")
    print("ACTIVE SUBPROJECT:", subproject_id)
    print("SUBPROJECT NAME:", metadata.get("name"))
    print("SUBPROJECT STATUS:", metadata.get("status"))

    state_path = metadata.get("workflow_state")
    if state_path:
        state = load_json(ROOT / state_path)
        mission = state.get("active_mission", {})
        print("MISSION:", mission.get("id"), "-", mission.get("title"))
        print("MISSION STATUS:", mission.get("status"))
        print("CURRENT STAGE:", mission.get("current_stage"))
        action = state.get("next_action", {})
        print("NEXT ACTION:", action.get("id"))
        print("NEXT ACTION STATUS:", action.get("status"))
    else:
        print("WORKFLOW: NOT CONFIGURED")
    return 0


def command_add_subproject(args):
    _parent, registry, _active, entries = load_control()
    subproject_id = args.id

    if not re.fullmatch(r"[A-Z][A-Z0-9_]{1,39}", subproject_id):
        raise ManagerError(
            "ID must use uppercase letters, digits, and underscores; "
            "it must start with a letter."
        )

    if any(item["id"] == subproject_id for item in entries):
        raise ManagerError(f"Subproject already registered: {subproject_id}")

    directory = SUBPROJECTS_DIR / subproject_id
    metadata_file = directory / "subproject.json"

    if directory.exists():
        raise ManagerError(f"Subproject directory already exists: {subproject_id}")

    metadata = {
        "schema_version": 1,
        "parent_project_id": "2FUN",
        "subproject_id": subproject_id,
        "name": args.name,
        "description": args.description or "",
        "status": "DRAFT",
        "workflow_engine": None,
        "mission_catalog": None,
        "mission_document": None,
        "workflow_state": None,
        "workflow_history": None,
    }

    directory_created = False
    try:
        directory.mkdir(parents=True, exist_ok=False)
        directory_created = True

        (directory / "evidence").mkdir()
        (directory / "context").mkdir()

        with metadata_file.open("x", encoding="utf-8") as handle:
            json.dump(metadata, handle, ensure_ascii=False, indent=2)
            handle.write("\n")

        registry["subprojects"].append({
            "id": subproject_id,
            "name": args.name,
            "status": "DRAFT",
        })
        write_json_atomic(REGISTRY_FILE, registry)

    except Exception:
        if directory_created:
            shutil.rmtree(directory, ignore_errors=True)
        raise

    print("SUBPROJECT REGISTERED:", subproject_id)
    print("STATUS: DRAFT")
    print("ACTIVE SUBPROJECT: UNCHANGED")
    print("MISSION: NOT CREATED")
    return 0


def command_select_subproject(args):
    _parent, registry, active, entries = load_control()
    subproject_id = args.id

    entry = next((item for item in entries if item["id"] == subproject_id), None)
    if entry is None:
        raise ManagerError(f"Unknown subproject: {subproject_id}")
    if entry.get("status") != "ACTIVE":
        raise ManagerError("Only an ACTIVE subproject can be selected.")

    metadata = load_subproject(subproject_id)
    ready, reason = workflow_paths_ready(metadata)
    if not ready:
        raise ManagerError(f"Cannot select subproject: {reason}")

    previous_id = active["active_subproject_id"]
    if previous_id != subproject_id:
        active["active_subproject_id"] = subproject_id
        write_json_atomic(ACTIVE_FILE, active)

    print("ACTIVE SUBPROJECT:", subproject_id)
    print("PREVIOUS SUBPROJECT:", previous_id)
    return 0



def restore_file_snapshot(path, content):
    if content is None:
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        return

    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".rollback",
        dir=str(path.parent),
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, path)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def append_global_history(event):
    GLOBAL_HISTORY_FILE.parent.mkdir(parents=True, exist_ok=True)
    previous = (
        GLOBAL_HISTORY_FILE.read_bytes()
        if GLOBAL_HISTORY_FILE.exists()
        else b""
    )
    if previous and not previous.endswith(b"\n"):
        raise ManagerError("Global history has an incomplete final line.")

    line = (
        json.dumps(event, ensure_ascii=False, separators=(",", ":")) + "\n"
    ).encode("utf-8")

    fd, temp_name = tempfile.mkstemp(
        prefix=f".{GLOBAL_HISTORY_FILE.name}.",
        suffix=".tmp",
        dir=str(GLOBAL_HISTORY_FILE.parent),
    )
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(previous)
            handle.write(line)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temp_name, GLOBAL_HISTORY_FILE)
    except Exception:
        try:
            os.unlink(temp_name)
        except FileNotFoundError:
            pass
        raise


def change_subproject_lifecycle(subproject_id, expected_status, new_status):
    _parent, registry, active, entries = load_control()

    entry = next(
        (item for item in entries if item["id"] == subproject_id),
        None,
    )
    if entry is None:
        raise ManagerError(f"Unknown subproject: {subproject_id}")

    if entry.get("status") != expected_status:
        raise ManagerError(
            f"{subproject_id} must be {expected_status}; "
            f"current status is {entry.get('status')}."
        )

    if expected_status == "ACTIVE" and (
        active["active_subproject_id"] == subproject_id
    ):
        raise ManagerError(
            "Cannot pause the selected subproject. "
            "Select another ACTIVE subproject first."
        )

    metadata = load_subproject(subproject_id)
    if metadata.get("status") != expected_status:
        raise ManagerError(
            f"{subproject_id}: registry and metadata status mismatch."
        )

    if new_status == "ACTIVE":
        ready, reason = workflow_paths_ready(metadata)
        if not ready:
            raise ManagerError(
                f"Cannot resume subproject: {reason}"
            )

    registry_path = REGISTRY_FILE
    metadata_path = SUBPROJECTS_DIR / subproject_id / "subproject.json"
    history_path = GLOBAL_HISTORY_FILE

    snapshots = {}
    for file_path in (registry_path, metadata_path, history_path):
        snapshots[file_path] = (
            file_path.read_bytes() if file_path.exists() else None
        )

    entry["status"] = new_status
    metadata["status"] = new_status

    event = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "event": "SUBPROJECT_PAUSED" if new_status == "PAUSED"
                 else "SUBPROJECT_RESUMED",
        "subproject_id": subproject_id,
        "previous_status": expected_status,
        "new_status": new_status,
        "selected_subproject_id": active["active_subproject_id"],
    }

    try:
        write_json_atomic(registry_path, registry)
        write_json_atomic(metadata_path, metadata)
        append_global_history(event)
    except Exception:
        rollback_errors = []
        for file_path, content in snapshots.items():
            try:
                restore_file_snapshot(file_path, content)
            except Exception as rollback_error:
                rollback_errors.append(
                    f"{file_path}: {rollback_error}"
                )
        if rollback_errors:
            raise ManagerError(
                "Lifecycle update failed and rollback was incomplete: "
                + "; ".join(rollback_errors)
            )
        raise

    print("SUBPROJECT:", subproject_id)
    print("PREVIOUS STATUS:", expected_status)
    print("CURRENT STATUS:", new_status)
    print("SELECTED SUBPROJECT: UNCHANGED")
    print("GLOBAL HISTORY: APPENDED")
    return 0


def command_pause_subproject(args):
    return change_subproject_lifecycle(
        args.id, "ACTIVE", "PAUSED"
    )


def command_resume_subproject(args):
    return change_subproject_lifecycle(
        args.id, "PAUSED", "ACTIVE"
    )


def build_parser():
    parser = argparse.ArgumentParser(
        description="Central manager for the 2FUN parent project"
    )
    commands = parser.add_subparsers(dest="command", required=True)

    for name, handler, description in (
        ("list", command_list, "List registered subprojects"),
        ("status", command_status, "Show active subproject workflow status"),
        ("verify", command_verify, "Validate central project control"),
    ):
        sub = commands.add_parser(name, help=description)
        sub.set_defaults(handler=handler)

    add = commands.add_parser(
        "add-subproject", help="Register a new subproject as DRAFT"
    )
    add.add_argument("--id", required=True)
    add.add_argument("--name", required=True)
    add.add_argument("--description")
    add.set_defaults(handler=command_add_subproject)

    select = commands.add_parser(
        "select-subproject", help="Select a prepared ACTIVE subproject"
    )
    select.add_argument("id")
    select.set_defaults(handler=command_select_subproject)

    pause = commands.add_parser(
        "pause-subproject", help="Pause a non-selected ACTIVE subproject"
    )
    pause.add_argument("id")
    pause.set_defaults(handler=command_pause_subproject)

    resume = commands.add_parser(
        "resume-subproject", help="Resume a PAUSED subproject"
    )
    resume.add_argument("id")
    resume.set_defaults(handler=command_resume_subproject)

    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()
    try:
        return args.handler(args)
    except (ManagerError, OSError, KeyError, TypeError, ValueError) as exc:
        print(f"PROJECT MANAGER ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
