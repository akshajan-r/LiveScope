# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-06 01:01 UTC._

| | |
|---|---|
| Snapshots collected | **85** (248,573 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-06 01:01 UTC |
| Hours captured since the first snapshot | 82 of 88 (93%) |
| Creators in the tracking panel | 20,790 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-10-05 07:01 | ok | 2,000 | 670 | 18,476 |  |
| 2026-10-05 06:01 | ok | 2,000 | 639 | 18,267 |  |
| 2026-10-05 05:01 | ok | 2,000 | 715 | 18,059 |  |
| 2026-10-05 04:01 | ok | 2,000 | 808 | 17,876 |  |
| 2026-10-05 03:01 | ok | 2,000 | 910 | 17,689 |  |
| 2026-10-05 02:01 | ok | 2,000 | 951 | 17,508 |  |
| 2026-10-05 01:02 | ok | 2,000 | 1,004 | 17,343 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
