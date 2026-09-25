from .ai_advisor import AIAdvisor
from .conflict_resolver import ConflictResolver
from .governance_score import GovernanceScore
from .penalty_evaluator import PenaltyEvaluator
from .rule_evaluator import RuleEvaluator
from .rule_validator import RuleValidator


class UserGovernanceEngine:
    """
    Migrated Legacy EngineEntry.process_user contract.

    AI remains advisory. Governance components produce the
    authoritative rule/validation/penalty result.

    Optional event_adapter bridges the pipeline to the
    central 2FUN EventBus without changing the result contract.
    """

    def __init__(self, event_adapter=None):
        self.ai_advisor = AIAdvisor()
        self.evaluator = RuleEvaluator()
        self.validator = RuleValidator()
        self.penalty_evaluator = PenaltyEvaluator()
        self.conflict_resolver = ConflictResolver()
        self.governance_score = GovernanceScore()
        self.event_adapter = event_adapter

    def _emit(self, event_type, value):
        if self.event_adapter is not None:
            return self.event_adapter.emit_stage(event_type, value)
        return None

    def process_user(self, user_data):
        self._emit("INPUT", user_data)

        ai_analysis = self.ai_advisor.analyze_user(user_data)
        self._emit("AI_ANALYSIS", ai_analysis)

        governance_score = self.governance_score.calculate(user_data)
        self._emit("GOVERNANCE_SCORE", governance_score)

        evaluation = self.evaluator.evaluate_promotion(user_data)
        self._emit("EVALUATION", evaluation)

        validation = self.validator.validate(
            evaluation,
            user_data,
        )
        self._emit("VALIDATION", validation)

        penalty_raw = self.penalty_evaluator.evaluate_penalty(user_data)
        self._emit("PENALTY_RAW", penalty_raw)

        final_penalty = self.conflict_resolver.resolve(penalty_raw)
        self._emit("PENALTY_FINAL", final_penalty)

        result = {
            "evaluation": evaluation,
            "validation": validation,
            "penalty": final_penalty,
            "ai_analysis": ai_analysis,
            "governance_score": governance_score,
        }

        self._emit("FINAL_OUTPUT", result)

        return result
