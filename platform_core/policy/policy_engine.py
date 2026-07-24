class PolicyEngine:

    def __init__(self):

        # -----------------------------------
        # Policy Rules
        # لیست قوانین سیاست‌گذاری
        # -----------------------------------

        self.rules = []

    # -----------------------------------
    # Add Rule
    # افزودن قانون
    # -----------------------------------

    def add_rule(self, rule_fn):

        self.rules.append(rule_fn)

    # -----------------------------------
    # Evaluate Event
    # ارزیابی رویداد
    # -----------------------------------

    def evaluate(self, event):

        result = {"status": "APPROVED", "matched_rules": [], "risk_override": None}

        # -----------------------------------
        # Execute Rules
        # اجرای قوانین
        # -----------------------------------

        for rule in self.rules:

            try:

                rule_result = rule(event)

                # اگر خروجی قانون None بود
                if not rule_result:

                    continue

                # -----------------------------------
                # BLOCK CONDITION
                # مسدودسازی رویداد
                # -----------------------------------

                if rule_result.get("block"):

                    return {
                        "status": "BLOCKED",
                        "reason": rule_result.get("reason", "POLICY_BLOCKED"),
                        "rule": rule_result.get("rule", "UNKNOWN_RULE"),
                    }

                # -----------------------------------
                # FLAG CONDITION
                # علامت‌گذاری رویداد
                # -----------------------------------

                if rule_result.get("flag"):

                    result["matched_rules"].append(
                        {
                            "rule": rule_result.get("rule", "UNNAMED_RULE"),
                            "reason": rule_result.get("reason", "FLAGGED"),
                            "severity": rule_result.get("severity", "medium"),
                        }
                    )

                # -----------------------------------
                # RISK OVERRIDE
                # بازنویسی سطح ریسک
                # -----------------------------------

                if rule_result.get("risk_override"):

                    result["risk_override"] = rule_result.get("risk_override")

            except Exception as e:

                result["matched_rules"].append(
                    {
                        "rule": "POLICY_ENGINE_ERROR",
                        "reason": str(e),
                        "severity": "critical",
                    }
                )

        # -----------------------------------
        # Final Result
        # خروجی نهایی
        # -----------------------------------

        return result
