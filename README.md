# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-15 13:01 UTC._

| | |
|---|---|
| Snapshots collected | **318** (1,194,584 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-15 13:01 UTC |
| Hours captured since the first snapshot | 310 of 316 (98%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-15 13:01 | ok | 2,000 | 2,141 | 30,000 |  |
| 2026-10-15 12:01 | ok | 2,000 | 1,960 | 30,000 |  |
| 2026-10-15 11:01 | ok | 2,000 | 1,766 | 30,000 |  |
| 2026-10-15 10:01 | ok | 2,000 | 1,653 | 30,000 |  |
| 2026-10-15 09:01 | ok | 2,000 | 1,505 | 30,000 |  |
| 2026-10-15 08:01 | ok | 2,000 | 1,473 | 30,000 |  |
| 2026-10-15 07:01 | ok | 2,000 | 1,547 | 30,000 |  |
| 2026-10-15 06:01 | ok | 2,000 | 1,662 | 30,000 |  |
| 2026-10-15 05:01 | ok | 2,000 | 1,847 | 30,000 |  |
| 2026-10-15 04:01 | ok | 2,000 | 2,083 | 30,000 |  |
| 2026-10-15 03:01 | ok | 2,000 | 2,254 | 30,000 |  |
| 2026-10-15 02:01 | ok | 2,000 | 2,368 | 30,000 |  |
| 2026-10-15 01:01 | ok | 2,000 | 2,436 | 30,000 |  |
| 2026-10-15 00:01 | ok | 2,000 | 2,437 | 30,000 |  |
| 2026-10-14 23:01 | ok | 2,000 | 2,466 | 30,000 |  |
| 2026-10-14 22:01 | ok | 2,000 | 2,648 | 30,000 |  |
| 2026-10-14 21:01 | ok | 2,000 | 2,867 | 30,000 |  |
| 2026-10-14 20:01 | ok | 2,000 | 3,019 | 30,000 |  |
| 2026-10-14 19:02 | ok | 2,000 | 3,042 | 30,000 |  |
| 2026-10-14 19:00 | ok | 2,000 | 3,036 | 30,000 |  |
| 2026-10-14 18:01 | ok | 2,000 | 3,064 | 30,000 |  |
| 2026-10-14 17:01 | ok | 2,000 | 2,905 | 30,000 |  |
| 2026-10-14 16:01 | ok | 2,000 | 2,635 | 30,000 |  |
| 2026-10-14 15:01 | ok | 2,000 | 2,431 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
