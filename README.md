# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-21 04:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,201** (4,800,520 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-21 04:01 UTC |
| Hours captured since the first snapshot | 1,189 of 1,195 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-21 04:01 | ok | 2,000 | 2,501 | 30,000 |  |
| 2026-11-21 03:01 | ok | 2,000 | 2,572 | 30,000 |  |
| 2026-11-21 02:01 | ok | 2,000 | 2,649 | 30,000 |  |
| 2026-11-21 01:01 | ok | 2,000 | 2,665 | 30,000 |  |
| 2026-11-21 00:01 | ok | 2,000 | 2,806 | 30,000 |  |
| 2026-11-20 23:01 | ok | 2,000 | 2,901 | 30,000 |  |
| 2026-11-20 22:01 | ok | 2,000 | 3,099 | 30,000 |  |
| 2026-11-20 21:01 | ok | 2,000 | 3,217 | 30,000 |  |
| 2026-11-20 20:01 | ok | 2,000 | 3,217 | 30,000 |  |
| 2026-11-20 19:01 | ok | 2,000 | 3,056 | 30,000 |  |
| 2026-11-20 18:01 | ok | 2,000 | 3,010 | 30,000 |  |
| 2026-11-20 17:01 | ok | 2,000 | 2,794 | 30,000 |  |
| 2026-11-20 16:01 | ok | 2,000 | 2,729 | 30,000 |  |
| 2026-11-20 15:01 | ok | 2,000 | 2,519 | 30,000 |  |
| 2026-11-20 14:01 | ok | 2,000 | 2,415 | 30,000 |  |
| 2026-11-20 13:01 | ok | 2,000 | 2,141 | 30,000 |  |
| 2026-11-20 12:01 | ok | 2,000 | 1,963 | 30,000 |  |
| 2026-11-20 11:01 | ok | 2,000 | 1,840 | 30,000 |  |
| 2026-11-20 10:01 | ok | 2,000 | 1,769 | 30,000 |  |
| 2026-11-20 09:01 | ok | 2,000 | 1,756 | 30,000 |  |
| 2026-11-20 08:01 | ok | 2,000 | 1,723 | 30,000 |  |
| 2026-11-20 07:01 | ok | 2,000 | 1,862 | 30,000 |  |
| 2026-11-20 06:01 | ok | 2,000 | 2,069 | 30,000 |  |
| 2026-11-20 05:01 | ok | 2,000 | 2,266 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
