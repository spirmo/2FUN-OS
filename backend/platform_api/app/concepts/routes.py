from fastapi import APIRouter
from engines.tandil.knowledge.concept.models import Concept, ConceptItem
from engines.tandil.knowledge.concept.application import ConceptApplication
from db.repositories.concept_version_repository import ConceptVersionRepository


router = APIRouter(
    prefix="/concepts",
    tags=["Concepts"]
)


application = ConceptApplication()


@router.post("/submit")
async def submit_concept(payload: dict):
    from engines.tandil.knowledge.concept.models import Concept, ConceptItem

    concept = Concept()

    for key, value in payload.get("items", {}).items():
        if concept.has_valid_item_key(key):
            concept.set_item(
                ConceptItem(
                    item_key=key,
                    value=value,
                )
            )

    return application.submit_for_review(
        concept,
        user_id=str(payload.get("creator_user_code") or ""),
        creator_user_code=payload.get("creator_user_code"),
        source_mobile_id=payload.get("source_mobile_id"),
    )


@router.get("/pending")
async def pending_concepts():
    return {
        "status": "MIGRATION_PENDING",
        "owner": "ConceptVersionRepository.get_pending_approvals",
    }


@router.post("/{queue_id}/approve")
async def approve_concept(queue_id: int, payload: dict):
    approved_by = str(payload.get("approved_by") or "").strip()

    if not approved_by:
        return {
            "success": False,
            "reason": "APPROVED_BY_REQUIRED",
            "approval_id": queue_id,
        }

    return application.approve_submission(
        approval_id=queue_id,
        approved_by=approved_by,
    )
