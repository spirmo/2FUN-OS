from TANDIL_GOVERNANCE.core_engine.snapshot_manager import SnapshotManager

sm = SnapshotManager()


def on_dev_feature_success(feature_name: str, notes: str = ""):
    return sm.save_development(
        {
            "feature_name": feature_name,
            "status": "passed",
            "notes": notes,
        }
    )


def auto_dev_snapshot(feature_name, status, notes=""):
    if status != "passed":
        return

    return on_dev_feature_success(
        feature_name,
        notes,
    )
