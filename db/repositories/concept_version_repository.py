"""
2FUN / TANDIL
Concept Version Repository

Persistence authority for the new Concept Version Architecture.

This repository:
- persists Concept identity
- persists Concept versions
- persists lifecycle history
- persists approval queue records

It does NOT:
- validate Concept structure
- calculate completeness
- calculate scores
- decide lifecycle transitions
- generate Concept identity

Those responsibilities remain in their respective engines.
"""

import json
from datetime import datetime
from typing import Optional

from sqlalchemy import text

from db.database import SessionLocal


class ConceptVersionRepository:
    """Persistence layer for the new Concept Version Architecture."""

    # ==========================================================
    # INTERNAL HELPERS
    # ==========================================================

    @staticmethod
    def _now() -> str:
        return datetime.utcnow().isoformat()

    # ==========================================================
    # CONCEPT IDENTITY
    # ==========================================================

    def create_concept(
        self,
        *,
        creator: Optional[str] = None,
        concept_code: Optional[str] = None,
        version: str = "1.0",
        status: str = "OPEN_FOR_COMPLETION",
        completeness: int = 0,
    ) -> int:

        with SessionLocal() as db:
            result = db.execute(
                text("""
                    INSERT INTO concepts_v2
                    (
                        concept_code,
                        creator,
                        current_version,
                        current_status,
                        current_completeness,
                        created_at,
                        updated_at
                    )
                    VALUES
                    (
                        :concept_code,
                        :creator,
                        :version,
                        :status,
                        :completeness,
                        :created_at,
                        :updated_at
                    )
                """),
                {
                    "concept_code": concept_code,
                    "creator": creator,
                    "version": version,
                    "status": status,
                    "completeness": completeness,
                    "created_at": self._now(),
                    "updated_at": self._now(),
                },
            )

            db.commit()
            return result.lastrowid

    def get_concept(self, concept_id: int):
        with SessionLocal() as db:
            return db.execute(
                text("""
                    SELECT
                        id,
                        concept_code,
                        creator,
                        current_version,
                        current_status,
                        current_completeness,
                        created_at,
                        updated_at
                    FROM concepts_v2
                    WHERE id = :concept_id
                """),
                {"concept_id": concept_id},
            ).mappings().first()

    def get_by_code(self, concept_code: str):
        with SessionLocal() as db:
            return db.execute(
                text("""
                    SELECT
                        id,
                        concept_code,
                        creator,
                        current_version,
                        current_status,
                        current_completeness,
                        created_at,
                        updated_at
                    FROM concepts_v2
                    WHERE concept_code = :concept_code
                """),
                {"concept_code": concept_code},
            ).mappings().first()

    # ==========================================================
    # VERSION PERSISTENCE
    # ==========================================================

    def create_version(
        self,
        *,
        concept_id: int,
        concept_code: str,
        version: str,
        payload: dict,
        completeness: int = 0,
        status: str = "OPEN_FOR_COMPLETION",
        created_by: Optional[str] = None,
        snapshot_reference: Optional[str] = None,
    ) -> int:

        with SessionLocal() as db:
            result = db.execute(
                text("""
                    INSERT INTO concept_versions
                    (
                        concept_id,
                        concept_code,
                        version,
                        payload,
                        completeness,
                        status,
                        created_by,
                        created_at,
                        snapshot_reference
                    )
                    VALUES
                    (
                        :concept_id,
                        :concept_code,
                        :version,
                        :payload,
                        :completeness,
                        :status,
                        :created_by,
                        :created_at,
                        :snapshot_reference
                    )
                """),
                {
                    "concept_id": concept_id,
                    "concept_code": concept_code,
                    "version": version,
                    "payload": json.dumps(payload, ensure_ascii=False),
                    "completeness": completeness,
                    "status": status,
                    "created_by": created_by,
                    "created_at": self._now(),
                    "snapshot_reference": snapshot_reference,
                },
            )

            db.commit()
            return result.lastrowid

    def get_version(
        self,
        concept_code: str,
        version: str,
    ):
        with SessionLocal() as db:
            return db.execute(
                text("""
                    SELECT
                        id,
                        concept_id,
                        concept_code,
                        version,
                        payload,
                        completeness,
                        status,
                        created_by,
                        created_at,
                        approved_by,
                        approved_at,
                        snapshot_reference
                    FROM concept_versions
                    WHERE concept_code = :concept_code
                      AND version = :version
                """),
                {
                    "concept_code": concept_code,
                    "version": version,
                },
            ).mappings().first()

    def get_versions(self, concept_code: str):
        with SessionLocal() as db:
            return db.execute(
                text("""
                    SELECT
                        id,
                        concept_id,
                        concept_code,
                        version,
                        payload,
                        completeness,
                        status,
                        created_by,
                        created_at,
                        approved_by,
                        approved_at,
                        snapshot_reference
                    FROM concept_versions
                    WHERE concept_code = :concept_code
                    ORDER BY id ASC
                """),
                {"concept_code": concept_code},
            ).mappings().all()

    # ==========================================================
    # CURRENT CONCEPT STATE
    # ==========================================================

    def update_current_state(
        self,
        *,
        concept_id: int,
        version: str,
        status: str,
        completeness: int,
    ) -> None:

        with SessionLocal() as db:
            db.execute(
                text("""
                    UPDATE concepts_v2
                    SET
                        current_version = :version,
                        current_status = :status,
                        current_completeness = :completeness,
                        updated_at = :updated_at
                    WHERE id = :concept_id
                """),
                {
                    "concept_id": concept_id,
                    "version": version,
                    "status": status,
                    "completeness": completeness,
                    "updated_at": self._now(),
                },
            )

            db.commit()

    # ==========================================================
    # HISTORY
    # ==========================================================

    def add_history(
        self,
        *,
        concept_id: int,
        concept_code: Optional[str],
        version: Optional[str],
        actor: Optional[str],
        event_type: str,
        from_state: Optional[str] = None,
        to_state: Optional[str] = None,
        details: Optional[dict] = None,
    ) -> int:

        with SessionLocal() as db:
            result = db.execute(
                text("""
                    INSERT INTO concept_version_history
                    (
                        concept_id,
                        concept_code,
                        version,
                        actor,
                        event_type,
                        from_state,
                        to_state,
                        details,
                        created_at
                    )
                    VALUES
                    (
                        :concept_id,
                        :concept_code,
                        :version,
                        :actor,
                        :event_type,
                        :from_state,
                        :to_state,
                        :details,
                        :created_at
                    )
                """),
                {
                    "concept_id": concept_id,
                    "concept_code": concept_code,
                    "version": version,
                    "actor": actor,
                    "event_type": event_type,
                    "from_state": from_state,
                    "to_state": to_state,
                    "details": (
                        json.dumps(details, ensure_ascii=False)
                        if details is not None
                        else None
                    ),
                    "created_at": self._now(),
                },
            )

            db.commit()
            return result.lastrowid

    # ==========================================================
    # APPROVAL QUEUE
    # ==========================================================

    def create_approval_submission(
        self,
        *,
        concept_id: Optional[int],
        concept_code: Optional[str],
        version: str,
        creator_user_code: Optional[str],
        source_mobile_id: Optional[str],
        payload: dict,
    ) -> int:

        with SessionLocal() as db:
            result = db.execute(
                text("""
                    INSERT INTO concept_approval_queue_v2
                    (
                        concept_id,
                        concept_code,
                        version,
                        creator_user_code,
                        source_mobile_id,
                        payload,
                        status,
                        created_at
                    )
                    VALUES
                    (
                        :concept_id,
                        :concept_code,
                        :version,
                        :creator_user_code,
                        :source_mobile_id,
                        :payload,
                        'SUBMITTED',
                        :created_at
                    )
                """),
                {
                    "concept_id": concept_id,
                    "concept_code": concept_code,
                    "version": version,
                    "creator_user_code": creator_user_code,
                    "source_mobile_id": source_mobile_id,
                    "payload": json.dumps(
                        payload,
                        ensure_ascii=False,
                    ),
                    "created_at": self._now(),
                },
            )

            db.commit()
            return result.lastrowid

    def get_pending_approvals(self):
        with SessionLocal() as db:
            return db.execute(
                text("""
                    SELECT
                        id,
                        concept_id,
                        concept_code,
                        version,
                        creator_user_code,
                        source_mobile_id,
                        payload,
                        status,
                        created_at,
                        approved_by,
                        reviewed_at
                    FROM concept_approval_queue_v2
                    WHERE status = 'SUBMITTED'
                    ORDER BY id ASC
                """)
            ).mappings().all()

    # ==========================================================
    # EXISTENCE
    # ==========================================================

    def exists(
        self,
        *,
        concept_code: str,
        version: Optional[str] = None,
    ) -> bool:

        with SessionLocal() as db:

            if version is None:
                result = db.execute(
                    text("""
                        SELECT 1
                        FROM concepts_v2
                        WHERE concept_code = :concept_code
                        LIMIT 1
                    """),
                    {"concept_code": concept_code},
                )
            else:
                result = db.execute(
                    text("""
                        SELECT 1
                        FROM concept_versions
                        WHERE concept_code = :concept_code
                          AND version = :version
                        LIMIT 1
                    """),
                    {
                        "concept_code": concept_code,
                        "version": version,
                    },
                )

            return result.first() is not None
