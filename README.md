# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-19 12:01 UTC._

| | |
|---|---|
| Snapshots collected | **414** (1,593,993 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-19 12:01 UTC |
| Hours captured since the first snapshot | 405 of 411 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-19 12:01 | ok | 2,000 | 1,580 | 30,000 |  |
| 2026-10-19 11:01 | ok | 2,000 | 1,444 | 30,000 |  |
| 2026-10-19 10:01 | ok | 2,000 | 1,342 | 30,000 |  |
| 2026-10-19 09:01 | ok | 2,000 | 1,299 | 30,000 |  |
| 2026-10-19 08:01 | ok | 2,000 | 1,232 | 30,000 |  |
| 2026-10-19 07:01 | ok | 2,000 | 1,249 | 30,000 |  |
| 2026-10-19 06:01 | ok | 2,000 | 1,304 | 30,000 |  |
| 2026-10-19 05:01 | ok | 2,000 | 1,462 | 30,000 |  |
| 2026-10-19 04:01 | ok | 2,000 | 1,583 | 30,000 |  |
| 2026-10-19 03:01 | ok | 2,000 | 1,683 | 30,000 |  |
| 2026-10-19 02:01 | ok | 2,000 | 1,812 | 30,000 |  |
| 2026-10-19 01:01 | ok | 2,000 | 1,898 | 30,000 |  |
| 2026-10-19 00:01 | ok | 2,000 | 1,944 | 30,000 |  |
| 2026-10-18 23:01 | ok | 2,000 | 2,059 | 30,000 |  |
| 2026-10-18 22:01 | ok | 2,000 | 2,253 | 30,000 |  |
| 2026-10-18 21:01 | ok | 2,000 | 2,432 | 30,000 |  |
| 2026-10-18 20:01 | ok | 2,000 | 2,640 | 30,000 |  |
| 2026-10-18 19:01 | ok | 2,000 | 2,624 | 30,000 |  |
| 2026-10-18 18:01 | ok | 2,000 | 2,592 | 30,000 |  |
| 2026-10-18 17:01 | ok | 2,000 | 2,406 | 30,000 |  |
| 2026-10-18 16:01 | ok | 2,000 | 2,269 | 30,000 |  |
| 2026-10-18 15:01 | ok | 2,000 | 2,117 | 30,000 |  |
| 2026-10-18 14:01 | ok | 2,000 | 2,015 | 30,000 |  |
| 2026-10-18 13:01 | ok | 2,000 | 1,866 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
