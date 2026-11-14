# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-14 19:01 UTC._

| | |
|---|---|
| Snapshots collected | **1,048** (4,168,234 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-14 19:01 UTC |
| Hours captured since the first snapshot | 1,036 of 1,042 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-14 19:01 | ok | 2,000 | 2,365 | 30,000 |  |
| 2026-11-14 18:01 | ok | 2,000 | 2,206 | 30,000 |  |
| 2026-11-14 17:01 | ok | 2,000 | 2,160 | 30,000 |  |
| 2026-11-14 16:01 | ok | 2,000 | 2,062 | 30,000 |  |
| 2026-11-14 15:01 | ok | 2,000 | 1,931 | 30,000 |  |
| 2026-11-14 14:01 | ok | 2,000 | 1,841 | 30,000 |  |
| 2026-11-14 13:01 | ok | 2,000 | 1,677 | 30,000 |  |
| 2026-11-14 12:01 | ok | 2,000 | 1,573 | 30,000 |  |
| 2026-11-14 11:01 | ok | 2,000 | 1,503 | 30,000 |  |
| 2026-11-14 10:01 | ok | 2,000 | 1,434 | 30,000 |  |
| 2026-11-14 09:01 | ok | 2,000 | 1,440 | 30,000 |  |
| 2026-11-14 08:01 | ok | 2,000 | 1,522 | 30,000 |  |
| 2026-11-14 07:01 | ok | 2,000 | 1,659 | 30,000 |  |
| 2026-11-14 06:01 | ok | 2,000 | 1,853 | 30,000 |  |
| 2026-11-14 05:01 | ok | 2,000 | 2,029 | 30,000 |  |
| 2026-11-14 04:01 | ok | 2,000 | 2,207 | 30,000 |  |
| 2026-11-14 03:01 | ok | 2,000 | 2,325 | 30,000 |  |
| 2026-11-14 02:01 | ok | 2,000 | 2,399 | 30,000 |  |
| 2026-11-14 01:01 | ok | 2,000 | 2,453 | 30,000 |  |
| 2026-11-14 00:01 | ok | 2,000 | 2,499 | 30,000 |  |
| 2026-11-13 23:01 | ok | 2,000 | 2,658 | 30,000 |  |
| 2026-11-13 22:01 | ok | 2,000 | 2,769 | 30,000 |  |
| 2026-11-13 21:01 | ok | 2,000 | 2,854 | 30,000 |  |
| 2026-11-13 20:01 | ok | 2,000 | 2,825 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
