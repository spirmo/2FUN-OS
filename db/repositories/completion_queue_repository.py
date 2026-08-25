from datetime import datetime

from sqlalchemy import text

from db.database import SessionLocal


class CompletionQueueRepository:
    """
    Persistence layer for Concept Completion Queue.

    Stores approved but incomplete Concepts
    waiting for user completion.
    """

    @staticmethod
    def _now():
        return datetime.utcnow().isoformat()

    def add(
        self,
        *,
        concept_id: int,
        concept_code: str,
        completeness: int,
    ):
        with SessionLocal() as db:
            db.execute(
                text("""
                    INSERT OR REPLACE INTO concept_completion_queue
                    (
                        concept_id,
                        concept_code,
                        current_completeness,
                        target_completeness,
                        status,
                        created_at,
                        updated_at
                    )
                    VALUES
                    (
                        :concept_id,
                        :concept_code,
                        :completeness,
                        36,
                        'NEED_COMPLETION',
                        :created_at,
                        :updated_at
                    )
                """),
                {
                    "concept_id": concept_id,
                    "concept_code": concept_code,
                    "completeness": completeness,
                    "created_at": self._now(),
                    "updated_at": self._now(),
                },
            )

            db.commit()

            return {
                "status": "QUEUED",
                "concept_id": concept_id,
                "concept_code": concept_code,
            }

    def get_pending(self):
        with SessionLocal() as db:
            rows = db.execute(
                text("""
                    SELECT
                        id,
                        concept_id,
                        concept_code,
                        current_completeness,
                        status
                    FROM concept_completion_queue
                    WHERE status = 'NEED_COMPLETION'
                """)
            ).mappings().all()

            return [dict(row) for row in rows]

    def mark_completed(self, concept_id: int):
        with SessionLocal() as db:
            db.execute(
                text("""
                    UPDATE concept_completion_queue
                    SET
                        status='COMPLETED',
                        updated_at=:updated_at
                    WHERE concept_id=:concept_id
                """),
                {
                    "concept_id": concept_id,
                    "updated_at": self._now(),
                },
            )

            db.commit()

            return {
                "status": "COMPLETED",
                "concept_id": concept_id,
            }
