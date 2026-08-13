from fastapi import APIRouter

from app.diagnostic.storage import DiagnosticStorage


router = APIRouter(
    prefix="/diagnostic",
    tags=["Diagnostic"],
)

storage = DiagnosticStorage()


@router.post("/crash")
async def receive_crash(payload: dict):
    storage.save(payload)

    return {
        "status": "received",
    }
