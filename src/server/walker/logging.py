import logging
import sys

import loguru
from pydantic import BaseModel, Field

from .attrs import LoggingConfig as LoggingConfigAttrs


class _InterceptHandler(logging.Handler):
    def emit(self, record):
        logger_opt = loguru.logger.opt(depth=6, exception=record.exc_info)
        logger_opt.log(record.levelno, record.getMessage())


class LoggingOptions(BaseModel):
    destination: str | None = Field(None, alias=LoggingConfigAttrs.DESTINATION)
    level: str = Field(..., alias=LoggingConfigAttrs.LEVEL)


def configure(
    logger: logging.Logger,
    options: LoggingOptions,
) -> None:
    """Configures a logger."""
    try:
        loguru.logger.remove(handler_id=0)
    except ValueError:
        pass

    destination = options.destination
    if destination in ["-", None]:
        destination = sys.stdout
    loguru.logger.add(destination, level=options.level)

    clear_logger(logger)
    logger.addHandler(_InterceptHandler(level=options.level))


def clear_logger(logger: logging.Logger) -> None:
    """Clears a specific logger by removing all of its handlers."""
    logger.handlers = []


__all__ = ["LoggingOptions", "clear_logger", "configure"]
