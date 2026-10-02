# Setup

## 1. Twitch credentials

1. Sign in at [dev.twitch.tv/console](https://dev.twitch.tv/console) (two-factor authentication must be enabled on the Twitch account).
2. **Register Your Application**: any name, OAuth redirect URL `http://localhost`, category *Analytics Tool*, client type *Confidential*.
3. Open the app, copy the **Client ID**, and click **New Secret** to get a **Client Secret**.
4. In the GitHub repository: **Settings → Secrets and variables → Actions → New repository secret**:
   - `TWITCH_CLIENT_ID`
   - `TWITCH_CLIENT_SECRET`

The collector uses the client-credentials flow (an app access token), so no user login is involved.

## 2. Turn on GitHub Pages

**Settings → Pages → Build and deployment → Source: GitHub Actions.** The `Collect and publish` workflow deploys the dashboard there. The site will be at `https://<user>.github.io/LiveScope/`.

## 3. Start collecting

**Actions → Collect and publish → Run workflow.** The first run creates the `data` branch, stores one snapshot and publishes the dashboard. After that the workflow runs at minute 7 of every hour and republishes the dashboard once a day (06:07 UTC).

Optional repository **variables** (Settings → Secrets and variables → Actions → Variables):

| Variable | Default | Meaning |
|---|---|---|
| `LIVESCOPE_MAX_STREAMS` | `2000` | top live streams captured per snapshot |
| `LIVESCOPE_PANEL_MAX` | `5000` | creators tracked outside the top list |
| `REBUILD_EVERY_RUN` | unset | `true` republishes the dashboard every hour instead of daily |

Minutes: an ingest run takes about a minute and a publish run a few minutes. Public repositories have unlimited Actions minutes; on a private repository hourly collection uses roughly 750–1,500 of the 2,000 free minutes a month.

## 4. BigQuery (optional, free sandbox)

1. Create a project at [console.cloud.google.com](https://console.cloud.google.com). The BigQuery sandbox needs no billing account; tables expire after 60 days, which is fine because every publish reloads them.
2. **IAM & Admin → Service accounts → Create**, grant *BigQuery Data Editor* and *BigQuery Job User*, then **Keys → Add key → JSON**.
3. Add the JSON as the secret `GCP_SA_KEY` and the project id as the variable `GCP_PROJECT` (optionally `BQ_DATASET`, default `livescope`).

The publish job then loads every exported table (`creator_week`, `platform_week`, ...) into BigQuery. Example query:

```sql
select week_start, viewer_hours, active_creators, drop_off_rate
from `your-project.livescope.platform_week`
order by week_start;
```

## 5. UCSD dataset

**Actions → UCSD dataset → Run workflow**, choose `100k` (DuckDB, a few minutes) or `full` (use the `spark` engine). Results are uploaded as a workflow artifact. Read [data.md](data.md#2-ucsd-twitch-interactions-dataset) for the licence note first.

## 6. Local development

```bash
python -m venv .venv && . .venv/bin/activate
pip install -e ".[dev]"
python -m pytest

# Work on the dashboard with synthetic data (clearly labelled as such on every page)
export LIVESCOPE_DATASTORE=demo-store
python -m livescope demo
python -m livescope build
cp exports/dashboard/* dashboard/src/data/
cd dashboard && npm install && npm run dev

# Or analyse the real data: check out the data branch next to the code
git worktree add datastore data
LIVESCOPE_DATASTORE=datastore python -m livescope build
```

Commands:

| Command | What it does |
|---|---|
| `python -m livescope ingest` | one snapshot (needs the Twitch secrets as environment variables) |
| `python -m livescope build` | warehouse, analyses, exports for the dashboard / Tableau / BigQuery |
| `python -m livescope demo` | synthetic snapshots for development |
| `python -m livescope ucsd` | download and process the UCSD dataset |
| `python -m livescope abtest-validate` | simulation check of the A/B testing toolkit |
| `python -m livescope bigquery --project ...` | load exports into BigQuery |
