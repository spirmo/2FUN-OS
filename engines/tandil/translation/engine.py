from .application import TranslationApplication


class TranslationEngine:
    """
    Core Translation Engine.

    Owns translation orchestration.
    Persistence remains in TranslationRepository.
    """

    def __init__(self):
        self.application = TranslationApplication()

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
        return self.application.create_translation(
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
        return self.application.get_translation(
            translation_key=translation_key,
            language=language,
        )

    def get(
        self,
        translation_key: str,
        language: str,
    ) -> str:
        row = self.get_translation(
            translation_key=translation_key,
            language=language,
        )

        if row is None:
            return translation_key

        if row["status"] != "Approved":
            return translation_key

        return row["translation"]

    def inject_language(
        self,
        language: str,
        user_id: str,
        item_key: str,
        base_value,
        difficulty: str,
    ):
        return self.application.emit_injection_event(
            language=language,
            user_id=user_id,
            item_key=item_key,
            base_value=base_value,
            difficulty=difficulty,
        )
