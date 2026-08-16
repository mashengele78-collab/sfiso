from __future__ import annotations

import httpx
import pytest

from fbcli.errors import GraphError
from fbcli.graph import GraphClient, appsecret_proof


def test_url_is_versioned(client: GraphClient) -> None:
    assert client.url("me/accounts") == "https://graph.facebook.com/v26.0/me/accounts"
    assert client.url("/v26.0/me") == "https://graph.facebook.com/v26.0/me"
    assert client.url("https://graph.facebook.com/x") == "https://graph.facebook.com/x"


def test_get_sends_token_in_query(client: GraphClient, recorder) -> None:
    recorder.queue({"id": "1", "name": "Page"})
    assert client.get("me", fields="id,name") == {"id": "1", "name": "Page"}
    params = recorder.params()
    assert params["access_token"] == "tok"
    assert params["fields"] == "id,name"


def test_post_sends_token_in_body(client: GraphClient, recorder) -> None:
    recorder.queue({"id": "post_1"})
    client.post("123/feed", message="hello")
    assert recorder.last.method == "POST"
    body = recorder.body()
    assert body["message"] == "hello"
    assert body["access_token"] == "tok"


def test_appsecret_proof_added(recorder) -> None:
    http = httpx.Client(transport=httpx.MockTransport(recorder.handler))
    graph = GraphClient("tok", app_secret="s3cret", client=http)
    recorder.queue({"id": "1"})
    graph.get("me")
    assert recorder.params()["appsecret_proof"] == appsecret_proof("tok", "s3cret")
    http.close()


def test_params_are_normalised(client: GraphClient, recorder) -> None:
    recorder.queue({"data": []})
    client.get("me/feed", fields=["id", "message"], published=True, empty=None)
    params = recorder.params()
    assert params["fields"] == "id,message"
    assert params["published"] == "true"
    assert "empty" not in params


def test_error_raises_graph_error(client: GraphClient, recorder) -> None:
    recorder.queue(
        {"error": {"message": "Invalid OAuth token", "type": "OAuthException",
                   "code": 190, "fbtrace_id": "abc"}},
        status=401,
    )
    with pytest.raises(GraphError) as excinfo:
        client.get("me")
    err = excinfo.value
    assert err.code == 190
    assert err.is_auth
    assert "expired" in (err.hint() or "")


def test_rate_limit_flag() -> None:
    err = GraphError("slow down", status_code=400, code=4)
    assert err.is_rate_limit


def test_retry_then_success(client: GraphClient, recorder) -> None:
    recorder.queue({"error": {"message": "busy"}}, status=500).queue({"id": "ok"})
    assert client.get("me") == {"id": "ok"}
    assert len(recorder.requests) == 2


def test_paginate_follows_cursor(client: GraphClient, recorder) -> None:
    recorder.queue(
        {"data": [{"id": "1"}, {"id": "2"}],
         "paging": {"next": "https://graph.facebook.com/v26.0/me/feed?after=xyz"}}
    ).queue({"data": [{"id": "3"}]})
    assert [i["id"] for i in client.paginate("me/feed", page_size=2)] == ["1", "2", "3"]


def test_paginate_respects_limit(client: GraphClient, recorder) -> None:
    recorder.queue(
        {"data": [{"id": "1"}, {"id": "2"}, {"id": "3"}],
         "paging": {"next": "https://graph.facebook.com/v26.0/me/feed?after=xyz"}}
    )
    assert len(client.collect("me/feed", limit=2)) == 2
    assert len(recorder.requests) == 1


def test_usage_header_recorded(client: GraphClient, recorder) -> None:
    recorder.queue({"id": "1"})
    client.get("me")
    assert client.last_usage["x-app-usage"] == {"call_count": 3}
