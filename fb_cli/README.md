# fbcli — Facebook Graph API from the command line

A small, explicit command-line client for the [Facebook Graph API](https://developers.facebook.com/docs/graph-api).
It manages tokens, lists the Pages you administer, publishes and moderates posts,
reads insights, and can push this repository's soccer-ML report straight to a Page.

Targets Graph API **v26.0** (released 29 July 2026); override with `--api-version`.

```bash
fbcli auth login --token "$TOKEN" --app-id 123 --app-secret abc
fbcli pages list
fbcli pages use 1234567890
fbcli posts publish -m "Kick-off in an hour." 
fbcli slip publish --stakes
```

## Install

```bash
cd fb_cli
python -m venv .venv && source .venv/bin/activate
pip install -e '.[dev]'
```

Requires Python 3.11+.

## Getting a token

1. Create an app at [developers.facebook.com](https://developers.facebook.com/apps).
2. In the **Graph API Explorer**, select your app and Page, and request the scopes you need:
   - `pages_show_list` — list your Pages
   - `pages_read_engagement` — read posts and comments
   - `pages_manage_posts` — publish, edit and delete posts
   - `pages_manage_engagement` — reply to, hide and delete comments
   - `read_insights` — Page and post insights
3. Copy the user token and hand it to `fbcli auth login`.
4. Optional but recommended — trade it for a ~60-day token:

```bash
fbcli auth exchange     # needs --app-id / --app-secret stored
fbcli auth debug        # shows scopes, validity and expiry
```

`fbcli pages list` caches the per-Page tokens it receives, so later Page commands
use the right token automatically. Page tokens derived from a long-lived user
token do not expire.

## Credentials and safety

Credentials are stored at `~/.config/fbcli/credentials.json`, written with mode
`0600`. Environment variables always win over the stored file:

| Variable | Purpose |
|---|---|
| `FB_ACCESS_TOKEN` | Access token (use this in CI) |
| `FB_APP_ID` / `FB_APP_SECRET` | Enables `appsecret_proof` on every call |
| `FB_API_VERSION` | Pin a Graph API version |
| `FB_PROFILE` | Select a stored profile |
| `FBCLI_CONFIG_DIR` | Move the credentials file |

Tokens are never printed in full — `auth status` and `pages list` mask them.
When an app secret is available, every request is signed with `appsecret_proof`,
as Meta recommends for server-side calls.

Two more guard rails:

- Every write asks for confirmation unless you pass `--yes`.
- `--dry-run` prints the exact request instead of sending it.

```bash
fbcli --dry-run posts publish -m "test"   # shows the payload, sends nothing
```

## Commands

| Group | What it does |
|---|---|
| `auth` | `login`, `status`, `debug`, `exchange`, `whoami`, `profiles`, `logout` |
| `pages` | `list`, `use`, `show`, `search` |
| `posts` | `list`, `get`, `publish`, `photo`, `update`, `delete` |
| `comments` | `list`, `reply`, `hide`, `delete`, `like` |
| `insights` | `page`, `post`, `usage` |
| `slip` | `preview`, `publish` — post the soccer-ML report |
| `api` | `get`, `post`, `delete` — call any edge directly |

Every command accepts `--output table|json|csv`, so results pipe into other tools:

```bash
fbcli -o json posts list -n 50 | jq '.[] | select(.likes > 10) | .url'
fbcli -o csv insights page --metrics page_impressions > impressions.csv
```

### Posting

```bash
fbcli posts publish -m "Full time: 2-1."
fbcli posts publish --file notes.md --link https://example.com
fbcli posts publish -m "Team news" --schedule 2026-08-20T18:30:00+02:00
fbcli posts publish -m "Draft for review" --draft
fbcli posts photo lineup.png --caption "Starting XI"
```

Scheduling is validated locally: Facebook only accepts times between 10 minutes
and 75 days ahead, so a bad `--schedule` fails before a request is made.

### Reading and moderating

```bash
fbcli posts list -n 20
fbcli comments list 1234_5678 --order reverse_chronological
fbcli comments reply 1234_5678 -m "Thanks for watching!"
fbcli comments hide 1234_5678
```

### Insights

```bash
fbcli insights page --period week
fbcli insights post 1234_5678
fbcli insights usage          # current rate-limit headroom
```

### Raw API access

Anything not wrapped by a command is still reachable:

```bash
fbcli api get me/accounts -d fields=id,name
fbcli api get 1234/feed --paginate -n 500
fbcli api post 1234/feed -d message=hello --yes
```

## Publishing soccer-ML reports

`fbcli slip` reads `soccer_ml/reports/latest.json` — the artefact the daily
workflow writes — and renders it as a Page post. It finds the report by walking
up from the current directory, or takes `--report`.

```bash
fbcli slip preview                    # render the text, touch nothing
fbcli slip publish --stakes --yes     # post it
```

Behaviour worth knowing:

- With no qualifying selections it **skips posting** by default; pass
  `--post-if-empty` to publish the "no qualifying bets" message instead.
- Monetary stakes are omitted unless you ask for `--stakes`.
- Every post carries the project's standard disclaimer (estimates, not
  guarantees; 18+; bet only where legal).

Daily automation, using a Page token in `FB_ACCESS_TOKEN`:

```yaml
- name: Publish predictions to Facebook
  env:
    FB_ACCESS_TOKEN: ${{ secrets.FB_PAGE_TOKEN }}
  run: |
    pip install -e fb_cli
    fbcli slip publish --page "${{ vars.FB_PAGE_ID }}" --yes
```

## Errors

Graph errors are surfaced with their type, code, subcode and trace id, plus a
hint for the common cases (expired token, missing permission, rate limit):

```
Graph API error: Invalid OAuth access token. (type=OAuthException, code=190, http=401)
hint: The access token is invalid or expired. Run `fbcli auth login --token ...`.
```

Exit codes: `2` for a Graph API error, `3` for a configuration error,
`130` on interrupt.

Transient failures (429, 5xx, network drops) are retried up to three times with
exponential backoff, honouring `Retry-After`.

## Tests

```bash
cd fb_cli
pip install -e '.[dev]'
ruff check src tests
pytest --cov=fbcli --cov-report=term-missing
```

All HTTP is mocked with `httpx.MockTransport`; the suite never contacts Facebook.

## Scope

This tool uses the official Graph API only — it does not scrape, and it cannot
reach data Meta does not expose through the API (personal profiles, friend
lists, most Group content). Access to Page data requires App Review and Business
Verification on the Meta side. Use it in line with Meta's Platform Terms.
