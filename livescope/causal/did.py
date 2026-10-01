"""Difference-in-differences for a natural experiment on the creator-week panel.

Question: when a creator moves more of their streaming into platform peak
hours, does their average audience change?

This is observational. Creators choose to move, so the estimate is only
credible if treated and control creators were on parallel trends before the
move; `event_study` estimates the week-by-week gaps so that can be checked.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm


def _ols_cluster(y: np.ndarray, X: pd.DataFrame, groups: np.ndarray):
    return sm.OLS(y, X).fit(cov_type="cluster", cov_kwds={"groups": groups})


def did_2x2(df: pd.DataFrame, outcome: str, unit: str, treated: str, post: str) -> dict:
    """Classic 2x2 DiD on unit-period means, SEs clustered by unit."""
    agg = df.groupby([unit, treated, post], as_index=False)[outcome].mean()
    X = pd.DataFrame(
        {
            "const": 1.0,
            "treated": agg[treated].astype(float),
            "post": agg[post].astype(float),
            "treated_x_post": (agg[treated] & agg[post]).astype(float),
        }
    )
    fit = _ols_cluster(agg[outcome].to_numpy(float), X, agg[unit].to_numpy())
    est, se = fit.params["treated_x_post"], fit.bse["treated_x_post"]
    lo, hi = fit.conf_int().loc["treated_x_post"]
    return {"estimate": float(est), "se": float(se), "ci_low": float(lo), "ci_high": float(hi),
            "p_value": float(fit.pvalues["treated_x_post"])}


def event_study(df: pd.DataFrame, outcome: str, unit: str, time: str, treated: str, event_time: int, ref: int = -1) -> pd.DataFrame:
    """Treated x relative-week coefficients with unit and week fixed effects.

    Unit fixed effects are absorbed by demeaning every variable within unit,
    which by Frisch-Waugh-Lovell gives the same coefficients as unit dummies.
    """
    d = df[[unit, time, treated, outcome]].copy()
    d["rel"] = d[time] - event_time
    rels = sorted(r for r in d["rel"].unique() if r != ref)
    X = pd.DataFrame(index=d.index)
    for r in rels:
        X[f"treat_rel_{r}"] = ((d["rel"] == r) & d[treated]).astype(float)
    weeks = pd.get_dummies(d[time], prefix="week", drop_first=True, dtype=float)
    X = pd.concat([X, weeks], axis=1)
    y = d[outcome].astype(float)
    g = d[unit]
    y_dm = y - y.groupby(g).transform("mean")
    X_dm = X - X.groupby(g).transform("mean")
    X_dm = X_dm.loc[:, X_dm.abs().sum() > 0]
    fit = _ols_cluster(y_dm.to_numpy(), X_dm, g.to_numpy())
    ci = fit.conf_int()
    rows = [{"rel_week": ref, "estimate": 0.0, "ci_low": 0.0, "ci_high": 0.0}]
    for r in rels:
        name = f"treat_rel_{r}"
        if name in fit.params:
            rows.append({"rel_week": r, "estimate": fit.params[name], "ci_low": ci.loc[name, 0], "ci_high": ci.loc[name, 1]})
    return pd.DataFrame(rows).sort_values("rel_week").reset_index(drop=True)


@dataclass
class PeakHoursDiD:
    event_week_index: int
    n_treated: int
    n_control: int
    did: dict
    event_study: pd.DataFrame
    pretrend_p_value: float
    panel: pd.DataFrame


def peak_hours_did(
    creator_week: pd.DataFrame,
    event_week_index: int | None = None,
    window: int = 3,
    min_weeks_each_side: int = 2,
    treat_shift: float = 0.25,
    control_band: float = 0.05,
) -> PeakHoursDiD:
    """Treated: creators whose share of live hours in peak hours rose by at least
    `treat_shift` from the `window` weeks before `event_week_index` to the
    `window` weeks from it on. Control: share moved by less than `control_band`.
    Outcome: log(1 + average viewers).
    """
    cw = creator_week[creator_week["is_complete_week"]].copy()
    weeks = np.sort(cw["week_index"].unique())
    if len(weeks) < 2 * window:
        raise ValueError(f"need {2 * window} complete weeks, have {len(weeks)}")
    if event_week_index is None:
        event_week_index = int(weeks[len(weeks) // 2])
    lo, hi = event_week_index - window, event_week_index + window
    cw = cw[(cw["week_index"] >= lo) & (cw["week_index"] < hi)]
    cw["post"] = cw["week_index"] >= event_week_index
    cw["log_viewers"] = np.log1p(cw["avg_viewers"])

    side = cw.groupby(["user_id", "post"]).agg(weeks=("week_index", "size"), share=("peak_hour_share", "mean")).unstack("post")
    side = side.dropna()
    side = side[(side[("weeks", False)] >= min_weeks_each_side) & (side[("weeks", True)] >= min_weeks_each_side)]
    shift = side[("share", True)] - side[("share", False)]
    treated_ids = set(shift[shift >= treat_shift].index)
    control_ids = set(shift[shift.abs() < control_band].index)

    panel = cw[cw["user_id"].isin(treated_ids | control_ids)].copy()
    panel["treated"] = panel["user_id"].isin(treated_ids)
    if not treated_ids or not control_ids:
        raise ValueError("no treated or no control creators with these thresholds")

    did = did_2x2(panel, "log_viewers", "user_id", "treated", "post")
    did["pct_effect"] = float(np.expm1(did["estimate"]))
    es = event_study(panel, "log_viewers", "user_id", "week_index", "treated", event_week_index)

    # Joint test that all pre-period coefficients are zero (parallel pre-trends).
    pre = es[es["rel_week"] < -1]
    pretrend_p = _pretrend_test(panel, event_week_index) if len(pre) else float("nan")
    return PeakHoursDiD(event_week_index, len(treated_ids), len(control_ids), did, es, pretrend_p, panel)


def _pretrend_test(panel: pd.DataFrame, event_week_index: int) -> float:
    """Pre-period only: does the treated-control gap trend over time?"""
    pre = panel[~panel["post"]].copy()
    if pre["week_index"].nunique() < 2:
        return float("nan")
    t = pre["week_index"] - event_week_index
    X = pd.DataFrame({"const": 1.0, "treated": pre["treated"].astype(float), "t": t.astype(float),
                      "treated_x_t": (pre["treated"] * t).astype(float)})
    fit = _ols_cluster(pre["log_viewers"].to_numpy(float), X, pre["user_id"].to_numpy())
    return float(fit.pvalues["treated_x_t"])
