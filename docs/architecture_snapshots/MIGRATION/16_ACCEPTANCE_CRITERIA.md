# Migration Acceptance Criteria


## Purpose

This document defines the conditions required to consider the 2FUN_GAME to 2FUN-OS migration successful.

The migration is accepted only when ownership, lifecycle, data integrity, and event architecture are validated.


# Infrastructure Criteria


## EventBus

Required:

- Single EventBus authority.
- Runtime owns EventBus lifecycle.
- Event schema compatibility.
- Subscriber system working.
- Listener architecture operational.
- Snapshot listeners working.
- Event logging validated.



## Runtime

Required:

- Single runtime initialization.
- Runtime is the only lifecycle authority.
- No duplicated service ownership.
- Module startup registry operational.
- Dependency initialization order validated.



## Database

Required:

- Complete data backup completed.
- Migration validation passed.
- User data preserved.
- Historical snapshots preserved.
- Rollback source available.



# Engine Criteria


## Governance Engine

Required:

- Existing rules preserved.
- Decision engine tests passed.
- Approval flow operational.
- Governance operates through EventBus listeners.
- No direct Game ownership.



## Knowledge Engine

Required:

- Existing concepts preserved.
- Taxonomy preserved.
- Knowledge services accessible.
- Knowledge operates as shared OS capability.



## Identity Engine

Required:

- Users preserved.
- Reputation preserved.
- Roles preserved.
- Identity services separated from Game logic.



## Economy Engine

Required:

- Wallet data preserved.
- Conversion rules preserved.
- Transactions validated.
- Economy events processed through EventBus.



## AI Engine

Required:

- Advisory mode only.
- No governance authority.
- No rule override permission.
- Explainable recommendations.



# Module Criteria


## Game Module

Required:

- Game runs through OS services.
- Events published correctly.
- No loss of gameplay logic.
- No direct ownership of infrastructure.
- No direct access to Governance or Database.



## Other Modules

Required:

- Social module integration validated.
- Marketplace integration validated.
- Wallet integration validated.
- Learning module integration validated.



# Application Criteria


## Mobile / Web / Admin / Telegram

Required:

- API compatibility maintained.
- Authentication flow validated.
- Existing user flows preserved.
- Applications consume platform services only.



# Final Acceptance


Migration is complete when:

- All tests pass.
- Data validation passes.
- Event architecture is operational.
- Runtime ownership is transferred.
- Module ownership is transferred.
- No duplicated infrastructure remains.
- Rollback point is confirmed.
- Architecture Lock can be applied.


# Acceptance Principle

2FUN-OS migration is successful when:

Infrastructure is owned by Platform.

Capabilities are owned by Modules.

Decisions are owned by Engines.

Applications consume OS services.
