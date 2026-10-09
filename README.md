# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-09 06:02 UTC._

| | |
|---|---|
| Snapshots collected | **164** (556,086 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-09 06:01 UTC |
| Hours captured since the first snapshot | 159 of 165 (96%) |
| Creators in the tracking panel | 27,373 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-09 06:01 | ok | 2,000 | 1,505 | 27,373 |  |
| 2026-10-09 05:01 | ok | 2,000 | 1,685 | 27,286 |  |
| 2026-10-09 04:01 | ok | 2,000 | 1,891 | 27,193 |  |
| 2026-10-09 03:01 | ok | 2,000 | 2,101 | 27,127 |  |
| 2026-10-09 02:01 | ok | 2,000 | 2,157 | 27,044 |  |
| 2026-10-09 01:01 | ok | 2,000 | 2,188 | 26,962 |  |
| 2026-10-09 00:01 | ok | 2,000 | 2,157 | 26,869 |  |
| 2026-10-08 23:01 | ok | 2,000 | 2,282 | 26,795 |  |
| 2026-10-08 22:01 | ok | 2,000 | 2,450 | 26,730 |  |
| 2026-10-08 21:01 | ok | 2,000 | 2,688 | 26,660 |  |
| 2026-10-08 20:01 | ok | 2,000 | 2,874 | 26,604 |  |
| 2026-10-08 19:01 | ok | 2,000 | 2,858 | 26,546 |  |
| 2026-10-08 18:01 | ok | 2,000 | 2,811 | 26,499 |  |
| 2026-10-08 17:02 | ok | 2,000 | 2,709 | 26,445 |  |
| 2026-10-08 17:00 | ok | 2,000 | 2,677 | 26,438 |  |
| 2026-10-08 16:01 | ok | 2,000 | 2,562 | 26,389 |  |
| 2026-10-08 15:01 | ok | 2,000 | 2,297 | 26,334 |  |
| 2026-10-08 14:01 | ok | 2,000 | 2,147 | 26,273 |  |
| 2026-10-08 13:01 | ok | 2,000 | 1,934 | 26,222 |  |
| 2026-10-08 12:01 | ok | 2,000 | 1,782 | 26,162 |  |
| 2026-10-08 11:01 | ok | 2,000 | 1,605 | 26,088 |  |
| 2026-10-08 10:01 | ok | 2,000 | 1,469 | 26,025 |  |
| 2026-10-08 09:01 | ok | 2,000 | 1,437 | 25,947 |  |
| 2026-10-08 08:01 | ok | 2,000 | 1,289 | 25,864 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
