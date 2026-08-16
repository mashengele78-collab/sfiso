from pathlib import Path

from soccer_betway.config import load_config
from soccer_betway.providers.demo import demo_quotes
from soccer_betway.selector import scan


def test_scan_applies_all_gates(tmp_path, monkeypatch):
    monkeypatch.chdir(Path(__file__).parents[1])
    cfg = load_config()
    cfg["selection"]["minimum_edge"] = 0.0
    candidates = scan(demo_quotes(), cfg, bankroll=1000)
    assert all(c.estimated_probability >= 0.80 for c in candidates)
    assert all(c.bankroll_fraction <= 0.02 for c in candidates)


def test_strict_threshold_returns_none(monkeypatch):
    monkeypatch.chdir(Path(__file__).parents[1])
    cfg = load_config()
    cfg["selection"]["minimum_probability"] = 0.999
    assert scan(demo_quotes(), cfg) == []
