# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-08 15:01 UTC._

| | |
|---|---|
| Snapshots collected | **900** (3,573,152 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-08 15:01 UTC |
| Hours captured since the first snapshot | 888 of 894 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-08 15:01 | ok | 2,000 | 2,088 | 30,000 |  |
| 2026-11-08 14:01 | ok | 2,000 | 1,875 | 30,000 |  |
| 2026-11-08 13:01 | ok | 2,000 | 1,751 | 30,000 |  |
| 2026-11-08 12:01 | ok | 2,000 | 1,613 | 30,000 |  |
| 2026-11-08 11:01 | ok | 2,000 | 1,567 | 30,000 |  |
| 2026-11-08 10:01 | ok | 2,000 | 1,526 | 30,000 |  |
| 2026-11-08 09:01 | ok | 2,000 | 1,546 | 30,000 |  |
| 2026-11-08 08:01 | ok | 2,000 | 1,559 | 30,000 |  |
| 2026-11-08 07:01 | ok | 2,000 | 1,726 | 30,000 |  |
| 2026-11-08 06:01 | ok | 2,000 | 1,848 | 30,000 |  |
| 2026-11-08 05:01 | ok | 2,000 | 1,979 | 30,000 |  |
| 2026-11-08 04:01 | ok | 2,000 | 2,102 | 30,000 |  |
| 2026-11-08 03:01 | ok | 2,000 | 2,113 | 30,000 |  |
| 2026-11-08 02:01 | ok | 2,000 | 2,203 | 30,000 |  |
| 2026-11-08 01:01 | ok | 2,000 | 2,212 | 30,000 |  |
| 2026-11-08 00:01 | ok | 2,000 | 2,335 | 30,000 |  |
| 2026-11-07 23:01 | ok | 2,000 | 2,480 | 30,000 |  |
| 2026-11-07 22:01 | ok | 2,000 | 2,619 | 30,000 |  |
| 2026-11-07 21:01 | ok | 2,000 | 2,737 | 30,000 |  |
| 2026-11-07 20:01 | ok | 2,000 | 2,807 | 30,000 |  |
| 2026-11-07 19:01 | ok | 2,000 | 2,637 | 30,000 |  |
| 2026-11-07 18:01 | ok | 2,000 | 2,543 | 30,000 |  |
| 2026-11-07 17:01 | ok | 2,000 | 2,411 | 30,000 |  |
| 2026-11-07 16:01 | ok | 2,000 | 2,344 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
