# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-06 08:01 UTC._

| | |
|---|---|
| Snapshots collected | **845** (3,340,895 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-06 08:01 UTC |
| Hours captured since the first snapshot | 833 of 839 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-06 08:01 | ok | 2,000 | 1,773 | 30,000 |  |
| 2026-11-06 07:04 | ok | 2,000 | 1,891 | 30,000 |  |
| 2026-11-06 07:01 | ok | 2,000 | 1,871 | 30,000 |  |
| 2026-11-06 06:01 | ok | 2,000 | 2,058 | 30,000 |  |
| 2026-11-06 05:01 | ok | 2,000 | 2,231 | 30,000 |  |
| 2026-11-06 04:01 | ok | 2,000 | 2,332 | 30,000 |  |
| 2026-11-06 03:01 | ok | 2,000 | 2,423 | 30,000 |  |
| 2026-11-06 02:01 | ok | 2,000 | 2,452 | 30,000 |  |
| 2026-11-06 01:01 | ok | 2,000 | 2,494 | 30,000 |  |
| 2026-11-06 00:01 | ok | 2,000 | 2,603 | 30,000 |  |
| 2026-11-05 23:01 | ok | 2,000 | 2,725 | 30,000 |  |
| 2026-11-05 22:01 | ok | 2,000 | 2,957 | 30,000 |  |
| 2026-11-05 21:01 | ok | 2,000 | 3,061 | 30,000 |  |
| 2026-11-05 20:01 | ok | 2,000 | 3,040 | 30,000 |  |
| 2026-11-05 19:01 | ok | 2,000 | 2,995 | 30,000 |  |
| 2026-11-05 18:01 | ok | 2,000 | 2,904 | 30,000 |  |
| 2026-11-05 17:01 | ok | 2,000 | 2,727 | 30,000 |  |
| 2026-11-05 16:01 | ok | 2,000 | 2,510 | 30,000 |  |
| 2026-11-05 15:01 | ok | 2,000 | 2,367 | 30,000 |  |
| 2026-11-05 14:01 | ok | 2,000 | 2,256 | 30,000 |  |
| 2026-11-05 13:01 | ok | 2,000 | 2,066 | 30,000 |  |
| 2026-11-05 12:01 | ok | 2,000 | 1,900 | 30,000 |  |
| 2026-11-05 11:01 | ok | 2,000 | 1,826 | 30,000 |  |
| 2026-11-05 10:01 | ok | 2,000 | 1,751 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
