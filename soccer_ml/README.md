# Soccer Betway ML

A conservative, automated soccer value-bet scanner inspired by the workflow of `NBA-Machine-Learning-Sports-Betting`, rebuilt for soccer and Betway.

It dynamically discovers **every active soccer competition exposed by the licensed odds provider**, gathers Betway prices plus market consensus, removes bookmaker margin, estimates outcome probability, and publishes only selections that pass every configured gate—by default:

- estimated probability **≥ 80%**;
- model edge over Betway implied probability **≥ 3 percentage points**;
- prices observed from **at least 3 books**;
- Betway quote less than **180 minutes old**;
- optional quarter-Kelly stake capped at **2% of bankroll**.

If nothing qualifies, the correct output is **No qualifying bets**.

> **Important:** An 80% model estimate is not an 80%-guaranteed winner. Soccer is uncertain, models drift, odds change, and any bet can lose. This software is informational, not financial advice. Use only where legal, verify prices manually, and never chase losses.

## What is included

- Dynamic all-soccer-league discovery—no league list to maintain.
- Licensed [The Odds API](https://the-odds-api.com/) integration using bookmaker key `betway`.
- Core markets: 1X2, totals, both teams to score, draw-no-bet, and double chance when the provider/Betway exposes them.
- No-vig probability ensemble across books.
- Optional trained probability calibrator with a conservative baseline fallback.
- Expected value, edge, fractional Kelly, quote freshness, and coverage filters.
- Markdown and JSON reports.
- Daily GitHub Actions automation.
- Demo mode, tests, type-safe data models, and one-command setup.

## Architecture

```text
The Odds API
    ├── /sports                         discover active soccer competitions
    ├── /sports/{league}/odds          featured 1X2/totals + consensus books
    └── /events/{event}/odds           Betway additional markets
                 │
                 ▼
       normalize + de-duplicate quotes
                 │
                 ▼
     remove vig within each book/market
                 │
                 ▼
 calibrated model OR conservative baseline
                 │
                 ▼
 probability + edge + freshness + coverage gates
                 │
                 ▼
      reports/latest.md + latest.json
```

## Five-minute setup

### 1. Create a licensed API key

Create a key at The Odds API. Confirm that your plan includes the leagues, additional markets, request volume, and Betway coverage you need. Betway is currently identified by bookmaker key `betway` in the provider’s UK bookmaker list. Availability can vary by event and jurisdiction.

### 2. Install

```bash
git clone <your-new-repository-url>
cd soccer-betway-ml
./scripts/bootstrap.sh
source .venv/bin/activate
```

### 3. Test without an API key

```bash
soccer-betway predict --demo
```

### 4. Run live

```bash
export ODDS_API_KEY="your_key"
export BANKROLL="1000"       # optional; omit to hide monetary stake
soccer-betway predict
```

Open `reports/latest.md` for the human-readable output.

## Minimal-work GitHub setup

Run one command:

```bash
./scripts/publish_to_github.sh
```

Approve the official GitHub browser login and paste your licensed odds API key when prompted. The script creates the public repository, pushes the code, stores encrypted secrets, enables GitHub Pages, starts the first scan, and prints every final link. See [`APPROVE_AND_PUBLISH.md`](APPROVE_AND_PUBLISH.md).

The workflow then runs every day at `05:15 UTC`, commits refreshed reports, and publishes the read-only dashboard.

## Configuration

Edit `config/settings.yml`:

```yaml
selection:
  minimum_probability: 0.80
  minimum_edge: 0.03
  minimum_consensus_books: 3
  fractional_kelly: 0.25
  maximum_bankroll_fraction: 0.02
```

For an exceptionally strict interpretation of “80% confidence,” set:

```yaml
use_lower_confidence_bound: true
```

This requires the approximate lower confidence bound—not merely the point estimate—to exceed 80%, and will usually produce very few picks.

## Markets and API usage

`h2h` and `totals` are featured markets. `btts`, `draw_no_bet`, and `double_chance` are additional event-level markets. Additional markets can consume substantially more API quota because the scanner queries them event by event.

To reduce API use:

```yaml
provider:
  markets: [h2h, totals]
  days_ahead: 2
```

The scanner covers all **active provider soccer leagues with available odds**, not literally every competition shown on every country-specific Betway website. A licensed feed cannot return a market it does not carry.

## Probability model

### Safe baseline

With no `models/calibrator.joblib`, the scanner uses a market-ensemble baseline:

1. convert each book’s decimal prices to implied probabilities;
2. normalize each complete market to remove overround;
3. average across books;
4. shrink extreme estimates toward a neutral prior;
5. require value versus the Betway price.

This is transparent and useful as a production fallback, but it is a **market model**, not a claim of independent predictive alpha.

### Train a calibrator

Prepare chronological, settled, out-of-sample prediction rows:

```csv
market_probability,dispersion,book_count,betway_implied,won
0.82,0.018,9,0.77,1
```

Then run:

```bash
python -m soccer_betway.model.train data/processed/training.csv \
  --output models/calibrator.joblib
```

At least 500 settled examples are required. Never train and evaluate on the same match rows. Use chronological validation and inspect calibration/Brier score, log loss, return on investment, maximum drawdown, and closing-line value before risking money.

## Output fields

- `estimated_probability`: model’s calibrated point estimate.
- `lower_probability`: conservative approximate lower bound.
- `implied_probability`: `1 / Betway decimal odds`.
- `edge`: estimate minus raw Betway implied probability.
- `expected_value`: `probability × odds − 1`.
- `bankroll_fraction`: configured fractional-Kelly stake, hard capped.
- `model_source`: trained calibrator or consensus baseline.

## Development

```bash
pip install -e '.[dev]'
pytest
ruff check src tests
```

## Deliberate safeguards

- No martingale, accumulator builder, loss chasing, or “guaranteed win” language.
- No recommendation without both probability and value.
- No stale or already-started fixture.
- No recommendation based on a single bookmaker.
- Hard stake cap and normal `no bet` outcome.
- API key only through environment/GitHub Secrets; never committed.

## Legal and operational notes

This repository does not scrape Betway. It uses a licensed third-party feed. You are responsible for API licensing, local law, Betway terms, age restrictions, taxes, and responsible gambling controls. Market names and availability differ by region. Always check the live Betway slip before placing anything.

## License

MIT
