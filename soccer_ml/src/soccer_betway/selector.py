from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from soccer_betway.domain import Candidate, Quote
from soccer_betway.model.probability import ProbabilityEngine, no_vig_probabilities


def scan(quotes: list[Quote], config: dict[str, Any], bankroll: float | None = None) -> list[Candidate]:
    settings = config["selection"]
    target_book = config["provider"].get("bookmaker", "betway")
    probs = no_vig_probabilities(quotes)
    engine = ProbabilityEngine({**config.get("model", {}), **settings})
    results: list[Candidate] = []
    now = datetime.now(UTC)

    for q in quotes:
        if q.bookmaker != target_book:
            continue
        consensus = probs.get(q.selection_key, [])
        probability, lower, source = engine.estimate(consensus, q.market, q.price)
        gate_probability = lower if settings.get("use_lower_confidence_bound", False) else probability
        implied = 1 / q.price
        edge = probability - implied
        ev = probability * q.price - 1
        stale = q.last_update and (now - q.last_update).total_seconds() > 60 * settings["maximum_odds_age_minutes"]
        checks = [
            gate_probability >= settings["minimum_probability"],
            edge >= settings["minimum_edge"],
            len(consensus) >= settings["minimum_consensus_books"],
            q.price <= settings["maximum_decimal_odds"],
            not stale,
            q.commence_time > now,
        ]
        if not all(checks):
            continue
        full_kelly = max(0.0, (q.price * probability - 1) / (q.price - 1))
        fraction = min(full_kelly * settings["fractional_kelly"], settings["maximum_bankroll_fraction"])
        results.append(Candidate(
            event_id=q.event_id, league=q.league, commence_time=q.commence_time,
            fixture=f"{q.home_team} vs {q.away_team}", market=q.market,
            selection=q.selection, point=q.point, betway_odds=q.price,
            estimated_probability=probability, lower_probability=lower,
            implied_probability=implied, edge=edge, expected_value=ev,
            consensus_books=len(consensus), model_source=source,
            bankroll_fraction=fraction, stake=round(bankroll * fraction, 2) if bankroll else None,
            link=q.link, notes=["Passes configured probability and value gates"],
        ))
    return sorted(results, key=lambda x: (x.expected_value, x.estimated_probability), reverse=True)
