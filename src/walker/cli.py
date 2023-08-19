from typer import Typer

from . import asgi


def run() -> None:
    cli_app = Typer(name="walker", no_args_is_help=True)
    cli_app.command(name="server", no_args_is_help=True)(asgi.run)
    cli_app()


__all__ = ["run"]
