from modules.knowledge.trait_registry import TRAITS


DOMAIN_TRAIT_FILES = {
    "ISLAMIC_EDUCATION": {
        "صداقت": "HONESTY",
        "راستگویی": "HONESTY",
        "عدالت": "JUSTICE",
        "منصف": "JUSTICE",
        "صبر": "PATIENCE",
        "شکیبایی": "PATIENCE",
        "امانت": "TRUSTWORTHINESS",
        "امانتداری": "TRUSTWORTHINESS",
        "مسئولیت": "RESPONSIBILITY",
        "مسئولیت پذیری": "RESPONSIBILITY",
        "کنترل نفس": "SELF_CONTROL",
        "خویشتنداری": "SELF_CONTROL",
        "شکر": "GRATITUDE",
        "شکرگزاری": "GRATITUDE",
    },
    "ISLAMIC_CULTURE": {
        "احترام": "RESPECT",
        "همکاری": "COOPERATION",
        "همدلی": "EMPATHY",
        "وفاداری": "LOYALTY",
        "هویت فرهنگی": "CULTURAL_IDENTITY",
        "روحیه جمعی": "COMMUNITY_SPIRIT",
    },
    "ISLAMIC_ECONOMICS": {
        "انضباط مالی": "FINANCIAL_DISCIPLINE",
        "مدیریت منابع": "RESOURCE_MANAGEMENT",
        "مسئولیت مالی": "ECONOMIC_RESPONSIBILITY",
        "تولید ثروت": "VALUE_CREATION",
        "کسب حلال": "HONESTY",
        "عدالت اقتصادی": "JUSTICE",
    },
    "ANCIENT_IRAN": {
        "هویت ایرانی": "CULTURAL_IDENTITY",
        "تمدن": "CIVILIZATION_AWARENESS",
        "تمدن سازی": "CIVILIZATION_AWARENESS",
        "تفکر بلندمدت": "LONG_TERM_THINKING",
        "میراث فرهنگی": "LEGACY_PRESERVATION",
        "حفظ میراث": "LEGACY_PRESERVATION",
        "حکمت ایرانی": "STRATEGIC_THINKING",
    },
    "SOCIOLOGY_OF_NATIONS": {
        "اعتماد": "TRUST_BUILDING",
        "اعتماد اجتماعی": "TRUST_BUILDING",
        "همکاری": "COOPERATION",
        "مسئولیت اجتماعی": "SOCIAL_RESPONSIBILITY",
        "روحیه جمعی": "COMMUNITY_SPIRIT",
        "حل تعارض": "CONFLICT_RESOLUTION",
        "همدلی": "EMPATHY",
    },
    "GENERAL_KNOWLEDGE": {
        "کنجکاوی": "CURIOSITY",
        "یادگیری": "LEARNING_MINDSET",
        "تفکر انتقادی": "CRITICAL_THINKING",
        "تفکر تحلیلی": "ANALYTICAL_THINKING",
        "حل مسئله": "PROBLEM_SOLVING",
    },
    "GAME_AND_PROJECT": {
        "رهبری": "LEADERSHIP",
        "تفکر پروژه ای": "PROJECT_THINKING",
        "تصمیم گیری": "DECISION_MAKING",
        "پاسخگویی": "ACCOUNTABILITY",
        "پشتکار": "PERSISTENCE",
        "تفکر راهبردی": "STRATEGIC_THINKING",
    },
    "ISLAMIC_LIFE_ADAB": {
        "احترام": "RESPECT",
        "کنترل خشم": "SELF_CONTROL",
        "کنترل نفس": "SELF_CONTROL",
        "راستگویی": "HONESTY",
        "تواضع": "HUMILITY",
        "شکرگزاری": "GRATITUDE",
        "رحمت": "COMPASSION",
        "امانتداری": "TRUSTWORTHINESS",
        "صبر": "PATIENCE",
        "وفای به عهد": "LOYALTY",
    },
}


def normalize_trait(value: str):
    if not value:
        return None

    value = value.strip()

    if value in TRAITS:
        return value

    for code, data in TRAITS.items():
        if value == data.get("fa"):
            return code

    for code, data in TRAITS.items():
        if value.lower() == data.get("en", "").lower():
            return code

    return value.upper()
