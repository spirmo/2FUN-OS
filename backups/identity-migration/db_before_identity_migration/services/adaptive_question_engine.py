import random

DOMAINS = [
    "ISLAMIC_EDUCATION",
    "ISLAMIC_CULTURE",
    "ISLAMIC_ECONOMICS",
    "ANCIENT_IRAN",
    "SOCIOLOGY_OF_NATIONS",
    "GENERAL_KNOWLEDGE",
    "GAME_AND_PROJECT"
]

def generate_next_question(context, action_result):

    last_domain = context.get("last_domain")

    # 🎯 جلوگیری از تکرار دامنه پشت سر هم
    available_domains = [d for d in DOMAINS if d != last_domain]

    domain = random.choice(available_domains)

    base_questions = {
        "GENERAL_KNOWLEDGE": "اگر بخوای یک تجربه مهم از زندگی‌ات تعریف کنی چی می‌گی؟",
        "SOCIOLOGY_OF_NATIONS": "فکر می‌کنی جامعه چطور روی تصمیم‌های انسان اثر می‌گذارد؟",
        "GAME_AND_PROJECT": "اگر بخوای یک بازی طراحی کنی که مردم رشد کنن، چطور می‌سازیش؟"
    }

    question = base_questions.get(
        domain,
        "نظر تو درباره این موضوع چیه؟"
    )

    return {
        "domain": domain,
        "question": question
    }
