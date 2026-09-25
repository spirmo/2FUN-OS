import time


class IdentityEngine:

    def __init__(self):

        self.identities = {}

    # -----------------------------------
    # Analyze Identity
    # تحلیل هویت
    # -----------------------------------

    def analyze(self, event):

        source = event.get("source", "UNKNOWN")

        if source not in self.identities:

            self.identities[source] = {
                "identity": "unknown",
                "trust_index": 50,
                "risk_index": 50,
                "stability_index": 50,
                "history": [],
                "created_at": time.time(),
            }

        profile = self.identities[source]

        # -----------------------------------
        # دریافت داده‌ها
        # -----------------------------------

        governance = event.get("governance", {})

        behavior = event.get("behavior", {})

        risk = event.get("risk", {})

        # -----------------------------------
        # Trust Analysis
        # تحلیل اعتماد
        # -----------------------------------

        trust_level = governance.get("trust_level")

        if trust_level == "high":

            profile["trust_index"] += 5

        elif trust_level == "medium":

            profile["trust_index"] += 1

        else:

            profile["trust_index"] -= 5

        # -----------------------------------
        # Risk Analysis
        # تحلیل ریسک
        # -----------------------------------

        risk_level = risk.get("risk_level")

        if risk_level == "high":

            profile["risk_index"] += 10

        elif risk_level == "medium":

            profile["risk_index"] += 5

        else:

            profile["risk_index"] -= 2

        # -----------------------------------
        # Stability Analysis
        # تحلیل پایداری
        # -----------------------------------

        stability = behavior.get("stability_score", 50)

        profile["stability_index"] = stability

        # -----------------------------------
        # Identity Decision
        # تصمیم هویتی
        # -----------------------------------

        if (
            profile["trust_index"] > 80
            and profile["risk_index"] < 30
            and stability > 80
        ):

            profile["identity"] = "trusted_operator"

        elif profile["risk_index"] > 80:

            profile["identity"] = "risky_actor"

        elif stability < 40:

            profile["identity"] = "unstable_entity"

        elif trust_level == "high":

            profile["identity"] = "secure_controller"

        else:

            profile["identity"] = "adaptive_user"

        # -----------------------------------
        # History
        # تاریخچه
        # -----------------------------------

        profile["history"].append(
            {
                "timestamp": time.time(),
                "identity": profile["identity"],
                "trust_index": profile["trust_index"],
                "risk_index": profile["risk_index"],
                "stability_index": profile["stability_index"],
            }
        )

        # -----------------------------------
        # Output
        # خروجی
        # -----------------------------------

        return {
            "source": source,
            "identity": profile["identity"],
            "trust_index": profile["trust_index"],
            "risk_index": profile["risk_index"],
            "stability_index": profile["stability_index"],
        }
