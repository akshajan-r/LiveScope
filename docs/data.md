# Data sources and caveats

## 1. Hourly Twitch snapshots (collected by this project)

**How.** `.github/workflows/collect.yml` is scheduled at minutes 23 and 53 of every hour and calls the Twitch Helix [Get Streams](https://dev.twitch.tv/docs/api/reference/#get-streams) endpoint with an app access token (client-credentials flow). A run that finds the current UTC hour already captured exits without doing anything, so there is one snapshot an hour with a second chance when GitHub skips a scheduled run (it delays or drops them at busy times). Each run captures:

- the top `LIVESCOPE_MAX_STREAMS` (default 2,000) live streams, ordered by current viewers (`source = "top"`, with `rank`);
- every live stream from the **tracking panel** that is not already in that list (`source = "panel"`). The panel is the first `LIVESCOPE_PANEL_MAX` (default 30,000) creators ever seen in a top list, looked up by `user_id` in batches of 100. Every creator who breaks into the top list joins the panel until it is full, so each week's newcomers can be followed afterwards (the basis of the retention and survival analysis).

At the defaults that is at most about 320 requests per run (20 for the top list, 300 for a full panel), inside Helix's limit of 800 points per minute.

**Fields kept:** snapshot time, stream id, broadcaster id/login/name, category id/name, language, viewer count, stream start time, mature flag, tags, source and rank. Stream titles and thumbnails are not stored.

**Storage.** One Parquet file per run on the `data` branch: `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`. Keeping data off `main` keeps the code history readable. At the defaults a snapshot is roughly 100 KB, so a month is around 70 MB.

**Quality checks** (`livescope/ingest/quality.py`), run before every write:

| Check | Severity |
|---|---|
| Required columns present | error |
| At least half of `LIVESCOPE_MAX_STREAMS` rows | error |
| No null stream id, user id or snapshot time | error |
| No duplicate stream ids | error |
| No negative viewer counts | error |
| One snapshot hour per file | error |
| `source` is `top` or `panel` | error |
| Streams starting after the snapshot time (beyond 5 min clock skew) | warning |
| Users with more than one live stream | warning |
| More than 20% of streams without a category | warning |

On an error nothing is written and the run fails; every run, failed or not, is logged to `manifest/runs.jsonl`.

### What this data can and cannot say

- **Selection.** Creators enter by ranking in the top list. "Creators" means the most-watched end of Twitch; small creators are mostly invisible. Results do not generalise to the long tail.
- **The panel fixes drop-off, not entry.** Once in the panel, a creator is observed whenever they are live, however few viewers they have, so declines and drop-off are measured properly. Creators who never reach the top list are never observed.
- **The panel fills up.** After it reaches `LIVESCOPE_PANEL_MAX`, new creators appear only while they rank, and the retention analysis stops admitting new cohorts (it only counts panel creators). At around 1,000–3,000 newcomers a week, 30,000 lasts a few months; raise it if needed, but very large panels make each run slower.
- **Panel creators join on a schedule set by the first run.** The first collection week puts thousands of already-established creators into the panel at once. That cohort is labelled as such in the retention analysis and kept apart from genuine newcomers.
- **Hourly sampling.** A stream shorter than an hour can fall between snapshots; a stream seen in three snapshots counts as three hours.
- **Language is not country.** The EU split uses broadcast language. Spanish and Portuguese are mostly Latin American and Brazilian audiences, English is global, and an EU creator streaming in English counts as English.
- **Viewer counts** are Twitch's concurrent viewer figures (they include embedded players and are not unique viewers).
- **Scheduling gaps.** GitHub can delay or drop scheduled runs at busy times. Weeks with less than 90% of hours captured are excluded from weekly metrics.
- **Scheduled workflows stop after 60 days without repository activity** on public repositories. The hourly commits to `data` count as activity, but if collection stops for any reason, re-enable the workflow under the Actions tab.

### Terms

Twitch's [Developer Services Agreement](https://legal.twitch.com/legal/developer-agreement/) governs use of the API. This project stores only public stream metadata and publishes aggregates and creator-level statistics derived from it. Re-read the agreement before publishing raw data.

## 2. UCSD Twitch interactions dataset

Rappaz, McAuley & Aberer, *Recommendation on Live-Streaming Platforms: Dynamic Availability and Repeat Consumption*, RecSys 2021. Files are linked from [github.com/JRappaz/liverec](https://github.com/JRappaz/liverec):

| File | Users | Streamers | Interactions |
|---|---|---|---|
| `100k_a.csv` | 100k | 162.6k | 3M |
| `full_a.csv.gz` | 15.5M | 465k | 124M |

Columns (no header): `user_id, stream_id, streamer, time_start, time_stop`. Times are 10-minute crawl rounds over 43 days. A row means the user was seen in that streamer's chat from `time_start` to `time_stop`, so it measures chatters, not all viewers.

**Licence.** The dataset is distributed for research by the McAuley lab; check the terms on the [lab's dataset page](https://cseweb.ucsd.edu/~jmcauley/datasets.html) before using it beyond personal research, and cite the paper. This repository never commits the raw file: `.github/workflows/ucsd.yml` downloads it inside the job (cached between runs), and only aggregates are exported.

**What we compute** (`livescope/ucsd.py`, DuckDB; `spark/ucsd_spark.py`, PySpark for the full file):

- streamer profiles: unique chatters, sessions, hours watched, average session length, active days, return rate (share of a streamer's chatters seen in more than one session);
- daily platform totals;
- concentration of watch time (share going to the top 0.1%, 1% and 10% of streamers);
- a viewer-return model: for each user-streamer pair seen before a cutoff day, will the user come back to that streamer within the next 7 days? Features use history before the cutoff only. Trained at day 21, tested at day 28, against a recency baseline.
