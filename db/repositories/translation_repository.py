from datetime import datetime
from typing import Optional

from sqlalchemy import text
from db.database import SessionLocal


class TranslationRepository:
    """
    Persistence layer for Translation Engine.

    Repository is responsible only for database persistence.
    It does not validate translations, approve them,
    calculate scores, or manage EventBus.
    """

    @staticmethod
    def _now() -> str:
        return datetime.utcnow().isoformat()

    def create_translation(
        self,
        translation_key: str,
        language: str,
        translation: str,
        created_by: Optional[str] = None,
        source_type: str = "MANUAL",
        status: str = "Draft",
        version: str = "1.0",
    ) -> int:
        now = self._now()

        with SessionLocal() as db:
            result = db.execute(
                text("""
                    INSERT INTO translation_entries (
                        translation_key,
                        language,
                        translation,
                        status,
                        version,
                        created_by,
                        created_at,
                        updated_at,
                        source_type
                    )
                    VALUES (
                        :translation_key,
                        :language,
                        :translation,
                        :status,
                        :version,
                        :created_by,
                        :created_at,
                        :updated_at,
                        :source_type
                    )
                """),
                {
                    "translation_key": translation_key,
                    "language": language,
                    "translation": translation,
                    "status": status,
                    "version": version,
                    "created_by": created_by,
                    "created_at": now,
                    "updated_at": now,
                    "source_type": source_type,
                },
            )

            db.commit()
            return result.lastrowid

    def get_translation(
        self,
        translation_key: str,
        language: str,
    ) -> Optional[dict]:
        with SessionLocal() as db:
            result = db.execute(
                text("""
                    SELECT
                        id,
                        translation_key,
                        language,
                        translation,
                        status,
                        version,
                        created_by,
                        verified_by,
                        created_at,
                        updated_at,
                        source_type
                    FROM translation_entries
                    WHERE translation_key = :translation_key
                      AND language = :language
                    ORDER BY id DESC
                    LIMIT 1
                """),
                {
                    "translation_key": translation_key,
                    "language": language,
                },
            )

            row = result.mappings().first()

            return dict(row) if row else None
