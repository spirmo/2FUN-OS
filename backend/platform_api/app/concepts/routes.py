from fastapi import APIRouter

from db.repositories.concept_repository import ConceptRepository


router = APIRouter(
    prefix="/concepts",
    tags=["Concepts"]
)


repository = ConceptRepository()


@router.post("/submit")
async def submit_concept(payload: dict):

    result = repository.submit_concept(

        concept_code=payload.get(
            "concept_code"
        ),

        creator_user_code=payload.get(
            "creator_user_code"
        ),

        title=payload.get(
            "title"
        ),

        domain=payload.get(
            "domain"
        ),

        payload=payload.get(
            "items",
            {}
        ),

        source_mobile_id=payload.get(
            "source_mobile_id"
        ),

    )

    return result



@router.get("/pending")
async def pending_concepts():

    items = repository.get_pending()

    return [
        {
            "id": item.id,
            "concept_code": item.concept_code,
            "title": item.title,
            "domain": item.domain,
            "status": item.status,
            "payload": item.payload,
        }
        for item in items
    ]



@router.post("/{queue_id}/approve")
async def approve_concept(queue_id: int):

    return repository.approve_concept(
        queue_id=queue_id,
        approver="GOVERNANCE_APP",
    )
