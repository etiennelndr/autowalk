import json
from functools import partial
from pathlib import Path

from loguru import logger
from quart import Quart
from walker.bp.states import states_bp
from walker.models.state import State

from ._base import Module


def load_states(path: Path) -> list[State]:
    logger.info(f"Loading training states from '{path}'")
    if not path.exists():
        logger.warning(f"No training file found at '{path}', skipping")
        return []

    with open(path, mode="r", encoding="utf-8") as fstream:
        states = json.load(fstream)
        if not isinstance(states, list):
            raise ValueError(f"File '{path}' does not contain valid training content")
        return [State(**s) for s in states]


def dump_states(path: Path, states: list[State]) -> None:
    logger.info(f"Dumping training states in '{path}'")

    try:
        with open(path, mode="w", encoding="utf-8") as fstream:
            states_as_dict = [s.dict() for s in states]
            json.dump(states_as_dict, fstream, indent=4)
    except FileNotFoundError:
        logger.exception(f"Unable to dump training states in '{path}'")


class TrainerModule(Module):
    states: list[State]

    def __init__(self, app: Quart | None = None, *, path: Path | None = None) -> None:
        self.path = path
        self.states = []

        super().__init__(app)

    def init_app(self, app: Quart) -> None:
        app.register_blueprint(states_bp)

        if self.path is not None:
            self.states = load_states(self.path)
            app.after_serving(partial(dump_states, path=self.path, states=self.states))
        else:
            logger.warning(
                "Training states won't be saved on application shutdown. Restart the application by"
                " providing a path to the training module"
            )

        setattr(app, "states", self.states)


__all__ = ["TrainerModule"]
