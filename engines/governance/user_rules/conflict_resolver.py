class ConflictResolver:
    """Legacy penalty conflict-resolution contract."""

    def __init__(self):
        self.priority_map = {
            "none": 0,
            "notify_user": 1,
            "restrict_access": 2,
            "temporary_restriction": 3,
            "council_review": 4,
            "trigger_governance_review": 4,
        }

    def resolve(self, penalty_results):
        if not penalty_results:
            return {
                "final_action": "none",
                "reason": "no penalties found",
            }

        if isinstance(penalty_results, dict):
            penalty_results = [penalty_results]

        best = penalty_results[0]

        for result in penalty_results:
            current_priority = self.priority_map.get(
                result.get("action", "none"), 0
            )
            best_priority = self.priority_map.get(
                best.get("action", "none"), 0
            )

            if current_priority > best_priority:
                best = result

        return {
            "final_action": best.get("action"),
            "penalty": best.get("penalty"),
            "resolution": "conflict_resolved",
        }
