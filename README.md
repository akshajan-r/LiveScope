# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-16 19:01 UTC._

| | |
|---|---|
| Snapshots collected | **349** (1,330,689 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-16 19:01 UTC |
| Hours captured since the first snapshot | 340 of 346 (98%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-16 19:01 | ok | 2,000 | 3,143 | 30,000 |  |
| 2026-10-16 18:01 | ok | 2,000 | 3,032 | 30,000 |  |
| 2026-10-16 17:03 | ok | 2,000 | 2,908 | 30,000 |  |
| 2026-10-16 17:01 | ok | 2,000 | 2,888 | 30,000 |  |
| 2026-10-16 16:01 | ok | 2,000 | 2,633 | 30,000 |  |
| 2026-10-16 15:01 | ok | 2,000 | 2,400 | 30,000 |  |
| 2026-10-16 14:01 | ok | 2,000 | 2,158 | 30,000 |  |
| 2026-10-16 13:01 | ok | 2,000 | 1,955 | 30,000 |  |
| 2026-10-16 12:01 | ok | 2,000 | 1,808 | 30,000 |  |
| 2026-10-16 11:01 | ok | 2,000 | 1,622 | 30,000 |  |
| 2026-10-16 10:01 | ok | 2,000 | 1,574 | 30,000 |  |
| 2026-10-16 09:01 | ok | 2,000 | 1,543 | 30,000 |  |
| 2026-10-16 08:01 | ok | 2,000 | 1,582 | 30,000 |  |
| 2026-10-16 07:01 | ok | 2,000 | 1,624 | 30,000 |  |
| 2026-10-16 06:01 | ok | 2,000 | 1,744 | 30,000 |  |
| 2026-10-16 05:01 | ok | 2,000 | 1,923 | 30,000 |  |
| 2026-10-16 04:01 | ok | 2,000 | 2,077 | 30,000 |  |
| 2026-10-16 03:01 | ok | 2,000 | 2,265 | 30,000 |  |
| 2026-10-16 02:01 | ok | 2,000 | 2,347 | 30,000 |  |
| 2026-10-16 01:01 | ok | 2,000 | 2,402 | 30,000 |  |
| 2026-10-16 00:01 | ok | 2,000 | 2,412 | 30,000 |  |
| 2026-10-15 23:01 | ok | 2,000 | 2,502 | 30,000 |  |
| 2026-10-15 22:01 | ok | 2,000 | 2,664 | 30,000 |  |
| 2026-10-15 21:01 | ok | 2,000 | 2,953 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
