# KNOWLEDGE INJECTION MVP v1.1
# ARCHITECTURE LOCKED

---

## KD-001
### Minimum Dataset

Mandatory fields:

- Node ID
- Persian Title
- Category
- Creator
- Create Date

A node cannot exist without these fields.

---

## KD-002
### Optional Dataset

Optional fields:

- Canonical Meaning
- Definition
- Source
- English Translation
- Arabic Translation
- Other Languages
- Related Concepts
- Questions
- Missions
- Tags
- Difficulty
- Notes

---

## KD-003
### Reward Based Completion

Optional fields are never mandatory.

Each completed field grants its own reward.

Example:

Concept
+10 XP

Canonical Meaning
+5 XP

Definition
+10 XP

Source
+15 XP

English Translation
+5 XP

Arabic Translation
+5 XP

Question
+10 XP

Mission
+15 XP

---

## KD-004
### Distributed Ownership

Every field has its own owner.

Example:

Concept → Developer A

Canonical Meaning → Developer B

Definition → Developer C

Source → Developer D

Each developer receives rewards only for the first approved completion of that field.

---

## KD-005
### History

Every field stores:

- Creator
- Last Editor
- Create Date
- Edit Date

No information is deleted.

---

## KD-006
### Approval Pipeline

Draft

↓

Minimum Check

↓

Under Review

↓

Approved

↓

Published

↓

Archived

Only Published nodes become active inside the ecosystem.

---

## KD-007
### Minimum Check Engine

Nodes failing minimum requirements receive:

Status = NEED_COMPLETION

---

## KD-008
### Completion Queue

Incomplete nodes enter

Completion Queue

where they wait for completion.

---

## KD-009
### Completion Team

Developers may complete unfinished nodes.

Rewards:

- XP
- SHIR
- Reputation

---

## KD-010
### Reward Split

Example:

30%

Immediate reward

+

70%

Released after Published

---

## KD-011
### Reward Release

Final rewards are released only after

Published

---

## KD-012
### Knowledge Completion Engine

A dedicated engine called

Knowledge Completion Engine (KCE)

manages

- Completion Queue
- Completion Tasks
- Reward Distribution
- Reward Release
- Ownership
- Minimum Validation

---

## KD-013
### Language Engine

Translations are generated from

Canonical Meaning

↓

Definition

↓

Translations

Never from Persian directly.

---

## KD-014
### Knowledge Completeness

Every node stores a completeness percentage.

Example:

🟥 25%

🟨 60%

🟩 90%

⭐ 100%

This percentage is used for rewards and progress tracking.
