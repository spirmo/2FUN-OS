# GAME EVENT CONTRACT v1.0

## Purpose

Defines official events produced by the 2FUN Game Module.

## Core Principle

Game does not directly control governance.

Game only emits events.

Governance, Economy, Knowledge and Identity consume events.

## Initial Events

### USER_ACTIVITY

Source:
game

Event:
USER_ACTIVITY

Target:
identity/governance

Payload:

{
 user_id,
 action,
 timestamp
}


### MISSION_COMPLETED

Source:
game

Event:
MISSION_COMPLETED

Target:
economy/knowledge

Payload:

{
 user_id,
 mission_id,
 reward
}


### POINTS_EARNED

Source:
game

Event:
POINTS_EARNED

Target:
economy/profile

Payload:

{
 user_id,
 amount,
 reason
}


## Migration Rule

All future game systems must communicate through EventBus.
