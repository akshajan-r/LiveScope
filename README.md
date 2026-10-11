# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-11 20:01 UTC._

| | |
|---|---|
| Snapshots collected | **228** (824,454 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-11 20:01 UTC |
| Hours captured since the first snapshot | 221 of 227 (97%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-10-11 08:01 | ok | 2,000 | 1,480 | 30,000 |  |
| 2026-10-11 07:01 | ok | 2,000 | 1,545 | 30,000 |  |
| 2026-10-11 06:01 | ok | 2,000 | 1,626 | 30,000 |  |
| 2026-10-11 05:01 | ok | 2,000 | 1,828 | 30,000 |  |
| 2026-10-11 04:01 | ok | 2,000 | 1,924 | 30,000 |  |
| 2026-10-11 03:01 | ok | 2,000 | 2,081 | 30,000 |  |
| 2026-10-11 02:01 | ok | 2,000 | 2,149 | 30,000 |  |
| 2026-10-11 01:01 | ok | 2,000 | 2,227 | 30,000 |  |
| 2026-10-11 00:01 | ok | 2,000 | 2,274 | 30,000 |  |
| 2026-10-10 23:01 | ok | 2,000 | 2,418 | 30,000 |  |
| 2026-10-10 22:01 | ok | 2,000 | 2,637 | 29,954 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
