import copy


class SimulationEngine:

    def __init__(self):
        self.history = []

    # -----------------------------
    # simulate event
    # شبیه‌سازی رویداد
    # -----------------------------

    def simulate(self, event, context=None):

        context = context or {}

        base_risk = event.get("risk", {}).get("risk_level", "low")

        behavior = event.get("behavior", {})
        identity = event.get("identity", {})
        governance = event.get("governance", {})

        # -----------------------------
        # Human scenario
        # سناریوی انسانی
        # -----------------------------

        human_scenario = {
            "path": "HUMAN_FLOW",
            "risk": base_risk,
            "trust_impact": +5,
            "stability_impact": 0,
            "description": "Human decision path executed",
        }

        # -----------------------------
        # Machine scenario
        # سناریوی ماشینی
        # -----------------------------

        machine_scenario = {
            "path": "MACHINE_FLOW",
            "risk": base_risk,
            "trust_impact": +2,
            "stability_impact": -1,
            "description": "Automated decision path executed",
        }

        # -----------------------------
        # Decision logic
        # منطق تصمیم
        # -----------------------------

        if identity.get("identity") == "secure_controller":
            best = "HUMAN_FLOW"
        else:
            best = "MACHINE_FLOW"

        # -----------------------------
        # Result
        # نتیجه
        # -----------------------------

        result = {
            "human_scenario": human_scenario,
            "machine_scenario": machine_scenario,
            "best_decision": best,
            "base_risk": base_risk,
        }

        self.history.append(result)

        return result
