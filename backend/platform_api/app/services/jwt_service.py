import jwt
from app.core.config import JWT_SECRET

def create_token(payload: dict) -> str:
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")
