def analyze_answer(question: str, answer: str):
    
    signals = {
        "self_awareness": 0,
        "honesty": 0,
        "reflection_depth": 0,
        "defensiveness": 0
    }

    text = answer.lower()

    # ساده ولی قابل توسعه
    if "نمی‌دانم" in answer:
        signals["self_awareness"] += 1

    if len(answer) > 50:
        signals["reflection_depth"] += 1

    if "اشتباه" in answer or "غلط" in answer:
        signals["honesty"] += 1

    if "دیگران" in answer:
        signals["defensiveness"] += 1

    return signals


if __name__ == "__main__":
    q = "خودت را توصیف کن"
    a = "من فکر می‌کنم گاهی در تصمیم‌گیری اشتباه می‌کنم و هنوز کامل خودم را نمی‌شناسم"

    result = analyze_answer(q, a)
    print(result)
