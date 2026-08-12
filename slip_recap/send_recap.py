#!/usr/bin/env python3
"""Settle the Mode B Betway slip and email mashcop23@gmail.com.

Designed for GitHub Actions (stdlib only). Scores + goal times come from
the public ESPN soccer API. 10 Minute Draw is settled on goals with
elapsed minute < 10. If play-by-play is missing, that leg is UNCONFIRMED.
"""

from __future__ import annotations

import json
import os
import ssl
import sys
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timedelta, timezone
from html import escape
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
SLIP_PATH = ROOT / "slip.json"
OUT_DIR = ROOT / "out"
SAST = timezone(timedelta(hours=2))
UA = "sfiso-slip-recap/1.0 (+https://github.com/mashengele78-collab/sfiso)"
ESPN = "https://site.api.espn.com/apis/site/v2/sports/soccer"


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    return " ".join(s.lower().replace(".", " ").split())


def get_json(url: str) -> dict[str, Any]:
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=30, context=ctx) as resp:
        return json.loads(resp.read().decode("utf-8"))


def post_formsubmit(to: str, subject: str, text: str, html: str) -> tuple[int, str]:
    payload = json.dumps(
        {
            "name": "Betway slip bot",
            "_subject": subject,
            "_template": "box",
            "_captcha": "false",
            "_honey": "",
            "message": text,
            "html": html,
        }
    ).encode("utf-8")
    url = f"https://formsubmit.co/ajax/{urllib.parse.quote(to)}"
    req = urllib.request.Request(
        url,
        data=payload,
        method="POST",
        headers={
            "User-Agent": UA,
            "Accept": "application/json",
            "Content-Type": "application/json",
        },
    )
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=45, context=ctx) as resp:
            return resp.status, resp.read().decode("utf-8", "replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", "replace")


def parse_clock_minutes(play: dict[str, Any]) -> float | None:
    clock = play.get("clock") or {}
    disp = str(clock.get("displayValue") or play.get("text") or "")
    # ESPN soccer clocks are usually "9'" or "45'+2'" or "9:32".
    digits = ""
    for ch in disp:
        if ch.isdigit():
            digits += ch
        elif digits:
            break
    if not digits:
        period = play.get("period") or {}
        if isinstance(period, dict) and period.get("number") == 1:
            # fall through
            pass
        return None
    minute = int(digits)
    # A display of 10' is the 10:00 mark — 10 Minute Draw is level at 9:59.
    return float(minute)


def first_ten_score(details: list[dict[str, Any]]) -> tuple[int, int] | None:
    """Score at 9:59. A goal shown as 10' is after the 10 Minute Draw line.

    Prefers each play's homeScore/awayScore snapshot. Returns None if there is
    no clocked scoring data at all (caller must mark UNCONFIRMED).
    """
    if not details:
        return None
    last = (0, 0)
    saw_clock = False
    for play in details:
        is_goal = bool(play.get("scoringPlay"))
        kind = ((play.get("type") or {}).get("text") or "").lower()
        if not is_goal and "goal" not in kind and "homeScore" not in play:
            continue
        minute = parse_clock_minutes(play)
        if minute is None:
            continue
        saw_clock = True
        if minute >= 10:
            continue
        if play.get("homeScore") is not None and play.get("awayScore") is not None:
            try:
                last = (int(play["homeScore"]), int(play["awayScore"]))
                continue
            except (TypeError, ValueError):
                pass
        home_away = (play.get("homeAway") or "").lower()
        if home_away == "home":
            last = (last[0] + 1, last[1])
        elif home_away == "away":
            last = (last[0], last[1] + 1)
        else:
            return None
    if not saw_clock:
        return None
    return last


def team_names(comp: dict[str, Any]) -> tuple[str, str]:
    home = away = ""
    for c in comp.get("competitors") or []:
        name = ((c.get("team") or {}).get("displayName") or c.get("displayName") or "")
        if c.get("homeAway") == "home":
            home = name
        else:
            away = name
    return home, away


def ft_score(comp: dict[str, Any]) -> tuple[int, int] | None:
    home = away = None
    for c in comp.get("competitors") or []:
        try:
            sc = int(c.get("score"))
        except (TypeError, ValueError):
            return None
        if c.get("homeAway") == "home":
            home = sc
        else:
            away = sc
    if home is None or away is None:
        return None
    return home, away


def match_event(leg: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any] | None:
    want = {norm(a) for a in leg.get("aliases") or []}
    want.add(norm(leg["home"]))
    want.add(norm(leg["away"]))
    best = None
    best_hits = 0
    for ev in events:
        comps = ev.get("competitions") or []
        if not comps:
            continue
        home, away = team_names(comps[0])
        names = {norm(home), norm(away)}
        hits = 0
        for n in names:
            if n in want or any(n in w or w in n for w in want if len(w) > 3):
                hits += 1
        if hits > best_hits:
            best_hits = hits
            best = ev
    return best if best_hits >= 2 else None


