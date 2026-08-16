from __future__ import annotations

import typer

from fbcli import DEFAULT_API_VERSION, __version__
from fbcli.commands import auth, comments, insights, pages, posts, raw, slip
from fbcli.context import AppState
from fbcli.errors import ConfigError, GraphError
from fbcli.output import FORMATS, err_console

app = typer.Typer(
    name="fbcli",
    no_args_is_help=True,
    add_completion=True,
    help="Interact with the Facebook Graph API from the terminal.",
    rich_markup_mode="rich",
)

app.add_typer(auth.app, name="auth")
app.add_typer(pages.app, name="pages")
app.add_typer(posts.app, name="posts")
app.add_typer(comments.app, name="comments")
app.add_typer(insights.app, name="insights")
app.add_typer(slip.app, name="slip")
app.add_typer(raw.app, name="api")


def _version(value: bool) -> None:
    if value:
        typer.echo(f"fbcli {__version__} (Graph API {DEFAULT_API_VERSION})")
        raise typer.Exit()


@app.callback()
def main(
    ctx: typer.Context,
    profile: str | None = typer.Option(None, "--profile", "-p", help="Credential profile to use.",
                                       envvar="FB_PROFILE"),
    api_version: str | None = typer.Option(None, "--api-version", envvar="FB_API_VERSION",
                                           help="Override the Graph API version."),
    output: str = typer.Option("table", "--output", "-o",
                               help=f"Output format: {', '.join(FORMATS)}."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Print writes instead of sending them."),
    timeout: float = typer.Option(30.0, "--timeout", help="HTTP timeout in seconds."),
    version: bool = typer.Option(False, "--version", callback=_version, is_eager=True,
                                 help="Show the version and exit."),
) -> None:
    """A small, explicit Graph API client.

    Credentials live in ~/.config/fbcli/credentials.json (chmod 600) or in the
    FB_ACCESS_TOKEN / FB_APP_ID / FB_APP_SECRET environment variables.
    """
    if output not in FORMATS:
        raise typer.BadParameter(f"--output must be one of {', '.join(FORMATS)}")
    ctx.obj = AppState(
        profile_name=profile, api_version=api_version, output=output,
        dry_run=dry_run, timeout=timeout,
    )


def run() -> None:
    """Entry point with friendly error reporting."""
    try:
        app()
    except GraphError as exc:
        err_console.print(f"[red]Graph API error:[/red] {exc}")
        hint = exc.hint()
        if hint:
            err_console.print(f"[yellow]hint:[/yellow] {hint}")
        raise SystemExit(2) from exc
    except ConfigError as exc:
        err_console.print(f"[red]Configuration error:[/red] {exc}")
        raise SystemExit(3) from exc
    except KeyboardInterrupt:  # pragma: no cover
        err_console.print("[yellow]Aborted.[/yellow]")
        raise SystemExit(130) from None


if __name__ == "__main__":
    run()
