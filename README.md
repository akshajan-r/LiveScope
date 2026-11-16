# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-16 12:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,089** (4,322,672 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-16 12:01 UTC |
| Hours captured since the first snapshot | 1,077 of 1,083 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-16 12:01 | ok | 2,000 | 1,376 | 30,000 |  |
| 2026-11-16 11:01 | ok | 2,000 | 1,314 | 30,000 |  |
| 2026-11-16 10:01 | ok | 2,000 | 1,219 | 30,000 |  |
| 2026-11-16 09:01 | ok | 2,000 | 1,168 | 30,000 |  |
| 2026-11-16 08:01 | ok | 2,000 | 1,168 | 30,000 |  |
| 2026-11-16 07:01 | ok | 2,000 | 1,249 | 30,000 |  |
| 2026-11-16 06:01 | ok | 2,000 | 1,337 | 30,000 |  |
| 2026-11-16 05:01 | ok | 2,000 | 1,395 | 30,000 |  |
| 2026-11-16 04:01 | ok | 2,000 | 1,521 | 30,000 |  |
| 2026-11-16 03:01 | ok | 2,000 | 1,646 | 30,000 |  |
| 2026-11-16 02:01 | ok | 2,000 | 1,695 | 30,000 |  |
| 2026-11-16 01:01 | ok | 2,000 | 1,756 | 30,000 |  |
| 2026-11-16 00:01 | ok | 2,000 | 1,890 | 30,000 |  |
| 2026-11-15 23:01 | ok | 2,000 | 2,058 | 30,000 |  |
| 2026-11-15 22:01 | ok | 2,000 | 2,233 | 30,000 |  |
| 2026-11-15 21:01 | ok | 2,000 | 2,373 | 30,000 |  |
| 2026-11-15 20:01 | ok | 2,000 | 2,385 | 30,000 |  |
| 2026-11-15 19:01 | ok | 2,000 | 2,267 | 30,000 |  |
| 2026-11-15 18:01 | ok | 2,000 | 2,245 | 30,000 |  |
| 2026-11-15 17:01 | ok | 2,000 | 2,144 | 30,000 |  |
| 2026-11-15 16:01 | ok | 2,000 | 1,981 | 30,000 |  |
| 2026-11-15 15:01 | ok | 2,000 | 1,850 | 30,000 |  |
| 2026-11-15 14:01 | ok | 2,000 | 1,709 | 30,000 |  |
| 2026-11-15 13:01 | ok | 2,000 | 1,624 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
