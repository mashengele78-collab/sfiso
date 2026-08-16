from __future__ import annotations

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class Quote(BaseModel):
    event_id: str
    league_key: str
    league: str
    commence_time: datetime
    home_team: str
    away_team: str
    bookmaker: str
    market: str
    selection: str
    price: float = Field(gt=1.0)
    point: float | None = None
    last_update: datetime | None = None
    link: str | None = None

    @property
    def selection_key(self) -> tuple[str, str, str, float | None]:
        return self.event_id, self.market, self.selection, self.point


class Candidate(BaseModel):
    event_id: str
    league: str
    commence_time: datetime
    fixture: str
    market: str
    selection: str
    point: float | None = None
    betway_odds: float
    estimated_probability: float
    lower_probability: float
    implied_probability: float
    edge: float
    expected_value: float
    consensus_books: int
    model_source: str
    bankroll_fraction: float
    stake: float | None = None
    link: str | None = None
    notes: list[str] = Field(default_factory=list)

    def json_dict(self) -> dict[str, Any]:
        return self.model_dump(mode="json")
