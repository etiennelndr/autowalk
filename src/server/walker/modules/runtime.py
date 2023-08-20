from quart import Quart

from walker.bp.walks import walks_bp

from ._base import Module


class RuntimeModule(Module):
    def init_app(app: Quart) -> None:
        app.register_blueprint(walks_bp)


__all__ = ["RuntimeModule"]
