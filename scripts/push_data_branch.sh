#!/usr/bin/env bash
# Commit everything in the data checkout $1 and push it, retrying on races.
set -euo pipefail
dir="$1"
message="$2"
cd "$dir"
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A
if git diff --cached --quiet; then
  echo "nothing to commit"
  exit 0
fi
git commit --quiet -m "$message"
for attempt in 1 2 3 4; do
  if git push --quiet origin HEAD:data; then
    exit 0
  fi
  sleep $((2 ** attempt))
  git pull --quiet --rebase origin data
done
echo "push failed after retries" >&2
exit 1
