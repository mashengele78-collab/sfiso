# Sfiso — Soccer Betting Automation

An automated soccer-analysis project containing a conservative Betway value scanner and a separate slip-recap service.

[![Soccer ML tests](https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-tests.yml/badge.svg)](https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-tests.yml)
[![Daily predictions](https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-daily.yml/badge.svg)](https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-daily.yml)

> **Probabilities are estimates, not guarantees.** Verify every live price before betting. Bet only where legal and only what you can afford to lose.

## Project components

### Soccer ML value scanner

Located in [`soccer_ml/`](soccer_ml/).

The scanner discovers active soccer competitions from a licensed odds provider, collects Betway and consensus prices, removes bookmaker margin, estimates fair probabilities, and publishes only selections that pass every configured quality gate.

Default requirements:

- Estimated probability of at least **80%**
- Edge over Betway’s implied probability of at least **3 percentage points**
- Prices from at least **3 bookmakers**
- Fresh Betway odds
- Fixture must not have started
- Fractional-Kelly stake capped at **2% of bankroll**

If no selection qualifies, the system reports:

> **No qualifying bets**

The system does not force bets.

### Supported markets

When available from Betway and the odds provider:

- Match winner / 1X2
- Over/under totals
- Both teams to score
- Draw no bet
- Double chance

### Slip recap

Located in [`slip_recap/`](slip_recap/).

This existing component settles configured Betway slips from match results and sends a profit/loss recap. It operates independently from the prediction engine.

### Facebook CLI

Located in [`fb_cli/`](fb_cli/).

`fbcli` is a command-line client for the Facebook Graph API (v26.0). It authenticates, manages Pages, publishes and schedules posts, moderates comments, and reads insights. It also knows how to publish the scanner's daily report:

```bash
cd fb_cli
pip install -e '.[dev]'

fbcli auth login --token "$FB_ACCESS_TOKEN"
fbcli pages list          # caches per-Page tokens, sets a default Page
fbcli slip publish --stakes --dry-run
```

Every mutating command supports `--dry-run` to preview the exact payload and prompts for confirmation unless `--yes` is passed. Slip posts always append the responsible-gambling disclaimer, and the CLI never invents selections — when nothing qualifies it either skips or posts an explicit "no qualifying bets" note.

See [`fb_cli/README.md`](fb_cli/README.md) for the full command reference.

## Live links

- [Prediction dashboard](https://mashengele78-collab.github.io/sfiso/soccer-ml/)
- [Daily prediction workflow](https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-daily.yml)
- [Automated tests](https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-tests.yml)
- [GitHub Actions secrets](https://github.com/mashengele78-collab/sfiso/settings/secrets/actions)
- [All workflow runs](https://github.com/mashengele78-collab/sfiso/actions)

## How it works

```text
Licensed odds API
    │
    ├── Discover active soccer competitions
    ├── Fetch Betway prices
    └── Fetch consensus prices from other bookmakers
    │
    ▼
Normalize and de-duplicate odds
    │
    ▼
Remove bookmaker margin
    │
    ▼
Probability calibrator or conservative consensus model
    │
    ▼
Probability, edge, coverage and freshness checks
    │
    ▼
Markdown report, JSON report and web dashboard
```

## Setup

The project requires a licensed [The Odds API](https://the-odds-api.com/) key.

Add the following under:

**Repository → Settings → Secrets and variables → Actions**

| Secret | Required | Purpose |
|---|---:|---|
| `ODDS_API_KEY` | Yes | Retrieves licensed soccer and bookmaker odds |
| `BANKROLL` | No | Enables monetary stake suggestions |

Never place API keys directly inside repository files.

## Run the predictor

Open the [Daily prediction workflow](https://github.com/mashengele78-collab/sfiso/actions/workflows/soccer-ml-daily.yml), click **Run workflow**, and confirm.

The workflow also runs automatically every day at:

```text
05:15 UTC
```

It updates:

```text
soccer_ml/reports/latest.md
soccer_ml/reports/latest.json
soccer-ml/latest.json
```

## Run locally

Requirements:

- Python 3.11+
- Git
- A licensed odds API key for live predictions

Install:

```bash
cd soccer_ml
python -m venv .venv
source .venv/bin/activate
pip install -e '.[dev]'
```

Run demo mode without an API key:

```bash
soccer-betway predict --demo
```

Run a live scan:

```bash
export ODDS_API_KEY="your-key"
export BANKROLL="1000"
soccer-betway predict
```

Reports are written to:

```text
soccer_ml/reports/
```

## Configuration

Primary configuration:

```text
soccer_ml/config/settings.yml
```

Default selection rules:

```yaml
selection:
  minimum_probability: 0.80
  minimum_edge: 0.03
  minimum_consensus_books: 3
  fractional_kelly: 0.25
  maximum_bankroll_fraction: 0.02
```

For a stricter probability rule:

```yaml
use_lower_confidence_bound: true
```

This requires the approximate lower probability bound—not only the point estimate—to reach 80%.

## Probability model

If this model file exists:

```text
soccer_ml/models/calibrator.joblib
```

the application uses the trained probability calibrator.

Without a trained model, it uses a conservative market-consensus baseline:

1. Convert decimal prices into implied probabilities.
2. Remove each bookmaker’s market margin.
3. Average fair probabilities across available bookmakers.
4. Shrink extreme estimates toward a neutral prior.
5. Compare the estimate with the Betway price.
6. Apply probability, edge, freshness and coverage gates.

The fallback is a market-consensus model. It is not proof of independent predictive advantage.

## Train a calibrator

Prepare chronological settled data with these columns:

```csv
market_probability,dispersion,book_count,betway_implied,won
0.82,0.018,9,0.77,1
```

Train:

```bash
cd soccer_ml
python -m soccer_betway.model.train data/processed/training.csv \
  --output models/calibrator.joblib
```

At least 500 settled examples are required.

Before using a trained model, evaluate:

- Brier score
- Log loss
- Calibration
- Closing-line value
- Return on investment
- Maximum drawdown
- Performance on unseen chronological data

## Tests

Install development dependencies:

```bash
cd soccer_ml
pip install -e '.[dev]'
```

Run quality checks:

```bash
ruff check src tests
pytest --cov=soccer_betway --cov-report=term-missing
```

Pull requests that change the predictor automatically trigger the Soccer ML test workflow.

## Repository structure

```text
.github/workflows/
├── soccer-ml-daily.yml
├── soccer-ml-tests.yml
└── fb-cli-tests.yml

soccer_ml/
├── config/
│   └── settings.yml
├── models/
├── reports/
├── src/soccer_betway/
└── tests/

slip_recap/
└── send_recap.py

fb_cli/
├── src/fbcli/
│   ├── cli.py
│   ├── config.py
│   ├── graph.py
│   └── commands/
└── tests/
```
