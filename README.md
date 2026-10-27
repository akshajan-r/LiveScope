# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-27 00:01 UTC._

| | |
|---|---|
| Snapshots collected | **595** (2,331,958 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-27 00:01 UTC |
| Hours captured since the first snapshot | 585 of 591 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-27 00:01 | ok | 2,000 | 2,354 | 30,000 |  |
| 2026-10-26 23:01 | ok | 2,000 | 2,520 | 30,000 |  |
| 2026-10-26 22:01 | ok | 2,000 | 2,662 | 30,000 |  |
| 2026-10-26 21:01 | ok | 2,000 | 2,796 | 30,000 |  |
| 2026-10-26 20:01 | ok | 2,000 | 2,777 | 30,000 |  |
| 2026-10-26 19:01 | ok | 2,000 | 2,651 | 30,000 |  |
| 2026-10-26 18:01 | ok | 2,000 | 2,474 | 30,000 |  |
| 2026-10-26 17:01 | ok | 2,000 | 2,292 | 30,000 |  |
| 2026-10-26 16:01 | ok | 2,000 | 2,091 | 30,000 |  |
| 2026-10-26 15:01 | ok | 2,000 | 1,912 | 30,000 |  |
| 2026-10-26 14:01 | ok | 2,000 | 1,739 | 30,000 |  |
| 2026-10-26 13:01 | ok | 2,000 | 1,571 | 30,000 |  |
| 2026-10-26 12:01 | ok | 2,000 | 1,435 | 30,000 |  |
| 2026-10-26 11:01 | ok | 2,000 | 1,301 | 30,000 |  |
| 2026-10-26 10:01 | ok | 2,000 | 1,216 | 30,000 |  |
| 2026-10-26 09:01 | ok | 2,000 | 1,165 | 30,000 |  |
| 2026-10-26 08:01 | ok | 2,000 | 1,100 | 30,000 |  |
| 2026-10-26 07:01 | ok | 2,000 | 1,149 | 30,000 |  |
| 2026-10-26 06:01 | ok | 2,000 | 1,280 | 30,000 |  |
| 2026-10-26 05:01 | ok | 2,000 | 1,439 | 30,000 |  |
| 2026-10-26 04:01 | ok | 2,000 | 1,642 | 30,000 |  |
| 2026-10-26 03:01 | ok | 2,000 | 1,775 | 30,000 |  |
| 2026-10-26 02:01 | ok | 2,000 | 1,884 | 30,000 |  |
| 2026-10-26 01:01 | ok | 2,000 | 1,939 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
