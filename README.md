# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-25 14:01 UTC._

| | |
|---|---|
| Snapshots collected | **561** (2,195,931 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-25 14:01 UTC |
| Hours captured since the first snapshot | 551 of 557 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-25 14:01 | ok | 2,000 | 1,801 | 30,000 |  |
| 2026-10-25 13:01 | ok | 2,000 | 1,629 | 30,000 |  |
| 2026-10-25 12:01 | ok | 2,000 | 1,474 | 30,000 |  |
| 2026-10-25 11:01 | ok | 2,000 | 1,390 | 30,000 |  |
| 2026-10-25 10:01 | ok | 2,000 | 1,328 | 30,000 |  |
| 2026-10-25 09:01 | ok | 2,000 | 1,316 | 30,000 |  |
| 2026-10-25 08:01 | ok | 2,000 | 1,282 | 30,000 |  |
| 2026-10-25 07:01 | ok | 2,000 | 1,330 | 30,000 |  |
| 2026-10-25 06:01 | ok | 2,000 | 1,501 | 30,000 |  |
| 2026-10-25 05:01 | ok | 2,000 | 1,673 | 30,000 |  |
| 2026-10-25 04:01 | ok | 2,000 | 1,816 | 30,000 |  |
| 2026-10-25 03:01 | ok | 2,000 | 1,951 | 30,000 |  |
| 2026-10-25 02:01 | ok | 2,000 | 2,010 | 30,000 |  |
| 2026-10-25 01:01 | ok | 2,000 | 2,111 | 30,000 |  |
| 2026-10-25 00:01 | ok | 2,000 | 2,161 | 30,000 |  |
| 2026-10-24 23:01 | ok | 2,000 | 2,232 | 30,000 |  |
| 2026-10-24 22:03 | ok | 2,000 | 2,495 | 30,000 |  |
| 2026-10-24 22:00 | ok | 2,000 | 2,467 | 30,000 |  |
| 2026-10-24 21:01 | ok | 2,000 | 2,591 | 30,000 |  |
| 2026-10-24 20:01 | ok | 2,000 | 2,608 | 30,000 |  |
| 2026-10-24 19:01 | ok | 2,000 | 2,578 | 30,000 |  |
| 2026-10-24 18:01 | ok | 2,000 | 2,509 | 30,000 |  |
| 2026-10-24 17:01 | ok | 2,000 | 2,350 | 30,000 |  |
| 2026-10-24 16:01 | ok | 2,000 | 2,245 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
