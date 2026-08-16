from __future__ import annotations

import os
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from soccer_betway.config import load_config
from soccer_betway.providers.demo import demo_quotes
from soccer_betway.providers.odds_api import OddsApiProvider
from soccer_betway.reporting import write_reports
from soccer_betway.selector import scan

app = typer.Typer(no_args_is_help=True)
console = Console()


@app.callback()
def main() -> None:
    """Conservative Betway soccer value-bet scanner."""


@app.command()
def predict(config: Path = typer.Option(Path("config/settings.yml")), demo: bool = False,
            bankroll: float | None = typer.Option(None, envvar="BANKROLL")) -> None:
    """Scan every active soccer league and write only qualifying selections."""
    cfg = load_config(config)
    if demo:
        quotes = demo_quotes()
    else:
        key = os.getenv("ODDS_API_KEY")
        if not key:
            raise typer.BadParameter("Set ODDS_API_KEY or use --demo")
        quotes = OddsApiProvider(key, cfg["provider"]).fetch_all_soccer_quotes()
    candidates = scan(quotes, cfg, bankroll)
    json_path, md_path = write_reports(candidates, cfg["report"], len(quotes))
    table = Table("League", "Fixture", "Market", "Selection", "Odds", "Probability", "Edge")
    for c in candidates:
        table.add_row(c.league, c.fixture, c.market, c.selection, f"{c.betway_odds:.2f}",
                      f"{c.estimated_probability:.1%}", f"{c.edge:.1%}")
    if candidates:
        console.print(table)
    else:
        console.print("[yellow]No qualifying bets. Discipline beats forced action.[/yellow]")
    console.print(f"Reports: {md_path}, {json_path}")


if __name__ == "__main__":
    app()
