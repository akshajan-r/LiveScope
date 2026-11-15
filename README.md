# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-15 11:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,064** (4,229,531 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-15 11:01 UTC |
| Hours captured since the first snapshot | 1,052 of 1,058 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-15 11:01 | ok | 2,000 | 1,461 | 30,000 |  |
| 2026-11-15 10:01 | ok | 2,000 | 1,397 | 30,000 |  |
| 2026-11-15 09:01 | ok | 2,000 | 1,357 | 30,000 |  |
| 2026-11-15 08:01 | ok | 2,000 | 1,391 | 30,000 |  |
| 2026-11-15 07:01 | ok | 2,000 | 1,456 | 30,000 |  |
| 2026-11-15 06:01 | ok | 2,000 | 1,546 | 30,000 |  |
| 2026-11-15 05:01 | ok | 2,000 | 1,704 | 30,000 |  |
| 2026-11-15 04:01 | ok | 2,000 | 1,786 | 30,000 |  |
| 2026-11-15 03:01 | ok | 2,000 | 1,847 | 30,000 |  |
| 2026-11-15 02:01 | ok | 2,000 | 1,912 | 30,000 |  |
| 2026-11-15 01:01 | ok | 2,000 | 2,001 | 30,000 |  |
| 2026-11-15 00:01 | ok | 2,000 | 2,089 | 30,000 |  |
| 2026-11-14 23:01 | ok | 2,000 | 2,196 | 30,000 |  |
| 2026-11-14 22:01 | ok | 2,000 | 2,323 | 30,000 |  |
| 2026-11-14 21:01 | ok | 2,000 | 2,426 | 30,000 |  |
| 2026-11-14 20:01 | ok | 2,000 | 2,405 | 30,000 |  |
| 2026-11-14 19:01 | ok | 2,000 | 2,365 | 30,000 |  |
| 2026-11-14 18:01 | ok | 2,000 | 2,206 | 30,000 |  |
| 2026-11-14 17:01 | ok | 2,000 | 2,160 | 30,000 |  |
| 2026-11-14 16:01 | ok | 2,000 | 2,062 | 30,000 |  |
| 2026-11-14 15:01 | ok | 2,000 | 1,931 | 30,000 |  |
| 2026-11-14 14:01 | ok | 2,000 | 1,841 | 30,000 |  |
| 2026-11-14 13:01 | ok | 2,000 | 1,677 | 30,000 |  |
| 2026-11-14 12:01 | ok | 2,000 | 1,573 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
