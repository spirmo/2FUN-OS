from fastapi import APIRouter

from app.channel.models import ChannelRequest, ChannelResponse


router = APIRouter(
    prefix="/channel",
    tags=["Channel"],
)


@router.post("/request")
async def receive_channel_request(request: ChannelRequest):
    return ChannelResponse(
        status="accepted",
        response=None,
        events=[],
        metadata={
            "channel": request.channel,
            "external_user": request.external_user,
        },
    )
