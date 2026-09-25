class RuleValidator:
    """Legacy promotion validation contract."""

    def validate(self, rule_result, user_data):
        if rule_result["eligible"] is False:
            return {
                "valid": False,
                "reason": "Not eligible",
            }

        if user_data["violations"] > 5:
            return {
                "valid": False,
                "reason": "Too many violations",
            }

        return {
            "valid": True,
            "reason": "Passed validation",
        }
