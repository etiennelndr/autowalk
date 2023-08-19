from quart import Blueprint
from quart_schema import validate_request

from walker.models.state import State

states_bp = Blueprint(name="states", import_name=__name__, url_prefix="/states")


@states_bp.post("/", strict_slashes=False)
@validate_request(State)
async def create_state(data: State) -> str:
    return "State created"


__all__ = ["states_bp"]
