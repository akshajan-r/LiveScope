#!/usr/bin/env bash
# Clone the `data` branch into $1, or start it as an orphan branch on first run.
set -euo pipefail
dest="$1"
# DATA_REMOTE_URL overrides the remote (used for local testing).
url="${DATA_REMOTE_URL:-https://x-access-token:${GH_TOKEN}@github.com/${GITHUB_REPOSITORY}.git}"
if git ls-remote --exit-code --heads "$url" data >/dev/null 2>&1; then
  git clone --quiet --depth 1 --branch data --single-branch "$url" "$dest"
else
  git init --quiet -b data "$dest"
  git -C "$dest" remote add origin "$url"
  cat > "$dest/README.md" <<'MD'
# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
MD
fi
