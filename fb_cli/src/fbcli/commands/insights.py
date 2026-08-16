from __future__ import annotations

import typer

from fbcli.context import AppState, get_state
from fbcli.output import emit, emit_object

app = typer.Typer(no_args_is_help=True, help="Page and post insights.")

PAGE_METRICS = "page_impressions,page_impressions_unique,page_post_engagements,page_daily_follows"
POST_METRICS = "post_impressions,post_impressions_unique,post_engaged_users,post_clicks"


def _flatten(rows: list[dict]) -> list[dict]:
    out: list[dict] = []
    for metric in rows:
        for value in metric.get("values") or []:
            payload = value.get("value")
            if isinstance(payload, dict):
                for key, inner in payload.items():
                    out.append(
                        {
                            "metric": f"{metric.get('name')}.{key}",
                            "period": metric.get("period"),
                            "end_time": (value.get("end_time") or "")[:10],
                            "value": inner,
                        }
                    )
            else:
                out.append(
                    {
                        "metric": metric.get("name"),
                        "period": metric.get("period"),
                        "end_time": (value.get("end_time") or "")[:10],
                        "value": payload,
                    }
                )
    return out


@app.command("page")
def page_insights(
    ctx: typer.Context,
    page_id: str | None = typer.Option(None, "--page", "-P"),
    metrics: str = typer.Option(PAGE_METRICS, "--metrics", "-m", help="Comma-separated metrics."),
    period: str = typer.Option("day", "--period", help="day, week, days_28, month or lifetime."),
    since: str | None = typer.Option(None, "--since", help="ISO date or unix time."),
    until: str | None = typer.Option(None, "--until"),
) -> None:
    """Read Page-level insights."""
    state: AppState = get_state(ctx)
    client, pid = state.page_client(page_id)
    with client:
        payload = client.get(
            f"{pid}/insights", metric=metrics, period=period, since=since, until=until
        )
    emit(_flatten(payload.get("data", [])), fmt=state.output, title=f"Page insights · {pid}",
         empty="No insight data (new Pages and low-traffic Pages often return nothing).")


@app.command("post")
def post_insights(
    ctx: typer.Context,
    post_id: str = typer.Argument(...),
    metrics: str = typer.Option(POST_METRICS, "--metrics", "-m"),
    page_id: str | None = typer.Option(None, "--page", "-P"),
) -> None:
    """Read insights for a single post."""
    state: AppState = get_state(ctx)
    client, _ = state.page_client(page_id)
    with client:
        payload = client.get(f"{post_id}/insights", metric=metrics)
    emit(_flatten(payload.get("data", [])), fmt=state.output, title=f"Post insights · {post_id}",
         empty="No insight data for this post.")


@app.command("usage")
def usage(ctx: typer.Context) -> None:
    """Show rate-limit headers from a cheap probe call."""
    state: AppState = get_state(ctx)
    with state.client() as client:
        client.me("id")
        emit_object(client.last_usage or {"x-app-usage": "not reported"}, fmt=state.output,
                    title="Rate limit usage")
