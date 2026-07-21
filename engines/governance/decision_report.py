class DecisionReport:
    """
    Generates governance decision reports.
    """

    def create_report(
        self,
        entity_type: str,
        entity_id: int,
        validation_result: dict,
        rule_result: dict,
    ) -> dict:

        approved = (
            validation_result.get("valid", False)
            and rule_result.get("approved", False)
        )

        return {
            "entity_type": entity_type,
            "entity_id": entity_id,
            "approved": approved,
            "validation": validation_result,
            "rules": rule_result,
            "status": (
                "APPROVED"
                if approved
                else "REJECTED"
            ),
        }
