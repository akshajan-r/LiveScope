# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-24 05:01 UTC._

| | |
|---|---|
| Snapshots collected | **527** (2,064,157 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-24 05:01 UTC |
| Hours captured since the first snapshot | 518 of 524 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-24 05:01 | ok | 2,000 | 1,941 | 30,000 |  |
| 2026-10-24 04:01 | ok | 2,000 | 2,147 | 30,000 |  |
| 2026-10-24 03:01 | ok | 2,000 | 2,265 | 30,000 |  |
| 2026-10-24 02:01 | ok | 2,000 | 2,372 | 30,000 |  |
| 2026-10-24 01:01 | ok | 2,000 | 2,430 | 30,000 |  |
| 2026-10-24 00:01 | ok | 2,000 | 2,482 | 30,000 |  |
| 2026-10-23 23:01 | ok | 2,000 | 2,599 | 30,000 |  |
| 2026-10-23 22:01 | ok | 2,000 | 2,792 | 30,000 |  |
| 2026-10-23 21:01 | ok | 2,000 | 2,973 | 30,000 |  |
| 2026-10-23 20:01 | ok | 2,000 | 3,126 | 30,000 |  |
| 2026-10-23 19:01 | ok | 2,000 | 3,093 | 30,000 |  |
| 2026-10-23 18:01 | ok | 2,000 | 3,007 | 30,000 |  |
| 2026-10-23 17:01 | ok | 2,000 | 2,894 | 30,000 |  |
| 2026-10-23 16:01 | ok | 2,000 | 2,657 | 30,000 |  |
| 2026-10-23 15:01 | ok | 2,000 | 2,465 | 30,000 |  |
| 2026-10-23 14:01 | ok | 2,000 | 2,200 | 30,000 |  |
| 2026-10-23 13:01 | ok | 2,000 | 2,005 | 30,000 |  |
| 2026-10-23 12:01 | ok | 2,000 | 1,803 | 30,000 |  |
| 2026-10-23 11:01 | ok | 2,000 | 1,635 | 30,000 |  |
| 2026-10-23 10:01 | ok | 2,000 | 1,536 | 30,000 |  |
| 2026-10-23 09:01 | ok | 2,000 | 1,492 | 30,000 |  |
| 2026-10-23 08:01 | ok | 2,000 | 1,443 | 30,000 |  |
| 2026-10-23 07:01 | ok | 2,000 | 1,485 | 30,000 |  |
| 2026-10-23 06:01 | ok | 2,000 | 1,569 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
