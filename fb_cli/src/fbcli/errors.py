from __future__ import annotations

from typing import Any


class FbCliError(Exception):
    """Base class for every error this tool raises deliberately."""


class ConfigError(FbCliError):
    """Missing or malformed local configuration/credentials."""


class GraphError(FbCliError):
    """A structured error returned by the Graph API."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int,
        error_type: str | None = None,
        code: int | None = None,
        subcode: int | None = None,
        fbtrace_id: str | None = None,
        user_title: str | None = None,
        user_message: str | None = None,
        raw: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.error_type = error_type
        self.code = code
        self.subcode = subcode
        self.fbtrace_id = fbtrace_id
        self.user_title = user_title
        self.user_message = user_message
        self.raw = raw or {}

    @classmethod
    def from_response(cls, status_code: int, payload: dict[str, Any]) -> GraphError:
        err = payload.get("error") or {}
        return cls(
            err.get("message") or f"HTTP {status_code} from the Graph API",
            status_code=status_code,
            error_type=err.get("type"),
            code=err.get("code"),
            subcode=err.get("error_subcode"),
            fbtrace_id=err.get("fbtrace_id"),
            user_title=err.get("error_user_title"),
            user_message=err.get("error_user_msg"),
            raw=payload,
        )

    @property
    def is_rate_limit(self) -> bool:
        return self.code in {4, 17, 32, 613} or self.subcode == 2446079

    @property
    def is_auth(self) -> bool:
        return self.status_code in {401, 403} or self.code in {102, 190, 200, 10}

    def hint(self) -> str | None:
        """Actionable next step for the most common failures."""
        if self.code == 190:
            return (
                "The access token is invalid or expired. Run `fbcli auth login --token ...` "
                "with a fresh token, or `fbcli auth exchange` to mint a long-lived one."
            )
        if self.code in {200, 10} or self.status_code == 403:
            return (
                "The token lacks a required permission for this edge. Check "
                "`fbcli auth debug` and re-authorise with the scopes the endpoint needs."
            )
        if self.is_rate_limit:
            return "Rate limited. Back off and retry later; see the X-App-Usage header."
        if self.code == 100:
            return "Unsupported field, parameter or object id for this Graph API version."
        return None

    def __str__(self) -> str:  # pragma: no cover - formatting only
        bits = [self.message]
        detail = ", ".join(
            f"{k}={v}"
            for k, v in (
                ("type", self.error_type),
                ("code", self.code),
                ("subcode", self.subcode),
                ("http", self.status_code),
                ("trace", self.fbtrace_id),
            )
            if v is not None
        )
        if detail:
            bits.append(f"({detail})")
        return " ".join(bits)
