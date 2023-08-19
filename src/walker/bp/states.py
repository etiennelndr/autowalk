from quart import Blueprint, current_app
from quart_schema import validate_request

from walker.models.state import State
from walker.modules.trainer import get_training_states

states_bp = Blueprint(name="states", import_name=__name__, url_prefix="/states")


@states_bp.post("/", strict_slashes=False)
@validate_request(State)
async def create_state(data: State) -> str:
    states = get_training_states(current_app)
    states.append(data)
    return "State saved"


__all__ = ["states_bp"]