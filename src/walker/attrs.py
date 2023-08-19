from typing import Final, TypeAlias

FinalStr: TypeAlias = Final[str]


class App:
    STATES: FinalStr = "states"


class AppConfig:
    PORT: FinalStr = "port"
    HOST: FinalStr = "host"
    DEBUG: FinalStr = "DEBUG"
    LOGGING: FinalStr = "logging"
    MODULES: FinalStr = "modules"


class ModulesConfig:
    TRAINING: FinalStr = "training"
    RUNTIME: FinalStr = "runtime"


class TrainingModuleConfig:
    PATH: FinalStr = "path"


class LoggingConfig:
    LEVEL: FinalStr = "level"
    DESTINATION: FinalStr = "destination"


__all__ = ["AppConfig", "LoggingConfig"]
