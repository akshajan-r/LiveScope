# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-06 08:01 UTC._

| | |
|---|---|
| Snapshots collected | **92** (271,412 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-06 08:01 UTC |
| Hours captured since the first snapshot | 89 of 95 (94%) |
| Creators in the tracking panel | 21,702 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-06 08:01 | ok | 2,000 | 1,007 | 21,702 |  |
| 2026-10-06 07:01 | ok | 2,000 | 1,071 | 21,586 |  |
| 2026-10-06 06:01 | ok | 2,000 | 1,081 | 21,454 |  |
| 2026-10-06 05:01 | ok | 2,000 | 1,215 | 21,325 |  |
| 2026-10-06 04:01 | ok | 2,000 | 1,403 | 21,190 |  |
| 2026-10-06 03:01 | ok | 2,000 | 1,500 | 21,061 |  |
| 2026-10-06 02:01 | ok | 2,000 | 1,562 | 20,918 |  |
| 2026-10-06 01:01 | ok | 2,000 | 1,571 | 20,790 |  |
| 2026-10-06 00:01 | ok | 2,000 | 1,570 | 20,659 |  |
| 2026-10-05 23:01 | ok | 2,000 | 1,638 | 20,527 |  |
| 2026-10-05 22:01 | ok | 2,000 | 1,775 | 20,395 |  |
| 2026-10-05 20:26 | ok | 2,000 | 1,976 | 20,238 |  |
| 2026-10-05 19:06 | ok | 2,000 | 2,109 | 20,112 |  |
| 2026-10-05 18:01 | ok | 2,000 | 2,013 | 19,991 |  |
| 2026-10-05 17:01 | ok | 2,000 | 1,827 | 19,885 |  |
| 2026-10-05 16:01 | ok | 2,000 | 1,650 | 19,758 |  |
| 2026-10-05 15:01 | ok | 2,000 | 1,504 | 19,651 |  |
| 2026-10-05 14:01 | ok | 2,000 | 1,389 | 19,528 |  |
| 2026-10-05 13:01 | ok | 2,000 | 1,219 | 19,408 |  |
| 2026-10-05 12:01 | ok | 2,000 | 1,000 | 19,263 |  |
| 2026-10-05 11:01 | ok | 2,000 | 887 | 19,114 |  |
| 2026-10-05 10:01 | ok | 2,000 | 844 | 18,958 |  |
| 2026-10-05 09:01 | ok | 2,000 | 774 | 18,815 |  |
| 2026-10-05 08:01 | ok | 2,000 | 671 | 18,657 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
