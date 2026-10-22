# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-22 14:01 UTC._

| | |
|---|---|
| Snapshots collected | **488** (1,895,214 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-22 14:01 UTC |
| Hours captured since the first snapshot | 479 of 485 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-22 14:01 | ok | 2,000 | 2,118 | 30,000 |  |
| 2026-10-22 13:01 | ok | 2,000 | 1,917 | 30,000 |  |
| 2026-10-22 12:01 | ok | 2,000 | 1,736 | 30,000 |  |
| 2026-10-22 11:01 | ok | 2,000 | 1,530 | 30,000 |  |
| 2026-10-22 10:01 | ok | 2,000 | 1,427 | 30,000 |  |
| 2026-10-22 09:01 | ok | 2,000 | 1,349 | 30,000 |  |
| 2026-10-22 08:01 | ok | 2,000 | 1,394 | 30,000 |  |
| 2026-10-22 07:01 | ok | 2,000 | 1,459 | 30,000 |  |
| 2026-10-22 06:01 | ok | 2,000 | 1,566 | 30,000 |  |
| 2026-10-22 05:01 | ok | 2,000 | 1,765 | 30,000 |  |
| 2026-10-22 04:01 | ok | 2,000 | 1,960 | 30,000 |  |
| 2026-10-22 03:01 | ok | 2,000 | 2,154 | 30,000 |  |
| 2026-10-22 02:01 | ok | 2,000 | 2,229 | 30,000 |  |
| 2026-10-22 01:01 | ok | 2,000 | 2,296 | 30,000 |  |
| 2026-10-22 00:01 | ok | 2,000 | 2,294 | 30,000 |  |
| 2026-10-21 23:01 | ok | 2,000 | 2,401 | 30,000 |  |
| 2026-10-21 22:01 | ok | 2,000 | 2,605 | 30,000 |  |
| 2026-10-21 21:01 | ok | 2,000 | 2,770 | 30,000 |  |
| 2026-10-21 20:01 | ok | 2,000 | 2,951 | 30,000 |  |
| 2026-10-21 19:01 | ok | 2,000 | 2,994 | 30,000 |  |
| 2026-10-21 18:01 | ok | 2,000 | 2,891 | 30,000 |  |
| 2026-10-21 17:01 | ok | 2,000 | 2,680 | 30,000 |  |
| 2026-10-21 16:01 | ok | 2,000 | 2,488 | 30,000 |  |
| 2026-10-21 15:01 | ok | 2,000 | 2,279 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
