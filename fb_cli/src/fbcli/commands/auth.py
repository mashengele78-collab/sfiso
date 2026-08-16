from __future__ import annotations

from datetime import UTC, datetime

import typer

from fbcli.config import Profile, mask
from fbcli.context import AppState, get_state
from fbcli.output import emit, emit_object, info, success, warn

app = typer.Typer(no_args_is_help=True, help="Manage tokens and profiles.")


def _ts(value: object) -> str:
    try:
        seconds = int(value)  # type: ignore[arg-type]
    except (TypeError, ValueError):
        return "—"
    if seconds == 0:
        return "never (long-lived)"
    return datetime.fromtimestamp(seconds, tz=UTC).strftime("%Y-%m-%d %H:%M UTC")


@app.command()
def login(
    ctx: typer.Context,
    token: str = typer.Option(..., "--token", "-t", prompt=True, hide_input=True,
                              help="User or page access token."),
    app_id: str | None = typer.Option(None, "--app-id",
                                      help="Meta app id (enables appsecret_proof)."),
    app_secret: str | None = typer.Option(None, "--app-secret", help="Meta app secret."),
    profile: str | None = typer.Option(None, "--as", help="Save under this profile name."),
    verify: bool = typer.Option(True, help="Call /me to confirm the token works."),
) -> None:
    """Store credentials in ~/.config/fbcli/credentials.json (chmod 600)."""
    state: AppState = get_state(ctx)
    name = profile or state.profile_name or state.store.current_name()
    existing = state.store.load(name)
    saved = Profile(
        name=name,
        access_token=token,
        app_id=app_id or existing.app_id,
        app_secret=app_secret or existing.app_secret,
        api_version=state.api_version or existing.api_version,
        base_url=existing.base_url,
        default_page_id=existing.default_page_id,
        pages=existing.pages,
    )
    state.store.save(saved)
    success(f"Saved profile [bold]{name}[/bold] → {state.store.path}")
    if verify:
        state._profile = saved
        with state.client() as client:
            who = client.me("id,name")
        emit_object(who, fmt=state.output, title="Authenticated as")


@app.command()
def status(ctx: typer.Context) -> None:
    """Show the active profile without revealing secrets."""
    state: AppState = get_state(ctx)
    p = state.profile
    emit_object(
        {
            "profile": p.name,
            "api_version": p.api_version,
            "access_token": mask(p.access_token),
            "app_id": p.app_id or "—",
            "app_secret": mask(p.app_secret),
            "appsecret_proof": "enabled" if p.app_secret else "disabled",
            "default_page_id": p.default_page_id or "—",
            "graph_host": p.base_url,
            "cached_page_tokens": len(p.pages),
            "store": str(state.store.path),
        },
        fmt=state.output,
        title="fbcli profile",
    )


@app.command("debug")
def debug_token(
    ctx: typer.Context,
    token: str | None = typer.Option(None, "--token", help="Token to inspect (default: active)."),
) -> None:
    """Inspect a token: app, scopes, expiry, validity."""
    state: AppState = get_state(ctx)
    p = state.profile
    app_id, app_secret = p.require_app()
    subject = token or p.require_token()
    with state.client() as client:
        data = client.debug_token(subject, f"{app_id}|{app_secret}")
    scopes = data.get("scopes") or []
    emit_object(
        {
            "app_id": data.get("app_id"),
            "application": data.get("application"),
            "type": data.get("type"),
            "user_id": data.get("user_id"),
            "is_valid": data.get("is_valid"),
            "issued_at": _ts(data.get("issued_at")),
            "expires_at": _ts(data.get("expires_at")),
            "data_access_expires_at": _ts(data.get("data_access_expires_at")),
            "scopes": ", ".join(scopes) if scopes else "—",
        },
        fmt=state.output,
        title="Token debug",
    )
    if not data.get("is_valid"):
        warn("This token is not valid. Mint a new one in the Graph API Explorer.")


@app.command()
def exchange(ctx: typer.Context) -> None:
    """Exchange a short-lived user token for a long-lived one (~60 days)."""
    state: AppState = get_state(ctx)
    p = state.profile
    app_id, app_secret = p.require_app()
    with state.client() as client:
        payload = client.exchange_long_lived(app_id, app_secret, p.require_token())
    new_token = payload.get("access_token")
    if not new_token:
        warn("No access_token in the response.")
        emit_object(payload, fmt=state.output)
        raise typer.Exit(1)
    p.access_token = new_token
    state.store.save(p)
    expires = payload.get("expires_in")
    success(
        f"Long-lived token stored ({mask(new_token)})"
        + (f", expires in {int(expires) // 86400} days" if expires else "")
    )


@app.command("whoami")
def whoami(
    ctx: typer.Context,
    fields: str = typer.Option("id,name", "--fields", "-f"),
) -> None:
    """Fetch /me for the active token."""
    state: AppState = get_state(ctx)
    with state.client() as client:
        emit_object(client.me(fields), fmt=state.output, title="/me")


@app.command("profiles")
def list_profiles(ctx: typer.Context) -> None:
    """List saved profiles."""
    state: AppState = get_state(ctx)
    current = state.store.current_name()
    rows = []
    for name in state.store.profile_names():
        p = state.store.load(name)
        rows.append(
            {
                "profile": name,
                "current": "*" if name == current else "",
                "api_version": p.api_version,
                "token": mask(p.access_token),
                "default_page": p.default_page_id or "—",
            }
        )
    emit(rows, fmt=state.output, title="Profiles",
         empty="No profiles saved yet — run `fbcli auth login`.")


@app.command()
def logout(
    ctx: typer.Context,
    profile: str | None = typer.Option(None, "--profile", "-p"),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip confirmation."),
) -> None:
    """Delete a stored profile and its cached page tokens."""
    state: AppState = get_state(ctx)
    name = profile or state.store.current_name()
    if not yes:
        typer.confirm(f"Delete profile '{name}' and its tokens?", abort=True)
    if state.store.delete(name):
        success(f"Removed profile {name}.")
    else:
        info(f"No stored profile named {name}.")
