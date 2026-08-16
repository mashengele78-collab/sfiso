from __future__ import annotations

import json

import typer

from fbcli.context import AppState, get_state
from fbcli.output import console, emit, emit_object

app = typer.Typer(no_args_is_help=True, help="Call any Graph API endpoint directly.")


def _parse_pairs(pairs: list[str]) -> dict[str, str]:
    out: dict[str, str] = {}
    for pair in pairs:
        if "=" not in pair:
            raise typer.BadParameter(f"Expected key=value, got {pair!r}")
        key, value = pair.split("=", 1)
        out[key.strip()] = value
    return out


@app.command("get")
def raw_get(
    ctx: typer.Context,
    path: str = typer.Argument(..., help="Edge, e.g. me/accounts or 12345/feed."),
    param: list[str] = typer.Option([], "--param", "-d", help="key=value (repeatable)."),
    page_id: str | None = typer.Option(None, "--page", "-P", help="Use this page's token."),
    paginate: bool = typer.Option(False, "--paginate", help="Follow next cursors."),
    limit: int = typer.Option(100, "--limit", "-n", help="Max items when paginating."),
) -> None:
    """GET any edge."""
    state: AppState = get_state(ctx)
    params = _parse_pairs(param)
    client, _ = state.page_client(page_id) if page_id else (state.client(), None)
    with client:
        if paginate:
            emit(client.collect(path, limit=limit, **params),
                 fmt=state.output if state.output != "table" else "json")
            return
        payload = client.get(path, **params)
    if isinstance(payload, dict) and isinstance(payload.get("data"), list):
        emit(payload["data"], fmt=state.output if state.output != "table" else "json")
    elif isinstance(payload, dict):
        emit_object(payload, fmt=state.output, title=path)
    else:
        console.print_json(json.dumps(payload, default=str))


@app.command("post")
def raw_post(
    ctx: typer.Context,
    path: str = typer.Argument(...),
    param: list[str] = typer.Option([], "--param", "-d", help="key=value (repeatable)."),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """POST to any edge. Writes are confirmed unless --yes."""
    state: AppState = get_state(ctx)
    params = _parse_pairs(param)
    client, _ = state.page_client(page_id) if page_id else (state.client(), None)
    if state.preview(f"POST /{path}", params):
        return
    if not yes:
        typer.confirm(f"POST /{path} with {params}?", abort=True)
    with client:
        emit_object(client.post(path, **params), fmt=state.output, title=path)


@app.command("delete")
def raw_delete(
    ctx: typer.Context,
    path: str = typer.Argument(...),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """DELETE any node."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id) if page_id else (state.client(), None)
    if state.preview(f"DELETE /{path}", {"path": path}):
        return
    if not yes:
        typer.confirm(f"DELETE /{path}?", abort=True)
    with client:
        emit_object(client.delete(path), fmt=state.output, title=path)
