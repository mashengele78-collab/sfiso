from __future__ import annotations

import json

import pytest
import typer

from fbcli.commands.slip import _load, render

REPORT = {
    "generated_at": "2026-08-16T14:00:40+02:00",
    "quote_count": 12,
    "candidates": [
        {
            "league": "Demo League",
            "fixture": "Cape Town City vs Example United",
            "market": "h2h",
            "selection": "Cape Town City",
            "betway_odds": 1.25,
            "estimated_probability": 0.86,
            "edge": 0.06,
            "commence_time": "2026-08-17T12:00:40Z",
            "stake": 20.0,
        }
    ],
}


def test_render_includes_selection_and_disclaimer() -> None:
    text = render(REPORT, max_selections=5, include_stakes=False)
    assert "Cape Town City vs Example United" in text
    assert "@ 1.25" in text
    assert "est. 86%" in text
    assert "edge +6.0%" in text
    assert "18+" in text
    assert "suggested stake" not in text


def test_render_can_include_stakes() -> None:
    text = render(REPORT, max_selections=5, include_stakes=True)
    assert "suggested stake 20.00" in text


def test_render_truncates_and_counts_remainder() -> None:
    many = {**REPORT, "candidates": [REPORT["candidates"][0]] * 4}
    text = render(many, max_selections=2, include_stakes=False)
    assert "…and 2 more" in text


def test_render_no_qualifying_bets() -> None:
    text = render({"generated_at": "2026-08-16T14:00:00+02:00", "quote_count": 9,
                   "candidates": []}, max_selections=5, include_stakes=False)
    assert "No qualifying bets today." in text
    assert "across 9 quotes" in text


def test_load_missing_file(tmp_path) -> None:
    with pytest.raises(typer.BadParameter, match="not found"):
        _load(tmp_path / "nope.json")


def test_load_bad_json(tmp_path) -> None:
    bad = tmp_path / "latest.json"
    bad.write_text("{oops", encoding="utf-8")
    with pytest.raises(typer.BadParameter, match="not valid JSON"):
        _load(bad)


def test_load_ok(tmp_path) -> None:
    good = tmp_path / "latest.json"
    good.write_text(json.dumps(REPORT), encoding="utf-8")
    assert _load(good)["quote_count"] == 12
