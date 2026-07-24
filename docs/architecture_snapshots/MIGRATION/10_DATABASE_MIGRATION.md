# Database Migration Strategy

## Purpose

This document defines the migration strategy of all 2FUN GAME data structures into the 2FUN-OS database architecture.

The goal is zero data loss.


# Current State

Current database location:

2FUN_GAME/db


Existing components:

- Core database
- Models
- Repositories
- Services
- Migrations
- Backups
- Snapshots


## Current Implementation Mapping (AS-IS)

Actual implementation:

- db/ is the current runtime database layer.
- db/core contains database initialization logic.
- db/models defines persistent entities.
- db/repositories provides data access abstraction.
- db/services contains database operations.
- db/migrations manages schema evolution.
- db_backups and snapshots preserve historical states.
- SQLite is currently the runtime Source of Truth.


# Target Location

2FUN-OS:

backend/database

and module-owned repositories.


## Target Database Ownership (TO-BE)

2FUN-OS database architecture:

- backend/database owns database infrastructure.
- Modules own their repository contracts.
- Database services provide controlled access.
- Schema ownership is separated by domain.
- Migration manager controls version transitions.


# Migration Principle

Database ownership moves from Game to OS.

Game modules access data through services.

Database is not directly accessed by modules.

All data access must pass through:

Module

↓

Service Layer

↓

Repository

↓

Database Layer


# Data Categories


## User Data

Includes:

- Identity
- Profile
- Progress
- Reputation


## Game Data

Includes:

- Characters
- Story state
- Missions
- Game progression


## Knowledge Data

Includes:

- Domains
- Topics
- Concepts
- Mastery


## Economy Data

Includes:

- Wallet
- Transactions
- Rewards


# Data Ownership Model (TO-BE)

## Identity Data

Owner:
backend/platform identity services


## Game Data

Owner:
modules/game


## Knowledge Data

Owner:
modules/knowledge


## Economy Data

Owner:
modules/economy and modules/wallet


## Governance Data

Owner:
engines/governance


# Migration Phases

Phase 1:

Create complete database inventory.

Phase 1.5:

Create database ownership map.

Identify:

- Current tables
- Models
- Relations
- Data dependencies
- Migration risks


Phase 2:

Freeze schemas.


Phase 3:

Create migration scripts.


Phase 4:

Validate migrated data.


Phase 5:

Switch runtime access.


# Preservation Rules

- No direct database deletion.
- All migrations require backup.
- Old database remains available during transition.
- Data validation required after migration.
- SQLite remains Source of Truth until migration validation completes.
- PostgreSQL migration happens only after schema freeze.
- Historical snapshots remain immutable.
- Every migrated table requires verification.
- Database changes require migration versioning.

# Rollback

If migration fails:

Runtime returns to previous database source.

No user data loss allowed.
