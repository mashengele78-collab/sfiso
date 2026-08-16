from __future__ import annotations

import typer

from fbcli.config import mask
from fbcli.context import AppState, get_state
from fbcli.output import emit, emit_object, success, warn

app = typer.Typer(no_args_is_help=True, help="Work with the Pages you manage.")


@app.command("list")
def list_pages(
    ctx: typer.Context,
    save_tokens: bool = typer.Option(True, "--save-tokens/--no-save-tokens",
                                     help="Cache page access tokens in the profile."),
    limit: int = typer.Option(50, "--limit", "-n"),
) -> None:
    """List Pages on /me/accounts and cache their page tokens."""
    state: AppState = get_state(ctx)
    profile = state.profile
    with state.client() as client:
        pages = client.collect(
            "me/accounts",
            limit=limit,
            fields="id,name,category,tasks,access_token,followers_count",
        )
    if save_tokens and pages:
        for page in pages:
            if page.get("access_token"):
                profile.pages[page["id"]] = page["access_token"]
        if not profile.default_page_id and len(pages) == 1:
            profile.default_page_id = pages[0]["id"]
        state.store.save(profile, make_current=False)
    rows = [
        {
            "id": page.get("id"),
            "name": page.get("name"),
            "category": page.get("category"),
            "followers": page.get("followers_count"),
            "tasks": ",".join(page.get("tasks") or []),
            "token": mask(page.get("access_token")),
            "default": "*" if page.get("id") == profile.default_page_id else "",
        }
        for page in pages
    ]
    emit(rows, fmt=state.output, title="Pages", empty="No Pages. The token needs pages_show_list.")
    if state.output == "table" and rows and not profile.default_page_id:
        warn("Pick a default with `fbcli pages use <id>`.")


@app.command("use")
def use_page(ctx: typer.Context, page_id: str = typer.Argument(...)) -> None:
    """Set the default Page for later commands."""
    state: AppState = get_state(ctx)
    profile = state.profile
    profile.default_page_id = page_id
    state.store.save(profile, make_current=False)
    success(f"Default page set to {page_id}.")


@app.command("show")
def show_page(
    ctx: typer.Context,
    page_id: str | None = typer.Option(None, "--page", "-P"),
    fields: str = typer.Option(
        "id,name,username,about,category,link,fan_count,followers_count,"
        "verification_status,website,phone,emails",
        "--fields",
        "-f",
    ),
) -> None:
    """Show profile details for a Page."""
    state: AppState = get_state(ctx)
    client, pid = state.page_client(page_id)
    with client:
        emit_object(client.get(pid, fields=fields), fmt=state.output, title=f"Page {pid}")


@app.command("search")
def search_pages(
    ctx: typer.Context,
    query: str = typer.Argument(..., help="Search term."),
    limit: int = typer.Option(10, "--limit", "-n"),
) -> None:
    """Search public Pages (requires Page Public Content Access)."""
    state: AppState = get_state(ctx)
    with state.client() as client:
        rows = client.collect(
            "pages/search", q=query, fields="id,name,link,verification_status", limit=limit
        )
    emit(rows, fmt=state.output, title=f"Pages matching {query!r}",
         empty="Nothing found (this edge needs Page Public Content Access).")
