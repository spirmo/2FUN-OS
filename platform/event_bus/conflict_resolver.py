class ConflictResolver:
    """
    Real Conflict Resolver (حل‌کننده واقعی تعارض)
    تصمیم‌گیری واقعی بین HUMAN / MACHINE / RULES
    """

    def __init__(self):

        # وزن‌ها (Weights = وزن اهمیت)
        self.weights = {
            "HUMAN": 1.0,  # انسان = بیشترین قدرت تصمیم
            "MACHINE": 0.7,  # ماشین = کمک‌کننده
            "RULE": 0.9,  # قوانین سیستم
        }

        # اولویت‌ها (Priority = اولویت تصمیم)
        self.priority_order = ["HUMAN", "RULE", "MACHINE"]

    def resolve(self, events):
        """
        events = لیست تصمیم‌ها
        """

        if not events:
            return {"decision": None, "reason": "no_events"}

        scored = []

        # 1. امتیازدهی (Scoring = امتیازدهی)
        for event in events:

            source = event.get("source")

            base_weight = self.weights.get(source, 0.5)

            # امتیاز ترکیبی
            score = base_weight * 100

            # اگر event ریسک بالا داشت، امتیاز کم شود
            risk = event.get("risk", {}).get("risk_level", "low")

            if risk == "high":
                score -= 40
            elif risk == "medium":
                score -= 15

            scored.append((score, event))

        # 2. مرتب‌سازی (Sorting = مرتب‌سازی)
        scored.sort(reverse=True, key=lambda x: x[0])

        best_score, best_event = scored[0]

        # 3. بررسی اولویت انسانی (Human Priority Override)
        human_events = [e for s, e in scored if e.get("source") == "HUMAN"]

        if human_events:
            # اگر HUMAN وجود دارد و خیلی ضعیف نیست، override می‌شود
            human_best = human_events[0]

            if best_event.get("source") != "HUMAN":

                return {
                    "decision": human_best,
                    "score": best_score,
                    "rule": "human_override",
                }

        # 4. تصمیم نهایی
        return {
            "decision": best_event,
            "score": best_score,
            "rule": "weighted_decision",
        }
