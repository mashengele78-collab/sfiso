from __future__ import annotations

import json

import httpx
import pytest
from typer.testing import CliRunner

from fbcli.cli import app
from fbcli.config import Profile, Store

runner = CliRunner()


@pytest.fixture
def fake_graph(monkeypatch, recorder):
    """Route every GraphClient through the mock transport."""
    import fbcli.context as context

    real = context.GraphClient

    def factory(token, **kwargs):
        kwargs.pop("timeout", None)
        kwargs["client"] = httpx.Client(transport=httpx.MockTransport(recorder.handler))
        return real(token, **kwargs)

    monkeypatch.setattr(context, "GraphClient", factory)
    return recorder


def test_version() -> None:
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0
    assert "fbcli" in result.stdout
    assert "v26.0" in result.stdout


def test_help_lists_command_groups() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    for group in ("auth", "pages", "posts", "comments", "insights", "slip", "api"):
        assert group in result.stdout


def test_rejects_bad_output_format(store: Store) -> None:
    result = runner.invoke(app, ["--output", "yaml", "auth", "status"])
    assert result.exit_code != 0


def test_auth_status_masks_token(store: Store) -> None:
    store.save(Profile(name="default", access_token="supersecrettoken12345", app_id="9"))
    result = runner.invoke(app, ["auth", "status"])
    assert result.exit_code == 0
    assert "supersecrettoken12345" not in result.stdout
    assert "v26.0" in result.stdout


def test_auth_status_without_credentials(store: Store) -> None:
    result = runner.invoke(app, ["auth", "status"])
    assert result.exit_code == 0
    assert "—" in result.stdout


def test_login_saves_and_verifies(store: Store, fake_graph) -> None:
    fake_graph.queue({"id": "42", "name": "Tester"})
    result = runner.invoke(app, ["auth", "login", "--token", "abc123"])
    assert result.exit_code == 0, result.stdout
    assert store.load("default").access_token == "abc123"
    assert "Tester" in result.stdout


def test_whoami_json_output(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="tok"))
    fake_graph.queue({"id": "1", "name": "Sfiso Page"})
    result = runner.invoke(app, ["--output", "json", "auth", "whoami"])
    assert result.exit_code == 0
    assert json.loads(result.stdout)["name"] == "Sfiso Page"


def test_pages_list_caches_tokens(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="user-token"))
    fake_graph.queue({"data": [{"id": "77", "name": "Sfiso Tips", "category": "Sports",
                                "access_token": "page-token", "tasks": ["CREATE_CONTENT"]}]})
    result = runner.invoke(app, ["pages", "list"])
    assert result.exit_code == 0, result.stdout
    saved = store.load("default")
    assert saved.pages["77"] == "page-token"
    assert saved.default_page_id == "77"
    assert "page-token" not in result.stdout


def test_pages_use_sets_default(store: Store) -> None:
    store.save(Profile(name="default", access_token="tok"))
    result = runner.invoke(app, ["pages", "use", "555"])
    assert result.exit_code == 0
    assert store.load("default").default_page_id == "555"


def test_posts_list_uses_page_token(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="user", default_page_id="77",
                       pages={"77": "page-token"}))
    fake_graph.queue({"data": [{"id": "77_1", "created_time": "2026-08-16T10:00:00+0000",
                                "message": "Hello world",
                                "likes": {"summary": {"total_count": 5}},
                                "comments": {"summary": {"total_count": 2}}}]})
    result = runner.invoke(app, ["posts", "list"])
    assert result.exit_code == 0, result.stdout
    assert "Hello world" in result.stdout
    assert fake_graph.params()["access_token"] == "page-token"


def test_publish_dry_run_sends_nothing(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77"))
    result = runner.invoke(app, ["--dry-run", "posts", "publish", "-m", "Match day", "--yes"])
    assert result.exit_code == 0
    assert "dry run" in result.stdout
    assert fake_graph.requests == []


def test_publish_posts_message(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77",
                       pages={"77": "page-token"}))
    fake_graph.queue({"id": "77_900"})
    result = runner.invoke(app, ["posts", "publish", "-m", "Match day", "--yes"])
    assert result.exit_code == 0, result.stdout
    body = fake_graph.body()
    assert body["message"] == "Match day"
    assert fake_graph.last.url.path == "/v26.0/77/feed"


