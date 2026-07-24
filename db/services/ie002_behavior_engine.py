def analyze_trust_behavior(interactions: list):

    signals = {
        "trustworthiness": 0,
        "honesty": 0,
        "consistency": 0,
        "manipulation_risk": 0
    }

    for text in interactions:

        text = text.lower()

        if "قول" in text or "متعهد" in text:
            signals["trustworthiness"] += 1

        if "دروغ" in text or "نادرست" in text:
            signals["honesty"] -= 1

        if "همیشه" in text:
            signals["consistency"] += 1

        if "مخفی" in text or "پنهان" in text:
            signals["manipulation_risk"] += 1

    return signals


if __name__ == "__main__":

    sample = [
        "من همیشه به قولم پایبندم",
        "این موضوع را پنهان کردم",
        "او دروغ گفت"
    ]

    result = analyze_trust_behavior(sample)
    print(result)
