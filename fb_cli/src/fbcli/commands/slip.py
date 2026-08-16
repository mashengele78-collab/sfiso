"""Publish this repository's soccer-ML output to a Facebook Page.

Reads soccer_ml/reports/latest.json (the artefact the daily workflow writes)
and turns it into a Page post. Nothing is invented: if there are no qualifying
selections the post says so.
"""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from typing import Any

import typer

from fbcli.context import AppState, get_state
from fbcli.output import console, emit_object, info, success, warn

app = typer.Typer(no_args_is_help=True, help="Publish soccer-ML reports to a Page.")

DISCLAIMER = (
    "Probabilities are estimates, not guarantees. Odds move — verify every price "
    "before betting. 18+. Bet only where legal and only what you can afford to lose."
)


def _default_report() -> Path:
    """Locate soccer_ml/reports/latest.json from anywhere in the repo."""
    for base in [Path.cwd(), *Path.cwd().parents]:
        candidate = base / "soccer_ml" / "reports" / "latest.json"
        if candidate.exists():
            return candidate
    return Path("soccer_ml/reports/latest.json")


def _load(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise typer.BadParameter(
            f"{path} not found. Run `soccer-betway predict --demo` first, or pass --report."
        )
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"{path} is not valid JSON: {exc}") from exc


def _kickoff(value: str | None) -> str:
    if not value:
        return "TBC"
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).strftime("%d %b %H:%M UTC")
    except ValueError:
        return value[:16].replace("T", " ")


def render(report: dict[str, Any], *, max_selections: int, include_stakes: bool) -> str:
    candidates = report.get("candidates") or []
    generated = _kickoff(report.get("generated_at"))
    lines = [f"⚽ Soccer value scan — {generated}", ""]

    if not candidates:
        lines += [
            "No qualifying bets today.",
            "",
            f"Nothing cleared the probability, edge, coverage and freshness gates "
            f"across {report.get('quote_count', 0)} quotes. No bet is a result too.",
        ]
    else:
        shown = candidates[:max_selections]
        lines.append(f"{len(candidates)} selection(s) cleared every gate:")
        lines.append("")
        for i, c in enumerate(shown, start=1):
            line = (
                f"{i}. {c.get('fixture')} ({c.get('league')})\n"
                f"   {c.get('market')} · {c.get('selection')} "
                f"@ {float(c.get('betway_odds', 0)):.2f}\n"
                f"   est. {float(c.get('estimated_probability', 0)):.0%} · "
                f"edge {float(c.get('edge', 0)):+.1%} · {_kickoff(c.get('commence_time'))}"
            )
            if include_stakes and c.get("stake") is not None:
                line += f"\n   suggested stake {float(c['stake']):.2f}"
            lines.append(line)
        if len(candidates) > len(shown):
            lines.append(f"…and {len(candidates) - len(shown)} more in the full report.")

    lines += ["", DISCLAIMER]
    return "\n".join(lines)


@app.command("preview")
def preview(
    ctx: typer.Context,
    report: Path | None = typer.Option(None, "--report", "-r", help="Path to latest.json."),
    max_selections: int = typer.Option(5, "--max", help="Selections to include."),
    include_stakes: bool = typer.Option(False, "--stakes/--no-stakes"),
) -> None:
    """Render the post text without touching Facebook."""
    state: AppState = get_state(ctx)
    path = report or _default_report()
    text = render(_load(path), max_selections=max_selections, include_stakes=include_stakes)
    if state.output == "json":
        emit_object({"source": str(path), "message": text, "characters": len(text)}, fmt="json")
        return
    info(f"source: {path}")
    console.print(text, highlight=False, markup=False)
    info(f"{len(text)} characters")


@app.command("publish")
def publish(
    ctx: typer.Context,
    report: Path | None = typer.Option(None, "--report", "-r"),
    page_id: str | None = typer.Option(None, "--page", "-P"),
    max_selections: int = typer.Option(5, "--max"),
    include_stakes: bool = typer.Option(False, "--stakes/--no-stakes",
                                        help="Include monetary stake suggestions."),
    skip_if_empty: bool = typer.Option(True, "--skip-if-empty/--post-if-empty",
                                       help="Do not post when there are no qualifying bets."),
    link: str | None = typer.Option(None, "--link", help="Link to the dashboard."),
    yes: bool = typer.Option(False, "--yes", "-y"),
) -> None:
    """Post the latest soccer-ML report to a Page."""
    state: AppState = get_state(ctx)
    path = report or _default_report()
    data = _load(path)
    candidates = data.get("candidates") or []
    if not candidates and skip_if_empty:
        warn("No qualifying bets — nothing published (use --post-if-empty to override).")
        raise typer.Exit(0)

    message = render(data, max_selections=max_selections, include_stakes=include_stakes)
    payload = {"message": message, "link": link}
    payload = {k: v for k, v in payload.items() if v is not None}
    client, pid = state.page_client(page_id)
    if state.preview(f"POST /{pid}/feed", payload):
        return
    if not yes:
        console.print(message, highlight=False, markup=False)
        typer.confirm(f"\nPublish this to page {pid}?", abort=True)
    with client:
        result = client.post(f"{pid}/feed", **payload)
    success(f"Published {result.get('id')} ({len(candidates)} selection(s)).")
    emit_object(result, fmt=state.output)
