from decimal import Decimal

from platform_core.runtime.runtime_context import get_event_bus


class KnowledgeCompletionEngine:
    """
    Knowledge Field Completion Processor

    مسئول:
    - دریافت تکمیل یک Field
    - ایجاد Event استاندارد Knowledge
    - ارسال Event به EventBus

    محاسبه ارزش، Transaction و Ledger
    توسط Universal Value Infrastructure (UVI) انجام می‌شود.
    """

    def __init__(self):
        self.event_bus = get_event_bus()

    def process_completion(
        self,
        user_id: str,
        concept_id: int,
        item_key: str,
        difficulty: str = "EASY",
        base_value: Decimal = Decimal("10"),
    ):
        event_result = self.event_bus.emit(
            "KNOWLEDGE",
            "FIELD_COMPLETED",
            "concept",
            {
                "user_id": str(user_id),
                "concept_id": concept_id,
                "item_key": item_key,
                "base_value": str(base_value),
                "difficulty": difficulty,
                "currency": "XP",
            },
        )

        return event_result


if __name__ == "__main__":
    engine = KnowledgeCompletionEngine()

    result = engine.process_completion(
        user_id="1",
        concept_id=100,
        item_key="definition",
        difficulty="HARD",
    )

    print(result)
