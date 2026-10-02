"""Synthetic snapshots with the same schema as the real collector.

Used by the tests and for developing the dashboard before real data exists.
Every file it writes lives under a separate data store and every export built
from it is labelled `synthetic` (see export.py), so it cannot be mistaken for
collected data.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from livescope.ingest.snapshot import SNAPSHOT_COLUMNS

CATEGORIES = [
    ("509658", "Just Chatting"),
    ("32982", "Grand Theft Auto V"),
    ("21779", "League of Legends"),
    ("516575", "VALORANT"),
    ("33214", "Fortnite"),
    ("27471", "Minecraft"),
    ("32399", "Counter-Strike"),
    ("511224", "Apex Legends"),
    ("26936", "Music"),
    ("509660", "Art"),
    ("29595", "Dota 2"),
    ("512710", "Call of Duty: Warzone"),
    ("509663", "Special Events"),
    ("518203", "Sports"),
    ("490100", "Lost Ark"),
    ("509670", "Science & Technology"),
    ("1469308723", "Software and Game Development"),
    ("509667", "Food & Drink"),
    ("509659", "ASMR"),
    ("2748", "Magic: The Gathering"),
    ("27546", "World of Tanks"),
    ("509672", "Travel & Outdoors"),
    ("488552", "Overwatch 2"),
    ("1745202732", "Chess"),
]
LANGUAGES = ["en", "en", "en", "es", "pt", "de", "fr", "ja", "ko"]


def generate(
    n_creators: int = 400,
    weeks: int = 8,
    start: str = "2026-01-05",
    seed: int = 7,
) -> pd.DataFrame:
    """Simulate hourly snapshots for `n_creators` over `weeks` weeks.

    Each creator has a base audience (log-normal), a weekly growth rate, a
    preferred start hour, a weekly schedule, a chance of churning and a chance
    of moving their schedule into the evening peak halfway through. Viewer
    counts get a time-of-day effect so peak hours exist in the data.
    """
    rng = np.random.default_rng(seed)
    hours = pd.date_range(start, periods=weeks * 168, freq="h", tz="UTC")
    n_hours = len(hours)
    hod = hours.hour.to_numpy()
    week_idx = np.arange(n_hours) // 168

    base = rng.lognormal(mean=4.0, sigma=1.3, size=n_creators)
    growth = rng.normal(0.0, 0.08, size=n_creators)  # weekly log growth
    pref_hour = rng.integers(0, 24, size=n_creators)
    session_len = rng.integers(2, 7, size=n_creators)
    days_per_week = rng.integers(1, 8, size=n_creators)
    churn_week = np.where(rng.random(n_creators) < 0.15, rng.integers(min(2, weeks), weeks + 1, size=n_creators), weeks + 1)
    # A third of creators debut after collection starts; newcomers churn more,
    # mostly within their first few weeks.
    debut_week = np.where(rng.random(n_creators) < 0.35, rng.integers(1, max(2, weeks - 1), size=n_creators), 0)
    newcomer_churn = (debut_week > 0) & (rng.random(n_creators) < 0.45)
    churn_week = np.where(newcomer_churn, debut_week + 1 + rng.geometric(0.4, size=n_creators), churn_week)
    # Some creators move their schedule to 20:00 UTC halfway through, giving the
    # difference-in-differences analysis something to find.
    moves_to_peak = rng.random(n_creators) < 0.15
    # Category popularity among creators is long-tailed (Zipf-like), and each
    # category has its own audience multiplier, so supply and demand differ.
    cat_weights = 1 / np.arange(1, len(CATEGORIES) + 1) ** 1.1
    cat = rng.choice(len(CATEGORIES), size=n_creators, p=cat_weights / cat_weights.sum())
    cat_demand = rng.lognormal(0.0, 0.5, size=len(CATEGORIES))
    lang = rng.choice(LANGUAGES, size=n_creators)
    # Platform-wide audience curve peaking around 20:00-01:00 UTC.
    tod_effect = 0.75 + 0.5 * np.exp(-0.5 * (((hod - 22 + 12) % 24 - 12) / 3.0) ** 2)

    rows = []
    for c in range(n_creators):
        live_days = rng.random((weeks, 7)) < days_per_week[c] / 7
        day_of_run = np.arange(n_hours) // 24
        dow_live = live_days[week_idx, day_of_run % 7]
        start_at = np.where(moves_to_peak[c] & (week_idx >= weeks // 2), 20, pref_hour[c])
        in_session = ((hod - start_at) % 24) < session_len[c]
        live = dow_live & in_session & (week_idx >= debut_week[c]) & (week_idx < churn_week[c])
        idx = np.flatnonzero(live)
        if idx.size == 0:
            continue
        mu = base[c] * cat_demand[cat[c]] * np.exp(growth[c] * week_idx[idx]) * tod_effect[idx]
        viewers = rng.poisson(np.maximum(mu, 0.5))
        # A new stream id each time a session starts.
        starts = np.r_[True, np.diff(idx) > 1]
        session_id = np.cumsum(starts)
        start_hour = hours[idx[starts]][session_id - 1]
        game_id, game_name = CATEGORIES[cat[c]]
        # Occasionally switch category within a week.
        switch = rng.random(idx.size) < 0.1
        alt = rng.integers(0, len(CATEGORIES), size=idx.size)
        for j, h in enumerate(idx):
            g_id, g_name = CATEGORIES[alt[j]] if switch[j] else (game_id, game_name)
            rows.append(
                (
                    hours[h] + pd.Timedelta(minutes=7),
                    hours[h],
                    f"s{c:05d}_{session_id[j]:04d}",
                    f"{100000 + c}",
                    f"creator_{c:04d}",
                    f"Creator{c:04d}",
                    g_id,
                    g_name,
                    lang[c],
                    int(viewers[j]),
                    start_hour[j],
                    False,
                    [],
                    "panel",
                    None,
                )
            )
    df = pd.DataFrame(rows, columns=SNAPSHOT_COLUMNS)
    df["rank"] = df.groupby("snapshot_hour")["viewer_count"].rank(method="first", ascending=False).astype("Int64")
    df["source"] = np.where(df["rank"] <= max(20, n_creators // 4), "top", "panel")
    df.loc[df["source"] == "panel", "rank"] = pd.NA
    for col in ("stream_id", "user_id", "user_login", "user_name", "game_id", "game_name", "language", "source"):
        df[col] = df[col].astype("string")
    df["is_mature"] = df["is_mature"].astype("boolean")
    return df


def write_demo_store(datastore: Path, **kwargs) -> int:
    """Write the synthetic snapshots as one Parquet file per day plus a marker file."""
    df = generate(**kwargs)
    raw = datastore / "raw" / "twitch_streams"
    for day, part in df.groupby(df["snapshot_hour"].dt.strftime("%Y-%m-%d")):
        out = raw / f"date={day}" / "synthetic.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        part.to_parquet(out, index=False)
    (datastore / "SYNTHETIC").write_text("This data store holds synthetic data generated by livescope.demo.\n")
    return len(df)
