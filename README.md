# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-10 02:01 UTC._

| | |
|---|---|
| Snapshots collected | **184** (642,698 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-10 02:01 UTC |
| Hours captured since the first snapshot | 179 of 185 (97%) |
| Creators in the tracking panel | 28,617 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-10 02:01 | ok | 2,000 | 2,469 | 28,617 |  |
| 2026-10-10 01:01 | ok | 2,000 | 2,511 | 28,543 |  |
| 2026-10-10 00:01 | ok | 2,000 | 2,542 | 28,471 |  |
| 2026-10-09 23:01 | ok | 2,000 | 2,604 | 28,384 |  |
| 2026-10-09 22:01 | ok | 2,000 | 2,821 | 28,331 |  |
| 2026-10-09 21:01 | ok | 2,000 | 2,984 | 28,274 |  |
| 2026-10-09 20:01 | ok | 2,000 | 3,097 | 28,220 |  |
| 2026-10-09 19:01 | ok | 2,000 | 3,068 | 28,163 |  |
| 2026-10-09 18:01 | ok | 2,000 | 2,974 | 28,113 |  |
| 2026-10-09 17:01 | ok | 2,000 | 2,845 | 28,056 |  |
| 2026-10-09 16:01 | ok | 2,000 | 2,585 | 28,007 |  |
| 2026-10-09 15:01 | ok | 2,000 | 2,404 | 27,950 |  |
| 2026-10-09 14:01 | ok | 2,000 | 2,295 | 27,899 |  |
| 2026-10-09 13:01 | ok | 2,000 | 2,068 | 27,851 |  |
| 2026-10-09 12:01 | ok | 2,000 | 1,875 | 27,800 |  |
| 2026-10-09 11:01 | ok | 2,000 | 1,664 | 27,744 |  |
| 2026-10-09 10:01 | ok | 2,000 | 1,571 | 27,684 |  |
| 2026-10-09 09:01 | ok | 2,000 | 1,466 | 27,621 |  |
| 2026-10-09 08:01 | ok | 2,000 | 1,390 | 27,551 |  |
| 2026-10-09 07:01 | ok | 2,000 | 1,379 | 27,464 |  |
| 2026-10-09 06:01 | ok | 2,000 | 1,505 | 27,373 |  |
| 2026-10-09 05:01 | ok | 2,000 | 1,685 | 27,286 |  |
| 2026-10-09 04:01 | ok | 2,000 | 1,891 | 27,193 |  |
| 2026-10-09 03:01 | ok | 2,000 | 2,101 | 27,127 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
