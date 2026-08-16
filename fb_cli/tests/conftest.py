from __future__ import annotations

import json
from typing import Any

import httpx
import pytest

from fbcli.config import ENV_CONFIG_HOME, Store
from fbcli.graph import GraphClient


class Recorder:
    """Collects requests and replays scripted responses."""

    def __init__(self) -> None:
        self.requests: list[httpx.Request] = []
        self.responses: list[tuple[int, Any]] = []

    def queue(self, payload: Any, status: int = 200) -> Recorder:
        self.responses.append((status, payload))
        return self

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.requests.append(request)
        status, payload = self.responses.pop(0) if self.responses else (200, {})
        return httpx.Response(
            status,
            json=payload,
            headers={"x-app-usage": json.dumps({"call_count": 3})},
        )

    @property
    def last(self) -> httpx.Request:
        return self.requests[-1]

    def params(self, index: int = -1) -> dict[str, str]:
        return dict(self.requests[index].url.params)

    def body(self, index: int = -1) -> dict[str, str]:
        raw = self.requests[index].content.decode()
        return dict(httpx.QueryParams(raw))


@pytest.fixture
def recorder() -> Recorder:
    return Recorder()


@pytest.fixture
def client(recorder: Recorder) -> GraphClient:
    transport = httpx.MockTransport(recorder.handler)
    http = httpx.Client(transport=transport)
    graph = GraphClient("tok", api_version="v26.0", client=http)
    yield graph
    http.close()


@pytest.fixture
def store(tmp_path, monkeypatch) -> Store:
    monkeypatch.setenv(ENV_CONFIG_HOME, str(tmp_path))
    for var in ("FB_ACCESS_TOKEN", "FB_APP_ID", "FB_APP_SECRET", "FB_API_VERSION", "FB_PROFILE"):
        monkeypatch.delenv(var, raising=False)
    return Store(tmp_path / "credentials.json")
