from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/telegram")
async def telegram_login():
    return {
        "status": "pending",
        "provider": "telegram"
    }

@router.get("/telegram/callback")
async def telegram_callback():
    return {
        "status": "callback_received"
    }
