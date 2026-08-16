from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import typer

from fbcli.context import AppState, get_state
from fbcli.output import emit, emit_object, info, success

app = typer.Typer(no_args_is_help=True, help="Publish, read and remove Page posts.")

FEED_FIELDS = (
    "id,created_time,message,permalink_url,status_type,is_published,"
    "shares,likes.summary(true).limit(0),comments.summary(true).limit(0)"
)


def _summarise(post: dict) -> dict:
    likes = ((post.get("likes") or {}).get("summary") or {}).get("total_count")
    comments = ((post.get("comments") or {}).get("summary") or {}).get("total_count")
    message = (post.get("message") or post.get("story") or "").replace("\n", " ")
    return {
        "id": post.get("id"),
        "created": (post.get("created_time") or "")[:16].replace("T", " "),
        "message": message,
        "likes": likes,
        "comments": comments,
        "shares": (post.get("shares") or {}).get("count", 0),
        "published": post.get("is_published", True),
        "url": post.get("permalink_url"),
    }


def _scheduled(when: str | None) -> int | None:
    if not when:
        return None
    try:
        dt = datetime.fromisoformat(when)
    except ValueError as exc:
        raise typer.BadParameter(
            "Use an ISO timestamp such as 2026-08-20T18:30:00+02:00"
        ) from exc
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=UTC)
    epoch = int(dt.timestamp())
    delta = epoch - int(datetime.now(tz=UTC).timestamp())
    if not (600 <= delta <= 60 * 60 * 24 * 75):
        raise typer.BadParameter(
            "Facebook only accepts schedules 10 minutes to 75 days ahead."
        )
    return epoch


@app.command("list")
def list_posts(
    ctx: typer.Context,
    page_id: str | None = typer.Option(None, "--page", "-P"),
    limit: int = typer.Option(10, "--limit", "-n"),
    edge: str = typer.Option("published_posts", "--edge",
                             help="published_posts, feed, posts or scheduled_posts."),
    since: str | None = typer.Option(None, "--since", help="ISO date or unix time."),
    until: str | None = typer.Option(None, "--until"),
    raw: bool = typer.Option(False, "--raw", help="Return the full Graph payload."),
) -> None:
    """List posts on a Page."""
    state: AppState = get_state(ctx)
    client, pid = state.page_client(page_id)
    with client:
        rows = client.collect(
            f"{pid}/{edge}", fields=FEED_FIELDS, limit=limit, since=since, until=until
        )
    if raw:
        emit(rows, fmt=state.output if state.output != "table" else "json")
        return
    emit([_summarise(r) for r in rows],
         columns=["id", "created", "message", "likes", "comments", "shares", "url"],
         fmt=state.output, title=f"{edge} · {pid}", empty="No posts found.")


@app.command("get")
def get_post(
    ctx: typer.Context,
    post_id: str = typer.Argument(...),
    fields: str = typer.Option(
        FEED_FIELDS + ",full_picture,attachments{title,type,url}", "--fields", "-f"
    ),
    page_id: str | None = typer.Option(None, "--page", "-P"),
) -> None:
    """Fetch a single post."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    with client:
        emit_object(client.get(post_id, fields=fields), fmt=state.output, title=post_id)


@app.command("publish")
def publish(
    ctx: typer.Context,
    message: str | None = typer.Option(None, "--message", "-m", help="Post text."),
    from_file: Path | None = typer.Option(None, "--file", exists=True, dir_okay=False,
                                          help="Read the message from a file."),
    link: str | None = typer.Option(None, "--link", "-l", help="Attach a link."),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    schedule: str | None = typer.Option(None, "--schedule",
                                        help="ISO time; 10 min to 75 days ahead."),
    draft: bool = typer.Option(False, "--draft", help="Create unpublished."),
    yes: bool = typer.Option(False, "--yes", "-y", help="Skip the confirmation prompt."),
) -> None:
    """Publish a text or link post to a Page."""
    state: AppState = get_state(ctx)
    text = from_file.read_text(encoding="utf-8").strip() if from_file else message
    if not text and not link:
        raise typer.BadParameter("Provide --message, --file or --link.")

    payload: dict[str, object] = {"message": text, "link": link}
    when = _scheduled(schedule)
    if when:
        payload["published"] = False
        payload["scheduled_publish_time"] = when
    elif draft:
        payload["published"] = False

    client, pid = state.page_client(page_id)
    payload = {k: v for k, v in payload.items() if v is not None}
    if state.preview(f"POST /{pid}/feed", payload):
        return
    if not yes:
        preview = (text or link or "")[:280]
        typer.confirm(f"Publish to page {pid}?\n\n{preview}\n", abort=True)
    with client:
        result = client.post(f"{pid}/feed", **payload)
    success(f"Post created: {result.get('id')}")
    if when:
        info(f"Scheduled for {datetime.fromtimestamp(when, tz=UTC).isoformat()}")
    emit_object(result, fmt=state.output)


@app.command("photo")
def photo(
    ctx: typer.Context,
    image: Path = typer.Argument(..., exists=True, dir_okay=False, help="Local image file."),
    caption: str | None = typer.Option(None, "--caption", "-c"),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    unpublished: bool = typer.Option(False, "--unpublished",
                                     help="Upload without posting (for multi-photo posts)."),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Upload a photo to a Page."""
    state: AppState = get_state(ctx)
    client, pid = state.page_client(page_id)
    payload = {"caption": caption, "published": not unpublished}
    if state.preview(f"POST /{pid}/photos ({image.name})", {**payload, "source": str(image)}):
        return
    if not yes:
        typer.confirm(f"Upload {image.name} to page {pid}?", abort=True)
    with client, image.open("rb") as fh:
        result = client.post(f"{pid}/photos", files={"source": (image.name, fh)}, **payload)
    success(f"Photo uploaded: {result.get('post_id') or result.get('id')}")
    emit_object(result, fmt=state.output)


@app.command("update")
def update_post(
    ctx: typer.Context,
    post_id: str = typer.Argument(...),
    message: str = typer.Option(..., "--message", "-m"),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Edit the text of an existing post."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    if state.preview(f"POST /{post_id}", {"message": message}):
        return
    if not yes:
        typer.confirm(f"Rewrite post {post_id}?", abort=True)
    with client:
        result = client.post(post_id, message=message)
    success(f"Updated {post_id}.")
    emit_object(result, fmt=state.output)


@app.command("delete")
def delete_post(
    ctx: typer.Context,
    post_id: str = typer.Argument(...),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Delete a post. This cannot be undone."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    if state.preview(f"DELETE /{post_id}", {"id": post_id}):
        return
    if not yes:
        typer.confirm(f"Permanently delete {post_id}?", abort=True)
    with client:
        result = client.delete(post_id)
    success(f"Deleted {post_id}.")
    emit_object(result, fmt=state.output)
