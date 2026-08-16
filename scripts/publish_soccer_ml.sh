#!/usr/bin/env bash
set -euo pipefail
REPO="mashengele78-collab/sfiso"
BRANCH="arena/soccer-ml-system"

if ! command -v gh >/dev/null 2>&1; then
  echo "Install GitHub CLI from https://cli.github.com/ and run this script again."
  exit 1
fi
if ! gh auth status >/dev/null 2>&1; then
  echo "Approve the official GitHub login in your browser."
  gh auth login --web --git-protocol https --scopes repo,workflow
else
  gh auth refresh --scopes workflow >/dev/null 2>&1 || true
fi

# A downloaded ZIP has no .git directory. Reconnect it safely to the existing
# repository and turn only the new files into a reviewable feature commit.
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  git init -b "$BRANCH"
  git config user.name "mashengele78-collab"
  git config user.email "mashengele78-collab@users.noreply.github.com"
  git remote add origin "https://github.com/$REPO.git"
  git add -A
  git commit -m "Temporary imported package snapshot" >/dev/null
  git fetch origin main
  git reset --soft origin/main
  git commit -m "feat: add automated Soccer Betway ML system"
else
  git checkout -B "$BRANCH"
fi

git push -u origin "$BRANCH" --force-with-lease

echo
read -rsp "Paste your The Odds API key (hidden): " ODDS_API_KEY
echo
if [[ -z "$ODDS_API_KEY" ]]; then
  echo "Get a key at https://the-odds-api.com/ and rerun this script."
  exit 1
fi
printf '%s' "$ODDS_API_KEY" | gh secret set ODDS_API_KEY --repo "$REPO"
unset ODDS_API_KEY
read -rp "Optional bankroll for stake sizing (Enter to omit): " BANKROLL
if [[ -n "$BANKROLL" ]]; then
  printf '%s' "$BANKROLL" | gh secret set BANKROLL --repo "$REPO"
fi

if gh pr view "$BRANCH" --repo "$REPO" >/dev/null 2>&1; then
  PR_URL="$(gh pr view "$BRANCH" --repo "$REPO" --json url --jq .url)"
else
  PR_URL="$(gh pr create --repo "$REPO" --base main --head "$BRANCH" \
    --title "Add automated Soccer Betway ML system" \
    --body "Adds the conservative 80% probability-gated soccer scanner under soccer_ml/, isolated workflows, tests, reports, and the /soccer-ml/ dashboard. Existing slip-recap files remain intact.")"
fi

echo
echo "Approval pull request: $PR_URL"
echo "After merging, run the first scan here:"
echo "https://github.com/$REPO/actions/workflows/soccer-ml-daily.yml"
echo "Live dashboard after the scan:"
echo "https://mashengele78-collab.github.io/sfiso/soccer-ml/"
echo "Secrets: https://github.com/$REPO/settings/secrets/actions"
gh pr view "$BRANCH" --repo "$REPO" --web
