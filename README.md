# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-27 15:02 UTC._

| | |
|---|---|
| Snapshots collected | **610** (2,386,551 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-27 15:01 UTC |
| Hours captured since the first snapshot | 600 of 606 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-27 15:01 | ok | 2,000 | 2,009 | 30,000 |  |
| 2026-10-27 14:01 | ok | 2,000 | 1,820 | 30,000 |  |
| 2026-10-27 13:01 | ok | 2,000 | 1,673 | 30,000 |  |
| 2026-10-27 12:01 | ok | 2,000 | 1,469 | 30,000 |  |
| 2026-10-27 11:01 | ok | 2,000 | 1,325 | 30,000 |  |
| 2026-10-27 10:01 | ok | 2,000 | 1,227 | 30,000 |  |
| 2026-10-27 09:01 | ok | 2,000 | 1,159 | 30,000 |  |
| 2026-10-27 08:01 | ok | 2,000 | 1,153 | 30,000 |  |
| 2026-10-27 07:01 | ok | 2,000 | 1,181 | 30,000 |  |
| 2026-10-27 06:01 | ok | 2,000 | 1,391 | 30,000 |  |
| 2026-10-27 05:01 | ok | 2,000 | 1,631 | 30,000 |  |
| 2026-10-27 04:01 | ok | 2,000 | 1,914 | 30,000 |  |
| 2026-10-27 03:01 | ok | 2,000 | 2,100 | 30,000 |  |
| 2026-10-27 02:01 | ok | 2,000 | 2,247 | 30,000 |  |
| 2026-10-27 01:01 | ok | 2,000 | 2,294 | 30,000 |  |
| 2026-10-27 00:01 | ok | 2,000 | 2,354 | 30,000 |  |
| 2026-10-26 23:01 | ok | 2,000 | 2,520 | 30,000 |  |
| 2026-10-26 22:01 | ok | 2,000 | 2,662 | 30,000 |  |
| 2026-10-26 21:01 | ok | 2,000 | 2,796 | 30,000 |  |
| 2026-10-26 20:01 | ok | 2,000 | 2,777 | 30,000 |  |
| 2026-10-26 19:01 | ok | 2,000 | 2,651 | 30,000 |  |
| 2026-10-26 18:01 | ok | 2,000 | 2,474 | 30,000 |  |
| 2026-10-26 17:01 | ok | 2,000 | 2,292 | 30,000 |  |
| 2026-10-26 16:01 | ok | 2,000 | 2,091 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
