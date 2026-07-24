DATABASE_MIGRATION_PLAN_v1

PROJECT:
2FUN / TANDIL GOVERNANCE SYSTEM

STATUS:
PRE-IMPLEMENTATION

VERSION:
1.0

DATE:
2026-06-04

========================================================
PURPOSE

Define database migration path from legacy user
structure to final user architecture.

========================================================
MASTER USER KEY

PRIMARY USER REFERENCE:

user_code

All user-related tables must use:

user_code TEXT UNIQUE

as the primary user reference.

Internal database id must never be used
as the architecture reference key.

========================================================
CORE TABLE

users

ROLE:

Core operational user registry.

FIELDS:

- id
- telegram_id
- username
- user_code
- colony_id
- status
- active
- joined_at

========================================================
TABLE
users_identity

CAPACITY:

20 Required Fields
20 Optional Fields

CORE FIELDS:

- user_code
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

OPTIONAL RESERVE:

- reserved01
- reserved02
- reserved03
- reserved04
- reserved05
- reserved06
- reserved07
- reserved08
- reserved09
- reserved10
- reserved11
- reserved12
- reserved13
- reserved14
- reserved15
- reserved16
- reserved17
- reserved18
- reserved19
- reserved20

========================================================
TABLE
users_public

CAPACITY:

15 Required Fields
15 Optional Fields

CORE FIELDS:

- user_code
- rank
- colony_rank
- activity_level
- contribution_score
- social_reputation
- badges
- achievements
- join_date

OPTIONAL RESERVE:

- reserved01
- reserved02
- reserved03
- reserved04
- reserved05
- reserved06
- reserved07
- reserved08
- reserved09
- reserved10
- reserved11
- reserved12
- reserved13
- reserved14
- reserved15

========================================================
TABLE
users_governance

CAPACITY:

15 Required Fields
15 Optional Fields

CORE FIELDS:

- user_code
- trust_index
- risk_index
- stability_index
- governance_score
- discipline_status
- violation_history
- loyalty_index
- retention_probability
- long_term_participation_index

OPTIONAL RESERVE:

- reserved01
- reserved02
- reserved03
- reserved04
- reserved05
- reserved06
- reserved07
- reserved08
- reserved09
- reserved10
- reserved11
- reserved12
- reserved13
- reserved14
- reserved15

========================================================
TABLE
users_hidden

CAPACITY:

15 Required Fields
15 Optional Fields

CORE FIELDS:

- user_code
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

OPTIONAL RESERVE:

- reserved01
- reserved02
- reserved03
- reserved04
- reserved05
- reserved06
- reserved07
- reserved08
- reserved09
- reserved10
- reserved11
- reserved12
- reserved13
- reserved14
- reserved15

========================================================
TABLE
users_position

CAPACITY:

10 Required Fields
10 Optional Fields

CORE FIELDS:

- user_code
- member_status
- contributor_status
- senior_contributor_status
- colony_leader_status
- governance_council_status
- founder_status

OPTIONAL RESERVE:

- reserved01
- reserved02
- reserved03
- reserved04
- reserved05
- reserved06
- reserved07
- reserved08
- reserved09
- reserved10

========================================================
LEGACY COMPONENT

users_extension

STATUS:

LEGACY

Must remain untouched until migration
is fully completed.

========================================================
MIGRATION ORDER

STEP 1

Create:

- users_identity
- users_public
- users_governance
- users_hidden
- users_position

STEP 2

Populate test records.

STEP 3

Validate architecture.

STEP 4

Transfer future production data.

STEP 5

Retire users_extension.

========================================================
END OF DOCUMENT
