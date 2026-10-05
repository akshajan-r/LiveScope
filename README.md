# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-05 14:01 UTC._

| | |
|---|---|
| Snapshots collected | **75** (210,940 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-05 14:01 UTC |
| Hours captured since the first snapshot | 72 of 77 (94%) |
| Creators in the tracking panel | 19,528 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-10-05 01:00 | ok | 2,000 | 986 | 17,321 |  |
| 2026-10-05 00:01 | ok | 2,000 | 1,050 | 17,122 |  |
| 2026-10-04 23:01 | ok | 2,000 | 1,154 | 16,929 |  |
| 2026-10-04 22:01 | ok | 2,000 | 1,339 | 16,765 |  |
| 2026-10-04 21:01 | ok | 2,000 | 1,480 | 16,633 |  |
| 2026-10-04 20:01 | ok | 2,000 | 1,602 | 16,509 |  |
| 2026-10-04 19:01 | ok | 2,000 | 1,593 | 16,369 |  |
| 2026-10-04 18:01 | ok | 2,000 | 1,530 | 16,217 |  |
| 2026-10-04 17:01 | ok | 2,000 | 1,500 | 16,090 |  |
| 2026-10-04 16:01 | ok | 2,000 | 1,352 | 15,953 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
