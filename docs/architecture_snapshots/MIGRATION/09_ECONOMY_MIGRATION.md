# Economy Migration Strategy

## Purpose

This document defines the migration strategy of the 2FUN economy system into the 2FUN-OS ecosystem.

The goal is preserving the economic model while making it available for all modules.


# Current State

Current economy exists inside the game ecosystem.

Main concepts:

- Points
- SHIR
- 2SHIR
- 2FUNC
- Rewards
- Player progression economy

## Current Implementation Mapping (AS-IS)

Actual implementation:

- Economy rules currently exist inside the Game ecosystem.
- Game progression is connected to Points and reward mechanisms.
- Conversion model includes:
  - Points
  - SHIR
  - 2SHIR
  - 2FUNC
- Reward calculation is currently triggered from game activities.
- Wallet and economic state require independent ownership in 2FUN-OS.


# Target Location

2FUN-OS:

modules/economy

and:

modules/wallet

Additional OS ownership:

- Economy Engine owns economic rules.
- Wallet Module owns balances and transactions.
- Marketplace consumes economy services.
- Governance may validate economic policies.

# Architecture Principle

Economy is an ecosystem service.

Game creates economic events.

Economy engine processes value changes.


# Target Flow

Game Module

↓

Economic Events

↓

EventBus

↓

Economy Engine

↓

Wallet / Transaction Layer

↓

Economy Response Events

↓

Game / Marketplace / User Profile


# Economy Ownership Rules

- Game Module cannot directly modify balances.
- All value changes must pass through Economy Engine.
- Wallet is the source of truth for user balances.
- Every transaction requires traceability.
- Conversion rules require versioning.
- Economic events must be auditable.
- AI cannot create or approve economic value.


# Migration Phases

Phase 1:

Freeze current economic rules.


Phase 2:

Extract economic calculations from game logic.


Phase 3:

Create economy service layer.


Phase 4:

Connect economy with EventBus.


# Preservation Rules

- Existing conversion rules preserved.
- User balances preserved.
- Transaction history preserved.
- No economy logic deleted.
- Existing Points → SHIR → 2SHIR → 2FUNC conversion chain preserved.
- Historical transactions remain immutable.
- Reward history remains traceable.
- Economy snapshots preserved before migration.

# Final State

Economy becomes a shared OS capability.

All modules can participate in the ecosystem economy.
