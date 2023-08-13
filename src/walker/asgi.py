import logging
from pathlib import Path

from uvicorn import Config as ASGIConfig
from uvicorn import Server as ASGIServer

from . import config as cnf
from .app import create_app
from .attrs import AppConfig as AppConfigAttrs
from .logging import clear_logger


def run(config: Path | None = None, host: str | None = None, port: int | None = None) -> None:
    app = create_app(config_path=config)

    host = host or cnf.get(app.config, AppConfigAttrs.HOST, cls=str)
    port = port or cnf.get(app.config, AppConfigAttrs.PORT, cls=int)

    server_config = ASGIConfig(app, host=host, port=port)
    # Deactivate the handlers of 'uvicorn' logger to avoid duplicate logs with 'uvicorn.error'.
    clear_logger(logging.getLogger("uvicorn"))
    logging.getLogger("uvicorn.access").handlers = app.logger.handlers
    logging.getLogger("uvicorn.error").handlers = app.logger.handlers

    server = ASGIServer(server_config)
    server.run()
