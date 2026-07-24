========================================================
PROJECT SNAPSHOT
2FUN GAME / IDENTITY SYSTEM
SNAPSHOT_IDENTITY_v1.0_ARCH_LOCKED
========================================================

DATE:
2026-06-02

STATUS:
ARCHITECTURE LOCKED
READY FOR IMPLEMENTATION

========================================================
1. IDENTITY MODEL
========================================================

Each user owns:

1. PERSONAL_CODE
2. HOME_COLONY_ID
3. INTERNAL_IDENTITY_CODE

--------------------------------------------------------
PERSONAL_CODE
--------------------------------------------------------

Length:
8 digits

Range:

00000001
...
99999999

Generation:

Sequential allocation

Released after permanent removal.

Examples:

00000001
00000002
00000003

--------------------------------------------------------
HOME_COLONY_ID
--------------------------------------------------------

Length:
6 digits

Range:

000001
...
999999

Generation:

Sequential allocation

NOT random.

Examples:

000001
000002
000003

HOME_COLONY_ID belongs permanently to the user's
origin colony.

It never changes.

========================================================
2. USER IDENTIFIERS
========================================================

--------------------------------------------------------
HOME COLONY DISPLAY
--------------------------------------------------------

Inside user's home colony:

Only PERSONAL_CODE is visible.

Example:

12345678

--------------------------------------------------------
HOST COLONY DISPLAY
--------------------------------------------------------

Inside host colonies:

HOME_COLONY_ID + PERSONAL_CODE

Example:

00012312345678

Length:

14 digits

This identifies guest members.

Native members show only:

12345678

Guest members show:

00012312345678

Therefore guest status is recognizable.

Host colony members cannot determine the exact colony
name from the identifier.

They only know the member is a guest.

========================================================
3. INTERNAL IDENTITY CODE
========================================================

Structure:

COUNTRY(3)
PROVINCE(2)
COUNTY(2)
CITY(2)
PERSONAL_CODE(8)

Total:

17 digits

Example:

12345678912345678

--------------------------------------------------------
PARTIAL IDENTITY
--------------------------------------------------------

Before full verification:

123-**-**-**-12345678

Unknown location sections remain masked.

--------------------------------------------------------
FULL IDENTITY
--------------------------------------------------------

After verification:

123-45-67-89-12345678

========================================================
4. LOCATION VISIBILITY
========================================================

Colony Leader:

Country
Province
County
City
Personal Code

First Deputy:

Country
Province
County
Personal Code

Second Deputy:

Country
Province
Personal Code

Normal Member:

Personal Code only

========================================================
5. USER STATUS MODEL
========================================================

ACTIVE

User is active and participating.

--------------------------------------------------------

DORMANT

User exists but is inactive.

No activity.

--------------------------------------------------------

REMOVED

User permanently removed from project.

Effects:

PERSONAL_CODE released
USER_ID removed

Historical records remain preserved.

========================================================
6. COLONY MODEL
========================================================

Every colony owns:

COLONY_ID
COLONY_NAME

Example:

COLONY_ID:
000123

COLONY_NAME:
Phoenix

COLONY_ID is permanent.

COLONY deletion is forbidden.

Colonies may weaken or strengthen.

Colonies may receive support.

Colonies never disappear.

========================================================
7. HOME COLONY PRINCIPLE
========================================================

Every user has exactly one:

HOME_COLONY

The colony that originally accepted the user.

HOME_COLONY never changes.

Users may become guests in other colonies.

Users never lose HOME_COLONY identity.

========================================================
8. TRAVEL LOG
========================================================

All guest movements must be stored.

Purpose:

Allow origin colony to track user movements.

Suggested storage:

users_extension.reserved1

Format:

JSON

Example:

[
  {
    "colony_id": "000321",
    "joined_at": "2026-06-02",
    "left_at": "2026-06-10"
  },
  {
    "colony_id": "000789",
    "joined_at": "2026-07-01",
    "left_at": null
  }
]

========================================================
9. DATABASE STATUS
========================================================

Existing tables:

users
users_extension
colonies
colonies_extension
colony_memberships

Current status field:

ACTIVE
DORMANT

REMOVED reserved for future implementation.

========================================================
10. IMPLEMENTATION PENDING
========================================================

identity_engine.py

Functions:

generate_personal_code()

generate_colony_id()

generate_guest_id()

generate_identity_code()

travel_log_manager()

guest_tracking()

========================================================
END OF SNAPSHOT
SNAPSHOT_IDENTITY_v1.0_ARCH_LOCKED
========================================================
