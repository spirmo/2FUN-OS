from typing import Any

from pydantic import BaseModel, Field


class ChannelRequest(BaseModel):
    """
    Unified HTTP request entering the 2FUN Platform API
    from an external Channel Layer such as 2FUN-BOT.
    """

    channel: str
    external_user: str
    message: str | None = None
    context: dict[str, Any] = Field(default_factory=dict)


class ChannelResponse(BaseModel):
    """
    Unified HTTP response leaving the 2FUN Platform API
    toward an external Channel Layer such as 2FUN-BOT.
    """

    status: str
    response: str | None = None
    events: list[dict[str, Any]] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)
