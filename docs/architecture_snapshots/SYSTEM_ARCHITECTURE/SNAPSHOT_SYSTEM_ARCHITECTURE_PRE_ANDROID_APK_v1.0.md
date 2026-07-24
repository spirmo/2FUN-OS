SNAPSHOT_SYSTEM_ARCHITECTURE_PRE_ANDROID_APK_v1.0

Project Snapshot

2FUN ECOSYSTEM

Date: 2026-07-06

---

STATUS

Architecture Locked

This snapshot records the official state of the project immediately before beginning Android APK implementation for the new 2FUN Super Application.

This document is considered an official governance and architecture checkpoint.

---

PROJECT IDENTITY

Official Ecosystem Name

2FUN OS

This replaces all previous naming used for the main ecosystem repository.

Repository

2FUN-OS

---

PROJECT ECOSYSTEM

The ecosystem is officially divided into three major pillars.

1. 2FUN GAME

Core Business Logic

Responsibilities:

- Governance
- Knowledge Engine
- Question Engine
- Economy
- Reputation
- Mission Engine
- Rule Engine
- TANDIL
- Civilization Logic
- Digital Twin
- Core Intelligence

The Game is the source of business logic and must never depend on UI.

---

2. 2FUN PLATFORM

Responsibilities

- Website
- API
- Dashboard
- Administration
- Statistics
- Reporting
- External Services

Platform consumes services from the Game.

Platform never owns Game Logic.

---

3. 2FUN APP

The final product delivered to users.

Responsibilities

- Super Application
- Game
- Wallet
- Marketplace
- AI Assistant
- Governance
- Missions
- Social
- Economy
- Notifications
- User Profile

The App consumes services from both Game and Platform.

---

OFFICIAL DIRECTORY STRUCTURE

The official root structure of 2FUN OS has been accepted.

2FUN/

- ecosystem/
- platform/
- apps/
- modules/
- shared/
- contracts/
- docs/
- tools/

This architecture is LOCKED.

---

MODULE STRUCTURE

Modules are treated as independent ecosystem components.

Current modules include

- game
- governance
- knowledge
- economy
- wallet
- marketplace
- ai
- social
- tandil
- ecosystem

Each module may contain its own internal engines.

The previous separation between "modules" and "engines" is no longer considered the long-term architecture.

---

CONTRACTS

Contracts have become a mandatory layer.

Official structure

contracts/

- api
- events
- schemas
- messages
- errors
- versions

Purpose

Single Source of Truth for communication between

- Game
- Platform
- App

No module should expose interfaces outside these contracts.

Future governance will reject modules that violate official contracts.

---

ARCHITECTURE PRINCIPLES

The following principles are officially accepted.

Single Source of Truth

Code follows Documents

Execution before Redesign

Migration before Refactoring

Modules communicate only through Contracts

Business Logic belongs only to Game

Platform is Presentation Layer

App is Consumer Layer

---

GOVERNANCE DECISION

Existing Governance inside 2FUN_GAME is accepted as Legacy Source.

No redesign will happen before migration.

Migration policy

Copy

Verify

Integrate

Improve

Never rewrite first.

---

CURRENT MIGRATION STATUS

Migration has NOT started.

Reason

Priority has changed.

Current priority

Android APK

Migration will continue after successful Android deployment.

---

DOCUMENTATION STATUS

The following documents have been reviewed during this phase.

- Original Project README
- Project Vision
- Governance Documents
- Core Architecture
- Colony Architecture
- Official Roadmap
- User Model
- Colony Model
- Events Model
- Ledger Model
- Negative History
- Expulsion Model

These documents are accepted as reference material for future migration.

---

GITHUB STATUS

Official repository

2FUN-OS

Git repository initialized.

Remote configured successfully.

Project identity synchronized.

---

ARCHITECTURE SNAPSHOTS

The project already owns a complete Architecture Snapshot system.

The official location for architecture history remains

docs/architecture_snapshots/

Future snapshots must continue to use this architecture.

No replacement architecture will be introduced.

---

NEXT MILESTONE

The project officially leaves the Architecture Planning phase.

The next milestone becomes

FIRST SUCCESSFUL ANDROID APK

Priority Order

1. Android APK
2. Super Application startup
3. Android Runtime verification
4. Module Migration
5. Governance Migration
6. Full 2FUN OS Integration

---

OFFICIAL FOUNDER DECISION

Architecture Phase

Completed

Migration Phase

Prepared

Android Phase

Started

This snapshot officially marks the transition from architecture planning into implementation of the first Android version of 2FUN OS.

Status

LOCKED
