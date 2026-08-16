from __future__ import annotations

from datetime import UTC, datetime, timedelta

from soccer_betway.domain import Quote


def demo_quotes() -> list[Quote]:
    """Deterministic fixture demonstrating one qualifying and one rejected selection."""
    start = datetime.now(UTC) + timedelta(days=1)
    rows = []
    # Intentionally stale-looking price disagreement for testing the value gate:
    # Betway offers 1.25 while three consensus books imply a much shorter favorite.
    prices = {"betway": [1.25, 8.0, 18.0], "pinnacle": [1.05, 25.0, 40.0],
              "betfair_ex_uk": [1.05, 25.0, 40.0], "williamhill": [1.05, 25.0, 40.0]}
    names = ["Cape Town City", "Draw", "Example United"]
    for book, odds in prices.items():
        for name, price in zip(names, odds):
            rows.append(Quote(event_id="demo-001", league_key="soccer_demo", league="Demo League",
                commence_time=start, home_team="Cape Town City", away_team="Example United",
                bookmaker=book, market="h2h", selection=name, price=price,
                last_update=datetime.now(UTC)))
    return rows
