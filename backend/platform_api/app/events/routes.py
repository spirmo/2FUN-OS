from fastapi import APIRouter
from app.core.platform_core_bridge import event_bus


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.post("/")
async def receive_event(payload: dict):

    result = event_bus.emit(
        source=payload.get("source"),
        event_type=payload.get("event_type"),
        target=payload.get("target"),
        value=payload.get("value"),
    )

    return result
