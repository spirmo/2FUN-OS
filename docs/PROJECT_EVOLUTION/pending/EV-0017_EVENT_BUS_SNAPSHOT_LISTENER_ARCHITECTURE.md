# EV-0017 — Event Bus Snapshot Listener Architecture

## Status
Pending

## Priority
High

## Trigger
After KCE Stabilization

## Objective

Introduce a dedicated Event Bus Snapshot Listener that automatically reacts to important events published on the Event Bus and triggers snapshot creation when project rules allow it.

## Motivation

Currently, snapshot generation can be initiated directly by system components.

The proposed architecture separates responsibilities by allowing the Event Bus to publish events while independent listeners decide how to react.

## Initial Listener

- Snapshot Listener

## Future Listeners

- Audit Listener
- Notification Listener
- Analytics Listener
- AI Listener

## Expected Benefits

- Loose coupling
- Better scalability
- Easier maintenance
- Independent evolution of system components
- Automatic project history generation

## Notes

This evolution is intended to integrate with the existing Snapshot Manager and Event Bus architecture without introducing direct dependencies between engines.
