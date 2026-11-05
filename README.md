# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-11-05 22:01 UTC._

| | |
|---|---|
| Snapshots collected | **834** (3,294,042 rows) |
| First / latest | 2026-10-02 10:42 / 2026-11-05 22:01 UTC |
| Hours captured since the first snapshot | 823 of 829 (99%) |
| Creators in the tracking panel | 30,000 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-11-05 22:01 | ok | 2,000 | 2,957 | 30,000 |  |
| 2026-11-05 21:01 | ok | 2,000 | 3,061 | 30,000 |  |
| 2026-11-05 20:01 | ok | 2,000 | 3,040 | 30,000 |  |
| 2026-11-05 19:01 | ok | 2,000 | 2,995 | 30,000 |  |
| 2026-11-05 18:01 | ok | 2,000 | 2,904 | 30,000 |  |
| 2026-11-05 17:01 | ok | 2,000 | 2,727 | 30,000 |  |
| 2026-11-05 16:01 | ok | 2,000 | 2,510 | 30,000 |  |
| 2026-11-05 15:01 | ok | 2,000 | 2,367 | 30,000 |  |
| 2026-11-05 14:01 | ok | 2,000 | 2,256 | 30,000 |  |
| 2026-11-05 13:01 | ok | 2,000 | 2,066 | 30,000 |  |
| 2026-11-05 12:01 | ok | 2,000 | 1,900 | 30,000 |  |
| 2026-11-05 11:01 | ok | 2,000 | 1,826 | 30,000 |  |
| 2026-11-05 10:01 | ok | 2,000 | 1,751 | 30,000 |  |
| 2026-11-05 09:01 | ok | 2,000 | 1,737 | 30,000 |  |
| 2026-11-05 08:01 | ok | 2,000 | 1,776 | 30,000 |  |
| 2026-11-05 07:01 | ok | 2,000 | 1,882 | 30,000 |  |
| 2026-11-05 06:01 | ok | 2,000 | 2,089 | 30,000 |  |
| 2026-11-05 05:01 | ok | 2,000 | 2,351 | 30,000 |  |
| 2026-11-05 04:01 | ok | 2,000 | 2,548 | 30,000 |  |
| 2026-11-05 03:01 | ok | 2,000 | 2,724 | 30,000 |  |
| 2026-11-05 02:01 | ok | 2,000 | 2,796 | 30,000 |  |
| 2026-11-05 01:01 | ok | 2,000 | 2,872 | 30,000 |  |
| 2026-11-05 00:01 | ok | 2,000 | 2,939 | 30,000 |  |
| 2026-11-04 23:01 | ok | 2,000 | 2,987 | 30,000 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
