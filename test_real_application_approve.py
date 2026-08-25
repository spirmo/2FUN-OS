from sqlalchemy import text

from db.database import SessionLocal
from db.repositories.concept_version_repository import ConceptVersionRepository
from engines.tandil.knowledge.concept.models import Concept
from engines.tandil.knowledge.concept.application import ConceptApplication
import engines.tandil.knowledge.concept.application as application_module


repo = ConceptVersionRepository()

# --------------------------------------------------
# Create real Concept identity
# --------------------------------------------------

concept_id = repo.create_concept(
    creator="TEST_USER",
    concept_code="C_REAL_APPROVE_002",
    version="1.0",
    status="PENDING_REVIEW",
    completeness=30,
)

version_id = repo.create_version(
    concept_id=concept_id,
    concept_code="C_REAL_APPROVE_002",
    version="1.0",
    payload={
        "concept_code": "C_REAL_APPROVE_002",
        "test": True,
    },
    completeness=30,
    status="PENDING_REVIEW",
    created_by="TEST_USER",
)

# --------------------------------------------------
# Create real approval queue record
# --------------------------------------------------

approval_id = repo.create_approval_submission(
    concept_id=concept_id,
    concept_code="C_REAL_APPROVE_002",
    version="1.0",
    creator_user_code="TEST_USER",
    source_mobile_id="TEST_MOBILE",
    payload={
        "concept_code": "C_REAL_APPROVE_002",
        "version": "1.0",
        "completeness": 30,
        "status": "PENDING_REVIEW",
        "test": True,
    },
)

# --------------------------------------------------
# Build Concept object
# --------------------------------------------------

concept = Concept()
concept.system.database_id = concept_id
concept.concept_code = "C_REAL_APPROVE_002"
concept.system.version = "1.0"
concept.status = "PENDING_REVIEW"
concept.completeness = 30

# --------------------------------------------------
# Real EventBus is NOT mocked here.
# --------------------------------------------------

app = ConceptApplication(repository=repo)

result = app.approve_submission(
    concept,
    approval_id=approval_id,
    approved_by="FOUNDER_TEST",
)

print("APPLICATION RESULT:")
print(result)

# --------------------------------------------------
# Read all three canonical persistence layers
# --------------------------------------------------

with SessionLocal() as db:

    queue = db.execute(
        text("""
            SELECT
                id,
                concept_code,
                version,
                status,
                approved_by,
                reviewed_at
            FROM concept_approval_queue_v2
            WHERE id = :id
        """),
        {"id": approval_id},
    ).mappings().first()

    version = db.execute(
        text("""
            SELECT
                id,
                concept_id,
                concept_code,
                version,
                status,
                approved_by,
                approved_at
            FROM concept_versions
            WHERE id = :id
        """),
        {"id": version_id},
    ).mappings().first()

    current = db.execute(
        text("""
            SELECT
                id,
                concept_code,
                current_version,
                current_status,
                current_completeness
            FROM concepts_v2
            WHERE id = :id
        """),
        {"id": concept_id},
    ).mappings().first()

print("QUEUE:")
print(dict(queue) if queue else None)

print("VERSION:")
print(dict(version) if version else None)

print("CURRENT CONCEPT:")
print(dict(current) if current else None)

# --------------------------------------------------
# Assertions
# --------------------------------------------------

assert result["success"] is True

assert queue["status"] == "APPROVED"
assert queue["approved_by"] == "FOUNDER_TEST"
assert queue["reviewed_at"] is not None

assert version["status"] == "APPROVED"
assert version["approved_by"] == "FOUNDER_TEST"
assert version["approved_at"] is not None

assert current["current_status"] == "APPROVED"
assert current["current_version"] == "1.0"
assert current["current_completeness"] == 30

print("REAL APPLICATION APPROVAL INTEGRATION TEST: OK")
