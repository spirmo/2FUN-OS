from pathlib import Path

from .rule_registry import RuleRegistry


class RuleEvaluator:
    """Legacy promotion-rule evaluation contract."""

    def __init__(self):
        self.registry = RuleRegistry()
        self.rules_path = Path(__file__).resolve().parent / "rules" / "promotion_rules.json"

    def evaluate_promotion(self, user_data):
        promotion_rules = self.registry.load_rule_file(str(self.rules_path))

        user_score = user_data.get("score", 0)
        user_reputation = user_data.get("reputation", 0)
        user_violations = user_data.get("violations", 0)

        best_rank = None

        for rule in promotion_rules["promotion_rules"]:
            if (
                user_score >= rule["required_score"]
                and user_reputation >= rule["required_reputation"]
                and user_violations <= rule["max_violations"]
            ):
                best_rank = rule["target_rank"]

        if best_rank:
            return {
                "eligible": True,
                "target_rank": best_rank,
            }

        return {
            "eligible": False,
            "target_rank": None,
        }
