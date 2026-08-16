#!/usr/bin/env bash
set -euo pipefail
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
pip install -e '.[dev]'
echo 'Ready. Run: source .venv/bin/activate && soccer-betway predict --demo'
