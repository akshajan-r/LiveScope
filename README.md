# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-20 03:01 UTC._

| | |
|---|---|
| Snapshots collected | **429** (1,658,407 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-20 03:01 UTC |
| Hours captured since the first snapshot | 420 of 426 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-20 03:01 | ok | 2,000 | 2,056 | 30,000 |  |
| 2026-10-20 02:01 | ok | 2,000 | 2,143 | 30,000 |  |
| 2026-10-20 01:01 | ok | 2,000 | 2,131 | 30,000 |  |
| 2026-10-20 00:01 | ok | 2,000 | 2,209 | 30,000 |  |
| 2026-10-19 23:01 | ok | 2,000 | 2,230 | 30,000 |  |
| 2026-10-19 22:01 | ok | 2,000 | 2,409 | 30,000 |  |
| 2026-10-19 21:01 | ok | 2,000 | 2,640 | 30,000 |  |
| 2026-10-19 20:01 | ok | 2,000 | 2,790 | 30,000 |  |
| 2026-10-19 19:01 | ok | 2,000 | 2,765 | 30,000 |  |
| 2026-10-19 18:01 | ok | 2,000 | 2,584 | 30,000 |  |
| 2026-10-19 17:01 | ok | 2,000 | 2,453 | 30,000 |  |
| 2026-10-19 16:01 | ok | 2,000 | 2,224 | 30,000 |  |
| 2026-10-19 15:01 | ok | 2,000 | 2,098 | 30,000 |  |
| 2026-10-19 14:01 | ok | 2,000 | 1,910 | 30,000 |  |
| 2026-10-19 13:01 | ok | 2,000 | 1,772 | 30,000 |  |
| 2026-10-19 12:01 | ok | 2,000 | 1,580 | 30,000 |  |
| 2026-10-19 11:01 | ok | 2,000 | 1,444 | 30,000 |  |
| 2026-10-19 10:01 | ok | 2,000 | 1,342 | 30,000 |  |
| 2026-10-19 09:01 | ok | 2,000 | 1,299 | 30,000 |  |
| 2026-10-19 08:01 | ok | 2,000 | 1,232 | 30,000 |  |
| 2026-10-19 07:01 | ok | 2,000 | 1,249 | 30,000 |  |
| 2026-10-19 06:01 | ok | 2,000 | 1,304 | 30,000 |  |
| 2026-10-19 05:01 | ok | 2,000 | 1,462 | 30,000 |  |
| 2026-10-19 04:01 | ok | 2,000 | 1,583 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
