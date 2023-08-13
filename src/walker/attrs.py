from typing import Final, TypeAlias

FinalStr: TypeAlias = Final[str]


class AppConfig:
    PORT: FinalStr = "port"
    HOST: FinalStr = "host"
    DEBUG: FinalStr = "DEBUG"
    LOGGING: FinalStr = "logging"


class LoggingConfig:
    LEVEL: FinalStr = "level"
    DESTINATION: FinalStr = "destination"


__all__ = ["AppConfig", "LoggingConfig"]
