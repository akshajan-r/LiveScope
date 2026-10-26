# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-26 01:01 UTC._

| | |
|---|---|
| Snapshots collected | **572** (2,242,733 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-26 01:01 UTC |
| Hours captured since the first snapshot | 562 of 568 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-26 01:01 | ok | 2,000 | 1,939 | 30,000 |  |
| 2026-10-26 00:01 | ok | 2,000 | 2,032 | 30,000 |  |
| 2026-10-25 23:01 | ok | 2,000 | 2,196 | 30,000 |  |
| 2026-10-25 22:01 | ok | 2,000 | 2,299 | 30,000 |  |
| 2026-10-25 21:01 | ok | 2,000 | 2,460 | 30,000 |  |
| 2026-10-25 20:01 | ok | 2,000 | 2,546 | 30,000 |  |
| 2026-10-25 19:01 | ok | 2,000 | 2,511 | 30,000 |  |
| 2026-10-25 18:01 | ok | 2,000 | 2,431 | 30,000 |  |
| 2026-10-25 17:01 | ok | 2,000 | 2,306 | 30,000 |  |
| 2026-10-25 16:01 | ok | 2,000 | 2,125 | 30,000 |  |
| 2026-10-25 15:01 | ok | 2,000 | 1,957 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
