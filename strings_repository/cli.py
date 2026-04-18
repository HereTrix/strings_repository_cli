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


@app.command(help="Initialize a new configuration file for strings repository.")
def init(
    filename: str = typer.Argument(
        None,
        help="Config filename (defaults to strings_repository.yaml)",
    ),
) -> None:
    host = typer.prompt("Enter host (with http or https)")

    typer.secho(
        "Enter environment variable name of API_TOKEN or press ENTER to skip"
    )
    env_var = input()
    access_token = ''
    if not env_var:
        access_token = typer.prompt("Enter access token")
    type = typer.prompt("Enter localization format")
    languages = typer.prompt("Enter languages codes separated by comma")
    tags = typer.prompt("Enter tags separated by comma")
    path = typer.prompt("Enter destination of localization")

    typer.secho(
        "Enter bundle version (e.g. v1, active) or press ENTER to skip"
    )
    bundle = input() or None

    App.init_config(
        filename=filename,
        host=host,
        token=access_token,
        env_var=env_var,
        type=type,
        languages=languages,
        tags=tags,
        path=path,
        bundle=bundle
    )


@app.command(help="Start MCP stdio proxy — forward JSON-RPC messages to the server's /api/mcp endpoint.")
def mcp(
    filename: str = typer.Argument(
        None,
        help="Config filename (defaults to strings_repository.yaml)",
    ),
) -> None:
    try:
        App.mcp(filename)
    except Exception as e:
        typer.secho(str(e), fg=typer.colors.RED)


@app.command(help="Pull localizations from strings repository using config.")
def pull(
    filename: str = typer.Argument(
        None,
        help="Config filename (defaults to strings_repository.yaml)",
    ),
    bundle: Optional[str] = typer.Option(
        None,
        "--bundle",
        "-b",
        help="Bundle version to export (e.g. v1, active). Overrides the bundle set in config.",
    ),
) -> None:
    try:
        App.pull(filename, bundle=bundle)
    except Exception as e:
        typer.secho(e, fg=typer.colors.RED)
