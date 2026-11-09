# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-09 09:01 UTC._

| | |
|---|---|
| Snapshots collected | **918** (3,645,203 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-09 09:01 UTC |
| Hours captured since the first snapshot | 906 of 912 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-09 09:01 | ok | 2,000 | 1,336 | 30,000 |  |
| 2026-11-09 08:01 | ok | 2,000 | 1,330 | 30,000 |  |
| 2026-11-09 07:01 | ok | 2,000 | 1,420 | 30,000 |  |
| 2026-11-09 06:01 | ok | 2,000 | 1,517 | 30,000 |  |
| 2026-11-09 05:01 | ok | 2,000 | 1,662 | 30,000 |  |
| 2026-11-09 04:01 | ok | 2,000 | 1,808 | 30,000 |  |
| 2026-11-09 03:01 | ok | 2,000 | 1,899 | 30,000 |  |
| 2026-11-09 02:01 | ok | 2,000 | 1,972 | 30,000 |  |
| 2026-11-09 01:01 | ok | 2,000 | 2,059 | 30,000 |  |
| 2026-11-09 00:01 | ok | 2,000 | 2,130 | 30,000 |  |
| 2026-11-08 23:01 | ok | 2,000 | 2,263 | 30,000 |  |
| 2026-11-08 22:01 | ok | 2,000 | 2,407 | 30,000 |  |
| 2026-11-08 21:01 | ok | 2,000 | 2,543 | 30,000 |  |
| 2026-11-08 20:01 | ok | 2,000 | 2,505 | 30,000 |  |
| 2026-11-08 19:01 | ok | 2,000 | 2,422 | 30,000 |  |
| 2026-11-08 18:01 | ok | 2,000 | 2,397 | 30,000 |  |
| 2026-11-08 17:01 | ok | 2,000 | 2,255 | 30,000 |  |
| 2026-11-08 16:01 | ok | 2,000 | 2,126 | 30,000 |  |
| 2026-11-08 15:01 | ok | 2,000 | 2,088 | 30,000 |  |
| 2026-11-08 14:01 | ok | 2,000 | 1,875 | 30,000 |  |
| 2026-11-08 13:01 | ok | 2,000 | 1,751 | 30,000 |  |
| 2026-11-08 12:01 | ok | 2,000 | 1,613 | 30,000 |  |
| 2026-11-08 11:01 | ok | 2,000 | 1,567 | 30,000 |  |
| 2026-11-08 10:01 | ok | 2,000 | 1,526 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
