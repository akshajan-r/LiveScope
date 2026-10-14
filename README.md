# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-14 18:01 UTC._

| | |
|---|---|
| Snapshots collected | **298** (1,110,374 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-14 18:01 UTC |
| Hours captured since the first snapshot | 291 of 297 (98%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-14 18:01 | ok | 2,000 | 3,064 | 30,000 |  |
| 2026-10-14 17:01 | ok | 2,000 | 2,905 | 30,000 |  |
| 2026-10-14 16:01 | ok | 2,000 | 2,635 | 30,000 |  |
| 2026-10-14 15:01 | ok | 2,000 | 2,431 | 30,000 |  |
| 2026-10-14 14:01 | ok | 2,000 | 2,231 | 30,000 |  |
| 2026-10-14 13:01 | ok | 2,000 | 2,034 | 30,000 |  |
| 2026-10-14 12:01 | ok | 2,000 | 1,875 | 30,000 |  |
| 2026-10-14 11:01 | ok | 2,000 | 1,709 | 30,000 |  |
| 2026-10-14 10:01 | ok | 2,000 | 1,589 | 30,000 |  |
| 2026-10-14 09:01 | ok | 2,000 | 1,494 | 30,000 |  |
| 2026-10-14 08:01 | ok | 2,000 | 1,458 | 30,000 |  |
| 2026-10-14 07:01 | ok | 2,000 | 1,492 | 30,000 |  |
| 2026-10-14 06:01 | ok | 2,000 | 1,646 | 30,000 |  |
| 2026-10-14 05:01 | ok | 2,000 | 1,804 | 30,000 |  |
| 2026-10-14 04:01 | ok | 2,000 | 2,046 | 30,000 |  |
| 2026-10-14 03:01 | ok | 2,000 | 2,200 | 30,000 |  |
| 2026-10-14 02:01 | ok | 2,000 | 2,321 | 30,000 |  |
| 2026-10-14 01:01 | ok | 2,000 | 2,323 | 30,000 |  |
| 2026-10-14 00:01 | ok | 2,000 | 2,374 | 30,000 |  |
| 2026-10-13 23:01 | ok | 2,000 | 2,417 | 30,000 |  |
| 2026-10-13 22:01 | ok | 2,000 | 2,682 | 30,000 |  |
| 2026-10-13 21:01 | ok | 2,000 | 2,868 | 30,000 |  |
| 2026-10-13 20:01 | ok | 2,000 | 3,013 | 30,000 |  |
| 2026-10-13 19:01 | ok | 2,000 | 3,070 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
