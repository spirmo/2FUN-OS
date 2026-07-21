from ..decision_engine import DecisionEngine


class GovernanceService:
    """
    Public service layer for governance operations.
    """

    def __init__(self):
        self.decision_engine = DecisionEngine()

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
