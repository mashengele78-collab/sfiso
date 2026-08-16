"""Train a probability calibrator from historical prediction rows.

Input CSV columns: market_probability, dispersion, book_count, betway_implied, won.
Rows must be chronological and the feature probabilities must not use future data.
"""
from __future__ import annotations

import argparse
from pathlib import Path

import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, log_loss

FEATURES = ["market_probability", "dispersion", "book_count", "betway_implied"]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("csv", type=Path)
    parser.add_argument("--output", type=Path, default=Path("models/calibrator.joblib"))
    args = parser.parse_args()
    data = pd.read_csv(args.csv).dropna(subset=FEATURES + ["won"])
    if len(data) < 500:
        raise ValueError("Need at least 500 chronological, settled examples")

    split = int(len(data) * 0.8)
    train, test = data.iloc[:split], data.iloc[split:]
    model = LogisticRegression(max_iter=2000, class_weight="balanced")
    model.fit(train[FEATURES], train["won"].astype(int))
    predictions = model.predict_proba(test[FEATURES])[:, 1]
    actual = test["won"].astype(int)
    print(
        f"Chronological holdout: Brier={brier_score_loss(actual, predictions):.4f} "
        f"LogLoss={log_loss(actual, predictions):.4f}"
    )

    # Refit on all settled history only after reporting untouched holdout quality.
    model.fit(data[FEATURES], data["won"].astype(int))
    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, args.output)


if __name__ == "__main__":
    main()
