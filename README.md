# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-07 08:01 UTC._

| | |
|---|---|
| Snapshots collected | **116** (361,387 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-07 08:01 UTC |
| Hours captured since the first snapshot | 113 of 119 (95%) |
| Creators in the tracking panel | 23,999 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-07 08:01 | ok | 2,000 | 1,100 | 23,999 |  |
| 2026-10-07 07:01 | ok | 2,000 | 1,153 | 23,914 |  |
| 2026-10-07 06:01 | ok | 2,000 | 1,271 | 23,804 |  |
| 2026-10-07 05:01 | ok | 2,000 | 1,472 | 23,686 |  |
| 2026-10-07 04:01 | ok | 2,000 | 1,655 | 23,573 |  |
| 2026-10-07 03:01 | ok | 2,000 | 1,783 | 23,475 |  |
| 2026-10-07 02:01 | ok | 2,000 | 1,870 | 23,369 |  |
| 2026-10-07 01:01 | ok | 2,000 | 1,842 | 23,277 |  |
| 2026-10-07 00:01 | ok | 2,000 | 1,830 | 23,173 |  |
| 2026-10-06 23:01 | ok | 2,000 | 1,881 | 23,069 |  |
| 2026-10-06 22:01 | ok | 2,000 | 2,123 | 22,952 |  |
| 2026-10-06 21:01 | ok | 2,000 | 2,275 | 22,874 |  |
| 2026-10-06 20:01 | ok | 2,000 | 2,453 | 22,796 |  |
| 2026-10-06 19:01 | ok | 2,000 | 2,568 | 22,706 |  |
| 2026-10-06 18:01 | ok | 2,000 | 2,556 | 22,635 |  |
| 2026-10-06 17:01 | ok | 2,000 | 2,326 | 22,558 |  |
| 2026-10-06 16:01 | ok | 2,000 | 2,053 | 22,472 |  |
| 2026-10-06 15:01 | ok | 2,000 | 1,865 | 22,393 |  |
| 2026-10-06 14:01 | ok | 2,000 | 1,678 | 22,300 |  |
| 2026-10-06 13:01 | ok | 2,000 | 1,504 | 22,205 |  |
| 2026-10-06 12:01 | ok | 2,000 | 1,369 | 22,117 |  |
| 2026-10-06 11:01 | ok | 2,000 | 1,173 | 22,005 |  |
| 2026-10-06 10:01 | ok | 2,000 | 1,118 | 21,909 |  |
| 2026-10-06 09:01 | ok | 2,000 | 1,057 | 21,801 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
