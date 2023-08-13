from ._base import Model


class Ray(Model):
    direction: str
    value: float


__all__ = ["Ray"]
