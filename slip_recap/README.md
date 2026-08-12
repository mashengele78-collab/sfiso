# Slip recap mailer

Emails **mashcop23@gmail.com** how the 15-leg Mode B Betway slip did.

| When (SAST) | What |
|---|---|
| First workflow run | Setup / activation mail (click FormSubmit confirm if asked) |
| 15–20 Aug 2026, 08:00 | Daily update for any legs that have finished |
| 20 Aug 2026, 06:00 | Extra pass after Wednesday’s Atlético game |

GitHub only runs `schedule:` crons from the **default branch**, and this token cannot push files under `.github/workflows/`.

**Enable the mailer (one step):** copy `slip_recap/github-action.yml` to `.github/workflows/slip-recap.yml` on `main`, then Actions → **Betway slip recap email** → Run workflow → `preview` (click the FormSubmit confirm link Gmail will get). After that the 15–20 Aug 08:00 SAST crons fire on their own.

Manual anytime: `RECAP_MODE=auto python3 slip_recap/send_recap.py`
