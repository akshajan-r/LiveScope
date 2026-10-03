# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-03 12:01 UTC._

| | |
|---|---|
| Snapshots collected | **22** (52,297 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-03 12:01 UTC |
| Hours captured since the first snapshot | 22 of 27 (81%) |
| Creators in the tracking panel | 10,898 |
| Failed runs | 0 |

### Last 22 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-03 12:01 | ok | 2,000 | 703 | 10,898 |  |
| 2026-10-03 11:01 | ok | 2,000 | 603 | 10,704 |  |
| 2026-10-03 10:01 | ok | 2,000 | 545 | 10,489 |  |
| 2026-10-03 09:01 | ok | 2,000 | 503 | 10,234 |  |
| 2026-10-03 08:01 | ok | 2,000 | 417 | 9,954 |  |
| 2026-10-03 07:01 | ok | 2,000 | 356 | 9,691 |  |
| 2026-10-03 06:01 | ok | 2,000 | 313 | 9,384 |  |
| 2026-10-03 05:01 | ok | 2,000 | 304 | 9,043 |  |
| 2026-10-03 04:01 | ok | 2,000 | 312 | 8,674 |  |
| 2026-10-03 03:01 | ok | 2,000 | 305 | 8,300 |  |
| 2026-10-03 02:01 | ok | 2,000 | 317 | 7,896 |  |
| 2026-10-03 01:01 | ok | 2,000 | 300 | 7,499 |  |
| 2026-10-03 00:01 | ok | 2,000 | 293 | 7,039 |  |
| 2026-10-02 23:01 | ok | 2,000 | 320 | 6,622 |  |
| 2026-10-02 22:01 | ok | 2,000 | 342 | 6,224 |  |
| 2026-10-02 21:01 | ok | 2,000 | 374 | 5,820 |  |
| 2026-10-02 20:01 | ok | 2,000 | 441 | 5,409 |  |
| 2026-10-02 19:01 | ok | 2,000 | 440 | 5,032 |  |
| 2026-10-02 18:50 | ok | 2,000 | 405 | 4,930 |  |
| 2026-10-02 16:12 | ok | 2,000 | 406 | 3,997 |  |
| 2026-10-02 13:43 | ok | 2,000 | 298 | 3,108 |  |
| 2026-10-02 10:42 | ok | 2,000 | 0 | 2,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
