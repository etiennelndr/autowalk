import os
from pathlib import Path
from typing import Any, Final, Mapping

from confuse import Configuration
from confuse import Optional as OptionalTemplate
from confuse import Path as PathTemplate
from confuse.sources import EnvSource, YamlSource
from loguru import logger
from quart import Quart
from quart_schema import QuartSchema

from walker.modules.runtime import RuntimeModule
from walker.modules.trainer import TrainerModule

from . import attrs, config, logging
from .logging import LoggingOptions

APP_NAME: Final[str] = "walker"
APP_CONFIG_TEMPLATE: Final[Mapping[str, Any]] = {
    attrs.AppConfig.HOST: str,
    attrs.AppConfig.PORT: int,
    attrs.AppConfig.DEBUG: bool,
    attrs.AppConfig.LOGGING: {
        attrs.LoggingConfig.DESTINATION: OptionalTemplate(str),
        attrs.LoggingConfig.LEVEL: str,
    },
    attrs.AppConfig.MODULES: {
        attrs.ModulesConfig.RUNTIME: {},
        attrs.ModulesConfig.TRAINING: {
            "path": PathTemplate(),
        },
    },
}


def activate_modules(app: Quart, modules_config: Mapping[str, Any]) -> None:
    training_module_config = config.get(modules_config, attrs.ModulesConfig.TRAINING, default=None)
    runtime_module_config = config.get(modules_config, attrs.ModulesConfig.RUNTIME, default=None)

    if training_module_config:
        logger.info("Running with 'training' module activated")
        TrainerModule(**training_module_config).init_app(app)
    if runtime_module_config:
        logger.info("Running with 'runtime' module activated")
        RuntimeModule(**runtime_module_config).init_app(app)


def configure_app(app: Quart, *, filepath: Path | None = None) -> None:
    """Configures application."""
    configuration = Configuration(appname=APP_NAME.replace("_", "").lower())

    # Define configuration sources, with the priority for environment variables
    if filepath is not None:
        configuration.set(YamlSource(filepath, loader=configuration.loader))
    configuration.set(
        EnvSource(
            f"{APP_NAME.upper()}_",
            loader=configuration.loader,
            parse_yaml_docs=True,
            handle_lists=False,
        )
    )

    app_name = APP_NAME.upper()
    app_env = os.getenv(f"{app_name}_ENV", default="development")

    config_global = configuration[app_env].get()
    config.update(app.config, config_global)
    # Validate parameters from the default configuration retrieved by Confuse. Those parameters
    # shall respect specific types to avoid configuration errors
    config_default = configuration[app_env].get(APP_CONFIG_TEMPLATE)
    config.update(app.config, config_default)
    # After loading the configuration from the file, overwrites the existing values with those
    # coming from the sources defined above
    config_from_sources = configuration.get()
    config.update(app.config, config_from_sources)

    logging.configure(app.logger, options=LoggingOptions(**app.config[attrs.AppConfig.LOGGING]))


def create_app(config_path: Path | None = None) -> Quart:
    app = Quart(__name__)
    configure_app(app, filepath=config_path)

    modules_config = config.get(app.config, attrs.AppConfig.MODULES)
    activate_modules(app, modules_config)
    # Enable request and response validations with QuartSchema
    QuartSchema(convert_casing=True).init_app(app)
    return app


__all__ = ["configure_app", "create_app"]
