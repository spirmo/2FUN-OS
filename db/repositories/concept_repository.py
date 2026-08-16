import json

from datetime import datetime
from sqlalchemy import text

from db.database import SessionLocal
from db.models.concept_approval import ConceptApprovalQueue
from platform_core.runtime.runtime_context import get_event_bus


class ConceptRepository:

    def submit_concept(
        self,
        concept_code,
        creator_user_code,
        title,
        domain,
        payload,
        source_mobile_id=None
    ):

        db = SessionLocal()

        try:

            existing = (
                db.query(ConceptApprovalQueue)
                .filter(
                    ConceptApprovalQueue.concept_code
                    == concept_code
                )
                .first()
            )

            if existing:
                return {
                    "status": "DUPLICATE",
                    "reason": "Concept already submitted",
                    "concept_code": concept_code
                }


            concept = ConceptApprovalQueue(
                concept_code=concept_code,
                creator_user_code=creator_user_code,
                source_mobile_id=source_mobile_id,
                title=title,
                domain=domain,
                payload=json.dumps(payload),
                status="SUBMITTED",
                created_at=datetime.utcnow()
            )


            db.add(concept)
            db.commit()
            db.refresh(concept)


            return {
                "status": "SUBMITTED",
                "queue_id": concept.id,
                "concept_code": concept.concept_code
            }


        finally:
            db.close()



    def get_pending(self):

        db = SessionLocal()

        try:

            return (
                db.query(ConceptApprovalQueue)
                .filter(
                    ConceptApprovalQueue.status
                    == "SUBMITTED"
                )
                .all()
            )

        finally:
            db.close()



    def approve_concept(
        self,
        queue_id,
        approver="SYSTEM"
    ):

        import json
        from datetime import datetime
        from db.models.concept import (
            Concept,
            ConceptItem,
            ConceptSystem
        )


        db = SessionLocal()

        try:

            queue = (
                db.query(ConceptApprovalQueue)
                .filter(
                    ConceptApprovalQueue.id == queue_id
                )
                .first()
            )


            if not queue:
                return {
                    "status": "NOT_FOUND"
                }


            if queue.status != "SUBMITTED":
                return {
                    "status": "INVALID_STATUS",
                    "current": queue.status
                }



            topic = db.execute(
                text(
                    """
                    SELECT id FROM topics
                    WHERE code = :code
                    """
                ),
                {
                    "code": f"{queue.domain}_GENERAL"
                }
            ).fetchone()


            if not topic:
                return {
                    "status": "TOPIC_NOT_FOUND"
                }



            concept = Concept(
                topic_id=topic[0],
                code=queue.concept_code,
                name_fa=queue.title,
                name_en=queue.title,
                name_ar=queue.title,
                description=queue.title,
                status="APPROVED",
                created_at=str(datetime.utcnow())
            )


            db.add(concept)
            db.flush()



            items = json.loads(queue.payload)


            for key, value in items.items():

                db.add(
                    ConceptItem(
                        concept_id=concept.id,
                        item_key=key,
                        item_value=str(value),
                        created_at=str(datetime.utcnow())
                    )
                )



            db.add(
                ConceptSystem(
                    concept_id=concept.id,
                    concept_code=queue.concept_code,
                    creator=queue.creator_user_code,
                    status="APPROVED",
                    completeness=len(items),
                    created_at=str(datetime.utcnow())
                )
            )



            queue.status = "APPROVED"
            queue.approved_by = approver
            queue.reviewed_at = datetime.utcnow()


            db.commit()



            event_bus = get_event_bus()

            event_bus.emit(
                "GOVERNANCE",
                "CONCEPT_APPROVED",
                "concept",
                {
                    "concept_id": concept.id,
                    "concept_code": concept.code,
                    "approved_by": approver,
                    "creator": queue.creator_user_code,
                }
            )



            return {
                "status": "APPROVED",
                "concept_id": concept.id,
                "concept_code": concept.code
            }


        finally:
            db.close()
