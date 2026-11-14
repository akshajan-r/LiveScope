# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-14 12:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,041** (4,139,992 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-14 12:01 UTC |
| Hours captured since the first snapshot | 1,029 of 1,035 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-14 12:01 | ok | 2,000 | 1,573 | 30,000 |  |
| 2026-11-14 11:01 | ok | 2,000 | 1,503 | 30,000 |  |
| 2026-11-14 10:01 | ok | 2,000 | 1,434 | 30,000 |  |
| 2026-11-14 09:01 | ok | 2,000 | 1,440 | 30,000 |  |
| 2026-11-14 08:01 | ok | 2,000 | 1,522 | 30,000 |  |
| 2026-11-14 07:01 | ok | 2,000 | 1,659 | 30,000 |  |
| 2026-11-14 06:01 | ok | 2,000 | 1,853 | 30,000 |  |
| 2026-11-14 05:01 | ok | 2,000 | 2,029 | 30,000 |  |
| 2026-11-14 04:01 | ok | 2,000 | 2,207 | 30,000 |  |
| 2026-11-14 03:01 | ok | 2,000 | 2,325 | 30,000 |  |
| 2026-11-14 02:01 | ok | 2,000 | 2,399 | 30,000 |  |
| 2026-11-14 01:01 | ok | 2,000 | 2,453 | 30,000 |  |
| 2026-11-14 00:01 | ok | 2,000 | 2,499 | 30,000 |  |
| 2026-11-13 23:01 | ok | 2,000 | 2,658 | 30,000 |  |
| 2026-11-13 22:01 | ok | 2,000 | 2,769 | 30,000 |  |
| 2026-11-13 21:01 | ok | 2,000 | 2,854 | 30,000 |  |
| 2026-11-13 20:01 | ok | 2,000 | 2,825 | 30,000 |  |
| 2026-11-13 19:01 | ok | 2,000 | 2,706 | 30,000 |  |
| 2026-11-13 18:01 | ok | 2,000 | 2,535 | 30,000 |  |
| 2026-11-13 17:01 | ok | 2,000 | 2,417 | 30,000 |  |
| 2026-11-13 16:01 | ok | 2,000 | 2,296 | 30,000 |  |
| 2026-11-13 15:01 | ok | 2,000 | 2,115 | 30,000 |  |
| 2026-11-13 14:01 | ok | 2,000 | 1,977 | 30,000 |  |
| 2026-11-13 13:01 | ok | 2,000 | 1,822 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
