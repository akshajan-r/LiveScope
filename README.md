# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-26 08:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,326** (5,302,349 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-26 08:01 UTC |
| Hours captured since the first snapshot | 1,312 of 1,319 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-26 08:01 | ok | 2,000 | 1,386 | 30,000 |  |
| 2026-11-26 07:01 | ok | 2,000 | 1,536 | 30,000 |  |
| 2026-11-26 06:01 | ok | 2,000 | 1,666 | 30,000 |  |
| 2026-11-26 05:01 | ok | 2,000 | 1,799 | 30,000 |  |
| 2026-11-26 04:01 | ok | 2,000 | 1,928 | 30,000 |  |
| 2026-11-26 03:01 | ok | 2,000 | 1,997 | 30,000 |  |
| 2026-11-26 02:01 | ok | 2,000 | 2,052 | 30,000 |  |
| 2026-11-26 01:01 | ok | 2,000 | 2,086 | 30,000 |  |
| 2026-11-26 00:01 | ok | 2,000 | 2,178 | 30,000 |  |
| 2026-11-25 23:01 | ok | 2,000 | 2,349 | 30,000 |  |
| 2026-11-25 22:01 | ok | 2,000 | 2,520 | 30,000 |  |
| 2026-11-25 21:01 | ok | 2,000 | 2,640 | 30,000 |  |
| 2026-11-25 20:01 | ok | 2,000 | 2,722 | 30,000 |  |
| 2026-11-25 19:01 | ok | 2,000 | 2,677 | 30,000 |  |
| 2026-11-25 18:01 | ok | 2,000 | 2,576 | 30,000 |  |
| 2026-11-25 17:01 | ok | 2,000 | 2,353 | 30,000 |  |
| 2026-11-25 15:01 | ok | 2,000 | 2,099 | 30,000 |  |
| 2026-11-25 14:01 | ok | 2,000 | 1,882 | 30,000 |  |
| 2026-11-25 13:01 | ok | 2,000 | 1,707 | 30,000 |  |
| 2026-11-25 12:01 | ok | 2,000 | 1,552 | 30,000 |  |
| 2026-11-25 11:01 | ok | 2,000 | 1,467 | 30,000 |  |
| 2026-11-25 10:02 | ok | 2,000 | 1,396 | 30,000 |  |
| 2026-11-25 09:01 | ok | 2,000 | 1,358 | 30,000 |  |
| 2026-11-25 08:01 | ok | 2,000 | 1,398 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
