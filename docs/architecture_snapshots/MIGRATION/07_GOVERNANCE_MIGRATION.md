# Governance Migration Strategy

## Purpose

This document defines the migration strategy for the TANDIL Governance System from 2FUN_GAME into 2FUN-OS.

The goal is preservation, not replacement.


# Current State

Location:

2FUN_GAME/TANDIL_GOVERNANCE


Current capabilities:

- Governance Engine
- Policy Engine
- Rule Engine
- Approval Layer
- Enforcement Engine
- Audit Engine
- Memory Integration
- Decision Routing
- Founder Rules
- Snapshot Integration
- EventBus Integration

## Current Implementation Mapping (AS-IS)

Actual runtime integration:

- TANDIL_GOVERNANCE/core_engine contains governance infrastructure.
- EventBus is the current communication channel.
- core/governance/bootstrap.py attaches governance and monitoring layers.
- Governance currently receives events and routes them through hooks.
- Runtime Context provides shared governance runtime access.
- Snapshot data is currently connected to governance lifecycle.


# Current Role

Governance receives events from EventBus.

It evaluates:

- Rules
- Policies
- Risk
- Approval requirements
- Enforcement decisions


# Target Location

2FUN-OS:

engines/governance

## Target Governance Ownership (TO-BE)

2FUN-OS engines/governance will own:

- Rule evaluation
- Policy enforcement
- Decision processing
- Risk analysis
- Approval workflows
- Audit chain management
- Governance state lifecycle

Governance remains independent from Game, Mobile, Web and Marketplace modules.



# Migration Principle

Governance becomes an OS engine.

The Game module does not own governance.

The Game only produces events.


# Target Flow


Game Module

↓

EventBus

↓

Governance Engine

↓

Governance Listeners

↓

Decision Engine

↓

Action / Response Events
Decision

↓

Game Response


# Migration Phases

Phase 1:

Freeze current governance behavior.


Phase 2:

Map existing engines into OS governance engine.


Phase 3:

Connect governance through EventBus listener.


Phase 4:

Remove direct game ownership.


# Governance Migration Rules

- Governance is an independent OS engine.
- Governance never imports Game modules.
- Game modules cannot modify governance rules directly.
- All governance decisions must originate from validated events.
- AI can advise but cannot override governance authority.
- Rule Engine remains the final authority.

# Preservation Rules

- No governance rule deletion.
- No policy loss.
- No decision logic rewrite.
- Existing tests remain valid.
- Existing snapshots remain historical references.


# Final State

TANDIL Governance becomes:

2FUN-OS Governance Engine

with:

- independent ownership
- event driven operation
- reusable across all modules
