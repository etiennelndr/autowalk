from typer import Typer

from . import asgi


def run() -> None:
    cli_app = Typer(name="walker", no_args_is_help=True)
    cli_app.command(name="server")(asgi.run)
    cli_app()


__all__ = ["run"]
