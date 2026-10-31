# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-31 15:01 UTC._

| | |
|---|---|
| Snapshots collected | **707** (2,783,669 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-31 15:01 UTC |
| Hours captured since the first snapshot | 696 of 702 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-31 15:01 | ok | 2,000 | 2,081 | 30,000 |  |
| 2026-10-31 14:01 | ok | 2,000 | 1,927 | 30,000 |  |
| 2026-10-31 13:01 | ok | 2,000 | 1,773 | 30,000 |  |
| 2026-10-31 12:01 | ok | 2,000 | 1,567 | 30,000 |  |
| 2026-10-31 11:01 | ok | 2,000 | 1,485 | 30,000 |  |
| 2026-10-31 10:01 | ok | 2,000 | 1,407 | 30,000 |  |
| 2026-10-31 09:01 | ok | 2,000 | 1,357 | 30,000 |  |
| 2026-10-31 08:01 | ok | 2,000 | 1,333 | 30,000 |  |
| 2026-10-31 07:01 | ok | 2,000 | 1,466 | 30,000 |  |
| 2026-10-31 06:01 | ok | 2,000 | 1,653 | 30,000 |  |
| 2026-10-31 05:01 | ok | 2,000 | 1,928 | 30,000 |  |
| 2026-10-31 04:01 | ok | 2,000 | 2,180 | 30,000 |  |
| 2026-10-31 03:01 | ok | 2,000 | 2,364 | 30,000 |  |
| 2026-10-31 02:01 | ok | 2,000 | 2,495 | 30,000 |  |
| 2026-10-31 01:01 | ok | 2,000 | 2,539 | 30,000 |  |
| 2026-10-31 00:01 | ok | 2,000 | 2,684 | 30,000 |  |
| 2026-10-30 23:01 | ok | 2,000 | 2,799 | 30,000 |  |
| 2026-10-30 22:01 | ok | 2,000 | 2,901 | 30,000 |  |
| 2026-10-30 21:01 | ok | 2,000 | 3,000 | 30,000 |  |
| 2026-10-30 20:01 | ok | 2,000 | 2,980 | 30,000 |  |
| 2026-10-30 19:01 | ok | 2,000 | 2,851 | 30,000 |  |
| 2026-10-30 18:02 | ok | 2,000 | 2,786 | 30,000 |  |
| 2026-10-30 17:01 | ok | 2,000 | 2,656 | 30,000 |  |
| 2026-10-30 16:01 | ok | 2,000 | 2,403 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
