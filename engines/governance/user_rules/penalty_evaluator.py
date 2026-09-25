import json
from pathlib import Path


class PenaltyEvaluator:
    """Legacy penalty-rule evaluation contract."""

    def __init__(self):
        rules_path = Path(__file__).resolve().parent / "rules" / "penalty_rules.json"
        self.penalty_rules = self.load_rules(rules_path)

    def load_rules(self, path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def evaluate_penalty(self, user_data):
        violations = user_data["violations"]

        selected = {
            "penalty": None,
            "action": "none",
        }

        for rule in self.penalty_rules["penalty_rules"]:
            if violations >= rule["min_violations"]:
                selected = {
                    "penalty": rule["penalty"],
                    "action": rule["action"],
                }

        return selected
