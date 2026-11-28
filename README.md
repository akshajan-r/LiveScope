# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-28 13:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,380** (5,507,554 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-28 13:01 UTC |
| Hours captured since the first snapshot | 1,365 of 1,372 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-28 13:01 | ok | 2,000 | 1,589 | 30,000 |  |
| 2026-11-28 12:01 | ok | 2,000 | 1,454 | 30,000 |  |
| 2026-11-28 11:01 | ok | 2,000 | 1,378 | 30,000 |  |
| 2026-11-28 10:01 | ok | 2,000 | 1,330 | 30,000 |  |
| 2026-11-28 09:01 | ok | 2,000 | 1,305 | 30,000 |  |
| 2026-11-28 08:01 | ok | 2,000 | 1,336 | 30,000 |  |
| 2026-11-28 07:01 | ok | 2,000 | 1,493 | 30,000 |  |
| 2026-11-28 06:01 | ok | 2,000 | 1,696 | 30,000 |  |
| 2026-11-28 05:01 | ok | 2,000 | 1,890 | 30,000 |  |
| 2026-11-28 04:01 | ok | 2,000 | 2,003 | 30,000 |  |
| 2026-11-28 03:01 | ok | 2,000 | 2,054 | 30,000 |  |
| 2026-11-28 02:01 | ok | 2,000 | 2,109 | 30,000 |  |
| 2026-11-28 01:01 | ok | 2,000 | 2,153 | 30,000 |  |
| 2026-11-28 00:01 | ok | 2,000 | 2,234 | 30,000 |  |
| 2026-11-27 23:01 | ok | 2,000 | 2,341 | 30,000 |  |
| 2026-11-27 22:01 | ok | 2,000 | 2,494 | 30,000 |  |
| 2026-11-27 21:01 | ok | 2,000 | 2,619 | 30,000 |  |
| 2026-11-27 20:04 | ok | 2,000 | 2,613 | 30,000 |  |
| 2026-11-27 20:00 | ok | 2,000 | 2,583 | 30,000 |  |
| 2026-11-27 19:01 | ok | 2,000 | 2,504 | 30,000 |  |
| 2026-11-27 18:01 | ok | 2,000 | 2,385 | 30,000 |  |
| 2026-11-27 17:01 | ok | 2,000 | 2,241 | 30,000 |  |
| 2026-11-27 16:01 | ok | 2,000 | 2,086 | 30,000 |  |
| 2026-11-27 15:01 | ok | 2,000 | 1,917 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
