# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-20 12:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,185** (4,724,229 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-20 12:01 UTC |
| Hours captured since the first snapshot | 1,173 of 1,179 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-20 12:01 | ok | 2,000 | 1,963 | 30,000 |  |
| 2026-11-20 11:01 | ok | 2,000 | 1,840 | 30,000 |  |
| 2026-11-20 10:01 | ok | 2,000 | 1,769 | 30,000 |  |
| 2026-11-20 09:01 | ok | 2,000 | 1,756 | 30,000 |  |
| 2026-11-20 08:01 | ok | 2,000 | 1,723 | 30,000 |  |
| 2026-11-20 07:01 | ok | 2,000 | 1,862 | 30,000 |  |
| 2026-11-20 06:01 | ok | 2,000 | 2,069 | 30,000 |  |
| 2026-11-20 05:01 | ok | 2,000 | 2,266 | 30,000 |  |
| 2026-11-20 04:01 | ok | 2,000 | 2,413 | 30,000 |  |
| 2026-11-20 03:01 | ok | 2,000 | 2,531 | 30,000 |  |
| 2026-11-20 02:01 | ok | 2,000 | 2,624 | 30,000 |  |
| 2026-11-20 01:01 | ok | 2,000 | 2,702 | 30,000 |  |
| 2026-11-20 00:01 | ok | 2,000 | 2,807 | 30,000 |  |
| 2026-11-19 23:01 | ok | 2,000 | 2,891 | 30,000 |  |
| 2026-11-19 22:01 | ok | 2,000 | 3,113 | 30,000 |  |
| 2026-11-19 21:01 | ok | 2,000 | 3,284 | 30,000 |  |
| 2026-11-19 20:01 | ok | 2,000 | 3,287 | 30,000 |  |
| 2026-11-19 19:01 | ok | 2,000 | 3,183 | 30,000 |  |
| 2026-11-19 18:01 | ok | 2,000 | 3,134 | 30,000 |  |
| 2026-11-19 17:01 | ok | 2,000 | 2,996 | 30,000 |  |
| 2026-11-19 16:01 | ok | 2,000 | 2,856 | 30,000 |  |
| 2026-11-19 15:01 | ok | 2,000 | 2,639 | 30,000 |  |
| 2026-11-19 14:01 | ok | 2,000 | 2,449 | 30,000 |  |
| 2026-11-19 13:01 | ok | 2,000 | 2,301 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
