from loguru import logger
from quart import Blueprint, websocket
from quart_schema import validate_request, validate_response

from walker.models.state import State
from walker.models.walk import Walk

walks_bp = Blueprint(name="walks", import_name=__name__, url_prefix="/walks")


@walks_bp.post("/", strict_slashes=False)
@validate_request(State)
@validate_response(Walk)
async def generate_walk(data: State) -> Walk:
    logger.debug(data.dict())
    return Walk(x=0, y=0)


@walks_bp.websocket("/")
async def generate_walks() -> None:
    while True:
        state: State = await websocket.receive_as(State)
        logger.debug(state.dict())
        await websocket.send_as(Walk(x=0, y=0), Walk)


__all__ = ["walks_bp"]
