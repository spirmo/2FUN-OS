"""
2FUN / TANDIL
Governance Rule Engine

Governance owns governance-specific rules.
Concept Contract and Concept completeness belong to Concept Engine.
"""

class GovernanceRuleEngine:

    def evaluate_concept(
        self,
        concept: dict,
        validation_result: dict | None = None,
    ) -> dict:
        """
        Evaluate governance-specific rules.

        Concept validity is owned by Concept Engine.
        Therefore this engine must not redefine mandatory items.
        """

        failed_rules = []

        # --------------------------------------------------
        # CONCEPT ENGINE VALIDATION GATE
        # --------------------------------------------------

        if validation_result is not None:
            if not validation_result.get("valid", False):
                failed_rules.append(
                    "CONCEPT_VALIDATION_FAILED"
                )

        # --------------------------------------------------
        # GOVERNANCE-SPECIFIC RULES
        # --------------------------------------------------

        # Reserved for governance rules that are NOT
        # part of the Concept Contract.

        return {
            "approved": len(failed_rules) == 0,
            "failed_rules": failed_rules,
        }
