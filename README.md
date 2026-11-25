# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-25 00:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,295** (5,179,783 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-25 00:01 UTC |
| Hours captured since the first snapshot | 1,281 of 1,287 (100%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-11-24 09:01 | ok | 2,000 | 1,362 | 30,000 |  |
| 2026-11-24 08:01 | ok | 2,000 | 1,428 | 30,000 |  |
| 2026-11-24 07:01 | ok | 2,000 | 1,528 | 30,000 |  |
| 2026-11-24 06:01 | ok | 2,000 | 1,707 | 30,000 |  |
| 2026-11-24 05:01 | ok | 2,000 | 1,860 | 30,000 |  |
| 2026-11-24 04:01 | ok | 2,000 | 1,987 | 30,000 |  |
| 2026-11-24 03:01 | ok | 2,000 | 2,072 | 30,000 |  |
| 2026-11-24 02:01 | ok | 2,000 | 2,104 | 30,000 |  |
| 2026-11-24 01:01 | ok | 2,000 | 2,136 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
