# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-04 14:01 UTC._

| | |
|---|---|
| Snapshots collected | **50** (133,619 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-04 14:01 UTC |
| Hours captured since the first snapshot | 48 of 53 (91%) |
| Creators in the tracking panel | 15,679 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-04 14:01 | ok | 2,000 | 1,123 | 15,679 |  |
| 2026-10-04 13:01 | ok | 2,000 | 1,116 | 15,532 |  |
| 2026-10-04 12:01 | ok | 2,000 | 1,006 | 15,417 |  |
| 2026-10-04 11:01 | ok | 2,000 | 896 | 15,290 |  |
| 2026-10-04 10:01 | ok | 2,000 | 847 | 15,164 |  |
| 2026-10-04 09:01 | ok | 2,000 | 772 | 15,026 |  |
| 2026-10-04 08:01 | ok | 2,000 | 706 | 14,879 |  |
| 2026-10-04 07:01 | ok | 2,000 | 669 | 14,707 |  |
| 2026-10-04 06:02 | ok | 2,000 | 653 | 14,556 |  |
| 2026-10-04 06:00 | ok | 2,000 | 650 | 14,546 |  |
| 2026-10-04 05:01 | ok | 2,000 | 705 | 14,355 |  |
| 2026-10-04 04:00 | ok | 2,000 | 724 | 14,154 |  |
| 2026-10-04 03:01 | ok | 2,000 | 763 | 13,940 |  |
| 2026-10-04 02:01 | ok | 2,000 | 781 | 13,710 |  |
| 2026-10-04 01:01 | ok | 2,000 | 805 | 13,495 |  |
| 2026-10-04 00:01 | ok | 2,000 | 840 | 13,261 |  |
| 2026-10-03 23:01 | ok | 2,000 | 920 | 13,044 |  |
| 2026-10-03 22:01 | ok | 2,000 | 1,003 | 12,836 |  |
| 2026-10-03 21:01 | ok | 2,000 | 1,080 | 12,666 |  |
| 2026-10-03 20:01 | ok | 2,000 | 1,125 | 12,480 |  |
| 2026-10-03 19:01 | ok | 2,000 | 1,129 | 12,282 |  |
| 2026-10-03 18:02 | ok | 2,000 | 1,139 | 12,087 |  |
| 2026-10-03 18:00 | ok | 2,000 | 1,121 | 12,067 |  |
| 2026-10-03 17:01 | ok | 2,000 | 1,103 | 11,894 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
