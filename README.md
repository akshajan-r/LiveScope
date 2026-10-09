# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-09 19:01 UTC._

| | |
|---|---|
| Snapshots collected | **177** (609,670 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-09 19:01 UTC |
| Hours captured since the first snapshot | 172 of 178 (97%) |
| Creators in the tracking panel | 28,163 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-09 19:01 | ok | 2,000 | 3,068 | 28,163 |  |
| 2026-10-09 18:01 | ok | 2,000 | 2,974 | 28,113 |  |
| 2026-10-09 17:01 | ok | 2,000 | 2,845 | 28,056 |  |
| 2026-10-09 16:01 | ok | 2,000 | 2,585 | 28,007 |  |
| 2026-10-09 15:01 | ok | 2,000 | 2,404 | 27,950 |  |
| 2026-10-09 14:01 | ok | 2,000 | 2,295 | 27,899 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
