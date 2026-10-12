# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-12 07:01 UTC._

| | |
|---|---|
| Snapshots collected | **239** (866,941 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-12 07:01 UTC |
| Hours captured since the first snapshot | 232 of 238 (97%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-12 07:01 | ok | 2,000 | 1,393 | 30,000 |  |
| 2026-10-12 06:01 | ok | 2,000 | 1,465 | 30,000 |  |
| 2026-10-12 05:01 | ok | 2,000 | 1,572 | 30,000 |  |
| 2026-10-12 04:01 | ok | 2,000 | 1,732 | 30,000 |  |
| 2026-10-12 03:01 | ok | 2,000 | 1,811 | 30,000 |  |
| 2026-10-12 02:01 | ok | 2,000 | 1,826 | 30,000 |  |
| 2026-10-12 01:01 | ok | 2,000 | 1,876 | 30,000 |  |
| 2026-10-12 00:01 | ok | 2,000 | 1,931 | 30,000 |  |
| 2026-10-11 23:01 | ok | 2,000 | 2,106 | 30,000 |  |
| 2026-10-11 22:01 | ok | 2,000 | 2,251 | 30,000 |  |
| 2026-10-11 21:01 | ok | 2,000 | 2,524 | 30,000 |  |
| 2026-10-11 20:01 | ok | 2,000 | 2,856 | 30,000 |  |
| 2026-10-11 19:01 | ok | 2,000 | 2,772 | 30,000 |  |
| 2026-10-11 18:01 | ok | 2,000 | 2,661 | 30,000 |  |
| 2026-10-11 17:01 | ok | 2,000 | 2,612 | 30,000 |  |
| 2026-10-11 16:01 | ok | 2,000 | 2,417 | 30,000 |  |
| 2026-10-11 15:01 | ok | 2,000 | 2,185 | 30,000 |  |
| 2026-10-11 14:01 | ok | 2,000 | 2,063 | 30,000 |  |
| 2026-10-11 13:01 | ok | 2,000 | 1,968 | 30,000 |  |
| 2026-10-11 12:01 | ok | 2,000 | 1,839 | 30,000 |  |
| 2026-10-11 11:01 | ok | 2,000 | 1,741 | 30,000 |  |
| 2026-10-11 10:01 | ok | 2,000 | 1,597 | 30,000 |  |
| 2026-10-11 09:02 | ok | 2,000 | 1,544 | 30,000 |  |
| 2026-10-11 09:00 | ok | 2,000 | 1,520 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
