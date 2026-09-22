"""
2FUN / توفان
TANDIL Life Narrative Engine

Functional migration of the Legacy 2FUN GAME Life Narrative v3.
"""

from engines.tandil.life_book.life_book_engine import generate_life_book_v2


def safe_join(items):
    return "، ".join(str(item) for item in items) if items else ""


def generate_life_narrative_v3(user_id: int) -> dict:
    book = generate_life_book_v2(user_id)
    chapters = book["chapters"]

    identity = chapters[0]["content"]
    strengths = chapters[1]["content"]
    weaknesses = chapters[2]["content"]
    timeline = chapters[3]["content"]
    evolution = chapters[4]["content"]
    summary = chapters[5]["content"]

    story = ""

    # -----------------------------
    # OPENING CONTEXT
    # -----------------------------
    story += (
        "این روایت بر اساس تحلیل داده‌های رفتاری، حافظه و الگوهای شخصیتی کاربر شکل گرفته است. "
        "هدف، توصیف مسیر شکل‌گیری هویت و تحول او در سیستم است.\n\n"
    )

    # -----------------------------
    # IDENTITY FLOW
    # -----------------------------
    identity_state = identity["identity_state"]
    traits = identity["dominant_traits"]

    story += (
        f"در بررسی اولیه، وضعیت هویتی کاربر در سطح «{identity_state}» قرار دارد "
        f"و الگوهای رفتاری نشان می‌دهد که ویژگی‌هایی مانند {safe_join(traits)} "
        f"به‌صورت پایدار در ساختار شخصیتی او تکرار شده‌اند. "
    )

    story += (
        "این الگوهای رفتاری در ادامه، در شکل‌گیری نقاط قوت او نیز تأثیر مستقیم داشته‌اند.\n\n"
    )

    # -----------------------------
    # STRENGTHS FLOW
    # -----------------------------
    if strengths:
        story += (
            f"در ادامه تحلیل، مشخص شد که نقاط قوت اصلی او شامل {safe_join(strengths)} است "
            f"که به‌عنوان ستون‌های رفتاری پایدار در تصمیم‌گیری‌ها و واکنش‌های او عمل می‌کنند. "
        )
    else:
        story += (
            "در داده‌های موجود، الگوی مشخص و پایدار از نقاط قوت برجسته مشاهده نمی‌شود. "
        )

    story += "این وضعیت نشان می‌دهد که ساختار شخصیتی هنوز در حال تثبیت است.\n\n"

    # -----------------------------
    # WEAKNESSES FLOW
    # -----------------------------
    if weaknesses:
        story += (
            f"در کنار این نقاط قوت، برخی نشانه‌های چالش در حوزه‌های {safe_join(weaknesses)} مشاهده می‌شود "
            f"که می‌تواند در مسیر رشد آینده نقش تعیین‌کننده‌ای داشته باشد. "
        )
    else:
        story += (
            "در حال حاضر، نشانه قابل توجهی از ضعف رفتاری پایدار ثبت نشده است. "
        )

    story += (
        "این تعادل نسبی میان نقاط قوت و ضعف، وضعیت فعلی رشد را شکل می‌دهد.\n\n"
    )

    # -----------------------------
    # TIMELINE FLOW
    # -----------------------------
    if timeline:
        first = timeline[0]

        story += (
            f"در خط زمانی رفتاری، نخستین نقطه ثبت‌شده با عنوان «{first['title']}» "
            f"نشان‌دهنده آغاز تعاملات سیستم با کاربر است. "
        )

        if len(timeline) > 1:
            story += (
                "در ادامه، رویدادهای بیشتری ثبت شده‌اند که به‌تدریج ساختار شخصیتی او را "
                "قابل مشاهده‌تر کرده‌اند. "
            )

        story += "\n\n"

    # -----------------------------
    # EVOLUTION FLOW
    # -----------------------------
    trajectory = evolution["trajectory"]
    stability = evolution["stability_index"]

    story += (
        f"در تحلیل تحول شخصیتی، مسیر کلی کاربر در وضعیت «{trajectory}» قرار دارد "
        f"و شاخص پایداری رفتاری او برابر با {stability} است. "
    )

    if evolution["signals"]["behavior_shift"] == "IMPROVING":
        story += (
            "این داده‌ها نشان‌دهنده یک روند تدریجی بهبود در الگوهای رفتاری او هستند. "
        )

    story += "\n\n"

    # -----------------------------
    # CLOSING SUMMARY
    # -----------------------------
    story += (
        "در جمع‌بندی کلی، داده‌ها نشان می‌دهد که شخصیت کاربر در حال شکل‌گیری و تثبیت تدریجی است "
        "و مسیر رشد او همچنان در حال تکامل می‌باشد."
    )

    return {
        "user_id": user_id,
        "narrative_version": "3.0",
        "story": story,
    }


__all__ = [
    "safe_join",
    "generate_life_narrative_v3",
]
