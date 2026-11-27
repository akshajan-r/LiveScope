# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-27 19:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,361** (5,432,880 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-27 19:01 UTC |
| Hours captured since the first snapshot | 1,347 of 1,354 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-27 19:01 | ok | 2,000 | 2,504 | 30,000 |  |
| 2026-11-27 18:01 | ok | 2,000 | 2,385 | 30,000 |  |
| 2026-11-27 17:01 | ok | 2,000 | 2,241 | 30,000 |  |
| 2026-11-27 16:01 | ok | 2,000 | 2,086 | 30,000 |  |
| 2026-11-27 15:01 | ok | 2,000 | 1,917 | 30,000 |  |
| 2026-11-27 14:01 | ok | 2,000 | 1,772 | 30,000 |  |
| 2026-11-27 13:01 | ok | 2,000 | 1,657 | 30,000 |  |
| 2026-11-27 12:01 | ok | 2,000 | 1,478 | 30,000 |  |
| 2026-11-27 11:01 | ok | 2,000 | 1,364 | 30,000 |  |
| 2026-11-27 10:01 | ok | 2,000 | 1,259 | 30,000 |  |
| 2026-11-27 09:01 | ok | 2,000 | 1,163 | 30,000 |  |
| 2026-11-27 08:01 | ok | 2,000 | 1,165 | 30,000 |  |
| 2026-11-27 07:01 | ok | 2,000 | 1,222 | 30,000 |  |
| 2026-11-27 06:01 | ok | 2,000 | 1,258 | 30,000 |  |
| 2026-11-27 05:01 | ok | 2,000 | 1,296 | 30,000 |  |
| 2026-11-27 04:01 | ok | 2,000 | 1,346 | 30,000 |  |
| 2026-11-27 03:01 | ok | 2,000 | 1,376 | 30,000 |  |
| 2026-11-27 02:01 | ok | 2,000 | 1,466 | 30,000 |  |
| 2026-11-27 01:01 | ok | 2,000 | 1,515 | 30,000 |  |
| 2026-11-27 00:01 | ok | 2,000 | 1,609 | 30,000 |  |
| 2026-11-26 23:01 | ok | 2,000 | 1,800 | 30,000 |  |
| 2026-11-26 22:01 | ok | 2,000 | 2,020 | 30,000 |  |
| 2026-11-26 21:01 | ok | 2,000 | 2,282 | 30,000 |  |
| 2026-11-26 20:01 | ok | 2,000 | 2,346 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
