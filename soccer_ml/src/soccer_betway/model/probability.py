from __future__ import annotations

from collections import defaultdict
from math import sqrt
from pathlib import Path
from typing import Any

import joblib
import numpy as np
import pandas as pd

from soccer_betway.domain import Quote

Key = tuple[str, str, str, float | None]


def _side(selection: str, home: str, away: str) -> str | None:
    name = selection.casefold()
    if selection == home or name in {"home", "1"}:
        return "home"
    if selection == away or name in {"away", "2"}:
        return "away"
    if name in {"draw", "x"}:
        return "draw"
    return None


def no_vig_probabilities(quotes: list[Quote]) -> dict[Key, list[float]]:
    """Estimate fair probabilities per book.

    Mutually exclusive markets are normalized directly. Draw-no-bet and double
    chance are derived from each book's no-vig 1X2 probabilities when possible.
    """
    groups: dict[tuple[str, str, float | None, str], list[Quote]] = defaultdict(list)
    event_teams: dict[str, tuple[str, str]] = {}
    for quote in quotes:
        groups[(quote.event_id, quote.market, quote.point, quote.bookmaker)].append(quote)
        event_teams[quote.event_id] = (quote.home_team, quote.away_team)

    result: dict[Key, list[float]] = defaultdict(list)
    h2h_by_book: dict[tuple[str, str], dict[str, float]] = {}

    # Standard mutually exclusive markets: 1X2, totals and BTTS.
    for (event_id, market, point, book), outcomes in groups.items():
        if market in {"double_chance", "draw_no_bet"}:
            continue
        inverse = [1 / quote.price for quote in outcomes]
        overround = sum(inverse)
        if len(outcomes) < 2 or overround <= 0:
            continue
        fair = [raw / overround for raw in inverse]
        for quote, probability in zip(outcomes, fair):
            result[quote.selection_key].append(probability)
        if market in {"h2h", "h2h_3_way"}:
            home, away = event_teams[event_id]
            sides = {_side(q.selection, home, away): p for q, p in zip(outcomes, fair)}
            if all(side in sides for side in ("home", "draw", "away")):
                h2h_by_book[(event_id, book)] = sides  # type: ignore[assignment]

    # Derived soccer markets. This avoids incorrectly normalizing overlapping
    # double-chance outcomes as though they were mutually exclusive.
    for (event_id, market, _point, book), outcomes in groups.items():
        if market not in {"double_chance", "draw_no_bet"}:
            continue
        base = h2h_by_book.get((event_id, book))
        if not base:
            continue
        home, away = event_teams[event_id]
        for quote in outcomes:
            text = quote.selection.casefold()
            if market == "draw_no_bet":
                side = _side(quote.selection, home, away)
                if side not in {"home", "away"}:
                    continue
                probability = base[side] / (base["home"] + base["away"])
            else:
                includes_home = "home" in text or home.casefold() in text or "1" in text
                includes_away = "away" in text or away.casefold() in text or "2" in text
                includes_draw = "draw" in text or "x" in text
                selected = {side for side, yes in (
                    ("home", includes_home), ("draw", includes_draw), ("away", includes_away)
                ) if yes}
                if len(selected) != 2:
                    continue
                probability = sum(base[side] for side in selected)
            result[quote.selection_key].append(probability)
    return result


class ProbabilityEngine:
    """Calibrated artifact when available; conservative consensus baseline otherwise."""

    def __init__(self, settings: dict[str, Any]):
        self.shrinkage = float(settings.get("probability_shrinkage", 0.08))
        self.z = float(settings.get("confidence_z", 1.28))
        path = Path(settings.get("artifact_path", "models/calibrator.joblib"))
        self.model = joblib.load(path) if path.exists() else None

    def estimate(self, probabilities: list[float], market: str, price: float) -> tuple[float, float, str]:
        if not probabilities:
            return 0.0, 0.0, "unavailable"
        mean = float(np.mean(probabilities))
        prior = 1 / 3 if market in {"h2h", "h2h_3_way"} else 1 / 2
        shrunk = (1 - self.shrinkage) * mean + self.shrinkage * prior
        features = pd.DataFrame([{
            "market_probability": shrunk,
            "dispersion": float(np.std(probabilities)),
            "book_count": len(probabilities),
            "betway_implied": 1 / price,
        }])
        if self.model is not None:
            estimate = float(self.model.predict_proba(features)[0, 1])
            source = "trained-calibrator"
        else:
            estimate = shrunk
            source = "no-vig-consensus-baseline"
        n = max(len(probabilities), 1)
        se = sqrt(max(estimate * (1 - estimate), 1e-9) / n)
        lower = max(0.0, estimate - self.z * se)
        return min(max(estimate, 0.0), 1.0), min(lower, estimate), source
