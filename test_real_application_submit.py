from sqlalchemy import text

from db.database import SessionLocal
from db.repositories.concept_version_repository import ConceptVersionRepository
from engines.tandil.knowledge.concept.models import Concept
from engines.tandil.knowledge.concept.application import ConceptApplication


repo = ConceptVersionRepository()

concept_id = repo.create_concept(
    creator="TEST_USER",
    concept_code="C_REAL_SUBMIT_002",
    version="1.0",
    status="OPEN_FOR_COMPLETION",
    completeness=30,
)

repo.create_version(
    concept_id=concept_id,
    concept_code="C_REAL_SUBMIT_002",
    version="1.0",
    payload={
        "concept_code": "C_REAL_SUBMIT_002",
        "test": True,
    },
    completeness=30,
    status="OPEN_FOR_COMPLETION",
    created_by="TEST_USER",
)

concept = Concept()
concept.system.database_id = concept_id
concept.concept_code = "C_REAL_SUBMIT_002"
concept.system.version = "1.0"
concept.status = "OPEN_FOR_COMPLETION"
# --------------------------------------------------
# Complete all mandatory Concept items
# --------------------------------------------------

mandatory_values = {
    "persian_title": "کانسپت تست",
    "domain": "General Knowledge",
    "category": "Integration Test",
    "canonical_meaning": "معنای اصلی تست",
    "definition": "تعریف کانسپت برای تست Submission",
    "short_description": "تست واقعی مسیر ارسال برای بررسی",
    "source": "2FUN Test Source",
    "source_url": "https://example.com/test",
    "source_author": "2FUN TEST",
    "source_year": "2026",
    "evidence": "Integration test evidence",
}

for item_key, value in mandatory_values.items():
    concept.set_item(
        __import__(
            "engines.tandil.knowledge.concept.models",
            fromlist=["ConceptItem"],
        ).ConceptItem(
            item_key=item_key,
            value=value,
            is_required=True,
        )
    )

app = ConceptApplication(repository=repo)

result = app.submit_for_review(
    concept,
    user_id="TEST_USER",
    creator_user_code="TEST_USER",
    source_mobile_id="TEST_MOBILE",
)

print("APPLICATION RESULT:")
print(result)

with SessionLocal() as db:
    queue = db.execute(
        text("""
            SELECT
                id,
                concept_code,
                version,
                status,
                creator_user_code,
                source_mobile_id
            FROM concept_approval_queue_v2
            WHERE id = :id
        """),
        {"id": result["approval_id"]},
    ).mappings().first()

print("QUEUE:")
print(dict(queue) if queue else None)

assert result["success"] is True
assert result["status"] == "PENDING_REVIEW"
assert queue["status"] == "SUBMITTED"
assert queue["creator_user_code"] == "TEST_USER"
assert queue["source_mobile_id"] == "TEST_MOBILE"

print("REAL APPLICATION SUBMIT INTEGRATION TEST: OK")
