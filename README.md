# LiveScope data branch

Written by the `Collect and publish` workflow; do not edit by hand.

## Collection status

_Updated 2026-10-10 17:01 UTC._

| | |
|---|---|
| Snapshots collected | **200** (707,351 rows) |
| First / latest | 2026-10-02 10:42 / 2026-10-10 17:01 UTC |
| Hours captured since the first snapshot | 194 of 200 (97%) |
| Creators in the tracking panel | 29,634 |
| Failed runs | 0 |

### Last 24 runs

| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |
|---|---|---|---|---|---|
| 2026-10-10 17:01 | ok | 2,000 | 2,652 | 29,634 |  |
| 2026-10-10 16:01 | ok | 2,000 | 2,519 | 29,581 |  |
| 2026-10-10 15:01 | ok | 2,000 | 2,342 | 29,528 |  |
| 2026-10-10 14:02 | ok | 2,000 | 2,227 | 29,474 |  |
| 2026-10-10 14:00 | ok | 2,000 | 2,205 | 29,467 |  |
| 2026-10-10 13:01 | ok | 2,000 | 2,058 | 29,413 |  |
| 2026-10-10 12:01 | ok | 2,000 | 1,937 | 29,349 |  |
| 2026-10-10 11:01 | ok | 2,000 | 1,817 | 29,295 |  |
| 2026-10-10 10:01 | ok | 2,000 | 1,727 | 29,248 |  |
| 2026-10-10 09:01 | ok | 2,000 | 1,662 | 29,159 |  |
| 2026-10-10 08:01 | ok | 2,000 | 1,572 | 29,088 |  |
| 2026-10-10 07:01 | ok | 2,000 | 1,618 | 28,998 |  |
| 2026-10-10 06:01 | ok | 2,000 | 1,750 | 28,908 |  |
| 2026-10-10 05:01 | ok | 2,000 | 1,992 | 28,824 |  |
| 2026-10-10 04:01 | ok | 2,000 | 2,198 | 28,754 |  |
| 2026-10-10 03:01 | ok | 2,000 | 2,377 | 28,683 |  |
| 2026-10-10 02:01 | ok | 2,000 | 2,469 | 28,617 |  |
| 2026-10-10 01:01 | ok | 2,000 | 2,511 | 28,543 |  |
| 2026-10-10 00:01 | ok | 2,000 | 2,542 | 28,471 |  |
| 2026-10-09 23:01 | ok | 2,000 | 2,604 | 28,384 |  |
| 2026-10-09 22:01 | ok | 2,000 | 2,821 | 28,331 |  |
| 2026-10-09 21:01 | ok | 2,000 | 2,984 | 28,274 |  |
| 2026-10-09 20:01 | ok | 2,000 | 3,097 | 28,220 |  |
| 2026-10-09 19:01 | ok | 2,000 | 3,068 | 28,163 |  |

## Layout

- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot
- `state/panel.parquet`: the creators tracked outside the top list
- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results
