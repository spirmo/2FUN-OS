import traceback
import logging

logger = logging.getLogger(__name__)

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
    try:
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

    except Exception as e:
        logger.error("CONCEPT SUBMIT FAILED")
        logger.error(str(e))
        logger.error(traceback.format_exc())

        return {
            "error": str(e),
            "type": type(e).__name__,
        }


@router.get("/pending")
async def pending_concepts():
    try:
        repository = ConceptVersionRepository()

        items = repository.get_pending_approvals()

        return {
            "success": True,
            "count": len(items),
            "items": items,
        }

    except Exception as e:
        logger.error("GET PENDING CONCEPTS FAILED")
        logger.error(str(e))
        logger.error(traceback.format_exc())

        return {
            "success": False,
            "error": str(e),
            "type": type(e).__name__,
        }

@router.get("")
async def get_concepts():
    try:
        repository = ConceptVersionRepository()
        items = repository.get_all_concepts()

        return {
            "success": True,
            "count": len(items),
            "items": [dict(item) for item in items],
        }

    except Exception as e:
        logger.error("GET CONCEPTS FAILED")
        logger.error(str(e))
        logger.error(traceback.format_exc())

        return {
            "success": False,
            "error": str(e),
            "type": type(e).__name__,
        }

@router.get("/{concept_code}")
async def get_concept(concept_code: str, version: str = "1.0"):
    try:
        repository = ConceptVersionRepository()

        concept = repository.load_concept(
            concept_code=concept_code,
            version=version,
        )

        if concept is None:
            return {
                "success": False,
                "reason": "CONCEPT_NOT_FOUND",
            }

        return {
            "success": True,
            "concept": {
                "id": concept.system.database_id,
                "concept_code": concept.concept_code,
                "version": concept.system.version,
                "status": concept.system.status,
                "completeness": concept.system.completeness,
                "creator": concept.system.creator,
                "items": {
                    key: item.value
                    for key, item in concept.items.items()
                },
            },
        }

    except Exception as e:
        logger.error("GET CONCEPT FAILED")
        logger.error(str(e))
        logger.error(traceback.format_exc())

        return {
            "success": False,
            "error": str(e),
            "type": type(e).__name__,
        }


@router.post("/{queue_id}/reject")
async def reject_concept(queue_id: int, payload: dict):
    rejected_by = str(payload.get("rejected_by") or "").strip()
    rejection_reason = str(
        payload.get("rejection_reason") or ""
    ).strip()

    if not rejected_by:
        return {
            "success": False,
            "reason": "REJECTED_BY_REQUIRED",
            "approval_id": queue_id,
        }

    if not rejection_reason:
        return {
            "success": False,
            "reason": "REJECTION_REASON_REQUIRED",
            "approval_id": queue_id,
        }

    submission = application.repository.get_approval_submission(
        queue_id
    )

    if not submission:
        return {
            "success": False,
            "reason": "APPROVAL_SUBMISSION_NOT_FOUND",
            "approval_id": queue_id,
        }

    if submission["status"] != "SUBMITTED":
        return {
            "success": False,
            "reason": "APPROVAL_SUBMISSION_ALREADY_REVIEWED",
            "status": submission["status"],
            "approval_id": queue_id,
        }

    import json

    payload_data = json.loads(submission["payload"])

    concept = Concept()

    for key, value in payload_data.get("items", {}).items():
        if concept.has_valid_item_key(key):
            concept.set_item(
                ConceptItem(
                    item_key=key,
                    value=value,
                )
            )

    concept.system.version = submission["version"]
    concept.system.status = payload_data.get(
        "status",
        "PENDING_REVIEW",
    )
    concept.system.completeness = payload_data.get(
        "completeness",
        0,
    )

    return application.reject_submission(
        concept,
        approval_id=queue_id,
        rejected_by=rejected_by,
        rejection_reason=rejection_reason,
    )


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
