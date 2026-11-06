import hashlib
import hmac
import json
import time
from urllib.parse import parse_qsl

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.platform_core_bridge import event_bus
from app.core.config import APP_SCHEME, BOT_TOKEN, BOT_USERNAME
from app.services.jwt_service import create_token
from db.database import SessionLocal
from db.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


class TelegramAuthRequest(BaseModel):
    init_data: str


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def validate_telegram_init_data(init_data: str) -> dict:
    if not BOT_TOKEN:
        raise HTTPException(
            status_code=503,
            detail="Telegram authentication is not configured",
        )

    try:
        pairs = parse_qsl(init_data, keep_blank_values=True, strict_parsing=True)
        data = dict(pairs)

        if len(data) != len(pairs):
            raise ValueError("Duplicate fields")

        received_hash = data.pop("hash")
        auth_date = int(data["auth_date"])

        if not hmac.compare_digest(received_hash, received_hash.lower()):
            raise ValueError("Invalid hash")

        data_check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(data.items())
        )

        secret_key = hmac.new(
            b"WebAppData",
            BOT_TOKEN.encode(),
            hashlib.sha256,
        ).digest()

        expected_hash = hmac.new(
            secret_key,
            data_check_string.encode(),
            hashlib.sha256,
        ).hexdigest()

        if not hmac.compare_digest(expected_hash, received_hash):
            raise ValueError("Signature mismatch")

        now = int(time.time())
        if auth_date > now + 30 or now - auth_date > 600:
            raise ValueError("Expired authentication data")

        telegram_user = json.loads(data["user"])
        telegram_id = int(telegram_user["id"])

        if telegram_id <= 0:
            raise ValueError("Invalid Telegram user")

        return {
            "telegram_id": telegram_id,
            "username": telegram_user.get("username"),
        }

    except HTTPException:
        raise
    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired Telegram authentication data",
        )


@router.get("/telegram")
async def telegram_login():
    return {
        "status": "pending",
        "provider": "telegram",
        "bot": BOT_USERNAME,
        "callback_scheme": APP_SCHEME,
        "required_authentication": "Telegram Web App initData",
    }


@router.get("/telegram/callback")
async def disabled_legacy_callback():
    raise HTTPException(
        status_code=410,
        detail="Legacy unauthenticated callback disabled; use verified Telegram initData",
    )


@router.post("/telegram/callback")
async def telegram_callback(
    request: TelegramAuthRequest,
    db: Session = Depends(get_db),
):
    identity = validate_telegram_init_data(request.init_data)

    user = (
        db.query(User)
        .filter(User.telegram_id == identity["telegram_id"])
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=403,
            detail="Telegram account is not linked to a registered 2FUN user",
        )

    if not user.active or str(user.status).upper() != "ACTIVE":
        raise HTTPException(status_code=403, detail="User account is inactive")

    token = create_token({
        "sub": str(user.id),
        "telegram_id": identity["telegram_id"],
    })

    event_bus.emit(
        source="platform_api",
        event_type="TELEGRAM_LOGIN_SUCCESS",
        target="identity",
        value={
            "provider": "telegram",
            "user_id": str(user.id),
            "telegram_id": identity["telegram_id"],
        },
    )

    return {
        "status": "authenticated",
        "access_token": token,
        "token_type": "Bearer",
        "expires_in": 3600,
    }
