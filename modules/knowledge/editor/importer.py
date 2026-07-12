import json
from pathlib import Path

from .validators import validate_node


def import_node(json_file: str, destination: str):
    """
    Import a Knowledge Node into the repository.
    """

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    valid, errors, metadata = validate_node(data)

    # ثبت وضعیت و درصد کامل بودن
    data["status"] = metadata["status"]
    data["completeness"] = metadata["completeness"]

    domain = data["category"]

    target_dir = Path(destination) / "domains" / domain / "concepts"
    target_dir.mkdir(parents=True, exist_ok=True)

    target_file = target_dir / f"{data['node_id']}.json"

    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    return {
        "valid": valid,
        "errors": errors,
        "status": metadata["status"],
        "completeness": metadata["completeness"],
        "file": str(target_file),
    }
