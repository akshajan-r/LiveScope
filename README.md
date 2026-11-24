# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-24 05:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,276** (5,103,819 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-24 05:01 UTC |
| Hours captured since the first snapshot | 1,262 of 1,268 (100%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-24 05:01 | ok | 2,000 | 1,860 | 30,000 |  |
| 2026-11-24 04:01 | ok | 2,000 | 1,987 | 30,000 |  |
| 2026-11-24 03:01 | ok | 2,000 | 2,072 | 30,000 |  |
| 2026-11-24 02:01 | ok | 2,000 | 2,104 | 30,000 |  |
| 2026-11-24 01:01 | ok | 2,000 | 2,136 | 30,000 |  |
| 2026-11-24 00:01 | ok | 2,000 | 2,193 | 30,000 |  |
| 2026-11-23 23:01 | ok | 2,000 | 2,300 | 30,000 |  |
| 2026-11-23 22:01 | ok | 2,000 | 2,479 | 30,000 |  |
| 2026-11-23 21:01 | ok | 2,000 | 2,620 | 30,000 |  |
| 2026-11-23 20:01 | ok | 2,000 | 2,622 | 30,000 |  |
| 2026-11-23 19:01 | ok | 2,000 | 2,642 | 30,000 |  |
| 2026-11-23 18:01 | ok | 2,000 | 2,464 | 30,000 |  |
| 2026-11-23 17:01 | ok | 2,000 | 2,282 | 30,000 |  |
| 2026-11-23 16:01 | ok | 2,000 | 2,109 | 30,000 |  |
| 2026-11-23 15:01 | ok | 2,000 | 1,954 | 30,000 |  |
| 2026-11-23 14:01 | ok | 2,000 | 1,821 | 30,000 |  |
| 2026-11-23 13:06 | ok | 2,000 | 1,669 | 30,000 |  |
| 2026-11-23 13:00 | ok | 2,000 | 1,627 | 30,000 |  |
| 2026-11-23 12:01 | ok | 2,000 | 1,495 | 30,000 |  |
| 2026-11-23 11:01 | ok | 2,000 | 1,438 | 30,000 |  |
| 2026-11-23 10:01 | ok | 2,000 | 1,360 | 30,000 |  |
| 2026-11-23 09:01 | ok | 2,000 | 1,321 | 30,000 |  |
| 2026-11-23 08:01 | ok | 2,000 | 1,313 | 30,000 |  |
| 2026-11-23 07:01 | ok | 2,000 | 1,389 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
