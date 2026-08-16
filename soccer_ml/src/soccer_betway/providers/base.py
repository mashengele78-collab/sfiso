from __future__ import annotations

from typing import Protocol

from soccer_betway.domain import Quote


class OddsProvider(Protocol):
    def fetch_all_soccer_quotes(self) -> list[Quote]: ...
