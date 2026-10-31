# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-31 06:01 UTC._

| | |
|---|---|
| Snapshots collected | **698** (2,751,273 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-31 06:01 UTC |
| Hours captured since the first snapshot | 687 of 693 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-31 06:01 | ok | 2,000 | 1,653 | 30,000 |  |
| 2026-10-31 05:01 | ok | 2,000 | 1,928 | 30,000 |  |
| 2026-10-31 04:01 | ok | 2,000 | 2,180 | 30,000 |  |
| 2026-10-31 03:01 | ok | 2,000 | 2,364 | 30,000 |  |
| 2026-10-31 02:01 | ok | 2,000 | 2,495 | 30,000 |  |
| 2026-10-31 01:01 | ok | 2,000 | 2,539 | 30,000 |  |
| 2026-10-31 00:01 | ok | 2,000 | 2,684 | 30,000 |  |
| 2026-10-30 23:01 | ok | 2,000 | 2,799 | 30,000 |  |
| 2026-10-30 22:01 | ok | 2,000 | 2,901 | 30,000 |  |
| 2026-10-30 21:01 | ok | 2,000 | 3,000 | 30,000 |  |
| 2026-10-30 20:01 | ok | 2,000 | 2,980 | 30,000 |  |
| 2026-10-30 19:01 | ok | 2,000 | 2,851 | 30,000 |  |
| 2026-10-30 18:02 | ok | 2,000 | 2,786 | 30,000 |  |
| 2026-10-30 17:01 | ok | 2,000 | 2,656 | 30,000 |  |
| 2026-10-30 16:01 | ok | 2,000 | 2,403 | 30,000 |  |
| 2026-10-30 15:01 | ok | 2,000 | 2,234 | 30,000 |  |
| 2026-10-30 14:01 | ok | 2,000 | 2,011 | 30,000 |  |
| 2026-10-30 13:01 | ok | 2,000 | 1,773 | 30,000 |  |
| 2026-10-30 12:01 | ok | 2,000 | 1,596 | 30,000 |  |
| 2026-10-30 11:01 | ok | 2,000 | 1,415 | 30,000 |  |
| 2026-10-30 10:01 | ok | 2,000 | 1,287 | 30,000 |  |
| 2026-10-30 09:01 | ok | 2,000 | 1,220 | 30,000 |  |
| 2026-10-30 08:01 | ok | 2,000 | 1,256 | 30,000 |  |
| 2026-10-30 07:01 | ok | 2,000 | 1,346 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