def load_scoreboard(league: str, day: str) -> list[dict[str, Any]]:
    url = f"{ESPN}/{league}/scoreboard?dates={day}&limit=50"
    data = get_json(url)
    return list(data.get("events") or [])


def load_summary(league: str, event_id: str) -> dict[str, Any]:
    url = f"{ESPN}/{league}/summary?event={event_id}"
    return get_json(url)


def settle_leg(leg: dict[str, Any], now: datetime) -> dict[str, Any]:
    kick = datetime.fromisoformat(leg["kickoff_sast"])
    if kick.tzinfo is None:
        kick = kick.replace(tzinfo=SAST)
    out = {
        **leg,
        "status": "pending",
        "result": None,
        "ft": None,
        "ten": None,
        "note": "",
        "returns": 0.0,
        "profit": 0.0,
    }
    if now < kick:
        out["note"] = "Not kicked off yet."
        return out

    day = kick.astimezone(timezone.utc).strftime("%Y%m%d")
    try:
        events = load_scoreboard(leg["espn_league"], day)
    except Exception as e:
        out["status"] = "unconfirmed"
        out["note"] = f"Scoreboard fetch failed: {e}"
        return out

    ev = match_event(leg, events)
    if ev is None:
        # midnight-UTC spill: try SAST calendar day too
        day2 = kick.strftime("%Y%m%d")
        if day2 != day:
            try:
                ev = match_event(leg, load_scoreboard(leg["espn_league"], day2))
            except Exception:
                ev = None
    if ev is None:
        out["status"] = "unconfirmed"
        out["note"] = "Match not found on ESPN scoreboard."
        return out

    comp = (ev.get("competitions") or [{}])[0]
    state = ((comp.get("status") or {}).get("type") or {})
    completed = bool(state.get("completed"))
    desc = state.get("description") or state.get("name") or ""
    score = ft_score(comp)
    if score:
        out["ft"] = f"{score[0]}-{score[1]}"

    if not completed:
        out["status"] = "live" if "in" in desc.lower() or state.get("state") == "in" else "pending"
        out["note"] = desc or "In progress / not final."
        return out

    if score is None:
        out["status"] = "unconfirmed"
        out["note"] = "Final, but no score on the scoreboard."
        return out

    ten = None
    try:
        summary = load_summary(leg["espn_league"], str(ev.get("id")))
        details = ((summary.get("scoringPlays") or summary.get("plays")) or [])
        if not details:
            # some payloads nest scoring plays under header / atScoringPlays
            details = summary.get("atScoringPlays") or []
        ten = first_ten_score(details if isinstance(details, list) else [])
        # ESPN summary.scoringPlays is the reliable list when present.
        if ten is None and isinstance(summary.get("scoringPlays"), list):
            ten = first_ten_score(summary["scoringPlays"])
    except Exception as e:
        if leg["market"] == "10_minute_draw":
            out["status"] = "unconfirmed"
            out["note"] = f"Final {out['ft']}, but first-10 PBP missing ({e}). Check the app."
            return out

    if ten:
        out["ten"] = f"{ten[0]}-{ten[1]}"

    won = None
    if leg["market"] == "over_1_5":
        won = (score[0] + score[1]) >= 2
        out["note"] = f"FT {out['ft']} → {'Over' if won else 'Under'} 1.5"
    elif leg["market"] == "10_minute_draw":
        if ten is None:
            out["status"] = "unconfirmed"
            out["note"] = f"Final {out['ft']}, first-10 score not published. Do not trust this as settled."
            return out
        won = ten[0] == ten[1]
        out["note"] = f"Score at 10:00 {out['ten']} → {'level' if won else 'not level'}"
    else:
        out["status"] = "unconfirmed"
        out["note"] = f"Unknown market {leg['market']}"
        return out

    out["result"] = "WON" if won else "LOST"
    out["status"] = "settled"
    if won:
        out["returns"] = round(leg["stake"] * float(leg["odds"]), 2)
        out["profit"] = round(out["returns"] - leg["stake"], 2)
    else:
        out["returns"] = 0.0
        out["profit"] = -float(leg["stake"])
    return out


