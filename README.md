# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-03 00:01 UTC._

| | |
|---|---|
| Snapshots collected | **10** (23,319 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-03 00:01 UTC |
| Hours captured since the first snapshot | 10 of 15 (67%) |
| Creators in the tracking panel | 7,039 |
| Failed runs | 0 |

### Last 10 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
