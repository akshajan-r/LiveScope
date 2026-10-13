# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-13 10:01 UTC._

| | |
|---|---|
| Snapshots collected | **266** (974,832 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-13 10:01 UTC |
| Hours captured since the first snapshot | 259 of 265 (98%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-13 10:01 | ok | 2,000 | 1,458 | 30,000 |  |
| 2026-10-13 09:01 | ok | 2,000 | 1,408 | 30,000 |  |
| 2026-10-13 08:01 | ok | 2,000 | 1,356 | 30,000 |  |
| 2026-10-13 07:01 | ok | 2,000 | 1,403 | 30,000 |  |
| 2026-10-13 06:01 | ok | 2,000 | 1,548 | 30,000 |  |
| 2026-10-13 05:01 | ok | 2,000 | 1,722 | 30,000 |  |
| 2026-10-13 04:01 | ok | 2,000 | 1,920 | 30,000 |  |
| 2026-10-13 03:01 | ok | 2,000 | 2,102 | 30,000 |  |
| 2026-10-13 02:01 | ok | 2,000 | 2,160 | 30,000 |  |
| 2026-10-13 01:01 | ok | 2,000 | 2,214 | 30,000 |  |
| 2026-10-13 00:01 | ok | 2,000 | 2,229 | 30,000 |  |
| 2026-10-12 23:01 | ok | 2,000 | 2,330 | 30,000 |  |
| 2026-10-12 22:01 | ok | 2,000 | 2,524 | 30,000 |  |
| 2026-10-12 21:01 | ok | 2,000 | 2,770 | 30,000 |  |
| 2026-10-12 20:01 | ok | 2,000 | 2,909 | 30,000 |  |
| 2026-10-12 19:01 | ok | 2,000 | 2,865 | 30,000 |  |
| 2026-10-12 18:01 | ok | 2,000 | 2,835 | 30,000 |  |
| 2026-10-12 17:01 | ok | 2,000 | 2,611 | 30,000 |  |
| 2026-10-12 16:01 | ok | 2,000 | 2,371 | 30,000 |  |
| 2026-10-12 15:01 | ok | 2,000 | 2,170 | 30,000 |  |
| 2026-10-12 14:01 | ok | 2,000 | 1,998 | 30,000 |  |
| 2026-10-12 13:01 | ok | 2,000 | 1,797 | 30,000 |  |
| 2026-10-12 12:01 | ok | 2,000 | 1,609 | 30,000 |  |
| 2026-10-12 11:01 | ok | 2,000 | 1,454 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
