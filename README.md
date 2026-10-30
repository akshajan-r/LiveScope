# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-30 00:01 UTC._

| | |
|---|---|
| Snapshots collected | **667** (2,622,509 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-30 00:01 UTC |
| Hours captured since the first snapshot | 657 of 663 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-30 00:01 | ok | 2,000 | 2,511 | 30,000 |  |
| 2026-10-29 23:01 | ok | 2,000 | 2,659 | 30,000 |  |
| 2026-10-29 22:01 | ok | 2,000 | 2,785 | 30,000 |  |
| 2026-10-29 21:01 | ok | 2,000 | 2,917 | 30,000 |  |
| 2026-10-29 20:01 | ok | 2,000 | 2,929 | 30,000 |  |
| 2026-10-29 19:01 | ok | 2,000 | 2,810 | 30,000 |  |
| 2026-10-29 18:01 | ok | 2,000 | 2,641 | 30,000 |  |
| 2026-10-29 17:01 | ok | 2,000 | 2,497 | 30,000 |  |
| 2026-10-29 16:01 | ok | 2,000 | 2,350 | 30,000 |  |
| 2026-10-29 15:01 | ok | 2,000 | 2,132 | 30,000 |  |
| 2026-10-29 14:01 | ok | 2,000 | 1,933 | 30,000 |  |
| 2026-10-29 13:01 | ok | 2,000 | 1,743 | 30,000 |  |
| 2026-10-29 12:01 | ok | 2,000 | 1,561 | 30,000 |  |
| 2026-10-29 11:01 | ok | 2,000 | 1,405 | 30,000 |  |
| 2026-10-29 10:01 | ok | 2,000 | 1,269 | 30,000 |  |
| 2026-10-29 09:01 | ok | 2,000 | 1,228 | 30,000 |  |
| 2026-10-29 08:01 | ok | 2,000 | 1,250 | 30,000 |  |
| 2026-10-29 07:01 | ok | 2,000 | 1,308 | 30,000 |  |
| 2026-10-29 06:01 | ok | 2,000 | 1,569 | 30,000 |  |
| 2026-10-29 05:01 | ok | 2,000 | 1,712 | 30,000 |  |
| 2026-10-29 04:01 | ok | 2,000 | 2,009 | 30,000 |  |
| 2026-10-29 03:01 | ok | 2,000 | 2,214 | 30,000 |  |
| 2026-10-29 02:01 | ok | 2,000 | 2,317 | 30,000 |  |
| 2026-10-29 01:01 | ok | 2,000 | 2,332 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
