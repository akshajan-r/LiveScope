# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-02 00:01 UTC._

| | |
|---|---|
| Snapshots collected | **740** (2,914,187 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-02 00:01 UTC |
| Hours captured since the first snapshot | 729 of 735 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-02 00:01 | ok | 2,000 | 1,875 | 30,000 |  |
| 2026-11-01 23:01 | ok | 2,000 | 1,995 | 30,000 |  |
| 2026-11-01 22:01 | ok | 2,000 | 2,165 | 30,000 |  |
| 2026-11-01 21:01 | ok | 2,000 | 2,315 | 30,000 |  |
| 2026-11-01 20:01 | ok | 2,000 | 2,302 | 30,000 |  |
| 2026-11-01 19:01 | ok | 2,000 | 2,131 | 30,000 |  |
| 2026-11-01 18:01 | ok | 2,000 | 2,048 | 30,000 |  |
| 2026-11-01 17:01 | ok | 2,000 | 1,989 | 30,000 |  |
| 2026-11-01 16:01 | ok | 2,000 | 1,876 | 30,000 |  |
| 2026-11-01 15:01 | ok | 2,000 | 1,765 | 30,000 |  |
| 2026-11-01 14:01 | ok | 2,000 | 1,639 | 30,000 |  |
| 2026-11-01 13:01 | ok | 2,000 | 1,535 | 30,000 |  |
| 2026-11-01 12:01 | ok | 2,000 | 1,407 | 30,000 |  |
| 2026-11-01 11:01 | ok | 2,000 | 1,340 | 30,000 |  |
| 2026-11-01 10:01 | ok | 2,000 | 1,234 | 30,000 |  |
| 2026-11-01 09:01 | ok | 2,000 | 1,188 | 30,000 |  |
| 2026-11-01 08:01 | ok | 2,000 | 1,181 | 30,000 |  |
| 2026-11-01 07:01 | ok | 2,000 | 1,313 | 30,000 |  |
| 2026-11-01 06:01 | ok | 2,000 | 1,451 | 30,000 |  |
| 2026-11-01 05:01 | ok | 2,000 | 1,647 | 30,000 |  |
| 2026-11-01 04:01 | ok | 2,000 | 1,823 | 30,000 |  |
| 2026-11-01 03:01 | ok | 2,000 | 1,930 | 30,000 |  |
| 2026-11-01 02:01 | ok | 2,000 | 2,054 | 30,000 |  |
| 2026-11-01 01:01 | ok | 2,000 | 2,153 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
