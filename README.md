# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-02 09:02 UTC._

| | |
|---|---|
| Snapshots collected | **749** (2,945,642 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-02 09:01 UTC |
| Hours captured since the first snapshot | 738 of 744 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-02 09:01 | ok | 2,000 | 1,180 | 30,000 |  |
| 2026-11-02 08:01 | ok | 2,000 | 1,176 | 30,000 |  |
| 2026-11-02 07:01 | ok | 2,000 | 1,284 | 30,000 |  |
| 2026-11-02 06:01 | ok | 2,000 | 1,378 | 30,000 |  |
| 2026-11-02 05:01 | ok | 2,000 | 1,525 | 30,000 |  |
| 2026-11-02 04:01 | ok | 2,000 | 1,627 | 30,000 |  |
| 2026-11-02 03:01 | ok | 2,000 | 1,732 | 30,000 |  |
| 2026-11-02 02:01 | ok | 2,000 | 1,770 | 30,000 |  |
| 2026-11-02 01:01 | ok | 2,000 | 1,783 | 30,000 |  |
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

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
