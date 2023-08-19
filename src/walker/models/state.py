from ._base import Model
from .ray import RayCollision
from .speed import Speed


class State(Model):
    """Representation of a walker state."""

    collisions: list[RayCollision]
    speed: Speed


__all__ = ["State"]
