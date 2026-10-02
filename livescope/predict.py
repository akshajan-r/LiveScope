"""Predict next-week creator growth (or drop-off) from creator-week features.

Unit of prediction: a creator who was live in complete week t.
Targets (both defined on week t+1, which must also be a complete week):
  growth: viewer_hours(t+1) >= (1 + threshold) * viewer_hours(t). A creator who
          is not live in t+1 has 0 viewer hours, so drop-off counts as no growth.
  churn:  the creator is not live at all in t+1.

Evaluation uses a time-based split: the last `test_weeks` prediction weeks are
held out, so the model never trains on weeks after the ones it is scored on.
"""

from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np
import pandas as pd
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score, brier_score_loss, roc_auc_score
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

FEATURES = [
    "log_avg_viewers",
    "log_viewer_hours",
    "log_peak_viewers",
    "hours_live",
    "live_share",
    "days_live",
    "streams",
    "categories",
    "peak_hour_share",
    "top_list_share",
    "wow_avg_viewers_growth",
    "wow_hours_growth",
    "wow_viewer_hours_growth",
    "has_prev_week",
    "streak_weeks",
    "weeks_active_to_date",
    "rolling3_log_viewer_hours",
]


def build_dataset(creator_week: pd.DataFrame, threshold: float = 0.10) -> pd.DataFrame:
    cw = creator_week.sort_values(["user_id", "week_index"]).copy()
    complete_weeks = set(cw.loc[cw["is_complete_week"], "week_index"])

    cw["log_avg_viewers"] = np.log1p(cw["avg_viewers"])
    cw["log_viewer_hours"] = np.log1p(cw["viewer_hours"])
    cw["log_peak_viewers"] = np.log1p(cw["peak_viewers"])
    cw["has_prev_week"] = cw["wow_avg_viewers_growth"].notna().astype(int)
    for col in ("wow_avg_viewers_growth", "wow_hours_growth", "wow_viewer_hours_growth"):
        # Growth ratios are heavy-tailed; clip so one tiny base does not dominate.
        cw[col] = cw[col].fillna(0.0).clip(-1, 5)
    # Rolling mean over the creator's last 3 calendar weeks (inactive weeks count as 0).
    cw["rolling3_log_viewer_hours"] = _rolling_calendar_mean(cw, "log_viewer_hours", 3)

    nxt = cw[["user_id", "week_index", "viewer_hours"]].rename(columns={"viewer_hours": "next_viewer_hours"})
    nxt["week_index"] -= 1
    df = cw.merge(nxt, on=["user_id", "week_index"], how="left")

    eligible = df["week_index"].isin(complete_weeks) & (df["week_index"] + 1).isin(complete_weeks)
    df = df[eligible].copy()
    df["next_active"] = df["next_viewer_hours"].notna()
    df["next_viewer_hours"] = df["next_viewer_hours"].fillna(0.0)
    df["growth"] = (df["next_viewer_hours"] >= (1 + threshold) * df["viewer_hours"]).astype(int)
    df["churn"] = (~df["next_active"]).astype(int)
    return df.reset_index(drop=True)


def _rolling_calendar_mean(cw: pd.DataFrame, col: str, weeks: int) -> pd.Series:
    out = pd.Series(0.0, index=cw.index)
    for lag in range(weeks):
        shifted = cw[["user_id", "week_index", col]].copy()
        shifted["week_index"] += lag
        merged = cw[["user_id", "week_index"]].merge(shifted, on=["user_id", "week_index"], how="left")
        out += merged[col].fillna(0.0).to_numpy()
    return out / weeks


def time_split(df: pd.DataFrame, test_weeks: int = 2) -> tuple[pd.DataFrame, pd.DataFrame]:
    weeks = np.sort(df["week_index"].unique())
    if len(weeks) <= test_weeks:
        raise ValueError(f"need more than {test_weeks} prediction weeks, have {len(weeks)}")
    cutoff = weeks[-test_weeks]
    return df[df["week_index"] < cutoff], df[df["week_index"] >= cutoff]


