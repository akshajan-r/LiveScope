# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-03 06:01 UTC._

| | |
|---|---|
| Snapshots collected | **770** (3,027,596 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-03 06:01 UTC |
| Hours captured since the first snapshot | 759 of 765 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-03 06:01 | ok | 2,000 | 1,450 | 30,000 |  |
| 2026-11-03 05:01 | ok | 2,000 | 1,625 | 30,000 |  |
| 2026-11-03 04:01 | ok | 2,000 | 1,811 | 30,000 |  |
| 2026-11-03 03:01 | ok | 2,000 | 1,910 | 30,000 |  |
| 2026-11-03 02:01 | ok | 2,000 | 1,928 | 30,000 |  |
| 2026-11-03 01:01 | ok | 2,000 | 2,041 | 30,000 |  |
| 2026-11-03 00:01 | ok | 2,000 | 2,103 | 30,000 |  |
| 2026-11-02 23:01 | ok | 2,000 | 2,278 | 30,000 |  |
| 2026-11-02 22:01 | ok | 2,000 | 2,401 | 30,000 |  |
| 2026-11-02 21:01 | ok | 2,000 | 2,551 | 30,000 |  |
| 2026-11-02 20:01 | ok | 2,000 | 2,511 | 30,000 |  |
| 2026-11-02 19:01 | ok | 2,000 | 2,400 | 30,000 |  |
| 2026-11-02 18:01 | ok | 2,000 | 2,289 | 30,000 |  |
| 2026-11-02 17:01 | ok | 2,000 | 2,105 | 30,000 |  |
| 2026-11-02 16:01 | ok | 2,000 | 1,915 | 30,000 |  |
| 2026-11-02 15:01 | ok | 2,000 | 1,752 | 30,000 |  |
| 2026-11-02 14:01 | ok | 2,000 | 1,606 | 30,000 |  |
| 2026-11-02 13:01 | ok | 2,000 | 1,455 | 30,000 |  |
| 2026-11-02 12:01 | ok | 2,000 | 1,360 | 30,000 |  |
| 2026-11-02 11:01 | ok | 2,000 | 1,272 | 30,000 |  |
| 2026-11-02 10:01 | ok | 2,000 | 1,191 | 30,000 |  |
| 2026-11-02 09:01 | ok | 2,000 | 1,180 | 30,000 |  |
| 2026-11-02 08:01 | ok | 2,000 | 1,176 | 30,000 |  |
| 2026-11-02 07:01 | ok | 2,000 | 1,284 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
