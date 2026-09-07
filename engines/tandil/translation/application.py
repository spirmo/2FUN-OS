from platform_core.runtime.runtime_context import get_event_bus
from db.repositories.translation_repository import TranslationRepository
from engines.tandil.knowledge.injection import InjectionTarget
from engines.tandil.knowledge.injection.application import InjectionApplication


class TranslationApplication:
    """
    Application layer for Translation Engine.

    Business orchestration belongs here.
    Persistence belongs to TranslationRepository.
    """

    def __init__(self):
        self.repository = TranslationRepository()

    def create_translation(
        self,
        translation_key: str,
        language: str,
        translation: str,
        created_by: str | None = None,
        source_type: str = "MANUAL",
        status: str = "Draft",
        version: str = "1.0",
    ) -> int:
        return self.repository.create_translation(
            translation_key=translation_key,
            language=language,
            translation=translation,
            created_by=created_by,
            source_type=source_type,
            status=status,
            version=version,
        )

    def get_translation(
        self,
        translation_key: str,
        language: str,
    ):
        return self.repository.get_translation(
            translation_key=translation_key,
            language=language,
        )

    def build_injection_event(
        self,
        language: str,
        user_id: str,
        item_key: str,
        base_value,
        difficulty: str,
    ):
        target = InjectionTarget.language(language)

        return InjectionApplication.build_event(
            target=target,
            user_id=user_id,
            item_key=item_key,
            base_value=base_value,
            difficulty=difficulty,
        )

    def emit_injection_event(
        self,
        language: str,
        user_id: str,
        item_key: str,
        base_value,
        difficulty: str,
    ):
        target = InjectionTarget.language(language)

        event_payload = InjectionApplication.build_event(
            target=target,
            user_id=user_id,
            item_key=item_key,
            base_value=base_value,
            difficulty=difficulty,
        )
        event_bus = get_event_bus()

        return event_bus.emit(
            "KNOWLEDGE",
            "FIELD_COMPLETED",
            "language",
            event_payload,
        )
