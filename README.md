# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-18 02:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,127** (4,472,172 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-18 02:01 UTC |
| Hours captured since the first snapshot | 1,115 of 1,121 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-18 02:01 | ok | 2,000 | 2,069 | 30,000 |  |
| 2026-11-18 01:01 | ok | 2,000 | 2,054 | 30,000 |  |
| 2026-11-18 00:01 | ok | 2,000 | 2,092 | 30,000 |  |
| 2026-11-17 23:01 | ok | 2,000 | 2,174 | 30,000 |  |
| 2026-11-17 22:01 | ok | 2,000 | 2,316 | 30,000 |  |
| 2026-11-17 21:01 | ok | 2,000 | 2,451 | 30,000 |  |
| 2026-11-17 20:01 | ok | 2,000 | 2,545 | 30,000 |  |
| 2026-11-17 19:01 | ok | 2,000 | 2,496 | 30,000 |  |
| 2026-11-17 18:01 | ok | 2,000 | 2,375 | 30,000 |  |
| 2026-11-17 17:01 | ok | 2,000 | 2,295 | 30,000 |  |
| 2026-11-17 16:01 | ok | 2,000 | 2,112 | 30,000 |  |
| 2026-11-17 15:01 | ok | 2,000 | 1,942 | 30,000 |  |
| 2026-11-17 14:01 | ok | 2,000 | 1,773 | 30,000 |  |
| 2026-11-17 13:01 | ok | 2,000 | 1,627 | 30,000 |  |
| 2026-11-17 12:01 | ok | 2,000 | 1,516 | 30,000 |  |
| 2026-11-17 11:01 | ok | 2,000 | 1,375 | 30,000 |  |
| 2026-11-17 10:01 | ok | 2,000 | 1,251 | 30,000 |  |
| 2026-11-17 09:01 | ok | 2,000 | 1,191 | 30,000 |  |
| 2026-11-17 08:01 | ok | 2,000 | 1,183 | 30,000 |  |
| 2026-11-17 07:01 | ok | 2,000 | 1,271 | 30,000 |  |
| 2026-11-17 06:01 | ok | 2,000 | 1,379 | 30,000 |  |
| 2026-11-17 05:01 | ok | 2,000 | 1,547 | 30,000 |  |
| 2026-11-17 04:01 | ok | 2,000 | 1,736 | 30,000 |  |
| 2026-11-17 03:01 | ok | 2,000 | 1,831 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
