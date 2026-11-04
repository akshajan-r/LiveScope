# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-04 18:01 UTC._

| | |
|---|---|
| Snapshots collected | **806** (3,167,793 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-04 18:01 UTC |
| Hours captured since the first snapshot | 795 of 801 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-04 18:01 | ok | 2,000 | 2,551 | 30,000 |  |
| 2026-11-04 17:02 | ok | 2,000 | 2,414 | 30,000 |  |
| 2026-11-04 16:01 | ok | 2,000 | 2,245 | 30,000 |  |
| 2026-11-04 15:01 | ok | 2,000 | 2,096 | 30,000 |  |
| 2026-11-04 14:01 | ok | 2,000 | 1,983 | 30,000 |  |
| 2026-11-04 13:01 | ok | 2,000 | 1,760 | 30,000 |  |
| 2026-11-04 12:01 | ok | 2,000 | 1,576 | 30,000 |  |
| 2026-11-04 11:01 | ok | 2,000 | 1,485 | 30,000 |  |
| 2026-11-04 10:01 | ok | 2,000 | 1,370 | 30,000 |  |
| 2026-11-04 09:01 | ok | 2,000 | 1,309 | 30,000 |  |
| 2026-11-04 08:01 | ok | 2,000 | 1,307 | 30,000 |  |
| 2026-11-04 07:01 | ok | 2,000 | 1,421 | 30,000 |  |
| 2026-11-04 06:01 | ok | 2,000 | 1,630 | 30,000 |  |
| 2026-11-04 05:01 | ok | 2,000 | 1,836 | 30,000 |  |
| 2026-11-04 04:01 | ok | 2,000 | 2,029 | 30,000 |  |
| 2026-11-04 03:01 | ok | 2,000 | 2,184 | 30,000 |  |
| 2026-11-04 02:01 | ok | 2,000 | 2,253 | 30,000 |  |
| 2026-11-04 01:01 | ok | 2,000 | 2,250 | 30,000 |  |
| 2026-11-04 00:01 | ok | 2,000 | 2,261 | 30,000 |  |
| 2026-11-03 23:01 | ok | 2,000 | 2,406 | 30,000 |  |
| 2026-11-03 22:04 | ok | 2,000 | 2,570 | 30,000 |  |
| 2026-11-03 21:01 | ok | 2,000 | 2,639 | 30,000 |  |
| 2026-11-03 20:03 | ok | 2,000 | 2,685 | 30,000 |  |
| 2026-11-03 19:02 | ok | 2,000 | 2,593 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
