from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

import httpx

from soccer_betway.domain import Quote

FEATURED = {"h2h", "totals"}


class OddsApiError(RuntimeError):
    pass


class OddsApiProvider:
    """The Odds API v4 adapter. Discovers active soccer competitions dynamically."""

    def __init__(self, api_key: str, settings: dict[str, Any]):
        self.api_key = api_key
        self.base_url = settings["base_url"].rstrip("/")
        self.bookmaker = settings.get("bookmaker", "betway")
        self.regions = settings.get("regions", "uk")
        self.markets = list(settings.get("markets", ["h2h"]))
        self.days_ahead = int(settings.get("days_ahead", 3))
        self.client = httpx.Client(timeout=float(settings.get("request_timeout_seconds", 30)))

    def _get(self, path: str, **params: Any) -> tuple[Any, httpx.Headers]:
        params["apiKey"] = self.api_key
        response = self.client.get(f"{self.base_url}{path}", params=params)
        if response.status_code >= 400:
            message = response.text[:400]
            raise OddsApiError(f"Odds API returned {response.status_code}: {message}")
        return response.json(), response.headers

    def soccer_sports(self) -> list[dict[str, Any]]:
        payload, _ = self._get("/sports", all="false")
        return [s for s in payload if str(s.get("group", "")).lower().startswith("soccer")]

    def fetch_all_soccer_quotes(self) -> list[Quote]:
        quotes: list[Quote] = []
        for sport in self.soccer_sports():
            events = self._featured_events(sport["key"])
            quotes.extend(self._parse_events(events, include_all_books=True))
            extra = [m for m in self.markets if m not in FEATURED]
            if extra:
                # Additional soccer markets are event-level endpoints.
                for event in events:
                    detailed, _ = self._get(
                        f"/sports/{sport['key']}/events/{event['id']}/odds",
                        regions=self.regions,
                        markets=",".join(extra),
                        oddsFormat="decimal",
                        includeLinks="true",
                    )
                    quotes.extend(self._parse_events([detailed], include_all_books=False))
        return self._dedupe(quotes)

    def _featured_events(self, sport_key: str) -> list[dict[str, Any]]:
        until = (datetime.now(UTC) + timedelta(days=self.days_ahead)).isoformat()
        payload, _ = self._get(
            f"/sports/{sport_key}/odds",
            regions=self.regions,
            markets=",".join(m for m in self.markets if m in FEATURED) or "h2h",
            oddsFormat="decimal",
            commenceTimeTo=until,
            includeLinks="true",
        )
        return payload

    def _parse_events(self, events: list[dict[str, Any]], include_all_books: bool) -> list[Quote]:
        parsed: list[Quote] = []
        for event in events:
            for book in event.get("bookmakers", []):
                if not include_all_books and book.get("key") != self.bookmaker:
                    continue
                for market in book.get("markets", []):
                    for outcome in market.get("outcomes", []):
                        parsed.append(Quote(
                            event_id=event["id"], league_key=event["sport_key"],
                            league=event.get("sport_title", event["sport_key"]),
                            commence_time=event["commence_time"], home_team=event["home_team"],
                            away_team=event["away_team"], bookmaker=book["key"],
                            market=market["key"], selection=outcome["name"],
                            price=outcome["price"], point=outcome.get("point"),
                            last_update=market.get("last_update") or book.get("last_update"),
                            link=outcome.get("link") or market.get("link") or book.get("link"),
                        ))
        return parsed

    @staticmethod
    def _dedupe(quotes: list[Quote]) -> list[Quote]:
        found: dict[tuple, Quote] = {}
        for quote in quotes:
            key = (*quote.selection_key, quote.bookmaker)
            found[key] = quote
        return list(found.values())
