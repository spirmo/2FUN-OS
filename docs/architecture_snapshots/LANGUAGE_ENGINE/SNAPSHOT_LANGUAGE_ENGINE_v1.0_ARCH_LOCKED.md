# ============================================================================
# 2FUN LANGUAGE ENGINE
# TANDIL LANGUAGE ENGINE (TLE)
# ============================================================================
#
# Snapshot ID : SNAPSHOT_LANGUAGE_ENGINE_v1.0_ARCH_LOCKED
#
# Status      : ARCHITECTURE LOCKED
#
# Priority    : ⭐⭐⭐⭐⭐ CRITICAL
#
# Phase       :
# After Mobile MVP
# Before Knowledge Injection
#
# ============================================================================

# PURPOSE

Create one centralized multilingual engine for the entire 2FUN Ecosystem.

The Language Engine will be shared by:

- Mobile Application
- Telegram Game
- Website
- Telegram Bot
- Admin Panel
- Future AI Services

Only one Language Engine exists in the ecosystem.

---

# CORE PRINCIPLES

The Language Engine is completely independent from the Knowledge Engine.

Knowledge Engine stores:

- Concepts
- Questions
- Answers
- Missions
- Sources
- Evidences

Language Engine stores:

- User Interface
- Buttons
- Menus
- Dialogs
- Notifications
- Error Messages
- Shared Public Texts

These two engines are independent.

---

# GOLDEN RULE

No visible text is allowed inside source code.

Forbidden:

Text("Login")

Required:

LanguageEngine.get("BTN_LOGIN")

Every product must read its text through the Language Engine.

---

# MAIN OBJECTIVES

- Support 150 Languages
- Single Translation Repository
- High Translation Quality
- Shared Between All Products
- Future AI Learning
- Zero Duplicate Translations
- Version Control
- Translation Governance

---

# TRANSLATION REPOSITORY

The Translation Repository is the single source of truth.

Future storage:

Phase 1:
SQLite

Phase 2:
PostgreSQL

Each translation record contains:

- Translation Key
- Language
- Translation
- Status
- Version
- Created By
- Verified By
- Created Date
- Updated Date
- Source Type

---

# TRANSLATION STATUS

Each translation has one status.

Draft

AI Generated

Community Reviewed

Approved

Deprecated

---

# AI POLICY

Internal 2FUN AI is NOT responsible for translation.

During early phases the project may use external AI only for initial suggestions.

Possible providers:

- ChatGPT
- Gemini
- DeepL
- Other translation models

External AI never becomes the source of truth.

Only approved translations become official.

---

# LONG TERM GOAL

Create a dedicated 2FUN Translation AI.

Training data:

Only approved translations.

Target:

Completely remove permanent dependency on external AI services.

---

# COMMUNITY TRANSLATION

Native speakers may:

- Suggest translations
- Correct translations
- Vote
- Report mistakes

Community participation is encouraged.

---

# TRANSLATION GOVERNANCE

No single translator is trusted.

Translation quality is determined by:

- Reputation
- Consensus
- Language Examination
- Translation History
- Quality Score

TANDIL Governance performs final validation.

---

# LANGUAGE CERTIFICATION

Future translator levels:

Translator Level 1

Translator Level 2

Senior Translator

Language Validator

Language Reviewer

Permissions depend on Reputation.

---

# LANGUAGE BOOTSTRAP

Initial development language:

Persian (FA)

Other languages are added gradually.

UI translations are manually reviewed.

Large scale translations may initially use AI suggestions.

---

# INDEPENDENCE POLICY

Permanent dependency on external translation providers is forbidden.

External AI is considered a temporary bootstrap tool only.

---

# CONNECTION TO KNOWLEDGE ENGINE

The Knowledge Engine remains independent.

Only when required it requests translations from the Translation Repository.

Knowledge Engine never owns translations.

---

# ARCHITECTURE DECISION

Language Engine is an independent Core Engine inside 2FUN.

It is considered one of the foundational infrastructure modules.

---

# IMPLEMENTATION PRIORITY

⭐⭐⭐⭐⭐ CRITICAL

Implementation starts:

Immediately after Mobile MVP

Before Knowledge Injection

---

# ARCHITECTURE STATUS

LOCKED

Any future modification requires architecture review.
