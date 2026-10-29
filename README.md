# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-29 08:01 UTC._

| | |
|---|---|
| Snapshots collected | **651** (2,555,139 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-29 08:01 UTC |
| Hours captured since the first snapshot | 641 of 647 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-29 08:01 | ok | 2,000 | 1,250 | 30,000 |  |
| 2026-10-29 07:01 | ok | 2,000 | 1,308 | 30,000 |  |
| 2026-10-29 06:01 | ok | 2,000 | 1,569 | 30,000 |  |
| 2026-10-29 05:01 | ok | 2,000 | 1,712 | 30,000 |  |
| 2026-10-29 04:01 | ok | 2,000 | 2,009 | 30,000 |  |
| 2026-10-29 03:01 | ok | 2,000 | 2,214 | 30,000 |  |
| 2026-10-29 02:01 | ok | 2,000 | 2,317 | 30,000 |  |
| 2026-10-29 01:01 | ok | 2,000 | 2,332 | 30,000 |  |
| 2026-10-29 00:01 | ok | 2,000 | 2,397 | 30,000 |  |
| 2026-10-28 23:01 | ok | 2,000 | 2,574 | 30,000 |  |
| 2026-10-28 22:01 | ok | 2,000 | 2,686 | 30,000 |  |
| 2026-10-28 21:01 | ok | 2,000 | 2,802 | 30,000 |  |
| 2026-10-28 20:01 | ok | 2,000 | 2,904 | 30,000 |  |
| 2026-10-28 19:01 | ok | 2,000 | 2,767 | 30,000 |  |
| 2026-10-28 18:01 | ok | 2,000 | 2,649 | 30,000 |  |
| 2026-10-28 17:02 | ok | 2,000 | 2,489 | 30,000 |  |
| 2026-10-28 16:01 | ok | 2,000 | 2,319 | 30,000 |  |
| 2026-10-28 15:01 | ok | 2,000 | 2,104 | 30,000 |  |
| 2026-10-28 14:01 | ok | 2,000 | 1,946 | 30,000 |  |
| 2026-10-28 13:01 | ok | 2,000 | 1,769 | 30,000 |  |
| 2026-10-28 12:01 | ok | 2,000 | 1,583 | 30,000 |  |
| 2026-10-28 11:01 | ok | 2,000 | 1,451 | 30,000 |  |
| 2026-10-28 10:01 | ok | 2,000 | 1,272 | 30,000 |  |
| 2026-10-28 09:01 | ok | 2,000 | 1,195 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
