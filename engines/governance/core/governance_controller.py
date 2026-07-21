from .governance_service import GovernanceService


class GovernanceController:
    """
    Entry point for governance requests.
    """

    def __init__(self):
        self.service = GovernanceService()

    def submit_concept(
        self,
        concept_id: int,
        concept: dict,
    ) -> dict:
        """
        Submit a concept for governance evaluation.
        """

        return self.service.approve_concept(
            concept_id=concept_id,
            concept=concept,
        )
