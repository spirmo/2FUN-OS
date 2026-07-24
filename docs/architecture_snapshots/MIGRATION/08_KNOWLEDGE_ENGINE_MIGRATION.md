# Knowledge Engine Migration Strategy

## Purpose

This document defines the migration strategy of the 2FUN knowledge system into the 2FUN-OS Knowledge Ecosystem.

The goal is preserving the existing knowledge architecture and expanding it.


# Current State

Location:

2FUN_GAME/core/knowledge


Current capabilities:

- Knowledge domains
- Knowledge mapping
- Traits
- Concepts
- User knowledge interaction
- Question pipeline
- Knowledge processing

## Current Implementation Mapping (AS-IS)

Actual implementation:

- core/knowledge contains the current Knowledge Runtime.
- Domain definitions are stored in knowledge domains.
- Trait system provides knowledge behavior mapping.
- Concept structures define knowledge nodes.
- Question pipeline manages user knowledge interaction.
- Knowledge Editor and KCE provide knowledge injection and completion workflows.
- Snapshots preserve historical knowledge states.


# Target Location

2FUN-OS:

modules/knowledge

and:

engines/tandil


# Architecture Principle

Knowledge is an ecosystem service.

Game is only one consumer of knowledge.

## Ownership Rules (TO-BE)

- modules/knowledge owns knowledge data structures.
- engines/tandil owns knowledge intelligence and processing logic.
- Game Module cannot modify core knowledge rules directly.
- All knowledge state changes must generate events.
- Knowledge snapshots are managed independently from EventBus.
- AI can analyze knowledge but cannot become knowledge authority.


# Target Flow

Knowledge Module

↓

Knowledge Engine

↓

Decision / Processing Layer

↓

EventBus

↓

Game / Platform / AI Modules


# Migration Phases

Phase 1:

Document current knowledge structures.


Phase 2:

Move schemas and repositories.


Phase 3:

Connect Knowledge Engine with EventBus.


Phase 4:

Enable all OS modules to consume knowledge services.


# Preservation Rules

- Existing taxonomy preserved.
- Existing concepts preserved.
- Existing user progress preserved.
- No knowledge data migration without backup.
- Existing Knowledge Taxonomy remains backward compatible.
- KCE data must be preserved.
- Knowledge graph evolution requires versioning.
- User mastery history must remain traceable.

# Final State

Knowledge becomes a shared OS capability.

The game remains a knowledge consumer, not the owner.
