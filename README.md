# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-09 13:01 UTC._

| | |
|---|---|
| Snapshots collected | **171** (581,499 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-09 13:01 UTC |
| Hours captured since the first snapshot | 166 of 172 (97%) |
| Creators in the tracking panel | 27,851 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-09 13:01 | ok | 2,000 | 2,068 | 27,851 |  |
| 2026-10-09 12:01 | ok | 2,000 | 1,875 | 27,800 |  |
| 2026-10-09 11:01 | ok | 2,000 | 1,664 | 27,744 |  |
| 2026-10-09 10:01 | ok | 2,000 | 1,571 | 27,684 |  |
| 2026-10-09 09:01 | ok | 2,000 | 1,466 | 27,621 |  |
| 2026-10-09 08:01 | ok | 2,000 | 1,390 | 27,551 |  |
| 2026-10-09 07:01 | ok | 2,000 | 1,379 | 27,464 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
