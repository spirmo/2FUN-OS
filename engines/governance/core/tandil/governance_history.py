import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[3]

HISTORY_PATH = (
    BASE_DIR / "engines" / "governance" / "logs" / "governance_history.json"
)


class GovernanceHistory:

    def __init__(self):

        HISTORY_PATH.parent.mkdir(exist_ok=True)

        if not HISTORY_PATH.exists():
            with open(HISTORY_PATH, "w", encoding="utf-8") as f:
                json.dump([], f)

    def record(
        self,
        event_id,
        governance_result,
        founder_decision=None,
    ):

        with open(HISTORY_PATH, "r", encoding="utf-8") as f:
            history = json.load(f)

        history.append(
            {
                "timestamp": time.time(),
                "event_id": event_id,
                "recommendation": governance_result.get("recommendation"),
                "severity": governance_result.get("severity"),
                "confidence": governance_result.get("confidence"),
                "explanation": governance_result.get("explanation"),
                "requires_founder_review": governance_result.get(
                    "requires_founder_review"
                ),
                "risk_score": governance_result.get("risk_score"),
                "trust_score": governance_result.get("trust_score"),
                "founder_decision": founder_decision,
            }
        )

        with open(HISTORY_PATH, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
