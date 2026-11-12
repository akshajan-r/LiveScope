# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-12 01:01 UTC._

| | |
|---|---|
| Snapshots collected | **982** (3,903,693 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-12 01:01 UTC |
| Hours captured since the first snapshot | 970 of 976 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-12 01:01 | ok | 2,000 | 2,210 | 30,000 |  |
| 2026-11-12 00:01 | ok | 2,000 | 2,295 | 30,000 |  |
| 2026-11-11 23:01 | ok | 2,000 | 2,355 | 30,000 |  |
| 2026-11-11 22:01 | ok | 2,000 | 2,509 | 30,000 |  |
| 2026-11-11 21:01 | ok | 2,000 | 2,674 | 30,000 |  |
| 2026-11-11 20:01 | ok | 2,000 | 2,695 | 30,000 |  |
| 2026-11-11 19:01 | ok | 2,000 | 2,617 | 30,000 |  |
| 2026-11-11 18:01 | ok | 2,000 | 2,519 | 30,000 |  |
| 2026-11-11 17:01 | ok | 2,000 | 2,400 | 30,000 |  |
| 2026-11-11 16:01 | ok | 2,000 | 2,262 | 30,000 |  |
| 2026-11-11 15:01 | ok | 2,000 | 2,132 | 30,000 |  |
| 2026-11-11 14:01 | ok | 2,000 | 1,913 | 30,000 |  |
| 2026-11-11 13:01 | ok | 2,000 | 1,743 | 30,000 |  |
| 2026-11-11 12:01 | ok | 2,000 | 1,598 | 30,000 |  |
| 2026-11-11 11:01 | ok | 2,000 | 1,551 | 30,000 |  |
| 2026-11-11 10:01 | ok | 2,000 | 1,480 | 30,000 |  |
| 2026-11-11 09:01 | ok | 2,000 | 1,461 | 30,000 |  |
| 2026-11-11 08:01 | ok | 2,000 | 1,387 | 30,000 |  |
| 2026-11-11 07:01 | ok | 2,000 | 1,446 | 30,000 |  |
| 2026-11-11 06:01 | ok | 2,000 | 1,648 | 30,000 |  |
| 2026-11-11 05:01 | ok | 2,000 | 1,878 | 30,000 |  |
| 2026-11-11 04:01 | ok | 2,000 | 2,050 | 30,000 |  |
| 2026-11-11 03:01 | ok | 2,000 | 2,189 | 30,000 |  |
| 2026-11-11 02:01 | ok | 2,000 | 2,280 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
