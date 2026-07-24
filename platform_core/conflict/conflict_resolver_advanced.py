class ConflictResolverAdvanced:

    def __init__(self):

        self.history = []

    # -----------------------------------
    # resolve conflicts
    # حل تعارض‌ها
    # -----------------------------------

    def resolve(self, event):

        identity = event.get("identity", {})
        behavior = event.get("behavior", {})
        simulation = event.get("simulation", {})

        human_score = 0
        machine_score = 0
        simulation_score = 0

        # -----------------------------------
        # Identity weight
        # وزن هویت
        # -----------------------------------

        if identity.get("identity") == "secure_controller":
            human_score += 50
        else:
            machine_score += 30

        # -----------------------------------
        # Behavior weight
        # وزن رفتار
        # -----------------------------------

        if behavior.get("behavior_type") == "stable":
            human_score += 20
        else:
            machine_score += 10

        # -----------------------------------
        # Simulation weight
        # وزن شبیه‌سازی
        # -----------------------------------

        if simulation.get("best_decision") == "HUMAN_FLOW":
            human_score += 30
        else:
            machine_score += 30

        # -----------------------------------
        # Final decision
        # تصمیم نهایی
        # -----------------------------------

        if human_score >= machine_score:
            decision = "HUMAN_APPROVED"
        else:
            decision = "MACHINE_OVERRIDE"

        result = {
            "human_score": human_score,
            "machine_score": machine_score,
            "decision": decision,
        }

        self.history.append(result)

        return result
