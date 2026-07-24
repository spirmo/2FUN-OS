# Identity Migration Strategy

## Purpose

This document defines the migration strategy of the 2FUN identity system into the 2FUN-OS ecosystem.

The goal is preserving user identity, trust, and progression.


# Current State

Identity related components exist across:

2FUN_GAME

including:

- User profile
- Player identity
- Progress tracking
- Behavioral data
- Reputation related data

## Current Implementation Mapping (AS-IS)

Current identity information is distributed across:

- User profile
- Reputation
- Progress
- Wallet ownership
- Governance participation
- Knowledge mastery
- Behavioral history
- Telegram identity


## Target Location

2FUN-OS

modules/profile

platform/identity

engines/tandil

modules/social (consumer only)


# Architecture Principle

Identity is an ecosystem layer.

Game identity becomes platform identity.

## Identity Ownership Rules (TO-BE)

Identity becomes a platform capability.

Ownership:

- platform/identity owns identity.
- modules/profile owns user profile.
- modules/social consumes identity.
- Governance consumes identity.
- Economy consumes identity.
- Knowledge consumes identity.

No module owns user identity independently.


# Target Flow

User Action

↓

EventBus

↓

Identity Engine

↓

Identity Events

↓

Profile
Reputation
Knowledge
Economy
Governance
Social


# Migration Phases

Phase 1:

Inventory existing identity data.

Phase 1.5

Identify ownership of:

- Authentication
- Identity
- Profile
- Reputation
- Wallet reference
- Knowledge reference


Phase 2:

Separate authentication from identity.


Phase 3:

Move identity services to OS layer.


Phase 4:

Connect identity with governance and economy.


# Preservation Rules

- User history preserved.
- Reputation preserved.
- Progress preserved.
- Existing accounts remain valid.
- Telegram identity preserved.
- Historical user IDs never change.
- Identity references remain immutable.
- Reputation history preserved.
- Cross-module identity mapping validated.


## Target Architecture

Identity becomes the central ecosystem reference.

Everything references Identity:

- Governance
- Knowledge
- Economy
- Marketplace
- Wallet
- Social
- Game


# Final State

A user is not only a game player.

A user becomes an ecosystem identity.
