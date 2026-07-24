# EventBus Migration Architecture v1.0

## Purpose

This document defines the migration strategy of the existing 2FUN_GAME EventBus into the 2FUN-OS platform infrastructure.

The migration goal is preservation, not rewrite.


# Current State (AS-IS)

Current EventBus location:
TANDIL_GOVERNANCE/core_engine/event_bus/

Current components:

- event_bus.py
- async_queue.py
- event_validator.py
- event_logger.py
- risk_analyzer.py
- conflict_resolver.py
- governance_score.py
- handlers.py
- event_rules.json


Current runtime flow:

Game Application
|
v
EventBus
|
+--> Governance
+--> Monitoring
+--> Hooks


# Current Integration

Application emits events:

app/main.py

bus.emit(
    source="telegram",
    event_type="ACTIVITY",
    target="governance",
    value={}
)


Runtime attaches listeners:

core/governance/bootstrap.py

bus.subscribe(listener)


Existing listener:

RealtimeMonitor.handler


# Migration Target (TO-BE)

New location:

2FUN-OS/platform/event_bus/


Ownership:

Platform Infrastructure


Responsibilities:

- Event publishing
- Event routing
- Event validation
- Event tracing
- Event history


# Architectural Rule

EventBus does not make final decisions.

EventBus only transports events.

Decision authority belongs to:

- Governance Engine
- Policy Engine
- Rule Engine


# Future Event Flow

modules/game
|
| emit event
v
platform/event_bus
|
+----------------+
|                |
v                v
Governance Engine   Economy Engine
|
v
Identity Engine


# Migration Strategy

Phase 1:
Freeze current EventBus behavior.

Phase 2:
Create platform/event_bus package.

Phase 3:
Move listeners independently.

Phase 4:
Connect Game module to new EventBus.

Phase 5:
Remove old imports only after validation.


# Preservation Rules

- No rewrite of EventBus logic.
- No deletion of current implementation.
- Existing tests remain valid.
- Migration requires compatibility layer.


# Acceptance Criteria

Migration succeeds when:

- Game emits events through platform EventBus.
- Governance receives events unchanged.
- Monitoring listeners work.
- Event snapshots remain compatible.
