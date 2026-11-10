# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-10 00:02 UTC._

| | |
|---|---|
| Snapshots collected | **933** (3,706,058 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-10 00:01 UTC |
| Hours captured since the first snapshot | 921 of 927 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-10 00:01 | ok | 2,000 | 2,225 | 30,000 |  |
| 2026-11-09 23:01 | ok | 2,000 | 2,279 | 30,000 |  |
| 2026-11-09 22:01 | ok | 2,000 | 2,411 | 30,000 |  |
| 2026-11-09 21:01 | ok | 2,000 | 2,618 | 30,000 |  |
| 2026-11-09 20:01 | ok | 2,000 | 2,578 | 30,000 |  |
| 2026-11-09 19:01 | ok | 2,000 | 2,463 | 30,000 |  |
| 2026-11-09 18:01 | ok | 2,000 | 2,345 | 30,000 |  |
| 2026-11-09 17:01 | ok | 2,000 | 2,201 | 30,000 |  |
| 2026-11-09 16:01 | ok | 2,000 | 2,054 | 30,000 |  |
| 2026-11-09 15:01 | ok | 2,000 | 1,936 | 30,000 |  |
| 2026-11-09 14:01 | ok | 2,000 | 1,790 | 30,000 |  |
| 2026-11-09 13:01 | ok | 2,000 | 1,679 | 30,000 |  |
| 2026-11-09 12:01 | ok | 2,000 | 1,497 | 30,000 |  |
| 2026-11-09 11:01 | ok | 2,000 | 1,415 | 30,000 |  |
| 2026-11-09 10:01 | ok | 2,000 | 1,364 | 30,000 |  |
| 2026-11-09 09:01 | ok | 2,000 | 1,336 | 30,000 |  |
| 2026-11-09 08:01 | ok | 2,000 | 1,330 | 30,000 |  |
| 2026-11-09 07:01 | ok | 2,000 | 1,420 | 30,000 |  |
| 2026-11-09 06:01 | ok | 2,000 | 1,517 | 30,000 |  |
| 2026-11-09 05:01 | ok | 2,000 | 1,662 | 30,000 |  |
| 2026-11-09 04:01 | ok | 2,000 | 1,808 | 30,000 |  |
| 2026-11-09 03:01 | ok | 2,000 | 1,899 | 30,000 |  |
| 2026-11-09 02:01 | ok | 2,000 | 1,972 | 30,000 |  |
| 2026-11-09 01:01 | ok | 2,000 | 2,059 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
