# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-28 18:01 UTC._

| | |
|---|---|
| Snapshots collected | **637** (2,496,298 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-28 18:01 UTC |
| Hours captured since the first snapshot | 627 of 633 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-28 18:01 | ok | 2,000 | 2,649 | 30,000 |  |
| 2026-10-28 17:02 | ok | 2,000 | 2,489 | 30,000 |  |
| 2026-10-28 16:01 | ok | 2,000 | 2,319 | 30,000 |  |
| 2026-10-28 15:01 | ok | 2,000 | 2,104 | 30,000 |  |
| 2026-10-28 14:01 | ok | 2,000 | 1,946 | 30,000 |  |
| 2026-10-28 13:01 | ok | 2,000 | 1,769 | 30,000 |  |
| 2026-10-28 12:01 | ok | 2,000 | 1,583 | 30,000 |  |
| 2026-10-28 11:01 | ok | 2,000 | 1,451 | 30,000 |  |
| 2026-10-28 10:01 | ok | 2,000 | 1,272 | 30,000 |  |
| 2026-10-28 09:01 | ok | 2,000 | 1,195 | 30,000 |  |
| 2026-10-28 08:01 | ok | 2,000 | 1,178 | 30,000 |  |
| 2026-10-28 07:01 | ok | 2,000 | 1,240 | 30,000 |  |
| 2026-10-28 06:01 | ok | 2,000 | 1,422 | 30,000 |  |
| 2026-10-28 05:01 | ok | 2,000 | 1,664 | 30,000 |  |
| 2026-10-28 04:01 | ok | 2,000 | 1,947 | 30,000 |  |
| 2026-10-28 03:01 | ok | 2,000 | 2,114 | 30,000 |  |
| 2026-10-28 02:01 | ok | 2,000 | 2,268 | 30,000 |  |
| 2026-10-28 01:01 | ok | 2,000 | 2,342 | 30,000 |  |
| 2026-10-28 00:01 | ok | 2,000 | 2,322 | 30,000 |  |
| 2026-10-27 23:01 | ok | 2,000 | 2,405 | 30,000 |  |
| 2026-10-27 22:01 | ok | 2,000 | 2,581 | 30,000 |  |
| 2026-10-27 21:01 | ok | 2,000 | 2,844 | 30,000 |  |
| 2026-10-27 20:01 | ok | 2,000 | 2,793 | 30,000 |  |
| 2026-10-27 19:01 | ok | 2,000 | 2,723 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
