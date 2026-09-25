class UserGovernanceEventAdapter:
    """
    Bridges the migrated Legacy User Governance pipeline
    to the central 2FUN EventBus.

    The Rule Pipeline remains authoritative for its governance
    result; EventBus is used only for centralized event logging
    and downstream processing.
    """

    def __init__(self, event_bus):
        self.event_bus = event_bus

    def emit_stage(self, event_type, value):
        return self.event_bus.emit(
            "USER_GOVERNANCE",
            event_type,
            "USER_RULE_PIPELINE",
            value,
        )
