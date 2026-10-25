# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-25 06:01 UTC._

| | |
|---|---|
| Snapshots collected | **553** (2,168,381 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-25 06:01 UTC |
| Hours captured since the first snapshot | 543 of 549 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-25 06:01 | ok | 2,000 | 1,501 | 30,000 |  |
| 2026-10-25 05:01 | ok | 2,000 | 1,673 | 30,000 |  |
| 2026-10-25 04:01 | ok | 2,000 | 1,816 | 30,000 |  |
| 2026-10-25 03:01 | ok | 2,000 | 1,951 | 30,000 |  |
| 2026-10-25 02:01 | ok | 2,000 | 2,010 | 30,000 |  |
| 2026-10-25 01:01 | ok | 2,000 | 2,111 | 30,000 |  |
| 2026-10-25 00:01 | ok | 2,000 | 2,161 | 30,000 |  |
| 2026-10-24 23:01 | ok | 2,000 | 2,232 | 30,000 |  |
| 2026-10-24 22:03 | ok | 2,000 | 2,495 | 30,000 |  |
| 2026-10-24 22:00 | ok | 2,000 | 2,467 | 30,000 |  |
| 2026-10-24 21:01 | ok | 2,000 | 2,591 | 30,000 |  |
| 2026-10-24 20:01 | ok | 2,000 | 2,608 | 30,000 |  |
| 2026-10-24 19:01 | ok | 2,000 | 2,578 | 30,000 |  |
| 2026-10-24 18:01 | ok | 2,000 | 2,509 | 30,000 |  |
| 2026-10-24 17:01 | ok | 2,000 | 2,350 | 30,000 |  |
| 2026-10-24 16:01 | ok | 2,000 | 2,245 | 30,000 |  |
| 2026-10-24 15:01 | ok | 2,000 | 2,110 | 30,000 |  |
| 2026-10-24 14:01 | ok | 2,000 | 1,933 | 30,000 |  |
| 2026-10-24 13:01 | ok | 2,000 | 1,808 | 30,000 |  |
| 2026-10-24 12:01 | ok | 2,000 | 1,651 | 30,000 |  |
| 2026-10-24 11:01 | ok | 2,000 | 1,564 | 30,000 |  |
| 2026-10-24 10:01 | ok | 2,000 | 1,518 | 30,000 |  |
| 2026-10-24 09:01 | ok | 2,000 | 1,471 | 30,000 |  |
| 2026-10-24 08:01 | ok | 2,000 | 1,472 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
