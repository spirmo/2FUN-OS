from .validation_engine import ValidationEngine
from .governance_rule_engine import GovernanceRuleEngine
from .decision_report import DecisionReport


class DecisionEngine:
    """
    Main governance decision coordinator.
    """

    def __init__(self):
        self.validation_engine = ValidationEngine()
        self.rule_engine = GovernanceRuleEngine()
        self.report_engine = DecisionReport()

    def evaluate_concept(
        self,
        concept_id: int,
        concept: dict,
    ) -> dict:

        validation_result = (
            self.validation_engine
            .validate_concept(concept)
        )

        rule_result = (
            self.rule_engine
            .evaluate_concept(concept)
        )

        report = (
            self.report_engine
            .create_report(
                entity_type="concept",
                entity_id=concept_id,
                validation_result=validation_result,
                rule_result=rule_result,
            )
        )

        return report
