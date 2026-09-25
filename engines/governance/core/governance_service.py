from ..decision_engine import DecisionEngine
from ..user_rules import UserGovernanceEngine
from ..user_rules.event_adapter import UserGovernanceEventAdapter
from platform_core.event_bus.event_bus import EventBus


class GovernanceService:
    """
    Public service layer for governance operations.

    Concept governance and user governance remain separate contracts.
    """

    def __init__(self):
        self.decision_engine = DecisionEngine()
        self.user_governance_engine = UserGovernanceEngine()

    def approve_concept(
        self,
        concept_id: int,
        concept: dict,
    ) -> dict:
        """
        Evaluate a concept and return governance decision.
        """
        return self.decision_engine.evaluate_concept(
            concept_id=concept_id,
            concept=concept,
        )

    def evaluate_user(
        self,
        user_data: dict,
    ) -> dict:
        """
        Evaluate a user through the migrated Legacy
        User Governance Rule Pipeline and central EventBus.
        """
        event_bus = EventBus()
        event_adapter = UserGovernanceEventAdapter(event_bus)

        engine = UserGovernanceEngine(
            event_adapter=event_adapter,
        )

        return engine.process_user(user_data)
