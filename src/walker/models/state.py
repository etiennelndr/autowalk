from ._base import Model
from .ray import Ray


class State(Model):
    rays: list[Ray]


__all__ = ["State"]
