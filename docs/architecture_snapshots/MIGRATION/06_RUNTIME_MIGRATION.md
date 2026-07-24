# Runtime Migration Strategy

## Purpose

This document defines the migration strategy from the current 2FUN_GAME runtime layer to the 2FUN-OS runtime architecture.


# Current Runtime

Location:

2FUN_GAME/core/governance/runtime.py


Current responsibilities:

- Create global EventBus instance
- Attach governance system
- Attach monitoring system
- Provide runtime access to event communication


Current flow:

Application Start

↓

Runtime Initialization

↓

Create EventBus

↓

Attach Governance

↓

Attach Monitoring

↓

System Ready


## Current Runtime Implementation Mapping (AS-IS)

Actual implementation:

- app/main.py is the current application entry point.
- core/governance/runtime.py creates the global EventBus singleton.
- attach_governance() connects governance layer to EventBus.
- attach_monitoring() registers monitoring listeners.
- TANDIL_GOVERNANCE runtime_context provides runtime-level access.
- EventBus currently performs snapshot loading and recovery.
- Test mode controls runtime initialization behavior.


# Target Runtime

Location:

2FUN-OS/platform/runtime


Responsibilities:

- Initialize ecosystem services
- Register modules
- Start event infrastructure
- Load configuration
- Manage lifecycle

## Target Runtime Ownership (TO-BE)

2FUN-OS runtime will become the single owner of:

- EventBus lifecycle
- Service initialization order
- Module registration
- Dependency injection
- Runtime configuration
- Startup and shutdown management

Modules including Game Module must not create infrastructure services.

# Migration Principle

Runtime logic will not move immediately.

First:

Create runtime adapter.


Old:

2FUN_GAME Runtime

↓

Adapter

↓

2FUN-OS Runtime


# Migration Phases

Phase 1:

Freeze current runtime behavior.


Phase 2:

Create OS runtime interface.


Phase 3:

Connect Game Module through adapter.


Phase 4:

Move service initialization ownership to 2FUN-OS.





# Rules

- No duplicate global EventBus instances.
- One runtime authority only.
- Modules cannot initialize core infrastructure themselves.
- Runtime owns lifecycle management.


# Rollback

If migration fails:

Original 2FUN_GAME runtime remains executable.
