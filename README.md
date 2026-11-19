# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-19 00:02 UTC._

| | |
|---|---|
| Snapshots collected | **1,149** (4,564,112 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-19 00:01 UTC |
| Hours captured since the first snapshot | 1,137 of 1,143 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-19 00:01 | ok | 2,000 | 2,780 | 30,000 |  |
| 2026-11-18 23:01 | ok | 2,000 | 2,847 | 30,000 |  |
| 2026-11-18 22:01 | ok | 2,000 | 2,794 | 30,000 |  |
| 2026-11-18 21:01 | ok | 2,000 | 2,856 | 30,000 |  |
| 2026-11-18 20:01 | ok | 2,000 | 2,859 | 30,000 |  |
| 2026-11-18 19:01 | ok | 2,000 | 2,836 | 30,000 |  |
| 2026-11-18 18:01 | ok | 2,000 | 2,785 | 30,000 |  |
| 2026-11-18 17:01 | ok | 2,000 | 2,590 | 30,000 |  |
| 2026-11-18 16:01 | ok | 2,000 | 2,451 | 30,000 |  |
| 2026-11-18 15:01 | ok | 2,000 | 2,330 | 30,000 |  |
| 2026-11-18 14:01 | ok | 2,000 | 2,192 | 30,000 |  |
| 2026-11-18 13:01 | ok | 2,000 | 2,101 | 30,000 |  |
| 2026-11-18 12:01 | ok | 2,000 | 1,875 | 30,000 |  |
| 2026-11-18 11:01 | ok | 2,000 | 1,819 | 30,000 |  |
| 2026-11-18 10:01 | ok | 2,000 | 1,425 | 30,000 |  |
| 2026-11-18 09:01 | ok | 2,000 | 1,305 | 30,000 |  |
| 2026-11-18 08:01 | ok | 2,000 | 1,340 | 30,000 |  |
| 2026-11-18 07:01 | ok | 2,000 | 1,478 | 30,000 |  |
| 2026-11-18 06:01 | ok | 2,000 | 1,594 | 30,000 |  |
| 2026-11-18 05:01 | ok | 2,000 | 1,752 | 30,000 |  |
| 2026-11-18 04:01 | ok | 2,000 | 1,895 | 30,000 |  |
| 2026-11-18 03:01 | ok | 2,000 | 2,036 | 30,000 |  |
| 2026-11-18 02:01 | ok | 2,000 | 2,069 | 30,000 |  |
| 2026-11-18 01:01 | ok | 2,000 | 2,054 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
