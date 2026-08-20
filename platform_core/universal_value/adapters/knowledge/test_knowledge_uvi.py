from decimal import Decimal

from platform_core.universal_value.adapters.knowledge.knowledge_value_adapter import (
    KnowledgeValueAdapter,
)
from platform_core.universal_value.core.value_engine import UniversalValueEngine
from platform_core.universal_value.pipeline.value_pipeline import ValuePipeline
from platform_core.universal_value.policies.knowledge_difficulty_policy import (
    KnowledgeDifficultyPolicy,
)


def test_knowledge_uvi_integration():
    adapter = KnowledgeValueAdapter()

    request = adapter.build_request(
        user_id="USER_1",
        event_id="TEST-EVENT-001",
        field_key="definition",
        base_value=Decimal("10"),
        difficulty="MEDIUM",
    )

    pipeline = ValuePipeline(
        engine=UniversalValueEngine(),
        policies=[
            KnowledgeDifficultyPolicy(),
        ],
    )

    result = adapter.calculate(
        pipeline,
        request,
    )

    assert result.user_id == "USER_1"
    assert result.event_id == "TEST-EVENT-001"
    assert result.source == "KNOWLEDGE"
    assert result.base_value == Decimal("40")
    assert result.multiplier == Decimal("1")
    assert result.final_value == Decimal("40")
    assert result.currency == "XP"

    print("Knowledge → UVI: OK")
    print("Final value:", result.final_value, result.currency)


if __name__ == "__main__":
    test_knowledge_uvi_integration()
    print("KNOWLEDGE UVI INTEGRATION TEST: OK")
