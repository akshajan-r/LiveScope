# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-08 13:01 UTC._

| | |
|---|---|
| Snapshots collected | **146** (478,047 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-08 13:01 UTC |
| Hours captured since the first snapshot | 142 of 148 (96%) |
| Creators in the tracking panel | 26,222 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-08 13:01 | ok | 2,000 | 1,934 | 26,222 |  |
| 2026-10-08 12:01 | ok | 2,000 | 1,782 | 26,162 |  |
| 2026-10-08 11:01 | ok | 2,000 | 1,605 | 26,088 |  |
| 2026-10-08 10:01 | ok | 2,000 | 1,469 | 26,025 |  |
| 2026-10-08 09:01 | ok | 2,000 | 1,437 | 25,947 |  |
| 2026-10-08 08:01 | ok | 2,000 | 1,289 | 25,864 |  |
| 2026-10-08 07:01 | ok | 2,000 | 1,273 | 25,771 |  |
| 2026-10-08 06:01 | ok | 2,000 | 1,369 | 25,683 |  |
| 2026-10-08 05:01 | ok | 2,000 | 1,536 | 25,587 |  |
| 2026-10-08 04:01 | ok | 2,000 | 1,764 | 25,513 |  |
| 2026-10-08 03:01 | ok | 2,000 | 1,912 | 25,417 |  |
| 2026-10-08 02:03 | ok | 2,000 | 2,015 | 25,337 |  |
| 2026-10-08 02:01 | ok | 2,000 | 2,015 | 25,326 |  |
| 2026-10-08 01:01 | ok | 2,000 | 2,011 | 25,236 |  |
| 2026-10-08 00:01 | ok | 2,000 | 2,069 | 25,149 |  |
| 2026-10-07 23:01 | ok | 2,000 | 2,105 | 25,064 |  |
| 2026-10-07 22:01 | ok | 2,000 | 2,254 | 24,982 |  |
| 2026-10-07 21:01 | ok | 2,000 | 2,454 | 24,900 |  |
| 2026-10-07 20:01 | ok | 2,000 | 2,634 | 24,824 |  |
| 2026-10-07 19:01 | ok | 2,000 | 2,677 | 24,745 |  |
| 2026-10-07 18:01 | ok | 2,000 | 2,660 | 24,695 |  |
| 2026-10-07 17:03 | ok | 2,000 | 2,513 | 24,633 |  |
| 2026-10-07 16:01 | ok | 2,000 | 2,280 | 24,553 |  |
| 2026-10-07 15:01 | ok | 2,000 | 2,173 | 24,508 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
