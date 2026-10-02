"""UCSD Twitch interactions dataset (Rappaz, McAuley & Aberer, RecSys 2021).

Files (Google Drive folder linked from https://github.com/JRappaz/liverec):
  100k_a.csv      ~3M interactions from 100k users (default)
  full_a.csv.gz   ~124M interactions from 15.5M users
Columns (no header): user_id, stream_id, streamer, time_start, time_stop.
Times are 10-minute crawl rounds over 43 days (6,148 rounds).

The data is downloaded inside the pipeline and never committed. Check the
dataset's terms on the McAuley lab page before redistributing anything derived
from it; this project only publishes aggregates.
"""

from __future__ import annotations

import logging
from pathlib import Path

import duckdb
import pandas as pd

log = logging.getLogger(__name__)

DRIVE_FOLDER = "https://drive.google.com/drive/folders/1BD8m7a8m7onaifZay05yYjaLxyVV40si"
ROUNDS_PER_DAY = 144  # 24h * 6 ten-minute rounds
FILES = {"100k": "100k", "full": "full_a"}  # name prefixes inside the Drive folder


def download(dest: Path, variant: str = "100k", file_id: str | None = None) -> Path:
    """Download one file from the dataset's Drive folder (needs the `ucsd` extra)."""
    import gdown

    dest.mkdir(parents=True, exist_ok=True)
    if file_id:
        out = dest / f"{FILES[variant]}.csv{'.gz' if variant == 'full' else ''}"
        gdown.download(id=file_id, output=str(out), quiet=False)
        return out
    listing = gdown.download_folder(url=DRIVE_FOLDER, skip_download=True, quiet=True)
    prefix = FILES[variant]
    matches = [f for f in listing if Path(f.path).name.startswith(prefix)]
    if not matches:
        names = [Path(f.path).name for f in listing]
        raise FileNotFoundError(f"no file starting with {prefix!r} in the Drive folder: {names}")
    target = matches[0]
    out = dest / Path(target.path).name
    if out.exists() and out.stat().st_size > 0:
        log.info("already downloaded: %s", out)
        return out
    gdown.download(id=target.id, output=str(out), quiet=False)
    return out


def load(con: duckdb.DuckDBPyConnection, csv_path: Path) -> None:
    con.execute(
        f"""
        create or replace view ucsd_interactions as
        select * from read_csv('{csv_path}', header = false, columns = {{
            'user_id': 'BIGINT', 'stream_id': 'BIGINT', 'streamer': 'VARCHAR',
            'time_start': 'INTEGER', 'time_stop': 'INTEGER'}})
        """
    )


PROFILE_SQL = """
create or replace table ucsd_streamer as
with pair as (
    select streamer, user_id, count(*) as sessions
    from ucsd_interactions group by streamer, user_id
)
select
    i.streamer,
    count(*)                                         as interactions,
    count(distinct i.user_id)                        as unique_viewers,
    count(distinct i.stream_id)                      as streams,
    sum(i.time_stop - i.time_start + 1) / 6.0        as watch_hours,
    avg(i.time_stop - i.time_start + 1) * 10         as avg_session_minutes,
    count(distinct i.time_start // {rpd})            as active_days,
    any_value(r.return_rate)                         as return_rate
from ucsd_interactions i
join (
    select streamer, avg(case when sessions > 1 then 1.0 else 0.0 end) as return_rate
    from pair group by streamer
) r using (streamer)
group by i.streamer;

create or replace table ucsd_streamer_day as
select
    streamer,
    time_start // {rpd}                     as day,
    count(distinct user_id)                 as viewers,
    sum(time_stop - time_start + 1) / 6.0   as watch_hours
from ucsd_interactions
group by 1, 2;

create or replace table ucsd_daily as
select
    time_start // {rpd}                     as day,
    count(distinct user_id)                 as users,
    count(distinct streamer)                as streamers,
    count(*)                                as interactions,
    sum(time_stop - time_start + 1) / 6.0   as watch_hours
from ucsd_interactions
group by 1;

-- Concentration of watch time: share going to the top x% of streamers.
create or replace table ucsd_concentration as
with ranked as (
    select watch_hours,
           row_number() over (order by watch_hours desc) as rnk,
           count(*) over () as n,
           sum(watch_hours) over () as total
    from ucsd_streamer
)
select
    pct,
    sum(watch_hours) / any_value(total) as watch_share
from ranked, (values (0.001), (0.01), (0.1)) t(pct)
where rnk <= greatest(1, ceil(n * pct))
group by pct
order by pct;
""".replace("{rpd}", str(ROUNDS_PER_DAY))


