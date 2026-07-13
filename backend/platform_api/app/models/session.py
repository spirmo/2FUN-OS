from pydantic import BaseModel

class UserSession(BaseModel):
    telegram_id: int
    username: str | None = None
    first_name: str | None = None
    language_code: str | None = None
    jwt_token: str | None = None
