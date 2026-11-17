# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-17 00:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,101** (4,371,794 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-17 00:01 UTC |
| Hours captured since the first snapshot | 1,089 of 1,095 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-17 00:01 | ok | 2,000 | 1,940 | 30,000 |  |
| 2026-11-16 23:01 | ok | 2,000 | 2,133 | 30,000 |  |
| 2026-11-16 22:01 | ok | 2,000 | 2,291 | 30,000 |  |
| 2026-11-16 21:01 | ok | 2,000 | 2,458 | 30,000 |  |
| 2026-11-16 20:01 | ok | 2,000 | 2,567 | 30,000 |  |
| 2026-11-16 19:01 | ok | 2,000 | 2,455 | 30,000 |  |
| 2026-11-16 18:01 | ok | 2,000 | 2,286 | 30,000 |  |
| 2026-11-16 17:01 | ok | 2,000 | 2,090 | 30,000 |  |
| 2026-11-16 16:01 | ok | 2,000 | 1,974 | 30,000 |  |
| 2026-11-16 15:01 | ok | 2,000 | 1,784 | 30,000 |  |
| 2026-11-16 14:01 | ok | 2,000 | 1,631 | 30,000 |  |
| 2026-11-16 13:01 | ok | 2,000 | 1,513 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
