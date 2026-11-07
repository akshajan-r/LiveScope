# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-07 01:01 UTC._

| | |
|---|---|
| Snapshots collected | **862** (3,417,566 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-07 01:01 UTC |
| Hours captured since the first snapshot | 850 of 856 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-07 01:01 | ok | 2,000 | 2,775 | 30,000 |  |
| 2026-11-07 00:01 | ok | 2,000 | 2,817 | 30,000 |  |
| 2026-11-06 23:01 | ok | 2,000 | 2,860 | 30,000 |  |
| 2026-11-06 22:01 | ok | 2,000 | 2,990 | 30,000 |  |
| 2026-11-06 21:01 | ok | 2,000 | 3,110 | 30,000 |  |
| 2026-11-06 20:01 | ok | 2,000 | 3,105 | 30,000 |  |
| 2026-11-06 19:01 | ok | 2,000 | 2,992 | 30,000 |  |
| 2026-11-06 18:01 | ok | 2,000 | 2,856 | 30,000 |  |
| 2026-11-06 17:01 | ok | 2,000 | 2,679 | 30,000 |  |
| 2026-11-06 16:01 | ok | 2,000 | 2,582 | 30,000 |  |
| 2026-11-06 15:01 | ok | 2,000 | 2,394 | 30,000 |  |
| 2026-11-06 14:01 | ok | 2,000 | 2,243 | 30,000 |  |
| 2026-11-06 13:01 | ok | 2,000 | 2,049 | 30,000 |  |
| 2026-11-06 12:01 | ok | 2,000 | 1,932 | 30,000 |  |
| 2026-11-06 11:01 | ok | 2,000 | 1,846 | 30,000 |  |
| 2026-11-06 10:01 | ok | 2,000 | 1,729 | 30,000 |  |
| 2026-11-06 09:01 | ok | 2,000 | 1,712 | 30,000 |  |
| 2026-11-06 08:01 | ok | 2,000 | 1,773 | 30,000 |  |
| 2026-11-06 07:04 | ok | 2,000 | 1,891 | 30,000 |  |
| 2026-11-06 07:01 | ok | 2,000 | 1,871 | 30,000 |  |
| 2026-11-06 06:01 | ok | 2,000 | 2,058 | 30,000 |  |
| 2026-11-06 05:01 | ok | 2,000 | 2,231 | 30,000 |  |
| 2026-11-06 04:01 | ok | 2,000 | 2,332 | 30,000 |  |
| 2026-11-06 03:01 | ok | 2,000 | 2,423 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