def _gbm(seed: int):
    try:
        from lightgbm import LGBMClassifier

        return "lightgbm", LGBMClassifier(
            n_estimators=300, learning_rate=0.05, num_leaves=15, min_child_samples=20,
            subsample=0.8, subsample_freq=1, colsample_bytree=0.8, random_state=seed, verbose=-1,
        )
    except ImportError:  # pragma: no cover - lightgbm is an optional extra
        return "hist_gradient_boosting", HistGradientBoostingClassifier(max_iter=300, learning_rate=0.05, random_state=seed)


@dataclass
class ModelReport:
    target: str
    train_rows: int
    test_rows: int
    train_weeks: list[int]
    test_weeks: list[int]
    base_rate_test: float
    metrics: pd.DataFrame
    importance: pd.DataFrame
    predictions: pd.DataFrame = field(repr=False)


def _scores(y: np.ndarray, p: np.ndarray) -> dict[str, float]:
    return {
        "roc_auc": float(roc_auc_score(y, p)),
        "pr_auc": float(average_precision_score(y, p)),
        "brier": float(brier_score_loss(y, np.clip(p, 0, 1))),
    }


def evaluate(df: pd.DataFrame, target: str = "growth", test_weeks: int = 2, seed: int = 0) -> ModelReport:
    train, test = time_split(df, test_weeks)
    X_tr, y_tr = train[FEATURES].to_numpy(float), train[target].to_numpy()
    X_te, y_te = test[FEATURES].to_numpy(float), test[target].to_numpy()
    if len(np.unique(y_tr)) < 2 or len(np.unique(y_te)) < 2:
        raise ValueError("both classes must appear in train and test")

    rows = []
    preds = test[["user_id", "user_login", "week_start", target]].copy()

    # Baseline 1: predict the training base rate for everyone (AUC 0.5 by construction).
    p = np.full(len(y_te), y_tr.mean())
    rows.append({"model": "base_rate", **_scores(y_te, p)})

    # Baseline 2: momentum. Last week's growth as the score (for churn, fewer hours = riskier).
    momentum = test["wow_viewer_hours_growth"].to_numpy()
    if target == "churn":
        momentum = -test["hours_live"].to_numpy(float)
    m_scores = _scores(y_te, (momentum - momentum.min()) / (np.ptp(momentum) or 1))
    m_scores["brier"] = np.nan  # not a calibrated probability
    rows.append({"model": "momentum_rule", **m_scores})

    logit = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
    logit.fit(X_tr, y_tr)
    preds["p_logistic"] = logit.predict_proba(X_te)[:, 1]
    rows.append({"model": "logistic_regression", **_scores(y_te, preds["p_logistic"].to_numpy())})

    gbm_name, gbm = _gbm(seed)
    gbm.fit(pd.DataFrame(X_tr, columns=FEATURES), y_tr)
    X_te_df = pd.DataFrame(X_te, columns=FEATURES)
    preds["p_gbm"] = gbm.predict_proba(X_te_df)[:, 1]
    rows.append({"model": gbm_name, **_scores(y_te, preds["p_gbm"].to_numpy())})

    perm = permutation_importance(gbm, X_te_df, y_te, scoring="roc_auc", n_repeats=5, random_state=seed)
    importance = pd.DataFrame(
        {
            "feature": FEATURES,
            "permutation_auc_drop": perm.importances_mean,
            "permutation_std": perm.importances_std,
            "logistic_coef": logit[-1].coef_[0],
        }
    )
    if hasattr(gbm, "booster_"):
        gain = gbm.booster_.feature_importance(importance_type="gain")
        importance["gbm_gain_share"] = gain / gain.sum()
    importance = importance.sort_values("permutation_auc_drop", ascending=False).reset_index(drop=True)

    return ModelReport(
        target=target,
        train_rows=len(train),
        test_rows=len(test),
        train_weeks=sorted(int(w) for w in train["week_index"].unique()),
        test_weeks=sorted(int(w) for w in test["week_index"].unique()),
        base_rate_test=float(y_te.mean()),
        metrics=pd.DataFrame(rows),
        importance=importance,
        predictions=preds,
    )
