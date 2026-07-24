import time


class BehavioralEngine:

    def __init__(self):

        # حافظه موقت رفتار
        self.user_profiles = {}

    # -----------------------------------
    # ثبت و تحلیل رفتار
    # -----------------------------------

    def analyze(self, event, memory):

        source = event.get("source", "UNKNOWN")

        if source not in self.user_profiles:

            self.user_profiles[source] = {
                "total_events": 0,
                "risk_events": 0,
                "safe_events": 0,
                "mode_changes": 0,
                "stability_score": 100,
                "risk_tendency": 0,
                "behavior_type": "unknown",
            }

        profile = self.user_profiles[source]

        profile["total_events"] += 1

        # -----------------------------------
        # تحلیل ریسک
        # -----------------------------------

        risk = event.get("risk", {}).get("risk_level")

        if risk == "high":
            profile["risk_events"] += 1
            profile["risk_tendency"] += 10

        elif risk == "medium":
            profile["risk_tendency"] += 5

        else:
            profile["safe_events"] += 1
            profile["risk_tendency"] -= 2

        # -----------------------------------
        # تشخیص تغییر رفتار
        # -----------------------------------

        if event.get("event_type") == "update":
            profile["mode_changes"] += 1

        # -----------------------------------
        # محاسبه stability (پایداری)
        # -----------------------------------

        profile["stability_score"] = max(
            0, 100 - profile["mode_changes"] * 5 - profile["risk_events"] * 10
        )

        # -----------------------------------
        # تعیین نوع رفتار
        # -----------------------------------

        if profile["risk_tendency"] > 20:
            profile["behavior_type"] = "risky"

        elif profile["stability_score"] > 80:
            profile["behavior_type"] = "stable"

        elif profile["risk_tendency"] < 0:
            profile["behavior_type"] = "safe"

        else:
            profile["behavior_type"] = "normal"

        # -----------------------------------
        # خروجی تحلیل
        # -----------------------------------

        return {
            "source": source,
            "behavior_type": profile["behavior_type"],
            "stability_score": profile["stability_score"],
            "risk_tendency": profile["risk_tendency"],
            "total_events": profile["total_events"],
        }
