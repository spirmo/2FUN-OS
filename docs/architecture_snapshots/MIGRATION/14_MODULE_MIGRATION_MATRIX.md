# Module Migration Matrix


## Purpose

This document defines the migration mapping between current 2FUN_GAME components and target 2FUN-OS modules.

The goal is clear ownership, controlled migration, and zero responsibility overlap.



# Migration Table


| Current Location | Target Location | Status |
|---|---|---|
| core/action | modules/game/action | Planned |
| core/cognition | engines/tandil/cognition | Planned |
| core/profile | modules/profile | Planned |
| core/knowledge | modules/knowledge | Planned |
| core/memory | engines/tandil/memory | Planned |
| core/twin | engines/tandil/digital_twin | Planned |
| TANDIL_GOVERNANCE | engines/governance | Planned |
| EventBus | platform/event_bus | Planned |
| core/runtime | backend/runtime | Planned |
| db | backend/database | Planned |
| wallet logic | modules/wallet | Planned |
| economy logic | modules/economy | Planned |
| AI components | engines/ai | Planned |



# Migration Order


## 1. Infrastructure

Components:

- Runtime
- EventBus
- Database
- Platform Services


## 2. Core Engines

Components:

- Identity Engine
- Knowledge Engine
- Governance Engine
- Economy Engine
- AI Engine


## 3. Modules

Components:

- Game Module
- Social Module
- Marketplace Module
- Wallet Module
- Learning Module
- Mission Module


## 4. Applications

Components:

- Mobile
- Web
- Admin
- Telegram Client



# Ownership Mapping


| Component | Target Owner |
|---|---|
| Runtime | Platform Runtime |
| EventBus | Platform Infrastructure |
| core/action | Game Module |
| core/cognition | Cognitive Engine |
| core/profile | Identity Engine |
| core/knowledge | Knowledge Engine |
| core/memory | Memory Engine |
| core/twin | Digital Twin Engine |
| TANDIL_GOVERNANCE | Governance Engine |
| db | Backend Database Layer |
| wallet logic | Wallet Module |
| economy logic | Economy Engine |
| AI components | AI Engine |



# Dependency Mapping


| Target Module | Depends On |
|---|---|
| modules/game | Runtime, EventBus, Identity, Economy, Knowledge |
| modules/social | Identity, EventBus |
| modules/wallet | Identity, Economy |
| marketplace | Wallet, Economy, Identity |
| governance engine | EventBus, Policy System, Memory |
| knowledge engine | Database, Taxonomy, EventBus |
| AI engine | Knowledge Engine, EventBus |



# Real Migration Status


| Component | Current State |
|---|---|
| EventBus | Existing Prototype |
| Governance Engine | Existing |
| Snapshot System | Existing |
| Knowledge Engine | Existing |
| Economy Layer | Existing Partial |
| Game Logic | Existing in 2FUN_GAME |
| Game Migration | Pending |
| Mobile Application | Reconstruction Phase |



# EventBus Migration Rule


EventBus is a platform-level infrastructure.

Game modules must not own EventBus.


Communication model:


Game Module

↓

EventBus

↓

Event Listeners

↓

Engines

↓

Decision / Action Events



All future modules communicate through events.



# Game Preservation Rule


The existing 2FUN_GAME logic will not be rewritten.

Migration includes:

- Event contract migration
- Runtime integration
- Identity connection
- Economy connection
- Governance hooks connection


Old implementation remains reference until migration completion.



# Migration Rules


- No module migration without dependency verification.
- No deletion before validation.
- Every migrated component requires tests.
- Every migrated component requires snapshot.
- Every migration requires rollback possibility.
- Old paths remain reference until migration completion.



# Final Goal


A complete 2FUN-OS ecosystem where:

- Every module has clear ownership.
- Infrastructure has single authority.
- Engines provide shared capabilities.
- Applications consume OS services.
