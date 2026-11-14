# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-14 02:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,031** (4,102,447 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-14 02:01 UTC |
| Hours captured since the first snapshot | 1,019 of 1,025 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-11-13 12:01 | ok | 2,000 | 1,622 | 30,000 |  |
| 2026-11-13 11:01 | ok | 2,000 | 1,485 | 30,000 |  |
| 2026-11-13 10:01 | ok | 2,000 | 1,399 | 30,000 |  |
| 2026-11-13 09:01 | ok | 2,000 | 1,387 | 30,000 |  |
| 2026-11-13 08:01 | ok | 2,000 | 1,431 | 30,000 |  |
| 2026-11-13 07:01 | ok | 2,000 | 1,475 | 30,000 |  |
| 2026-11-13 06:01 | ok | 2,000 | 1,612 | 30,000 |  |
| 2026-11-13 05:01 | ok | 2,000 | 1,833 | 30,000 |  |
| 2026-11-13 04:01 | ok | 2,000 | 1,962 | 30,000 |  |
| 2026-11-13 03:01 | ok | 2,000 | 2,057 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
