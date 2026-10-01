"""Creator segmentation on creator-week features.

Features are computed per creator over the last `window` complete weeks.
k is chosen by silhouette score for k-means; a Gaussian mixture with BIC is fit
alongside as a robustness check. Segment names come from simple rules on the
standardised cluster centres (see `name_segments`), so read the profile table
before trusting a name.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "log_avg_viewers",
    "viewer_trend",
    "active_share",
    "mean_hours_live",
    "peak_hour_share",
    "mean_categories",
]


def creator_features(creator_week: pd.DataFrame, window: int = 4, min_weeks: int = 2) -> pd.DataFrame:
    cw = creator_week[creator_week["is_complete_week"]].copy()
    if cw.empty:
        return pd.DataFrame(columns=["user_id", *FEATURES])
    weeks = np.sort(cw["week_index"].unique())[-window:]
    cw = cw[cw["week_index"].isin(weeks)]
    cw["log_viewers"] = np.log1p(cw["avg_viewers"])

    def trend(g: pd.DataFrame) -> float:
        # Slope of log(1 + avg viewers) per week, i.e. approximate weekly growth rate.
        if len(g) < 2:
            return 0.0
        return float(np.polyfit(g["week_index"], g["log_viewers"], 1)[0])

    grouped = cw.groupby("user_id")
    feats = pd.DataFrame(
        {
            "user_login": grouped["user_login"].last(),
            "weeks_active": grouped.size(),
            "log_avg_viewers": np.log1p(grouped["viewer_hours"].sum() / grouped["hours_live"].sum()),
            "viewer_trend": grouped[["week_index", "log_viewers"]].apply(trend),
            "active_share": grouped.size() / len(weeks),
            "mean_hours_live": grouped["hours_live"].mean(),
            "peak_hour_share": grouped["peak_hour_share"].mean(),
            "mean_categories": grouped["categories"].mean(),
            "active_last_week": grouped["week_index"].max() == weeks.max(),
        }
    ).reset_index()
    return feats[feats["weeks_active"] >= min_weeks].reset_index(drop=True)


@dataclass
class SegmentationResult:
    k: int
    silhouette_by_k: dict[int, float]
    bic_by_k: dict[int, float]
    assignments: pd.DataFrame
    profiles: pd.DataFrame


def choose_k(X: np.ndarray, k_range=range(2, 9), seed: int = 0) -> tuple[int, dict[int, float], dict[int, float]]:
    sil, bic = {}, {}
    for k in k_range:
        if k >= len(X):
            break
        labels = KMeans(n_clusters=k, n_init=10, random_state=seed).fit_predict(X)
        sample = min(len(X), 10_000)
        sil[k] = float(silhouette_score(X, labels, sample_size=sample, random_state=seed))
        bic[k] = float(GaussianMixture(n_components=k, random_state=seed).fit(X).bic(X))
    best = max(sil, key=sil.get)
    return best, sil, bic


def name_segments(centres_z: pd.DataFrame) -> dict[int, str]:
    """Rule-based names from standardised centres (rows: cluster id).

    Order matters: the most decision-relevant segments ("At risk", "Rising
    stars") are claimed first, each only if its centre is clearly away from the
    average (|z| > 0.5); everything else is described by volume and consistency.
    """
    names: dict[int, str] = {}
    remaining = set(centres_z.index)

    def take(cluster: int, name: str) -> None:
        names[cluster] = name
        remaining.discard(cluster)

    risk_score = centres_z["viewer_trend"] + centres_z["active_share"]
    at_risk = risk_score.idxmin()
    if risk_score[at_risk] < -0.5:
        take(at_risk, "At risk")

    rising = centres_z.loc[list(remaining), "viewer_trend"]
    if not rising.empty and rising.max() > 0.5:
        take(rising.idxmax(), "Rising stars")

    big = centres_z.loc[list(remaining), "log_avg_viewers"]
    if not big.empty and big.max() > 0.5:
        take(big.idxmax(), "Established")

    for c in sorted(remaining):
        row = centres_z.loc[c]
        if row["peak_hour_share"] > 1.0:
            names[c] = "Prime-time streamers"
        elif row["mean_hours_live"] > 0.5:
            names[c] = "High-volume streamers"
        elif row["active_share"] >= 0:
            names[c] = "Steady niche"
        else:
            names[c] = "Occasional"

    # Keep names unique so they can be used as labels.
    seen: dict[str, int] = {}
    for c in sorted(names):
        n = names[c]
        seen[n] = seen.get(n, 0) + 1
        if seen[n] > 1:
            names[c] = f"{n} {seen[n]}"
    return names


def segment(features: pd.DataFrame, k: int | None = None, seed: int = 0) -> SegmentationResult:
    if len(features) < 10:
        raise ValueError(f"need at least 10 creators to segment, got {len(features)}")
    scaler = StandardScaler()
    X = scaler.fit_transform(features[FEATURES].to_numpy(dtype=float))
    best_k, sil, bic = choose_k(X, seed=seed)
    k = k or best_k
    km = KMeans(n_clusters=k, n_init=10, random_state=seed).fit(X)

    centres_z = pd.DataFrame(km.cluster_centers_, columns=FEATURES)
    names = name_segments(centres_z)

    out = features.copy()
    out["cluster"] = km.labels_
    out["segment"] = out["cluster"].map(names)

    profiles = (
        out.groupby(["cluster", "segment"])
        .agg(
            creators=("user_id", "size"),
            avg_viewers=("log_avg_viewers", lambda s: float(np.expm1(s).median())),
            weekly_growth=("viewer_trend", "median"),
            active_share=("active_share", "mean"),
            hours_per_week=("mean_hours_live", "median"),
            peak_hour_share=("peak_hour_share", "mean"),
            categories=("mean_categories", "mean"),
        )
        .reset_index()
        .sort_values("creators", ascending=False)
    )
    profiles["share"] = profiles["creators"] / profiles["creators"].sum()
    return SegmentationResult(k=k, silhouette_by_k=sil, bic_by_k=bic, assignments=out, profiles=profiles)
