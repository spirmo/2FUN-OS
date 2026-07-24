========================================================
2FUN / TANDIL
CORE HARDENING SYSTEM
XP_HARDENING_v1_DRAFT
========================================================

STATUS:
DRAFT

PURPOSE:
Prevent abuse, farming, artificial growth,
and low-quality progression.

--------------------------------------------------------
1. XP CURVE
--------------------------------------------------------

def required_xp(level):

    base = 50

    return int(base * (level ** 1.75))

--------------------------------------------------------
2. BASE XP CALCULATION
--------------------------------------------------------

def calculate_xp(user):

    stars = getattr(user, "stars", 0)
    credit = getattr(user, "credit", 0)
    rank_step = getattr(user, "rank_step", 0)
    violations = getattr(user, "violations", 0)

    xp = (
        stars * 1.5 +
        credit * 1.0 +
        rank_step * 2.0
    ) - (violations * 10)

    return max(int(xp), 0)

--------------------------------------------------------
3. SOFT CAP SYSTEM
--------------------------------------------------------

def soft_cap(xp):

    if xp <= 120:
        return xp

    extra = xp - 120

    return 120 + (extra * 0.3)

--------------------------------------------------------
4. DECAY SYSTEM
--------------------------------------------------------

def apply_decay(user):

    if user.active == 0:
        return 0.7

    return 1.0

--------------------------------------------------------
5. ANTI ABUSE
--------------------------------------------------------

def abuse_penalty(user):

    if user.violations > 3:
        return 0.5

    if user.violations > 0:
        return 0.8

    return 1.0

--------------------------------------------------------
6. ADVANCED XP MODEL
--------------------------------------------------------

XP COMPONENTS:

1. Activity XP
2. Quality XP
3. Trust XP
4. Impact XP

--------------------------------------------------------
7. ADVANCED XP CALCULATION
--------------------------------------------------------

def calculate_xp_v2(user):

    activity = user.stars * 1.0

    quality = user.credit * 1.5

    trust = max(
        0,
        100 - user.violations * 20
    )

    impact = (
        user.social_reputation * 2.0
    )

    xp = (
        activity +
        quality +
        trust +
        impact
    )

    return int(xp)

--------------------------------------------------------
8. ANTI FARM INTELLIGENCE
--------------------------------------------------------

def anti_farm_multiplier(user):

    if user.repeated_actions > 50:
        return 0.3

    if user.similar_patterns > 20:
        return 0.6

    return 1.0

--------------------------------------------------------
9. FINAL XP
--------------------------------------------------------

def final_xp_v2(user):

    base = calculate_xp_v2(user)

    anti = anti_farm_multiplier(user)

    return int(base * anti)

--------------------------------------------------------
NOTES
--------------------------------------------------------

This document is not executable.

It is an architectural draft.

Implementation must occur after:

- User identity model lock
- XP model lock
- Governance model lock
- Database schema finalization

========================================================
END OF DOCUMENT
========================================================
