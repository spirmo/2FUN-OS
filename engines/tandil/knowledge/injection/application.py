from .contract import InjectionTarget, InjectionType


class InjectionApplication:
    """
    Shared application layer for Knowledge Injection.

    Concept and Language use the same injection mechanism.
    Only the injection target type differs.
    """

    @staticmethod
    def create_concept_target(concept_code: str) -> InjectionTarget:
        return InjectionTarget.concept(concept_code)

    @staticmethod
    def create_language_target(language_code: str) -> InjectionTarget:
        return InjectionTarget.language(language_code)

    @staticmethod
    def build_event(
        target: InjectionTarget,
        user_id: str,
        item_key: str,
        base_value,
        difficulty: str,
        completeness: int | None = None,
    ) -> dict:
        if not InjectionApplication.validate_target(target):
            raise ValueError("Invalid injection target")

        return {
            "user_id": str(user_id),
            "item_key": item_key,
            "base_value": str(base_value),
            "difficulty": difficulty,
            "currency": "XP",
            "completeness": completeness,
            "injection_type": target.injection_type.value,
            "target_id": target.target_id,
        }

    @staticmethod
    def build_language_event(
        language_code: str,
        user_id: str,
        item_key: str,
        base_value,
        difficulty: str,
    ) -> dict:
        target = InjectionApplication.create_language_target(
            language_code
        )

        return InjectionApplication.build_event(
            target=target,
            user_id=user_id,
            item_key=item_key,
            base_value=base_value,
            difficulty=difficulty,
        )

    @staticmethod
    def validate_target(target: InjectionTarget) -> bool:
        if not isinstance(target, InjectionTarget):
            return False

        if not isinstance(target.injection_type, InjectionType):
            return False

        return bool(target.target_id)
