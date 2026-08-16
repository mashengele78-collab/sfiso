from __future__ import annotations

import json
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from fbcli import DEFAULT_API_VERSION
from fbcli.errors import ConfigError
from fbcli.graph import GRAPH_HOST

ENV_TOKEN = "FB_ACCESS_TOKEN"
ENV_APP_ID = "FB_APP_ID"
ENV_APP_SECRET = "FB_APP_SECRET"
ENV_API_VERSION = "FB_API_VERSION"
ENV_GRAPH_HOST = "FB_GRAPH_HOST"
ENV_PROFILE = "FB_PROFILE"
ENV_CONFIG_HOME = "FBCLI_CONFIG_DIR"


def config_dir() -> Path:
    override = os.getenv(ENV_CONFIG_HOME)
    if override:
        return Path(override).expanduser()
    base = os.getenv("XDG_CONFIG_HOME") or str(Path.home() / ".config")
    return Path(base).expanduser() / "fbcli"


def credentials_path() -> Path:
    return config_dir() / "credentials.json"


@dataclass
class Profile:
    """One set of credentials. Tokens are secrets: never print them in full."""

    name: str = "default"
    access_token: str | None = None
    app_id: str | None = None
    app_secret: str | None = None
    api_version: str = DEFAULT_API_VERSION
    base_url: str = GRAPH_HOST
    default_page_id: str | None = None
    pages: dict[str, str] = field(default_factory=dict)  # page id -> page access token

    def to_dict(self) -> dict[str, Any]:
        return {
            "access_token": self.access_token,
            "app_id": self.app_id,
            "app_secret": self.app_secret,
            "api_version": self.api_version,
            "base_url": self.base_url,
            "default_page_id": self.default_page_id,
            "pages": self.pages,
        }

    @classmethod
    def from_dict(cls, name: str, data: dict[str, Any]) -> Profile:
        return cls(
            name=name,
            access_token=data.get("access_token"),
            app_id=data.get("app_id"),
            app_secret=data.get("app_secret"),
            api_version=data.get("api_version") or DEFAULT_API_VERSION,
            base_url=data.get("base_url") or GRAPH_HOST,
            default_page_id=data.get("default_page_id"),
            pages=dict(data.get("pages") or {}),
        )

    def require_token(self) -> str:
        if not self.access_token:
            raise ConfigError(
                "No access token. Run `fbcli auth login --token <token>` or set "
                f"{ENV_TOKEN} in the environment."
            )
        return self.access_token

    def require_app(self) -> tuple[str, str]:
        if not (self.app_id and self.app_secret):
            raise ConfigError(
                "App credentials required. Run `fbcli auth login --app-id ... "
                f"--app-secret ...` or set {ENV_APP_ID}/{ENV_APP_SECRET}."
            )
        return self.app_id, self.app_secret

    def token_for_page(self, page_id: str | None) -> tuple[str, str]:
        """Resolve (page_id, token) preferring a stored page token."""
        pid = page_id or self.default_page_id
        if not pid:
            raise ConfigError(
                "No page selected. Pass --page <id> or run `fbcli pages use <id>` "
                "after `fbcli pages list`."
            )
        return pid, self.pages.get(pid) or self.require_token()


class Store:
    """JSON-backed credential store, written with 0600 permissions."""

    def __init__(self, path: Path | None = None) -> None:
        self.path = path or credentials_path()

    def _read(self) -> dict[str, Any]:
        if not self.path.exists():
            return {"profiles": {}}
        try:
            data = json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ConfigError(f"{self.path} is not valid JSON: {exc}") from exc
        data.setdefault("profiles", {})
        return data

    def _write(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        os.chmod(tmp, 0o600)
        tmp.replace(self.path)
        os.chmod(self.path, 0o600)

    def profile_names(self) -> list[str]:
        return sorted(self._read()["profiles"])

    def load(self, name: str | None = None) -> Profile:
        """Stored profile overlaid with environment variables (env wins)."""
        data = self._read()
        name = name or os.getenv(ENV_PROFILE) or data.get("current") or "default"
        profile = Profile.from_dict(name, data["profiles"].get(name, {}))
        profile.access_token = os.getenv(ENV_TOKEN) or profile.access_token
        profile.app_id = os.getenv(ENV_APP_ID) or profile.app_id
        profile.app_secret = os.getenv(ENV_APP_SECRET) or profile.app_secret
        profile.api_version = os.getenv(ENV_API_VERSION) or profile.api_version
        profile.base_url = os.getenv(ENV_GRAPH_HOST) or profile.base_url
        return profile

    def save(self, profile: Profile, *, make_current: bool = True) -> None:
        data = self._read()
        data["profiles"][profile.name] = profile.to_dict()
        if make_current:
            data["current"] = profile.name
        self._write(data)

    def delete(self, name: str) -> bool:
        data = self._read()
        removed = data["profiles"].pop(name, None) is not None
        if data.get("current") == name:
            data["current"] = next(iter(sorted(data["profiles"])), "default")
        self._write(data)
        return removed

    def current_name(self) -> str:
        return os.getenv(ENV_PROFILE) or self._read().get("current") or "default"


def mask(secret: str | None, keep: int = 4) -> str:
    if not secret:
        return "—"
    if len(secret) <= keep * 2:
        return "*" * len(secret)
    return f"{secret[:keep]}…{secret[-keep:]} ({len(secret)} chars)"
