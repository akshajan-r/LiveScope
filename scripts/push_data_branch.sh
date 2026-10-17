#!/usr/bin/env bash
# Commit everything in the data checkout $1 and push it, retrying on races.
#
# With SQUASH=true the branch is replaced by a single new commit holding the
# current files. Used after old snapshots are compacted or deleted: otherwise
# git would keep every deleted file in history and the repository would keep
# growing. The push is guarded with --force-with-lease, so it fails (rather
# than overwrite) if anything else changed the branch in the meantime.
set -euo pipefail
dir="$1"
message="$2"
cd "$dir"
git config user.name "github-actions[bot]"
git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
git add -A
if [ "${SQUASH:-false}" = "true" ]; then
  base=$(git rev-parse --verify --quiet HEAD || true)
  git checkout --quiet --orphan squashed
  git add -A
  git commit --quiet -m "$message (history reset after compaction)"
  if [ -n "$base" ]; then
    git push --quiet --force-with-lease="data:$base" origin HEAD:data
  else
    git push --quiet origin HEAD:data
  fi
  exit 0
fi
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
