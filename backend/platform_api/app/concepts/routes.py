
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

        concept_code=payload.get("concept_code"),

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



