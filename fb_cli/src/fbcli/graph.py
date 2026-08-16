from __future__ import annotations

import hashlib
import hmac
import json
import time
from collections.abc import Iterator
from typing import Any

import httpx

from fbcli import DEFAULT_API_VERSION
from fbcli.errors import GraphError

GRAPH_HOST = "https://graph.facebook.com"
VIDEO_HOST = "https://graph-video.facebook.com"
RETRY_STATUS = {429, 500, 502, 503, 504}


def appsecret_proof(token: str, app_secret: str) -> str:
    """HMAC-SHA256 of the token, keyed by the app secret (Meta 'secure requests')."""
    return hmac.new(app_secret.encode(), token.encode(), hashlib.sha256).hexdigest()


class GraphClient:
    """Thin, well-behaved Graph API client.

    Handles versioned URLs, appsecret_proof, retry with backoff on transient
    failures, cursor pagination and X-App-Usage rate-limit reporting.
    """

    def __init__(
        self,
        access_token: str,
        *,
        api_version: str = DEFAULT_API_VERSION,
        app_secret: str | None = None,
        base_url: str = GRAPH_HOST,
        timeout: float = 30.0,
        max_retries: int = 3,
        client: httpx.Client | None = None,
    ) -> None:
        self.access_token = access_token
        self.api_version = api_version if api_version.startswith("v") else f"v{api_version}"
        self.app_secret = app_secret
        self.base_url = base_url.rstrip("/")
        self.max_retries = max_retries
        self._owns_client = client is None
        self._client = client or httpx.Client(timeout=timeout, follow_redirects=True)
        self.last_usage: dict[str, Any] = {}

    # -- context manager -------------------------------------------------
    def __enter__(self) -> GraphClient:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    # -- helpers ---------------------------------------------------------
    def url(self, path: str) -> str:
        if path.startswith("http://") or path.startswith("https://"):
            return path
        path = path.lstrip("/")
        if path.startswith(f"{self.api_version}/"):
            return f"{self.base_url}/{path}"
        return f"{self.base_url}/{self.api_version}/{path}"

    def _auth_params(self, token: str | None = None) -> dict[str, str]:
        token = token or self.access_token
        params = {"access_token": token}
        if self.app_secret:
            params["appsecret_proof"] = appsecret_proof(token, self.app_secret)
        return params

    @staticmethod
    def _clean(params: dict[str, Any] | None) -> dict[str, Any]:
        out: dict[str, Any] = {}
        for key, value in (params or {}).items():
            if value is None:
                continue
            if isinstance(value, bool):
                out[key] = "true" if value else "false"
            elif isinstance(value, (list, tuple)):
                out[key] = ",".join(str(v) for v in value)
            elif isinstance(value, (dict,)):
                out[key] = json.dumps(value)
            else:
                out[key] = value
        return out

    def _record_usage(self, response: httpx.Response) -> None:
        for header in ("x-app-usage", "x-page-usage", "x-business-use-case-usage"):
            raw = response.headers.get(header)
            if not raw:
                continue
            try:
                self.last_usage[header] = json.loads(raw)
            except json.JSONDecodeError:
                self.last_usage[header] = raw

    # -- core request ----------------------------------------------------
    def request(
        self,
        method: str,
        path: str,
        *,
        params: dict[str, Any] | None = None,
        data: dict[str, Any] | None = None,
        files: dict[str, Any] | None = None,
        token: str | None = None,
    ) -> Any:
        url = self.url(path)
        query = self._clean(params)
        body = self._clean(data)
        auth = self._auth_params(token)
        if method.upper() == "GET":
            query.update(auth)
        else:
            body.update(auth)

        last_exc: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                response = self._client.request(
                    method.upper(),
                    url,
                    params=query or None,
                    data=body or None,
                    files=files or None,
                )
            except httpx.TransportError as exc:  # network hiccup
                last_exc = exc
                if attempt >= self.max_retries:
                    raise GraphError(
                        f"Network error talking to the Graph API: {exc}", status_code=0
                    ) from exc
                time.sleep(self._backoff(attempt))
                continue

            self._record_usage(response)
            if response.status_code in RETRY_STATUS and attempt < self.max_retries:
                time.sleep(self._backoff(attempt, response))
                continue
            return self._parse(response)

        raise GraphError(  # pragma: no cover - defensive
            f"Request failed after retries: {last_exc}", status_code=0
        )

    @staticmethod
    def _backoff(attempt: int, response: httpx.Response | None = None) -> float:
        if response is not None:
            retry_after = response.headers.get("retry-after")
            if retry_after and retry_after.isdigit():
                return min(float(retry_after), 30.0)
        return min(2.0**attempt, 8.0)

    @staticmethod
    def _parse(response: httpx.Response) -> Any:
        text = response.text or ""
        try:
            payload = response.json() if text else {}
        except ValueError:
            if response.is_success:
                return {"raw": text}
            raise GraphError(
                f"HTTP {response.status_code}: {text[:300]}", status_code=response.status_code
            ) from None
        if not response.is_success or (isinstance(payload, dict) and "error" in payload):
            body = payload if isinstance(payload, dict) else {}
            raise GraphError.from_response(response.status_code, body)
        return payload

    # -- verbs -----------------------------------------------------------
    def get(self, path: str, **params: Any) -> Any:
        token = params.pop("token", None)
        return self.request("GET", path, params=params, token=token)

    def post(self, path: str, *, files: dict[str, Any] | None = None,
             token: str | None = None, **data: Any) -> Any:
        return self.request("POST", path, data=data, files=files, token=token)

    def delete(self, path: str, *, token: str | None = None, **params: Any) -> Any:
        return self.request("DELETE", path, params=params, token=token)

    # -- pagination ------------------------------------------------------
    def paginate(
        self,
        path: str,
        *,
        limit: int | None = None,
        page_size: int = 25,
        token: str | None = None,
        **params: Any,
    ) -> Iterator[dict[str, Any]]:
        """Yield items across cursor pages, stopping at `limit` items."""
        params = dict(params)
        params["limit"] = min(page_size, limit) if limit else page_size
        payload = self.request("GET", path, params=params, token=token)
        seen = 0
        while True:
            for item in payload.get("data", []):
                yield item
                seen += 1
                if limit and seen >= limit:
                    return
            nxt = ((payload.get("paging") or {}).get("next")) if isinstance(payload, dict) else None
            if not nxt:
                return
            payload = self.request("GET", nxt, token=token)

    def collect(self, path: str, *, limit: int | None = None,
                **kwargs: Any) -> list[dict[str, Any]]:
        return list(self.paginate(path, limit=limit, **kwargs))

    # -- convenience endpoints -------------------------------------------
    def me(self, fields: str = "id,name") -> dict[str, Any]:
        return self.get("me", fields=fields)

    def debug_token(self, token: str, app_token: str) -> dict[str, Any]:
        payload = self.request(
            "GET", "debug_token", params={"input_token": token}, token=app_token
        )
        return payload.get("data", payload)

    def exchange_long_lived(self, app_id: str, app_secret: str, token: str) -> dict[str, Any]:
        return self.request(
            "GET",
            "oauth/access_token",
            params={
                "grant_type": "fb_exchange_token",
                "client_id": app_id,
                "client_secret": app_secret,
                "fb_exchange_token": token,
            },
            token=token,
        )
