from ._base import Model
from .vector import Vector3


class Ray(Model):
    """An infinite line going in some direction."""

    origin: Vector3
    """Origin of the ray"""
    direction: Vector3
    """Direction of the ray"""


class RayCollision(Model):
    """Representation of the collision between a ray and a collider."""

    ray: Ray
    distance: float
    """Distance between the ray and the collider"""


__all__ = ["Ray", "RayCollision"]
