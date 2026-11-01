# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-01 16:01 UTC._

| | |
|---|---|
| Snapshots collected | **732** (2,881,367 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-01 16:01 UTC |
| Hours captured since the first snapshot | 721 of 727 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-01 16:01 | ok | 2,000 | 1,876 | 30,000 |  |
| 2026-11-01 15:01 | ok | 2,000 | 1,765 | 30,000 |  |
| 2026-11-01 14:01 | ok | 2,000 | 1,639 | 30,000 |  |
| 2026-11-01 13:01 | ok | 2,000 | 1,535 | 30,000 |  |
| 2026-11-01 12:01 | ok | 2,000 | 1,407 | 30,000 |  |
| 2026-11-01 11:01 | ok | 2,000 | 1,340 | 30,000 |  |
| 2026-11-01 10:01 | ok | 2,000 | 1,234 | 30,000 |  |
| 2026-11-01 09:01 | ok | 2,000 | 1,188 | 30,000 |  |
| 2026-11-01 08:01 | ok | 2,000 | 1,181 | 30,000 |  |
| 2026-11-01 07:01 | ok | 2,000 | 1,313 | 30,000 |  |
| 2026-11-01 06:01 | ok | 2,000 | 1,451 | 30,000 |  |
| 2026-11-01 05:01 | ok | 2,000 | 1,647 | 30,000 |  |
| 2026-11-01 04:01 | ok | 2,000 | 1,823 | 30,000 |  |
| 2026-11-01 03:01 | ok | 2,000 | 1,930 | 30,000 |  |
| 2026-11-01 02:01 | ok | 2,000 | 2,054 | 30,000 |  |
| 2026-11-01 01:01 | ok | 2,000 | 2,153 | 30,000 |  |
| 2026-11-01 00:01 | ok | 2,000 | 2,256 | 30,000 |  |
| 2026-10-31 23:01 | ok | 2,000 | 2,415 | 30,000 |  |
| 2026-10-31 22:01 | ok | 2,000 | 2,567 | 30,000 |  |
| 2026-10-31 21:01 | ok | 2,000 | 2,658 | 30,000 |  |
| 2026-10-31 20:01 | ok | 2,000 | 2,692 | 30,000 |  |
| 2026-10-31 19:01 | ok | 2,000 | 2,565 | 30,000 |  |
| 2026-10-31 18:01 | ok | 2,000 | 2,502 | 30,000 |  |
| 2026-10-31 17:01 | ok | 2,000 | 2,362 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