def summarise(legs: list[dict[str, Any]]) -> dict[str, Any]:
    settled = [x for x in legs if x["status"] == "settled"]
    pending = [x for x in legs if x["status"] in {"pending", "live"}]
    unconf = [x for x in legs if x["status"] == "unconfirmed"]
    won = [x for x in settled if x["result"] == "WON"]
    lost = [x for x in settled if x["result"] == "LOST"]
    stake_settled = sum(x["stake"] for x in settled)
    returns = sum(x["returns"] for x in settled)
    profit = sum(x["profit"] for x in settled)
    stake_open = sum(x["stake"] for x in pending + unconf)
    return {
        "settled": len(settled),
        "won": len(won),
        "lost": len(lost),
        "pending": len(pending),
        "unconfirmed": len(unconf),
        "stake_settled": stake_settled,
        "stake_open": stake_open,
        "returns": returns,
        "profit": profit,
        "hit_rate": (len(won) / len(settled)) if settled else None,
        "final": len(pending) == 0 and len(unconf) == 0,
    }


def money(n: float) -> str:
    sign = "-" if n < 0 else ""
    return f"{sign}R{abs(n):,.2f}"


def render_html(title: str, when: datetime, legs: list[dict[str, Any]], s: dict[str, Any]) -> str:
    rows = []
    for x in legs:
        colour = {"WON": "#15803d", "LOST": "#b91c1c"}.get(x["result"] or "", "#6b7280")
        badge = x["result"] or x["status"].upper()
        rows.append(
            f"""<tr>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;">{x['id']}</td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;">
                <div style="font-weight:600;">{escape(x['home'])} vs {escape(x['away'])}</div>
                <div style="color:#6b7280;font-size:12px;">{escape(x['league'])} · {escape(x['kickoff_sast'][5:16].replace('T',' ')) } SAST</div>
              </td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;">{escape(x['market_label'])}</td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;">{escape(x.get('ft') or '—')}</td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;">{escape(x.get('ten') or '—')}</td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;color:{colour};font-weight:700;">{escape(badge)}</td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;text-align:right;">{money(x['stake'])}</td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;text-align:right;">{x['odds']:.2f}</td>
              <td style="padding:10px 8px;border-bottom:1px solid #e5e7eb;text-align:right;color:{colour};">{money(x['profit']) if x['status']=='settled' else '—'}</td>
            </tr>
            <tr><td></td><td colspan="8" style="padding:0 8px 10px;color:#6b7280;font-size:12px;">{escape(x.get('note') or '')}</td></tr>"""
        )
    hit = f"{s['won']}/{s['settled']} ({s['hit_rate']*100:.0f}%)" if s["hit_rate"] is not None else "—"
    pnl_colour = "#15803d" if s["profit"] >= 0 else "#b91c1c"
    headline = "Final slip recap" if s["final"] else "Slip update — still legs in play"
    return f"""<!doctype html>
<html><body style="margin:0;background:#0b1220;font-family:Georgia,serif;color:#111827;">
  <div style="max-width:760px;margin:0 auto;padding:24px;">
    <div style="background:#111827;color:#f9fafb;padding:20px 24px;border-radius:12px 12px 0 0;">
      <div style="font-size:13px;letter-spacing:.08em;text-transform:uppercase;color:#c4a265;">Betway Mode B · 15 singles</div>
      <h1 style="margin:8px 0 0;font-size:26px;">{escape(headline)}</h1>
      <p style="margin:8px 0 0;color:#9ca3af;">{escape(title)}<br>Settled {escape(when.strftime('%A %d %B %Y, %H:%M'))} SAST</p>
    </div>
    <div style="background:#fff;padding:20px 24px;">
      <table style="width:100%;border-collapse:collapse;margin-bottom:16px;">
        <tr>
          <td style="padding:8px;background:#f3f4f6;border-radius:8px;">
            <div style="font-size:11px;color:#6b7280;">SETTLED P/L</div>
            <div style="font-size:22px;font-weight:700;color:{pnl_colour};">{money(s['profit'])}</div>
          </td>
          <td style="width:12px;"></td>
          <td style="padding:8px;background:#f3f4f6;border-radius:8px;">
            <div style="font-size:11px;color:#6b7280;">RETURNS</div>
            <div style="font-size:22px;font-weight:700;">{money(s['returns'])}</div>
          </td>
          <td style="width:12px;"></td>
          <td style="padding:8px;background:#f3f4f6;border-radius:8px;">
            <div style="font-size:11px;color:#6b7280;">HIT RATE</div>
            <div style="font-size:22px;font-weight:700;">{escape(hit)}</div>
          </td>
        </tr>
      </table>
      <p style="font-size:14px;color:#374151;">
        Staked on settled legs {money(s['stake_settled'])} · still open {money(s['stake_open'])} ·
        bankroll R500 · {s['won']} won · {s['lost']} lost · {s['pending']} pending · {s['unconfirmed']} unconfirmed.
      </p>
      <table style="width:100%;border-collapse:collapse;font-size:13px;">
        <thead>
          <tr style="text-align:left;color:#6b7280;">
            <th style="padding:8px;">#</th><th style="padding:8px;">Match</th><th style="padding:8px;">Market</th>
            <th style="padding:8px;">FT</th><th style="padding:8px;">10'</th><th style="padding:8px;">Result</th>
            <th style="padding:8px;text-align:right;">Stake</th><th style="padding:8px;text-align:right;">Odds</th>
            <th style="padding:8px;text-align:right;">P/L</th>
          </tr>
        </thead>
        <tbody>{''.join(rows)}</tbody>
      </table>
      <p style="font-size:12px;color:#6b7280;margin-top:20px;">
        10 Minute Draw is settled on the score at 9:59 (goals with minute &lt; 10).
        If ESPN did not publish goal times, that leg is UNCONFIRMED — check Betway history, do not assume a result.
        Odds are the planning band recorded when the slip was compiled, not a live Betway scrape.
        This is a results mail, not a new betting recommendation.
      </p>
    </div>
  </div>
</body></html>"""


