# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-21 21:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,218** (4,871,330 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-21 21:01 UTC |
| Hours captured since the first snapshot | 1,206 of 1,212 (100%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-21 21:01 | ok | 2,000 | 2,824 | 30,000 |  |
| 2026-11-21 20:01 | ok | 2,000 | 2,740 | 30,000 |  |
| 2026-11-21 19:01 | ok | 2,000 | 2,681 | 30,000 |  |
| 2026-11-21 18:01 | ok | 2,000 | 2,533 | 30,000 |  |
| 2026-11-21 17:01 | ok | 2,000 | 2,440 | 30,000 |  |
| 2026-11-21 16:01 | ok | 2,000 | 2,319 | 30,000 |  |
| 2026-11-21 15:01 | ok | 2,000 | 2,238 | 30,000 |  |
| 2026-11-21 14:01 | ok | 2,000 | 2,173 | 30,000 |  |
| 2026-11-21 13:01 | ok | 2,000 | 1,962 | 30,000 |  |
| 2026-11-21 12:01 | ok | 2,000 | 1,825 | 30,000 |  |
| 2026-11-21 11:01 | ok | 2,000 | 1,767 | 30,000 |  |
| 2026-11-21 10:01 | ok | 2,000 | 1,627 | 30,000 |  |
| 2026-11-21 09:01 | ok | 2,000 | 1,649 | 30,000 |  |
| 2026-11-21 08:01 | ok | 2,000 | 1,736 | 30,000 |  |
| 2026-11-21 07:01 | ok | 2,000 | 1,884 | 30,000 |  |
| 2026-11-21 06:01 | ok | 2,000 | 2,120 | 30,000 |  |
| 2026-11-21 05:01 | ok | 2,000 | 2,292 | 30,000 |  |
| 2026-11-21 04:01 | ok | 2,000 | 2,501 | 30,000 |  |
| 2026-11-21 03:01 | ok | 2,000 | 2,572 | 30,000 |  |
| 2026-11-21 02:01 | ok | 2,000 | 2,649 | 30,000 |  |
| 2026-11-21 01:01 | ok | 2,000 | 2,665 | 30,000 |  |
| 2026-11-21 00:01 | ok | 2,000 | 2,806 | 30,000 |  |
| 2026-11-20 23:01 | ok | 2,000 | 2,901 | 30,000 |  |
| 2026-11-20 22:01 | ok | 2,000 | 3,099 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