def build_profiles(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    con.execute(PROFILE_SQL)
    return {t: con.execute(f"select count(*) from {t}").fetchone()[0]
            for t in ("ucsd_streamer", "ucsd_streamer_day", "ucsd_daily", "ucsd_concentration")}


RETURN_FEATURES_SQL = """
with hist as (
    select * from ucsd_interactions where time_start < {cut}
),
pair as (
    select
        user_id, streamer,
        count(*)                                  as pair_sessions,
        sum(time_stop - time_start + 1)           as pair_rounds,
        count(distinct time_start // {rpd})       as pair_days,
        {cut} - max(time_stop)                    as rounds_since_last,
        {cut} - min(time_start)                   as rounds_since_first
    from hist group by user_id, streamer
),
usr as (
    select user_id,
           count(*)                        as user_sessions,
           count(distinct streamer)        as user_streamers,
           sum(time_stop - time_start + 1) as user_rounds
    from hist group by user_id
),
strm as (
    select streamer,
           count(distinct user_id)         as streamer_viewers,
           count(*)                        as streamer_sessions
    from hist group by streamer
),
strm_ret as (
    select streamer, avg(case when pair_sessions > 1 then 1.0 else 0.0 end) as streamer_return_rate
    from pair group by streamer
),
future as (
    select distinct user_id, streamer
    from ucsd_interactions
    where time_start >= {cut} and time_start < {cut} + {horizon}
)
select
    p.*,
    u.user_sessions, u.user_streamers, u.user_rounds,
    p.pair_rounds / u.user_rounds           as pair_share_of_user_time,
    s.streamer_viewers, s.streamer_sessions, r.streamer_return_rate,
    (f.user_id is not null)::int            as returned
from pair p
join usr u using (user_id)
join strm s using (streamer)
join strm_ret r using (streamer)
left join future f using (user_id, streamer)
{sample}
"""

RETURN_FEATURES = [
    "pair_sessions", "pair_rounds", "pair_days", "rounds_since_last", "rounds_since_first",
    "user_sessions", "user_streamers", "user_rounds", "pair_share_of_user_time",
    "streamer_viewers", "streamer_sessions", "streamer_return_rate",
]


def return_dataset(con: duckdb.DuckDBPyConnection, cutoff_day: int, horizon_days: int = 7, sample_rows: int | None = None,
                   seed: int = 0) -> pd.DataFrame:
    """User-streamer pairs seen before `cutoff_day`; label = the user watches that
    streamer again within the next `horizon_days`. Features use history only."""
    sample = f"using sample reservoir({int(sample_rows)} rows) repeatable ({seed})" if sample_rows else ""
    sql = RETURN_FEATURES_SQL.format(cut=cutoff_day * ROUNDS_PER_DAY, horizon=horizon_days * ROUNDS_PER_DAY,
                                     rpd=ROUNDS_PER_DAY, sample=sample)
    df = con.execute(sql).df()
    df["cutoff_day"] = cutoff_day
    return df


def evaluate_returns(con: duckdb.DuckDBPyConnection, train_cutoff: int = 21, test_cutoff: int = 28, horizon_days: int = 7,
                     sample_rows: int | None = 1_000_000, seed: int = 0) -> dict:
    """Temporal validation: fit on pairs at `train_cutoff`, score on pairs at `test_cutoff`.

    The training labels end at train_cutoff + horizon; keep that <= test_cutoff so
    no training label overlaps the test feature window.
    """
    if train_cutoff + horizon_days > test_cutoff:
        raise ValueError("training label window overlaps the test period")
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import average_precision_score, roc_auc_score
    from sklearn.pipeline import make_pipeline
    from sklearn.preprocessing import StandardScaler

    from livescope.predict import _gbm

    train = return_dataset(con, train_cutoff, horizon_days, sample_rows, seed)
    test = return_dataset(con, test_cutoff, horizon_days, sample_rows, seed + 1)
    X_tr, y_tr = train[RETURN_FEATURES].astype(float), train["returned"].to_numpy()
    X_te, y_te = test[RETURN_FEATURES].astype(float), test["returned"].to_numpy()

    results = []
    # Baseline: users come back to streamers they watched most recently.
    results.append({"model": "recency_rule", "roc_auc": roc_auc_score(y_te, -X_te["rounds_since_last"]),
                    "pr_auc": average_precision_score(y_te, -X_te["rounds_since_last"])})
    logit = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)).fit(X_tr, y_tr)
    p = logit.predict_proba(X_te)[:, 1]
    results.append({"model": "logistic_regression", "roc_auc": roc_auc_score(y_te, p), "pr_auc": average_precision_score(y_te, p)})
    name, gbm = _gbm(seed)
    gbm.fit(X_tr, y_tr)
    p = gbm.predict_proba(X_te)[:, 1]
    results.append({"model": name, "roc_auc": roc_auc_score(y_te, p), "pr_auc": average_precision_score(y_te, p)})

    importance = None
    if hasattr(gbm, "booster_"):
        gain = gbm.booster_.feature_importance(importance_type="gain")
        importance = (pd.DataFrame({"feature": RETURN_FEATURES, "gain_share": gain / gain.sum()})
                      .sort_values("gain_share", ascending=False).reset_index(drop=True))
    return {
        "train_rows": len(train), "test_rows": len(test),
        "train_base_rate": float(y_tr.mean()), "test_base_rate": float(y_te.mean()),
        "metrics": pd.DataFrame(results), "importance": importance,
    }


def synthetic_csv(path: Path, n_users: int = 2000, n_streamers: int = 150, days: int = 43, seed: int = 0) -> Path:
    """A small file in the UCSD format, for tests only."""
    import numpy as np

    rng = np.random.default_rng(seed)
    popularity = rng.pareto(1.2, n_streamers) + 1
    popularity /= popularity.sum()
    rows = []
    stream_id = 0
    for u in range(n_users):
        favourites = rng.choice(n_streamers, size=rng.integers(1, 6), p=popularity, replace=False)
        loyalty = rng.uniform(0.05, 0.6)
        for d in range(days):
            for s in favourites:
                if rng.random() < loyalty:
                    start = d * ROUNDS_PER_DAY + int(rng.integers(0, ROUNDS_PER_DAY - 20))
                    stream_id += 1
                    rows.append((u, stream_id, f"streamer_{s}", start, start + int(rng.integers(0, 18))))
    pd.DataFrame(rows).to_csv(path, header=False, index=False)
    return path