def render_text(title: str, when: datetime, legs: list[dict[str, Any]], s: dict[str, Any]) -> str:
    hit = f"{s['won']}/{s['settled']} ({s['hit_rate']*100:.0f}%)" if s["hit_rate"] is not None else "n/a"
    lines = [
        "BETWAY SLIP RECAP" if s["final"] else "BETWAY SLIP UPDATE",
        title,
        when.strftime("%A %d %B %Y, %H:%M SAST"),
        "",
        f"Settled P/L: {money(s['profit'])}",
        f"Returns:     {money(s['returns'])}",
        f"Hit rate:    {hit}",
        f"Open stake:  {money(s['stake_open'])}",
        "",
    ]
    for x in legs:
        badge = x["result"] or x["status"].upper()
        lines.append(
            f"#{x['id']:02d}  {x['home']} vs {x['away']}  [{x['market_label']}]  "
            f"FT {x.get('ft') or '—'}  10' {x.get('ten') or '—'}  {badge}  "
            f"{money(x['stake'])} @ {x['odds']:.2f}  "
            f"{money(x['profit']) if x['status']=='settled' else ''}"
        )
        if x.get("note"):
            lines.append(f"     {x['note']}")
    lines += [
        "",
        "10 Minute Draw = level at 9:59. UNCONFIRMED means goal times were not published — check the Betway app.",
        "Odds are the planning band from compile time, not live Betway.",
    ]
    return "\n".join(lines)


def main() -> int:
    mode = (os.environ.get("RECAP_MODE") or (sys.argv[1] if len(sys.argv) > 1 else "auto")).lower()
    now = datetime.now(SAST)
    slip = json.loads(SLIP_PATH.read_text(encoding="utf-8"))
    settled_legs = [settle_leg(leg, now) for leg in slip["legs"]]
    s = summarise(settled_legs)

    if mode == "preview":
        subject = "Activate + preview: your Betway slip recap is armed"
        # Don't pretend fixtures have results.
        for x in settled_legs:
            if x["status"] != "pending":
                continue
        headline_title = slip["title"] + " — setup mail"
    elif s["final"]:
        subject = f"Final slip recap: {money(s['profit'])} · {s['won']}/{s['settled']} hit"
        headline_title = slip["title"]
    else:
        subject = f"Slip update: {s['won']}W-{s['lost']}L · {s['pending']+s['unconfirmed']} still open · {money(s['profit'])}"
        headline_title = slip["title"]

    html = render_html(headline_title, now, settled_legs, s)
    text = render_text(headline_title, now, settled_legs, s)
    if mode == "preview":
        text = (
            "This is the setup mail.\n\n"
            "1) If FormSubmit asks you to confirm this inbox, click the link — "
            "otherwise the Thursday recap cannot be delivered.\n"
            "2) You will get the real result mail the morning after the last kick-off "
            "(Thu 20 Aug 2026, ~08:00 SAST), plus a daily update at 08:00 SAST on 15–20 Aug "
            "once any legs have finished.\n\n"
            + text
        )

    OUT_DIR.mkdir(exist_ok=True)
    (OUT_DIR / "recap.html").write_text(html, encoding="utf-8")
    (OUT_DIR / "recap.txt").write_text(text, encoding="utf-8")
    (OUT_DIR / "recap.json").write_text(json.dumps({"summary": s, "legs": settled_legs}, indent=2), encoding="utf-8")

    to = os.environ.get("RECAP_TO") or slip["recipient"]
    print(f"Sending to {to} · subject={subject!r} · mode={mode}")
    status, body = post_formsubmit(to, subject, text, html)
    print(f"FormSubmit HTTP {status}: {body[:500]}")
    (OUT_DIR / "send_response.txt").write_text(f"{status}\n{body}", encoding="utf-8")
    if status >= 400:
        print("Email send failed.", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
