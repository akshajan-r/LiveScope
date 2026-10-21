# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-21 20:01 UTC._

| | |
|---|---|
| Snapshots collected | **470** (1,824,244 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-21 20:01 UTC |
| Hours captured since the first snapshot | 461 of 467 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-21 20:01 | ok | 2,000 | 2,951 | 30,000 |  |
| 2026-10-21 19:01 | ok | 2,000 | 2,994 | 30,000 |  |
| 2026-10-21 18:01 | ok | 2,000 | 2,891 | 30,000 |  |
| 2026-10-21 17:01 | ok | 2,000 | 2,680 | 30,000 |  |
| 2026-10-21 16:01 | ok | 2,000 | 2,488 | 30,000 |  |
| 2026-10-21 15:01 | ok | 2,000 | 2,279 | 30,000 |  |
| 2026-10-21 14:01 | ok | 2,000 | 2,027 | 30,000 |  |
| 2026-10-21 13:01 | ok | 2,000 | 1,801 | 30,000 |  |
| 2026-10-21 12:01 | ok | 2,000 | 1,596 | 30,000 |  |
| 2026-10-21 11:01 | ok | 2,000 | 1,442 | 30,000 |  |
| 2026-10-21 10:01 | ok | 2,000 | 1,347 | 30,000 |  |
| 2026-10-21 09:01 | ok | 2,000 | 1,281 | 30,000 |  |
| 2026-10-21 08:01 | ok | 2,000 | 1,269 | 30,000 |  |
| 2026-10-21 07:01 | ok | 2,000 | 1,364 | 30,000 |  |
| 2026-10-21 06:01 | ok | 2,000 | 1,468 | 30,000 |  |
| 2026-10-21 05:01 | ok | 2,000 | 1,689 | 30,000 |  |
| 2026-10-21 04:01 | ok | 2,000 | 1,922 | 30,000 |  |
| 2026-10-21 03:01 | ok | 2,000 | 2,153 | 30,000 |  |
| 2026-10-21 02:01 | ok | 2,000 | 2,274 | 30,000 |  |
| 2026-10-21 01:01 | ok | 2,000 | 2,366 | 30,000 |  |
| 2026-10-21 00:01 | ok | 2,000 | 2,332 | 30,000 |  |
| 2026-10-20 23:01 | ok | 2,000 | 2,413 | 30,000 |  |
| 2026-10-20 22:01 | ok | 2,000 | 2,618 | 30,000 |  |
| 2026-10-20 21:01 | ok | 2,000 | 2,743 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
