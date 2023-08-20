from abc import ABC, abstractmethod

from quart import Quart


class Module(ABC):
    def __init__(self, app: Quart | None = None) -> None:
        if app is not None:
            self.init_app(app)

    @abstractmethod
    def init_app(app: Quart) -> None:
        pass


__all__ = ["Module"]
