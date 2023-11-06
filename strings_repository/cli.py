from typing import Optional
import typer
from strings_repository.strings_repository import __app_name__, __version__, App

app = typer.Typer()


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{__app_name__} v{__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show the application's version and exit.",
        callback=_version_callback,
        is_eager=True,
    )
) -> None:
    return


@app.command()
def init(
    init: str = typer.Option(
        None,
        "--init",
        "-i",
        help="Create config file",
    ),
) -> None:
    host = typer.prompt("Enter host (with http or https)")
    typer.secho(
        "Enter access token or leave empty to use environment variable STRINGS_REPOSITORY_KEY")
    access_token = input()
    type = typer.prompt("Enter localization format")
    languages = typer.prompt("Enter languages codes separated by comma")
    tags = typer.prompt("Enter tags separated by comma")
    path = typer.prompt("Enter destination of localization")

    App.init_config(
        host=host,
        token=access_token,
        type=type,
        languages=languages,
        tags=tags,
        path=path
    )


@app.command()
def pull(
    pull: str = typer.Option(
        None,
        "--pull",
        "-p",
        help="Pull from repository using config",
    )
) -> None:
    try:
        App.pull()
    except Exception as e:
        typer.secho(e, fg=typer.colors.RED)
