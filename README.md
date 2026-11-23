# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-23 10:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,256** (5,021,945 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-23 10:01 UTC |
| Hours captured since the first snapshot | 1,243 of 1,249 (100%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-23 10:01 | ok | 2,000 | 1,360 | 30,000 |  |
| 2026-11-23 09:01 | ok | 2,000 | 1,321 | 30,000 |  |
| 2026-11-23 08:01 | ok | 2,000 | 1,313 | 30,000 |  |
| 2026-11-23 07:01 | ok | 2,000 | 1,389 | 30,000 |  |
| 2026-11-23 06:01 | ok | 2,000 | 1,530 | 30,000 |  |
| 2026-11-23 05:01 | ok | 2,000 | 1,668 | 30,000 |  |
| 2026-11-23 04:01 | ok | 2,000 | 1,780 | 30,000 |  |
| 2026-11-23 03:01 | ok | 2,000 | 1,915 | 30,000 |  |
| 2026-11-23 02:01 | ok | 2,000 | 1,999 | 30,000 |  |
| 2026-11-23 01:01 | ok | 2,000 | 1,984 | 30,000 |  |
| 2026-11-23 00:01 | ok | 2,000 | 2,132 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
