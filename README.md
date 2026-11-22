# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-22 23:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,245** (4,981,554 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-22 23:01 UTC |
| Hours captured since the first snapshot | 1,232 of 1,238 (100%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-22 23:01 | ok | 2,000 | 2,193 | 30,000 |  |
| 2026-11-22 22:01 | ok | 2,000 | 2,414 | 30,000 |  |
| 2026-11-22 21:01 | ok | 2,000 | 2,568 | 30,000 |  |
| 2026-11-22 20:01 | ok | 2,000 | 2,551 | 30,000 |  |
| 2026-11-22 19:01 | ok | 2,000 | 2,524 | 30,000 |  |
| 2026-11-22 18:01 | ok | 2,000 | 2,432 | 30,000 |  |
| 2026-11-22 17:01 | ok | 2,000 | 2,318 | 30,000 |  |
| 2026-11-22 16:01 | ok | 2,000 | 2,210 | 30,000 |  |
| 2026-11-22 15:01 | ok | 2,000 | 2,175 | 30,000 |  |
| 2026-11-22 14:01 | ok | 2,000 | 2,036 | 30,000 |  |
| 2026-11-22 13:01 | ok | 2,000 | 1,909 | 30,000 |  |
| 2026-11-22 12:01 | ok | 2,000 | 1,694 | 30,000 |  |
| 2026-11-22 11:01 | ok | 2,000 | 1,596 | 30,000 |  |
| 2026-11-22 10:01 | ok | 2,000 | 1,488 | 30,000 |  |
| 2026-11-22 09:01 | ok | 2,000 | 1,504 | 30,000 |  |
| 2026-11-22 08:01 | ok | 2,000 | 1,492 | 30,000 |  |
| 2026-11-22 07:04 | ok | 2,000 | 1,612 | 30,000 |  |
| 2026-11-22 07:00 | ok | 2,000 | 1,595 | 30,000 |  |
| 2026-11-22 06:01 | ok | 2,000 | 1,784 | 30,000 |  |
| 2026-11-22 05:01 | ok | 2,000 | 1,915 | 30,000 |  |
| 2026-11-22 04:01 | ok | 2,000 | 2,105 | 30,000 |  |
| 2026-11-22 03:01 | ok | 2,000 | 2,187 | 30,000 |  |
| 2026-11-22 02:01 | ok | 2,000 | 2,248 | 30,000 |  |
| 2026-11-22 01:01 | ok | 2,000 | 2,225 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
