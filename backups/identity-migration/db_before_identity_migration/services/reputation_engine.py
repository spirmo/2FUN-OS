def calculate_reputation(behavior_signals: dict):

    score = 0

    score += behavior_signals.get("self_awareness", 0) * 2
    score += behavior_signals.get("honesty", 0) * 3
    score += behavior_signals.get("reflection_depth", 0) * 2
    score -= behavior_signals.get("defensiveness", 0) * 2

    if score < 0:
        score = 0

    if score > 10:
        level = "HIGH_TRUST"
    elif score > 6:
        level = "TRUSTED"
    elif score > 3:
        level = "NORMAL"
    else:
        level = "LOW"

    return {
        "score": score,
        "level": level
    }


if __name__ == "__main__":
    sample = {
        "self_awareness": 0,
        "honesty": 1,
        "reflection_depth": 1,
        "defensiveness": 0
    }

    result = calculate_reputation(sample)
    print(result)
