from fastapi import APIRouter

from app.core.platform_core_bridge import event_bus
from app.core.config import APP_SCHEME, BOT_USERNAME
from app.services.jwt_service import create_token

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
    token = create_token({"sub": "telegram_user"})
    event_bus.emit(
    source="platform_api",
    event_type="TELEGRAM_LOGIN_SUCCESS",
    target="identity",
    value={
        "provider": "telegram",
        "user": "telegram_user",
    },
)
    
    return {
        "status": "authenticated",
        "access_token": token,
        "token_type": "Bearer",
    }
