# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-20 16:01 UTC._

| | |
|---|---|
| Snapshots collected | **442** (1,706,426 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-20 16:01 UTC |
| Hours captured since the first snapshot | 433 of 439 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-20 16:01 | ok | 2,000 | 2,541 | 30,000 |  |
| 2026-10-20 15:01 | ok | 2,000 | 2,297 | 30,000 |  |
| 2026-10-20 14:01 | ok | 2,000 | 2,037 | 30,000 |  |
| 2026-10-20 13:01 | ok | 2,000 | 1,818 | 30,000 |  |
| 2026-10-20 12:01 | ok | 2,000 | 1,582 | 30,000 |  |
| 2026-10-20 11:01 | ok | 2,000 | 1,470 | 30,000 |  |
| 2026-10-20 10:01 | ok | 2,000 | 1,394 | 30,000 |  |
| 2026-10-20 09:01 | ok | 2,000 | 1,304 | 30,000 |  |
| 2026-10-20 08:01 | ok | 2,000 | 1,306 | 30,000 |  |
| 2026-10-20 07:01 | ok | 2,000 | 1,342 | 30,000 |  |
| 2026-10-20 06:01 | ok | 2,000 | 1,455 | 30,000 |  |
| 2026-10-20 05:01 | ok | 2,000 | 1,619 | 30,000 |  |
| 2026-10-20 04:01 | ok | 2,000 | 1,854 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
