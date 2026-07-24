SNAPSHOT_USER_DATABASE_ARCHITECTURE_v1.0_ARCH_LOCKED

PROJECT:
2FUN / TANDIL GOVERNANCE SYSTEM

STATUS:
ARCH LOCKED

VERSION:
1.0

DATE:
2026-06-04

========================================================
PURPOSE

Define the final user database architecture.

All future user-related data must belong to one of the structures defined in this snapshot.

No user attribute may exist outside this architecture.

========================================================
CORE DATABASE STRUCTURE

The user system is composed of:

1. users
2. users_identity
3. users_public
4. users_governance
5. users_hidden
6. users_position

========================================================
TABLE 1
users

ROLE:

Core user registry.

Contains only operational and system identifiers.

FIELDS:

- id
- telegram_id
- username
- user_code
- colony_id
- status
- active
- created_at

PURPOSE:

Root record for all user-related tables.

========================================================
TABLE 2
users_identity

ROLE:

Identity and verification layer.

FIELDS CAPACITY:

20 Required Fields
20 Optional Fields

PURPOSE:

Authentication
Identity Verification
Location Information

EXAMPLES:

- first_name
- last_name
- mobile
- email
- country
- province
- county
- city
- verification_level
- identity_status

========================================================
TABLE 3
users_public

ROLE:

Public user profile.

Visible to ordinary users.

FIELDS CAPACITY:

15 Required Fields
15 Optional Fields

PURPOSE:

Public reputation and activity information.

EXAMPLES:

- rank
- colony_rank
- activity_level
- contribution_score
- social_reputation
- badges
- achievements
- join_date

========================================================
TABLE 4
users_governance

ROLE:

Governance access layer.

Visible only to project organs.

FIELDS CAPACITY:

15 Required Fields
15 Optional Fields

PURPOSE:

Governance evaluation.

EXAMPLES:

- trust_index
- risk_index
- stability_index
- governance_score
- discipline_status
- loyalty_index
- retention_probability
- long_term_participation_index

========================================================
TABLE 5
users_hidden

ROLE:

Hidden analytics layer.

Visible only to system engines.

FIELDS CAPACITY:

15 Required Fields
15 Optional Fields

PURPOSE:

AI and analytics evaluation.

EXAMPLES:

- financial_intelligence
- technical_skill
- leadership
- networking_power
- decision_power
- crisis_management
- learning_index
- innovation_index
- influence_index
- behavior_pattern

========================================================
TABLE 6
users_position

ROLE:

Organizational hierarchy.

FIELDS CAPACITY:

10 Required Fields
10 Optional Fields

PURPOSE:

Project position and authority tracking.

EXAMPLES:

- member
- contributor
- senior_contributor
- colony_leader
- governance_council_member
- founder

========================================================
PROJECT ORGANS

Official project organs:

1. Founders
2. Governance Council

Only these entities possess governance authority.

========================================================
CORE RULE

Every future user attribute must belong to exactly one of the following:

1. users_identity
2. users_public
3. users_governance
4. users_hidden
5. users_position

No attribute may exist outside this structure.

========================================================
DATABASE STATUS

ARCHITECTURE LOCKED

Future versions may extend.

Structural removal is forbidden.

========================================================
END OF SNAPSHOT
