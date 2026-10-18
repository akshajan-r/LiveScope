# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-18 09:01 UTC._

| | |
|---|---|
| Snapshots collected | **387** (1,489,972 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-18 09:01 UTC |
| Hours captured since the first snapshot | 378 of 384 (98%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-18 09:01 | ok | 2,000 | 1,479 | 30,000 |  |
| 2026-10-18 08:01 | ok | 2,000 | 1,476 | 30,000 |  |
| 2026-10-18 07:01 | ok | 2,000 | 1,531 | 30,000 |  |
| 2026-10-18 06:01 | ok | 2,000 | 1,630 | 30,000 |  |
| 2026-10-18 05:01 | ok | 2,000 | 1,766 | 30,000 |  |
| 2026-10-18 04:01 | ok | 2,000 | 1,875 | 30,000 |  |
| 2026-10-18 03:01 | ok | 2,000 | 2,005 | 30,000 |  |
| 2026-10-18 02:01 | ok | 2,000 | 2,039 | 30,000 |  |
| 2026-10-18 01:01 | ok | 2,000 | 2,079 | 30,000 |  |
| 2026-10-18 00:01 | ok | 2,000 | 2,191 | 30,000 |  |
| 2026-10-17 23:01 | ok | 2,000 | 2,318 | 30,000 |  |
| 2026-10-17 22:01 | ok | 2,000 | 2,526 | 30,000 |  |
| 2026-10-17 21:01 | ok | 2,000 | 2,702 | 30,000 |  |
| 2026-10-17 20:01 | ok | 2,000 | 2,776 | 30,000 |  |
| 2026-10-17 19:01 | ok | 2,000 | 2,719 | 30,000 |  |
| 2026-10-17 18:01 | ok | 2,000 | 2,677 | 30,000 |  |
| 2026-10-17 17:01 | ok | 2,000 | 2,501 | 30,000 |  |
| 2026-10-17 16:01 | ok | 2,000 | 2,334 | 30,000 |  |
| 2026-10-17 15:01 | ok | 2,000 | 2,196 | 30,000 |  |
| 2026-10-17 14:01 | ok | 2,000 | 2,081 | 30,000 |  |
| 2026-10-17 13:01 | ok | 2,000 | 1,897 | 30,000 |  |
| 2026-10-17 12:01 | ok | 2,000 | 1,743 | 30,000 |  |
| 2026-10-17 11:01 | ok | 2,000 | 1,717 | 30,000 |  |
| 2026-10-17 10:01 | ok | 2,000 | 1,663 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
