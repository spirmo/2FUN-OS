# Platform Integration Strategy

## Purpose

This document defines how applications and modules integrate with the 2FUN-OS ecosystem.

The goal is creating a unified platform integration layer while preserving existing application behavior.


# Current State

Current clients:

- Mobile Application
- Web Interfaces
- Telegram Game
- Administrative Tools


## Current Integration Mapping (AS-IS)

Current platform consumers:

- Telegram Game
- Mobile Application
- Web Interface
- Admin Tools
- Governance Engine
- Knowledge Engine
- Economy
- Wallet


# Target Architecture

2FUN-OS becomes the central platform layer.

Applications communicate through:

- Backend APIs
- Platform Services
- EventBus


## Platform Ownership (TO-BE)

2FUN-OS owns:

- Platform Services
- Backend APIs
- Runtime
- EventBus
- Identity
- Database Infrastructure

Modules own only their business logic.


# Target Flow


Applications

(Mobile App / Web / Telegram Game / Admin)

↓

Backend APIs

(API Gateway)

↓

Platform Services

(Authentication / Identity / Runtime / Service Layer)

↓

EventBus

(Central Event Backbone)

↓

Shared Engines

├── Identity Engine  
├── Knowledge Engine  
├── Governance Engine  
├── Economy Engine  
└── AI Engine  


↓

Modules

├── Game  
├── Wallet  
├── Marketplace  
├── Social  
├── Learning  
├── Missions  
└── Profile  


↓

Result Events


↓

Platform Services


↓

Backend APIs


↓

Applications



# Game Integration

Game becomes:



The game communicates with OS through:

- Events
- Services
- APIs


## Module Integration Model

Every module integrates through:


Module

↓

EventBus

↓

Platform Services

↓

Shared Engines


No module communicates directly with another module.


# Governance Integration

Applications do not execute governance rules directly.

They request decisions through governance services.


## API Integration Rules

Applications never access:

- Database directly
- Governance directly
- Economy directly


Applications only use:


Backend APIs

↓

Platform Services

↓

Shared Engines



# Migration Phases


## Phase 1

Connect applications to backend services.


## Phase 2

Expose OS services through APIs.


## Phase 2.5

Validate:

- API compatibility
- Event compatibility
- Service ownership


## Phase 3

Move module ownership to OS.


## Phase 4

Remove duplicated infrastructure.



# Preservation Rules

- Existing user flows preserved.
- Existing Telegram integration preserved.
- Existing mobile clients remain operational.
- Existing game access preserved.
- APIs are versioned.
- Backward compatibility maintained during transition.



## Integration Principle

Everything integrates through the platform.

No application owns business logic.

The platform owns infrastructure.

Modules own capabilities.

Engines own decision making.



# Final State

2FUN-OS becomes the ecosystem operating platform.
