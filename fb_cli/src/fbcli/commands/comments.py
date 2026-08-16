from __future__ import annotations

import typer

from fbcli.context import AppState, get_state
from fbcli.output import emit, emit_object, success

app = typer.Typer(no_args_is_help=True, help="Read and moderate comments.")

COMMENT_FIELDS = "id,created_time,from{id,name},message,like_count,comment_count,permalink_url"


def _row(comment: dict) -> dict:
    return {
        "id": comment.get("id"),
        "created": (comment.get("created_time") or "")[:16].replace("T", " "),
        "from": (comment.get("from") or {}).get("name", "—"),
        "message": (comment.get("message") or "").replace("\n", " "),
        "likes": comment.get("like_count", 0),
        "replies": comment.get("comment_count", 0),
    }


@app.command("list")
def list_comments(
    ctx: typer.Context,
    object_id: str = typer.Argument(..., help="Post, photo or comment id."),
    limit: int = typer.Option(20, "--limit", "-n"),
    order: str = typer.Option("chronological", "--order",
                              help="chronological or reverse_chronological."),
    filter_: str = typer.Option("toplevel", "--filter", help="toplevel or stream."),
    page_id: str | None = typer.Option(None, "--page", "-P"),
) -> None:
    """List comments on a post or replies to a comment."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    with client:
        rows = client.collect(
            f"{object_id}/comments",
            fields=COMMENT_FIELDS,
            order=order,
            filter=filter_,
            limit=limit,
        )
    emit([_row(r) for r in rows], fmt=state.output, title=f"Comments on {object_id}",
         empty="No comments.")


@app.command("reply")
def reply(
    ctx: typer.Context,
    object_id: str = typer.Argument(..., help="Post or comment id to reply to."),
    message: str = typer.Option(..., "--message", "-m"),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Comment on a post, or reply to a comment."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    if state.preview(f"POST /{object_id}/comments", {"message": message}):
        return
    if not yes:
        typer.confirm(f"Reply to {object_id} as the Page?\n\n{message}\n", abort=True)
    with client:
        result = client.post(f"{object_id}/comments", message=message)
    success(f"Comment posted: {result.get('id')}")
    emit_object(result, fmt=state.output)


@app.command("hide")
def hide(
    ctx: typer.Context,
    comment_id: str = typer.Argument(...),
    unhide: bool = typer.Option(False, "--unhide", help="Reveal instead of hide."),
    page_id: str | None = typer.Option(None, "--page", "-P"),
) -> None:
    """Hide or unhide a comment."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    payload = {"is_hidden": not unhide}
    if state.preview(f"POST /{comment_id}", payload):
        return
    with client:
        client.post(comment_id, **payload)
    success(f"{'Unhid' if unhide else 'Hid'} {comment_id}.")


@app.command("delete")
def delete_comment(
    ctx: typer.Context,
    comment_id: str = typer.Argument(...),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Delete a comment."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    if state.preview(f"DELETE /{comment_id}", {"id": comment_id}):
        return
    if not yes:
        typer.confirm(f"Permanently delete comment {comment_id}?", abort=True)
    with client:
        client.delete(comment_id)
    success(f"Deleted {comment_id}.")


@app.command("like")
def like(
    ctx: typer.Context,
    object_id: str = typer.Argument(..., help="Post or comment id."),
    unlike: bool = typer.Option(False, "--unlike"),
    page_id: str | None = typer.Option(None, "--page", "-P"),
) -> None:
    """Like or unlike an object as the Page."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    verb = "DELETE" if unlike else "POST"
    if state.preview(f"{verb} /{object_id}/likes", {"id": object_id}):
        return
    with client:
        if unlike:
            client.delete(f"{object_id}/likes")
        else:
            client.post(f"{object_id}/likes")
    success(f"{'Unliked' if unlike else 'Liked'} {object_id}.")
