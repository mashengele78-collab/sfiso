from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import typer

from fbcli.config import Profile, Store
from fbcli.graph import GraphClient


@dataclass
class AppState:
    """Global options resolved once in the root callback."""

    profile_name: str | None = None
    api_version: str | None = None
    output: str = "table"
    dry_run: bool = False
    timeout: float = 30.0
    _store: Store | None = field(default=None, repr=False)
    _profile: Profile | None = field(default=None, repr=False)

    @property
    def store(self) -> Store:
        if self._store is None:
            self._store = Store()
        return self._store

    @property
    def profile(self) -> Profile:
        if self._profile is None:
            self._profile = self.store.load(self.profile_name)
            if self.api_version:
                self._profile.api_version = self.api_version
        return self._profile

    def client(self, token: str | None = None) -> GraphClient:
        profile = self.profile
        return GraphClient(
            token or profile.require_token(),
            api_version=profile.api_version,
            app_secret=profile.app_secret,
            base_url=profile.base_url,
            timeout=self.timeout,
        )

    def page_client(self, page_id: str | None) -> tuple[GraphClient, str]:
        """Client authenticated with the best token for a page."""
        pid, token = self.profile.token_for_page(page_id)
        return self.client(token), pid

    def preview(self, action: str, payload: dict[str, Any]) -> bool:
        """In dry-run mode print what would happen and return True."""
        if not self.dry_run:
            return False
        from fbcli.output import emit_object, warn

        warn(f"dry run — {action} not sent")
        emit_object(payload, fmt=self.output if self.output != "table" else "table")
        return True


def get_state(ctx: typer.Context) -> AppState:
    state = ctx.ensure_object(AppState)
    return state
