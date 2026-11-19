# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-19 23:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,172** (4,669,904 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-19 23:01 UTC |
| Hours captured since the first snapshot | 1,160 of 1,166 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-19 23:01 | ok | 2,000 | 2,891 | 30,000 |  |
| 2026-11-19 22:01 | ok | 2,000 | 3,113 | 30,000 |  |
| 2026-11-19 21:01 | ok | 2,000 | 3,284 | 30,000 |  |
| 2026-11-19 20:01 | ok | 2,000 | 3,287 | 30,000 |  |
| 2026-11-19 19:01 | ok | 2,000 | 3,183 | 30,000 |  |
| 2026-11-19 18:01 | ok | 2,000 | 3,134 | 30,000 |  |
| 2026-11-19 17:01 | ok | 2,000 | 2,996 | 30,000 |  |
| 2026-11-19 16:01 | ok | 2,000 | 2,856 | 30,000 |  |
| 2026-11-19 15:01 | ok | 2,000 | 2,639 | 30,000 |  |
| 2026-11-19 14:01 | ok | 2,000 | 2,449 | 30,000 |  |
| 2026-11-19 13:01 | ok | 2,000 | 2,301 | 30,000 |  |
| 2026-11-19 12:01 | ok | 2,000 | 2,138 | 30,000 |  |
| 2026-11-19 11:01 | ok | 2,000 | 2,042 | 30,000 |  |
| 2026-11-19 10:01 | ok | 2,000 | 1,980 | 30,000 |  |
| 2026-11-19 09:01 | ok | 2,000 | 2,031 | 30,000 |  |
| 2026-11-19 08:01 | ok | 2,000 | 2,076 | 30,000 |  |
| 2026-11-19 07:01 | ok | 2,000 | 2,208 | 30,000 |  |
| 2026-11-19 06:01 | ok | 2,000 | 2,386 | 30,000 |  |
| 2026-11-19 05:01 | ok | 2,000 | 2,450 | 30,000 |  |
| 2026-11-19 04:01 | ok | 2,000 | 2,445 | 30,000 |  |
| 2026-11-19 03:01 | ok | 2,000 | 2,571 | 30,000 |  |
| 2026-11-19 02:01 | ok | 2,000 | 2,627 | 30,000 |  |
| 2026-11-19 01:01 | ok | 2,000 | 2,705 | 30,000 |  |
| 2026-11-19 00:01 | ok | 2,000 | 2,780 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
