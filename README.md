# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-23 20:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,267** (5,066,068 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-23 20:01 UTC |
| Hours captured since the first snapshot | 1,253 of 1,259 (100%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-11-23 06:01 | ok | 2,000 | 1,530 | 30,000 |  |
| 2026-11-23 05:01 | ok | 2,000 | 1,668 | 30,000 |  |
| 2026-11-23 04:01 | ok | 2,000 | 1,780 | 30,000 |  |
| 2026-11-23 03:01 | ok | 2,000 | 1,915 | 30,000 |  |
| 2026-11-23 02:01 | ok | 2,000 | 1,999 | 30,000 |  |
| 2026-11-23 01:01 | ok | 2,000 | 1,984 | 30,000 |  |
| 2026-11-23 00:01 | ok | 2,000 | 2,132 | 30,000 |  |
| 2026-11-22 23:01 | ok | 2,000 | 2,193 | 30,000 |  |
| 2026-11-22 22:01 | ok | 2,000 | 2,414 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
