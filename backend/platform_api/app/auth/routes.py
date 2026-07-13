from fastapi import APIRouter
from app.core.config import BOT_USERNAME, APP_SCHEME

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/telegram")
async def telegram_login():
    return {
        "status": "pending",
        "provider": "telegram",
        "bot": BOT_USERNAME,
        "callback_scheme": APP_SCHEME,
    }

@router.get("/telegram/callback")
async def telegram_callback():
    return {
        "status": "callback_received"
    }
