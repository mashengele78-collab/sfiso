from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from soccer_betway.domain import Candidate


def write_reports(candidates: list[Candidate], report: dict, scanned_quotes: int) -> tuple[Path, Path]:
    tz = ZoneInfo(report.get("timezone", "UTC"))
    generated = datetime.now(tz)
    json_path, md_path = Path(report["output_json"]), Path(report["output_markdown"])
    json_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {"generated_at": generated.isoformat(), "quote_count": scanned_quotes,
               "candidate_count": len(candidates), "candidates": [c.json_dict() for c in candidates]}
    json_path.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = ["# Soccer value-bet report", "", f"Generated: **{generated:%Y-%m-%d %H:%M %Z}**",
             f"Quotes scanned: **{scanned_quotes}**", "",
             "> Probabilities are estimates, not guarantees. Odds move. Verify every price before betting.", ""]
    if not candidates:
        lines += ["## No qualifying bets", "", "No selection passed every probability, edge, liquidity/coverage, and freshness gate."]
    else:
        lines += ["## Qualifying selections", "",
                  "| League | Fixture | Market | Selection | Odds | Est. p | Edge | EV | Stake |", "|---|---|---|---|---:|---:|---:|---:|---:|"]
        for c in candidates:
            stake = f"{c.stake:.2f}" if c.stake is not None else "—"
            lines.append(f"| {c.league} | {c.fixture} | {c.market} | {c.selection} | {c.betway_odds:.2f} | {c.estimated_probability:.1%} | {c.edge:.1%} | {c.expected_value:.1%} | {stake} |")
    lines += ["", "## Rules", "", "- Only candidates at or above the configured estimated-probability threshold are shown.",
              "- A positive minimum edge and at least three consensus books are required.",
              "- Quarter-Kelly sizing is capped at 2% of bankroll; staking is optional.",
              "- `No bet` is a normal and desirable result.", "", "_For informational purposes only. Bet only where legal and only what you can afford to lose._"]
    md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return json_path, md_path
