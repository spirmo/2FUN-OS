class GovernanceRuleEngine:
    """
    Governance rules evaluator.
    """

    def evaluate_concept(self, concept: dict) -> dict:
        failed_rules = []

        if not concept.get("source"):
            failed_rules.append(
                "CONCEPT_MUST_HAVE_SOURCE"
            )

        if not concept.get("evidence"):
            failed_rules.append(
                "CONCEPT_MUST_HAVE_EVIDENCE"
            )

        if not concept.get("definition"):
            failed_rules.append(
                "CONCEPT_MUST_HAVE_DEFINITION"
            )

        return {
            "approved": len(failed_rules) == 0,
            "failed_rules": failed_rules,
        }
