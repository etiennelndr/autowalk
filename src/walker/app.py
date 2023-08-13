import os
from pathlib import Path
from typing import Any, Final, Mapping

from confuse import Configuration, Optional
from confuse.sources import EnvSource, YamlSource
from quart import Quart
from quart_schema import QuartSchema

from . import attrs, config, logging
from .bp.walks import walks_bp
from .logging import LoggingOptions

APP_NAME: Final[str] = "walker"
APP_CONFIG_TEMPLATE: Final[Mapping[str, Any]] = {
    attrs.AppConfig.HOST: str,
    attrs.AppConfig.PORT: int,
    attrs.AppConfig.DEBUG: bool,
    attrs.AppConfig.LOGGING: {
        attrs.LoggingConfig.DESTINATION: Optional(str),
        attrs.LoggingConfig.LEVEL: str,
    },
}


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
    # Validate parameters from the defaukt configuration retrieved by Confuse. Those parameters
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
    app.register_blueprint(walks_bp)
    configure_app(app, filepath=config_path)
    # Apply QuartSchema on the application to enable request and response validations
    QuartSchema(app, convert_casing=True)
    return app


__all__ = ["configure_app", "create_app"]
