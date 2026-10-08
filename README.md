# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-08 03:01 UTC._

| | |
|---|---|
| Snapshots collected | **136** (442,589 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-08 03:01 UTC |
| Hours captured since the first snapshot | 132 of 138 (96%) |
| Creators in the tracking panel | 25,417 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-10-07 14:01 | ok | 2,000 | 1,961 | 24,438 |  |
| 2026-10-07 13:01 | ok | 2,000 | 1,794 | 24,378 |  |
| 2026-10-07 12:01 | ok | 2,000 | 1,654 | 24,311 |  |
| 2026-10-07 11:01 | ok | 2,000 | 1,469 | 24,247 |  |
| 2026-10-07 10:01 | ok | 2,000 | 1,350 | 24,170 |  |
| 2026-10-07 09:01 | ok | 2,000 | 1,202 | 24,090 |  |
| 2026-10-07 08:01 | ok | 2,000 | 1,100 | 23,999 |  |
| 2026-10-07 07:01 | ok | 2,000 | 1,153 | 23,914 |  |
| 2026-10-07 06:01 | ok | 2,000 | 1,271 | 23,804 |  |
| 2026-10-07 05:01 | ok | 2,000 | 1,472 | 23,686 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
