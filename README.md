# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-21 00:01 UTC._

| | |
|---|---|
| Snapshots collected | **450** (1,743,962 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-21 00:01 UTC |
| Hours captured since the first snapshot | 441 of 447 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-21 00:01 | ok | 2,000 | 2,332 | 30,000 |  |
| 2026-10-20 23:01 | ok | 2,000 | 2,413 | 30,000 |  |
| 2026-10-20 22:01 | ok | 2,000 | 2,618 | 30,000 |  |
| 2026-10-20 21:01 | ok | 2,000 | 2,743 | 30,000 |  |
| 2026-10-20 20:01 | ok | 2,000 | 2,821 | 30,000 |  |
| 2026-10-20 19:01 | ok | 2,000 | 2,982 | 30,000 |  |
| 2026-10-20 18:01 | ok | 2,000 | 2,884 | 30,000 |  |
| 2026-10-20 17:01 | ok | 2,000 | 2,743 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
