# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-25 09:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,304** (5,213,781 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-25 09:01 UTC |
| Hours captured since the first snapshot | 1,290 of 1,296 (100%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-25 09:01 | ok | 2,000 | 1,358 | 30,000 |  |
| 2026-11-25 08:01 | ok | 2,000 | 1,398 | 30,000 |  |
| 2026-11-25 07:01 | ok | 2,000 | 1,529 | 30,000 |  |
| 2026-11-25 06:01 | ok | 2,000 | 1,623 | 30,000 |  |
| 2026-11-25 05:01 | ok | 2,000 | 1,791 | 30,000 |  |
| 2026-11-25 04:01 | ok | 2,000 | 1,925 | 30,000 |  |
| 2026-11-25 03:02 | ok | 2,000 | 2,110 | 30,000 |  |
| 2026-11-25 02:01 | ok | 2,000 | 2,116 | 30,000 |  |
| 2026-11-25 01:01 | ok | 2,000 | 2,148 | 30,000 |  |
| 2026-11-25 00:01 | ok | 2,000 | 2,229 | 30,000 |  |
| 2026-11-24 23:01 | ok | 2,000 | 2,291 | 30,000 |  |
| 2026-11-24 22:01 | ok | 2,000 | 2,415 | 30,000 |  |
| 2026-11-24 21:01 | ok | 2,000 | 2,570 | 30,000 |  |
| 2026-11-24 20:01 | ok | 2,000 | 2,634 | 30,000 |  |
| 2026-11-24 19:01 | ok | 2,000 | 2,643 | 30,000 |  |
| 2026-11-24 18:01 | ok | 2,000 | 2,563 | 30,000 |  |
| 2026-11-24 17:01 | ok | 2,000 | 2,378 | 30,000 |  |
| 2026-11-24 16:01 | ok | 2,000 | 2,153 | 30,000 |  |
| 2026-11-24 15:02 | ok | 2,000 | 2,071 | 30,000 |  |
| 2026-11-24 14:01 | ok | 2,000 | 1,896 | 30,000 |  |
| 2026-11-24 13:01 | ok | 2,000 | 1,741 | 30,000 |  |
| 2026-11-24 12:01 | ok | 2,000 | 1,560 | 30,000 |  |
| 2026-11-24 11:01 | ok | 2,000 | 1,439 | 30,000 |  |
| 2026-11-24 10:01 | ok | 2,000 | 1,356 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
