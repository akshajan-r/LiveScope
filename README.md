# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-24 16:01 UTC._

| | |
|---|---|
| Snapshots collected | **538** (2,105,328 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-24 16:01 UTC |
| Hours captured since the first snapshot | 529 of 535 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-24 16:01 | ok | 2,000 | 2,245 | 30,000 |  |
| 2026-10-24 15:01 | ok | 2,000 | 2,110 | 30,000 |  |
| 2026-10-24 14:01 | ok | 2,000 | 1,933 | 30,000 |  |
| 2026-10-24 13:01 | ok | 2,000 | 1,808 | 30,000 |  |
| 2026-10-24 12:01 | ok | 2,000 | 1,651 | 30,000 |  |
| 2026-10-24 11:01 | ok | 2,000 | 1,564 | 30,000 |  |
| 2026-10-24 10:01 | ok | 2,000 | 1,518 | 30,000 |  |
| 2026-10-24 09:01 | ok | 2,000 | 1,471 | 30,000 |  |
| 2026-10-24 08:01 | ok | 2,000 | 1,472 | 30,000 |  |
| 2026-10-24 07:01 | ok | 2,000 | 1,603 | 30,000 |  |
| 2026-10-24 06:01 | ok | 2,000 | 1,796 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
