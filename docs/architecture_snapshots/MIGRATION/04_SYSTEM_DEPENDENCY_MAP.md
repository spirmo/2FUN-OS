# 2FUN System Dependency Map

## Purpose

This document maps the relationship between the current 2FUN GAME architecture and the target 2FUN-OS ecosystem.

Migration will be performed based on dependency analysis, not file movement.


# Current System

## 2FUN_GAME

Main Components:

- Telegram Bot Layer
- Game Runtime
- User Profile System
- Knowledge System
- Action System
- Control System
- Memory System
- Civilization System
- TANDIL Governance
- EventBus


# Current Event Flow

Game Action

↓

Core Action Handler

↓

Event Creation

↓

EventBus

↓

Governance Pipeline

↓

Result / Enforcement / Snapshot


# Target Mapping


## Game Layer

Current:

2FUN_GAME/core/action
2FUN_GAME/bot
2FUN_GAME/app


Target:

2FUN-OS/modules/game


Responsibility:

- Game rules
- Story
- Player interaction
- Game events


---


## Governance Layer

Current:

2FUN_GAME/TANDIL_GOVERNANCE

Target:

2FUN-OS/engines/governance


Responsibility:

- Rules
- Approval
- Enforcement
- Audit
- Decision Engine


---


## Knowledge Layer

Current:

2FUN_GAME/core/knowledge


Target:

2FUN-OS/modules/knowledge

and:

2FUN-OS/engines/tandil


Responsibility:

- Knowledge graph
- Taxonomy
- Mastery
- Recommendations


---


## Economy Layer

Current:

Game economy components


Target:

2FUN-OS/modules/economy

and:

modules/wallet


Responsibility:

- Points
- SHIR
- 2SHIR
- 2FUNC
- Transactions


---


## Event System

Current:

TANDIL_GOVERNANCE/core_engine/event_bus


Target:

2FUN-OS/platform/event_bus


Migration Rule:

EventBus will not be rewritten.

It will be extracted and adapted.


---


# Migration Principle

Old system:

2FUN_GAME
+
TANDIL_GOVERNANCE


becomes:


2FUN-OS

with:

modules/game

+
engines/governance

+
engines/tandil


No functionality is removed.
Only ownership boundaries change.
