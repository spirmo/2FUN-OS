# 2FUN GAME Current Architecture (AS-IS)

## Overview

This document describes the current stable architecture of 2FUN GAME before migration to 2FUN-OS.

The current system contains:

- Game Runtime
- Telegram Bot Layer
- TANDIL Governance System
- Event Driven Architecture
- Knowledge Engine
- Database Layer
- Snapshot System


## Current Root Structure

2FUN_GAME/

- app/
- bot/
- core/
- db/
- TANDIL_GOVERNANCE/
- docs/


## Event Architecture

Current flow:

Game Event
    |
    v
EventBus
    |
    v
Governance Dispatcher
    |
    +--> Policy Engine
    +--> Approval Layer
    +--> Enforcement
    +--> Audit
    +--> Snapshot
    +--> Memory


## Current Runtime

Runtime entry point:

core/governance/runtime.py

Responsibilities:

- Create single EventBus instance
- Attach Governance
- Attach Monitoring
- Expose global bus


## Migration Principle

No destructive migration.

The current architecture remains protected.
Migration will happen through adapters and controlled phases.
