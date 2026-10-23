# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-23 11:01 UTC._

| | |
|---|---|
| Snapshots collected | **509** (1,982,906 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-23 11:01 UTC |
| Hours captured since the first snapshot | 500 of 506 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-23 11:01 | ok | 2,000 | 1,635 | 30,000 |  |
| 2026-10-23 10:01 | ok | 2,000 | 1,536 | 30,000 |  |
| 2026-10-23 09:01 | ok | 2,000 | 1,492 | 30,000 |  |
| 2026-10-23 08:01 | ok | 2,000 | 1,443 | 30,000 |  |
| 2026-10-23 07:01 | ok | 2,000 | 1,485 | 30,000 |  |
| 2026-10-23 06:01 | ok | 2,000 | 1,569 | 30,000 |  |
| 2026-10-23 05:01 | ok | 2,000 | 1,760 | 30,000 |  |
| 2026-10-23 04:01 | ok | 2,000 | 1,981 | 30,000 |  |
| 2026-10-23 03:01 | ok | 2,000 | 2,166 | 30,000 |  |
| 2026-10-23 02:01 | ok | 2,000 | 2,215 | 30,000 |  |
| 2026-10-23 01:01 | ok | 2,000 | 2,209 | 30,000 |  |
| 2026-10-23 00:01 | ok | 2,000 | 2,307 | 30,000 |  |
| 2026-10-22 23:01 | ok | 2,000 | 2,325 | 30,000 |  |
| 2026-10-22 22:01 | ok | 2,000 | 2,515 | 30,000 |  |
| 2026-10-22 21:01 | ok | 2,000 | 2,782 | 30,000 |  |
| 2026-10-22 20:01 | ok | 2,000 | 2,862 | 30,000 |  |
| 2026-10-22 19:01 | ok | 2,000 | 2,852 | 30,000 |  |
| 2026-10-22 18:01 | ok | 2,000 | 2,819 | 30,000 |  |
| 2026-10-22 17:01 | ok | 2,000 | 2,714 | 30,000 |  |
| 2026-10-22 16:01 | ok | 2,000 | 2,647 | 30,000 |  |
| 2026-10-22 15:01 | ok | 2,000 | 2,378 | 30,000 |  |
| 2026-10-22 14:01 | ok | 2,000 | 2,118 | 30,000 |  |
| 2026-10-22 13:01 | ok | 2,000 | 1,917 | 30,000 |  |
| 2026-10-22 12:01 | ok | 2,000 | 1,736 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
