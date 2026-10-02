# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-02 19:01 UTC._

| | |
|---|---|
| Snapshots collected | **5** (11,549 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-02 19:01 UTC |
| Hours captured since the first snapshot | 5 of 10 (50%) |
| Creators in the tracking panel | 5,032 |
| Failed runs | 0 |

### Last 5 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-02 19:01 | ok | 2,000 | 440 | 5,032 |  |
| 2026-10-02 18:50 | ok | 2,000 | 405 | 4,930 |  |
| 2026-10-02 16:12 | ok | 2,000 | 406 | 3,997 |  |
| 2026-10-02 13:43 | ok | 2,000 | 298 | 3,108 |  |
| 2026-10-02 10:42 | ok | 2,000 | 0 | 2,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
