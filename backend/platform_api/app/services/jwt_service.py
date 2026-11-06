from datetime import datetime, timedelta, timezone

import jwt
from app.core.config import JWT_SECRET

ALGORITHM = "HS256"
TOKEN_LIFETIME_MINUTES = 60


def create_token(payload: dict) -> str:
    now = datetime.now(timezone.utc)
    claims = dict(payload)
    claims["iat"] = now
    claims["exp"] = now + timedelta(minutes=TOKEN_LIFETIME_MINUTES)
    return jwt.encode(claims, JWT_SECRET, algorithm=ALGORITHM)


def verify_token(token: str) -> dict:
    return jwt.decode(
        token,
        JWT_SECRET,
        algorithms=[ALGORITHM],
        options={"require": ["sub", "iat", "exp"]},
    )
