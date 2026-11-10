# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-10 19:01 UTC._

| | |
|---|---|
| Snapshots collected | **952** (3,779,586 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-10 19:01 UTC |
| Hours captured since the first snapshot | 940 of 946 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-10 19:01 | ok | 2,000 | 2,575 | 30,000 |  |
| 2026-11-10 18:01 | ok | 2,000 | 2,479 | 30,000 |  |
| 2026-11-10 17:01 | ok | 2,000 | 2,274 | 30,000 |  |
| 2026-11-10 16:01 | ok | 2,000 | 2,134 | 30,000 |  |
| 2026-11-10 15:01 | ok | 2,000 | 2,033 | 30,000 |  |
| 2026-11-10 14:01 | ok | 2,000 | 1,849 | 30,000 |  |
| 2026-11-10 13:01 | ok | 2,000 | 1,723 | 30,000 |  |
| 2026-11-10 12:01 | ok | 2,000 | 1,546 | 30,000 |  |
| 2026-11-10 11:01 | ok | 2,000 | 1,446 | 30,000 |  |
| 2026-11-10 10:01 | ok | 2,000 | 1,374 | 30,000 |  |
| 2026-11-10 09:01 | ok | 2,000 | 1,354 | 30,000 |  |
| 2026-11-10 08:01 | ok | 2,000 | 1,367 | 30,000 |  |
| 2026-11-10 07:01 | ok | 2,000 | 1,471 | 30,000 |  |
| 2026-11-10 06:01 | ok | 2,000 | 1,658 | 30,000 |  |
| 2026-11-10 05:01 | ok | 2,000 | 1,841 | 30,000 |  |
| 2026-11-10 04:01 | ok | 2,000 | 2,013 | 30,000 |  |
| 2026-11-10 03:01 | ok | 2,000 | 2,094 | 30,000 |  |
| 2026-11-10 02:01 | ok | 2,000 | 2,121 | 30,000 |  |
| 2026-11-10 01:01 | ok | 2,000 | 2,176 | 30,000 |  |
| 2026-11-10 00:01 | ok | 2,000 | 2,225 | 30,000 |  |
| 2026-11-09 23:01 | ok | 2,000 | 2,279 | 30,000 |  |
| 2026-11-09 22:01 | ok | 2,000 | 2,411 | 30,000 |  |
| 2026-11-09 21:01 | ok | 2,000 | 2,618 | 30,000 |  |
| 2026-11-09 20:01 | ok | 2,000 | 2,578 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
