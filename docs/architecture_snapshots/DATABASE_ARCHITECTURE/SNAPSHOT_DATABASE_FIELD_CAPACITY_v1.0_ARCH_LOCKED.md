SNAPSHOT_DATABASE_FIELD_CAPACITY_v1.0_ARCH_LOCKED

PROJECT:
2FUN / TANDIL GOVERNANCE SYSTEM

STATUS:
ARCHITECTURE LOCKED

VERSION:
1.0

DATE:
2026-06-04

========================================================
PURPOSE

Define strict field capacity rules for all user-related
database tables in the 2FUN system.

This snapshot ensures predictable expansion limits
and prevents uncontrolled schema growth.

========================================================
GLOBAL RULE

Each table must define:

- REQUIRED FIELDS
- OPTIONAL FIELDS

Total capacity is fixed at design time.

No table is allowed to exceed its defined capacity
without version upgrade.

========================================================
TABLE CAPACITY DEFINITIONS

---

users_identity

CAPACITY:
20 Required + 20 Optional

RULE:
Identity data must be complete and structured.

USAGE:
Authentication + Identity + Location

---

users_public

CAPACITY:
15 Required + 15 Optional

RULE:
Public data must remain lightweight and readable.

USAGE:
Rank + Activity + Reputation

---

users_governance

CAPACITY:
15 Required + 15 Optional

RULE:
Governance data must be analytical and stable.

USAGE:
Trust + Risk + Loyalty + Governance Score

---

users_hidden

CAPACITY:
15 Required + 15 Optional

RULE:
Hidden analytics must support AI decision systems.

USAGE:
Behavior + Intelligence + Influence metrics

---

users_position

CAPACITY:
10 Required + 10 Optional

RULE:
Position data must represent hierarchy only.

USAGE:
Roles + Status + Organizational Level

========================================================
EXPANSION POLICY

1. No table may exceed defined capacity.
2. Any expansion requires:
   - New Snapshot Version
   - Migration Plan Update
   - Backward Compatibility Review

========================================================
SYSTEM IMPACT

This rule ensures:

- Controlled schema growth
- Predictable migrations
- Stable AI interpretation
- Governance consistency
- XP system balance

========================================================
LOCK STATUS

ARCHITECTURE LOCKED

No structural changes allowed without version upgrade.

========================================================
END OF SNAPSHOT
