# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-07 22:01 UTC._

| | |
|---|---|
| Snapshots collected | **130** (418,462 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-07 22:01 UTC |
| Hours captured since the first snapshot | 127 of 133 (95%) |
| Creators in the tracking panel | 24,982 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-10-07 04:01 | ok | 2,000 | 1,655 | 23,573 |  |
| 2026-10-07 03:01 | ok | 2,000 | 1,783 | 23,475 |  |
| 2026-10-07 02:01 | ok | 2,000 | 1,870 | 23,369 |  |
| 2026-10-07 01:01 | ok | 2,000 | 1,842 | 23,277 |  |
| 2026-10-07 00:01 | ok | 2,000 | 1,830 | 23,173 |  |
| 2026-10-06 23:01 | ok | 2,000 | 1,881 | 23,069 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
