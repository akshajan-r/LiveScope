# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-15 22:01 UTC._

| | |
|---|---|
| Snapshots collected | **327** (1,238,147 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-15 22:01 UTC |
| Hours captured since the first snapshot | 319 of 325 (98%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-15 22:01 | ok | 2,000 | 2,664 | 30,000 |  |
| 2026-10-15 21:01 | ok | 2,000 | 2,953 | 30,000 |  |
| 2026-10-15 20:01 | ok | 2,000 | 3,173 | 30,000 |  |
| 2026-10-15 19:01 | ok | 2,000 | 3,198 | 30,000 |  |
| 2026-10-15 18:01 | ok | 2,000 | 3,063 | 30,000 |  |
| 2026-10-15 17:01 | ok | 2,000 | 2,910 | 30,000 |  |
| 2026-10-15 16:01 | ok | 2,000 | 2,763 | 30,000 |  |
| 2026-10-15 15:01 | ok | 2,000 | 2,546 | 30,000 |  |
| 2026-10-15 14:01 | ok | 2,000 | 2,293 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
