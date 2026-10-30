# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-30 21:01 UTC._

| | |
|---|---|
| Snapshots collected | **689** (2,711,730 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-30 21:01 UTC |
| Hours captured since the first snapshot | 678 of 684 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
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
| 2026-10-30 06:01 | ok | 2,000 | 1,499 | 30,000 |  |
| 2026-10-30 05:01 | ok | 2,000 | 1,742 | 30,000 |  |
| 2026-10-30 04:01 | ok | 2,000 | 1,926 | 30,000 |  |
| 2026-10-30 03:01 | ok | 2,000 | 2,195 | 30,000 |  |
| 2026-10-30 02:03 | ok | 2,000 | 2,321 | 30,000 |  |
| 2026-10-30 02:00 | ok | 2,000 | 2,322 | 30,000 |  |
| 2026-10-30 01:01 | ok | 2,000 | 2,402 | 30,000 |  |
| 2026-10-30 00:01 | ok | 2,000 | 2,511 | 30,000 |  |
| 2026-10-29 23:01 | ok | 2,000 | 2,659 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
