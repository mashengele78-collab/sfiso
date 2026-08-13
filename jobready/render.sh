#!/usr/bin/env bash
# Render the JobReadyVideo composition to out/JobReadyVideo.mp4
# using the locally unpacked headless Chromium (no browser download needed).
set -euo pipefail
cd "$(dirname "$0")"

node scripts/prepare-chromium.mjs

export REMOTION_BROWSER_EXECUTABLE="${REMOTION_BROWSER_EXECUTABLE:-/tmp/chromium}"
export CHROMIUM_LIB_DIR="${CHROMIUM_LIB_DIR:-/tmp/al2023/lib}"

exec npx remotion render JobReadyVideo out/JobReadyVideo.mp4 \
  --chrome-mode=chrome-for-testing \
  "$@"
