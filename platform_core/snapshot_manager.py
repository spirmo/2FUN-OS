import uuid
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
PROJECT_STATE_PATH = BASE_DIR / "PROJECT_STATE.json"
SNAPSHOT_DIR = BASE_DIR / "snapshots"
SNAPSHOT_DIR.mkdir(exist_ok=True)
DEV_INDEX_PATH = SNAPSHOT_DIR / "development_index.json"
TARGO_DIR = SNAPSHOT_DIR / "targo"
TARGO_DIR.mkdir(exist_ok=True)


class SnapshotManager:
    def __init__(self):
        self.path = PROJECT_STATE_PATH

    def load(self):
        if not self.path.exists():
            return {}
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def update_development_index(self, snapshot_data: dict):

        if DEV_INDEX_PATH.exists():
            with open(
                DEV_INDEX_PATH,
                "r",
                encoding="utf-8",
            ) as f:
                index = json.load(f)
        else:
            index = []

        index.append(snapshot_data)

        MAX_DEV_RECORDS = 500

        index = index[-MAX_DEV_RECORDS:]

        with open(
            DEV_INDEX_PATH,
            "w",
            encoding="utf-8",
        ) as f:
            json.dump(
                index,
                f,
                indent=2,
                ensure_ascii=False,
            )

    def save_development(self, state: dict):

        dev_dir = SNAPSHOT_DIR / "development"
        dev_dir.mkdir(exist_ok=True)

        file_name = f"dev_{time.time_ns()}_{uuid.uuid4().hex[:6]}.json"
        file_path = dev_dir / file_name

        payload = {
            **state,
            "timestamp": time.time(),
            "version": "v1",
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(
                payload,
                f,
                indent=2,
                ensure_ascii=False,
            )

        self.update_development_index(
            {
                "file": file_name,
                "feature_name": payload.get("feature_name"),
                "status": payload.get("status"),
                "notes": payload.get("notes"),
                "timestamp": payload.get("timestamp"),
            }
        )

        return {
            "status": "development_snapshot_saved",
            "file": file_name,
        }


    def save_targo_snapshot(
        self,
        targo_name: str,
        state: dict
    ):

        file_name = (
            f"{targo_name}.snapshot.json"
        )

        file_path = TARGO_DIR / file_name

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(
                state,
                f,
                indent=2,
                ensure_ascii=False
            )

        return {
            "status": "targo_snapshot_saved",
            "file": file_name
        }



    def rollback(self, snapshot_file: str):
        snapshot_path = SNAPSHOT_DIR / snapshot_file

        if not snapshot_path.exists():
            raise FileNotFoundError(f"Snapshot not found: {snapshot_file}")

        with open(snapshot_path, "r", encoding="utf-8") as f:
            state = json.load(f)

        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        return {
            "status": "rolled_back",
            "snapshot": snapshot_file,
            "timestamp": time.time(),
        }

    def load_safe(self):
        try:
            if not self.path.exists():
                return {}

            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)

        except Exception as e:
            print(f"[SNAPSHOT ERROR] corrupted file detected: {e}")

            backup_path = self.path.with_suffix(".backup.json")

            if backup_path.exists():
                with open(backup_path, "r", encoding="utf-8") as f:
                    return json.load(f)

            return {}

    def save(self, state: dict):

        if "_meta" not in state:
            state["_meta"] = {}

        state["_meta"]["last_updated"] = time.time()
        state["_meta"]["version"] = "v1-auto-snapshot"

        # MAIN SAVE
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        # BACKUP SAVE
        backup_path = self.path.with_suffix(".backup.json")

        with open(backup_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        # SNAPSHOT SAVE
        snapshot_name = f"snapshot_{int(time.time())}.json"
        snapshot_path = SNAPSHOT_DIR / snapshot_name

        with open(snapshot_path, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2, ensure_ascii=False)

        # CLEANUP POLICY
        ARCHIVE_LIMIT = 200
        ROLLING_LIMIT = 100
        MAX_TOTAL = ARCHIVE_LIMIT + ROLLING_LIMIT

        snapshots = sorted(
            SNAPSHOT_DIR.glob("snapshot_*.json"),
            key=lambda p: p.stat().st_mtime,
        )

        if len(snapshots) > MAX_TOTAL:

            excess = snapshots[:-MAX_TOTAL]

            for old in excess:
                old.unlink()

    def update(self, key: str, value):
        state = self.load()

        if "_runtime_state" not in state:
            state["_runtime_state"] = {}

        state["_runtime_state"][key] = value
        self.save(state)


    def get_last_snapshot_time(self):
        snapshots = sorted(
            SNAPSHOT_DIR.glob("snapshot_*.json"),
            key=lambda p: p.stat().st_mtime,
            reverse=True,
        )

        for snapshot_path in snapshots:
            try:
                with open(snapshot_path, "r", encoding="utf-8") as f:
                    data = json.load(f)

                metadata = data.get("_snapshot_meta", {})
                created_at = metadata.get("created_at")

                if created_at is not None:
                    return float(created_at)

            except Exception:
                continue

        return 0
