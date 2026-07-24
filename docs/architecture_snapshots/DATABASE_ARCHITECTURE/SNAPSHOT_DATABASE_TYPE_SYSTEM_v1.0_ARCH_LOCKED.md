SNAPSHOT_DATABASE_TYPE_SYSTEM_v1.0_ARCH_LOCKED

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

Define the official data type standard for all
database tables in the 2FUN system.

This snapshot guarantees consistency across all
user-related, governance, and analytics layers.

No table may deviate from these data type rules.

========================================================
GLOBAL DATA TYPE RULES

1. All numeric metrics must be explicitly typed
   as INTEGER or REAL.

2. All timestamps must use DATETIME format.

3. All states must be TEXT (ENUM-like controlled values).

4. All identifiers must be TEXT or INTEGER,
   depending on role definition.

5. No ambiguous or implicit typing is allowed.

========================================================
TYPE DEFINITIONS

---

TEXT

Used for:

- Names
- Codes
- Labels
- Status fields
- Serialized small data

Examples:

username
country
rank
identity_status

---

INTEGER

Used for:

- Counts
- Levels
- Steps
- Flags (0/1)
- Discrete metrics

Examples:

stars
violations
activity_level
rank_step
verification_level

---

REAL

Used for:

- Scores
- Probabilities
- Indexes
- AI metrics

Examples:

trust_index
risk_index
social_reputation
governance_score
financial_intelligence

---

DATETIME

Used for:

- All time tracking

Examples:

joined_at
created_at
last_active_at

========================================================
SYSTEM DESIGN RULE

Every field in the database MUST strictly follow
one of the defined data types.

No mixed or undefined types are allowed.

========================================================
ARCHITECTURAL GUARANTEE

This type system ensures:

- Predictable database behavior
- Stable migrations
- AI compatibility
- Governance scalability
- XP system consistency

========================================================
LOCK STATUS

ARCHITECTURE LOCKED

No modifications allowed except extension
via future versioning.

========================================================
END OF SNAPSHOT