def test_publish_rejects_bad_schedule(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77"))
    result = runner.invoke(
        app, ["posts", "publish", "-m", "x", "--schedule", "2020-01-01", "--yes"]
    )
    assert result.exit_code != 0
    assert fake_graph.requests == []


def test_publish_requires_content(store: Store) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77"))
    result = runner.invoke(app, ["posts", "publish", "--yes"])
    assert result.exit_code != 0


def test_missing_page_is_a_clear_error(store: Store) -> None:
    store.save(Profile(name="default", access_token="tok"))
    result = runner.invoke(app, ["posts", "list"], catch_exceptions=True)
    assert result.exit_code != 0


def test_comments_reply(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77"))
    fake_graph.queue({"id": "c1"})
    result = runner.invoke(app, ["comments", "reply", "77_1", "-m", "Thanks!", "--yes"])
    assert result.exit_code == 0, result.stdout
    assert fake_graph.body()["message"] == "Thanks!"


def test_insights_flattens_values(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77"))
    fake_graph.queue({"data": [{
        "name": "page_impressions", "period": "day",
        "values": [{"value": 120, "end_time": "2026-08-15T07:00:00+0000"}],
    }]})
    result = runner.invoke(app, ["insights", "page"])
    assert result.exit_code == 0, result.stdout
    assert "page_impressions" in result.stdout
    assert "120" in result.stdout


def test_api_get_passes_params(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="tok"))
    fake_graph.queue({"id": "1", "name": "n"})
    result = runner.invoke(app, ["api", "get", "me", "-d", "fields=id,name"])
    assert result.exit_code == 0, result.stdout
    assert fake_graph.params()["fields"] == "id,name"


def test_api_get_rejects_malformed_param(store: Store) -> None:
    store.save(Profile(name="default", access_token="tok"))
    result = runner.invoke(app, ["api", "get", "me", "-d", "oops"])
    assert result.exit_code != 0


def test_graph_error_is_reported_cleanly(store: Store, fake_graph) -> None:
    store.save(Profile(name="default", access_token="bad"))
    fake_graph.queue({"error": {"message": "Invalid OAuth access token.",
                                "type": "OAuthException", "code": 190}}, status=401)
    result = runner.invoke(app, ["auth", "whoami"])
    assert result.exit_code != 0


def test_slip_preview_reads_report(store: Store, tmp_path) -> None:
    report = tmp_path / "latest.json"
    report.write_text(json.dumps({
        "generated_at": "2026-08-16T14:00:00+02:00", "quote_count": 12,
        "candidates": [{"league": "Demo League", "fixture": "A vs B", "market": "h2h",
                        "selection": "A", "betway_odds": 1.25,
                        "estimated_probability": 0.86, "edge": 0.06,
                        "commence_time": "2026-08-17T12:00:00Z", "stake": 20.0}],
    }), encoding="utf-8")
    result = runner.invoke(app, ["slip", "preview", "--report", str(report)])
    assert result.exit_code == 0, result.stdout
    assert "A vs B" in result.stdout


def test_slip_publish_skips_when_empty(store: Store, fake_graph, tmp_path) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77"))
    report = tmp_path / "latest.json"
    report.write_text(json.dumps({"generated_at": "2026-08-16T14:00:00+02:00",
                                  "quote_count": 5, "candidates": []}), encoding="utf-8")
    result = runner.invoke(app, ["slip", "publish", "--report", str(report), "--yes"])
    assert result.exit_code == 0
    assert "nothing published" in result.stdout.lower()
    assert fake_graph.requests == []


def test_slip_publish_sends_post(store: Store, fake_graph, tmp_path) -> None:
    store.save(Profile(name="default", access_token="tok", default_page_id="77",
                       pages={"77": "page-token"}))
    report = tmp_path / "latest.json"
    report.write_text(json.dumps({
        "generated_at": "2026-08-16T14:00:00+02:00", "quote_count": 12,
        "candidates": [{"league": "L", "fixture": "A vs B", "market": "h2h", "selection": "A",
                        "betway_odds": 1.25, "estimated_probability": 0.86, "edge": 0.06,
                        "commence_time": "2026-08-17T12:00:00Z", "stake": 20.0}],
    }), encoding="utf-8")
    fake_graph.queue({"id": "77_1"})
    result = runner.invoke(app, ["slip", "publish", "--report", str(report), "--yes"])
    assert result.exit_code == 0, result.stdout
    assert "A vs B" in fake_graph.body()["message"]


def test_pages_list_marks_new_default(store: Store, fake_graph) -> None:
    """The default marker reflects the page chosen during this run."""
    store.save(Profile(name="default", access_token="user-token"))
    fake_graph.queue({"data": [{"id": "77", "name": "Sfiso Tips",
                                "access_token": "page-token", "tasks": []}]})
    result = runner.invoke(app, ["--output", "json", "pages", "list"])
    assert result.exit_code == 0, result.stdout
    assert json.loads(result.stdout)[0]["default"] == "*"


def test_login_preserves_graph_host(store: Store, fake_graph, monkeypatch) -> None:
    """FB_GRAPH_HOST survives a login (regression: it was reset to the default)."""
    monkeypatch.setenv("FB_GRAPH_HOST", "http://localhost:8899")
    fake_graph.queue({"id": "1", "name": "Tester"})
    result = runner.invoke(app, ["auth", "login", "--token", "abc", "--no-verify"])
    assert result.exit_code == 0, result.stdout
    assert store.load("default").base_url == "http://localhost:8899"
