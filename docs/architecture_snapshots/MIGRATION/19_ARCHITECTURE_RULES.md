# Migration Architecture Rules


## Purpose

This document defines the permanent architecture rules during and after the migration to 2FUN-OS.

These rules become the foundation of the final ecosystem architecture.



# Core Rules



## Rule 1 - Single Ownership


Every system capability must have exactly one owner.


Examples:


Governance:

engines/governance


Knowledge:

engines/tandil + modules/knowledge


Economy:

modules/economy


Identity:

engines/identity


AI:

engines/ai


Infrastructure:

platform



No duplicated ownership is allowed.



## Rule 2 - Platform Owns Infrastructure


Platform owns:


- Runtime
- EventBus
- API Layer
- Database Infrastructure
- Service Bootstrap


Modules must not initialize or own infrastructure.



## Rule 3 - Runtime Authority


Only one runtime authority exists.


Runtime responsibilities:


- Service lifecycle
- Module startup order
- Dependency initialization
- Infrastructure activation


No module can create independent runtime instances.



## Rule 4 - Event Driven Communication


All ecosystem communication must happen through:


Module

↓

EventBus

↓

Listeners / Engines

↓

Action Events



Direct hidden dependencies between modules are forbidden.



## Rule 5 - EventBus Ownership


EventBus is a platform-level backbone.


Rules:


- One EventBus instance only.
- Runtime owns lifecycle.
- Modules publish events.
- Engines consume events.
- Event contracts must be versioned.



## Rule 6 - Governance Authority


Final decisions belong to:


Rules + Governance Engine


AI cannot:

- Override rules.
- Execute enforcement.
- Change governance decisions.



## Rule 7 - AI Advisory Only


AI is an intelligence assistant layer.


AI can:

- Analyze.
- Recommend.
- Predict.


AI cannot:

- Own decisions.
- Modify policies.
- Control execution.



## Rule 8 - Data Protection


No migration without:


- Backup
- Validation
- Recovery point
- Rollback plan



Protected data:


- Identity
- Reputation
- Knowledge
- Economy
- Event History



## Rule 9 - Database Ownership


Database infrastructure belongs to OS.


Modules access data through:


Services

↓

Repositories

↓

Database Layer



Direct database access from applications is forbidden.



## Rule 10 - Module Independence


Modules must be replaceable without breaking the OS.


Each module owns:

- Business logic
- Domain behavior
- Internal rules



Modules do not own:

- Runtime
- EventBus
- Database infrastructure



## Rule 11 - Backward Compatibility


During migration:


- Existing users remain valid.
- Existing data remains valid.
- Existing game behavior is preserved.
- APIs remain compatible.



## Rule 12 - Snapshot Preservation


Every migration phase requires:


- Architecture snapshot.
- Runtime snapshot.
- Migration record.


Historical references must remain available.



## Rule 13 - Documentation Lock


Every architectural change requires:


- Documentation update.
- Migration review.
- Architecture validation.



# Final Architecture Principle


2FUN-OS is an operating system for ecosystem modules.


Platform provides:

- Coordination
- Infrastructure
- Lifecycle


Engines provide:

- Intelligence
- Decisions


Modules provide:

- Capabilities


Applications provide:

- User interaction
