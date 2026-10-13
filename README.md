# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-13 21:01 UTC._

| | |
|---|---|
| Snapshots collected | **277** (1,023,644 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-13 21:01 UTC |
| Hours captured since the first snapshot | 270 of 276 (98%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-13 21:01 | ok | 2,000 | 2,868 | 30,000 |  |
| 2026-10-13 20:01 | ok | 2,000 | 3,013 | 30,000 |  |
| 2026-10-13 19:01 | ok | 2,000 | 3,070 | 30,000 |  |
| 2026-10-13 18:01 | ok | 2,000 | 2,891 | 30,000 |  |
| 2026-10-13 17:01 | ok | 2,000 | 2,883 | 30,000 |  |
| 2026-10-13 16:01 | ok | 2,000 | 2,572 | 30,000 |  |
| 2026-10-13 15:01 | ok | 2,000 | 2,311 | 30,000 |  |
| 2026-10-13 14:01 | ok | 2,000 | 2,106 | 30,000 |  |
| 2026-10-13 13:01 | ok | 2,000 | 1,851 | 30,000 |  |
| 2026-10-13 12:01 | ok | 2,000 | 1,688 | 30,000 |  |
| 2026-10-13 11:01 | ok | 2,000 | 1,559 | 30,000 |  |
| 2026-10-13 10:01 | ok | 2,000 | 1,458 | 30,000 |  |
| 2026-10-13 09:01 | ok | 2,000 | 1,408 | 30,000 |  |
| 2026-10-13 08:01 | ok | 2,000 | 1,356 | 30,000 |  |
| 2026-10-13 07:01 | ok | 2,000 | 1,403 | 30,000 |  |
| 2026-10-13 06:01 | ok | 2,000 | 1,548 | 30,000 |  |
| 2026-10-13 05:01 | ok | 2,000 | 1,722 | 30,000 |  |
| 2026-10-13 04:01 | ok | 2,000 | 1,920 | 30,000 |  |
| 2026-10-13 03:01 | ok | 2,000 | 2,102 | 30,000 |  |
| 2026-10-13 02:01 | ok | 2,000 | 2,160 | 30,000 |  |
| 2026-10-13 01:01 | ok | 2,000 | 2,214 | 30,000 |  |
| 2026-10-13 00:01 | ok | 2,000 | 2,229 | 30,000 |  |
| 2026-10-12 23:01 | ok | 2,000 | 2,330 | 30,000 |  |
| 2026-10-12 22:01 | ok | 2,000 | 2,524 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
