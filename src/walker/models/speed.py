from ._base import Model


class Speed(Model):
    """Representation of the speed of a walker, along the x and y axes."""

    x: float
    y: float


__all__ = ["Speed"]
