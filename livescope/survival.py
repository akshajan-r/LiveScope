"""Creator survival: Kaplan-Meier curves and log-rank tests on `creator_lifetime`.

Time is measured in weeks from a creator's cohort week (the week they first
entered the top list). The event is churn: no live week in the two most recent
complete weeks. Creators still streaming, or gone for less than two weeks, are
censored at the number of weeks observed, which is what Kaplan-Meier is for:
it uses the partial histories of recent cohorts instead of dropping them.

S(t) is the probability a creator is still streaming more than t weeks after
their cohort week.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
from scipy import stats

MILESTONES = (1, 2, 4, 8)


def kaplan_meier(durations, events, alpha: float = 0.05) -> pd.DataFrame:
    """Product-limit estimate with Greenwood variance and log-log CIs.

    Returns one row per distinct duration: time, at_risk, events, censored,
    survival, ci_low, ci_high. Durations are positive integers (weeks).
    """
    d = np.asarray(durations, dtype=float)
    e = np.asarray(events, dtype=bool)
    if d.size == 0:
        return pd.DataFrame(columns=["time", "at_risk", "events", "censored", "survival", "ci_low", "ci_high"])
    times = np.unique(d)
    z = stats.norm.ppf(1 - alpha / 2)
    rows = []
    s, greenwood = 1.0, 0.0
    for t in times:
        at_risk = int((d >= t).sum())
        n_events = int(((d == t) & e).sum())
        n_censored = int(((d == t) & ~e).sum())
        if n_events:
            s *= 1 - n_events / at_risk
            if at_risk > n_events:
                greenwood += n_events / (at_risk * (at_risk - n_events))
            else:
                greenwood = np.inf
        if 0 < s < 1 and np.isfinite(greenwood):
            # Log-log transformed interval stays inside [0, 1].
            se = np.sqrt(greenwood) / abs(np.log(s))
            lo, hi = s ** np.exp(z * se), s ** np.exp(-z * se)
        else:
            lo = hi = s
        rows.append({"time": int(t), "at_risk": at_risk, "events": n_events, "censored": n_censored,
                     "survival": s, "ci_low": lo, "ci_high": hi})
    return pd.DataFrame(rows)


def survival_at(km: pd.DataFrame, t: float) -> dict:
    """S(t) read off a KM table (step function, right-continuous)."""
    if km.empty:
        return {"survival": np.nan, "ci_low": np.nan, "ci_high": np.nan, "at_risk": 0}
    before = km[km["time"] <= t]
    if before.empty:
        return {"survival": 1.0, "ci_low": 1.0, "ci_high": 1.0, "at_risk": int(km["at_risk"].iloc[0])}
    row = before.iloc[-1]
    after = km[km["time"] > t]
    at_risk = int(after["at_risk"].iloc[0]) if not after.empty else 0
    # Beyond the longest follow-up the curve is undefined.
    if t > km["time"].max():
        return {"survival": np.nan, "ci_low": np.nan, "ci_high": np.nan, "at_risk": 0}
    return {"survival": float(row["survival"]), "ci_low": float(row["ci_low"]),
            "ci_high": float(row["ci_high"]), "at_risk": at_risk}


def median_survival(km: pd.DataFrame) -> float:
    below = km[km["survival"] <= 0.5]
    return float(below["time"].iloc[0]) if not below.empty else np.nan


def logrank(durations, events, groups) -> dict:
    """Log-rank test that all groups share one survival curve (chi-square, k-1 df)."""
    d = np.asarray(durations, dtype=float)
    e = np.asarray(events, dtype=bool)
    g = np.asarray(groups)
    labels = np.unique(g)
    k = len(labels)
    if k < 2:
        return {"chi2": np.nan, "dof": 0, "p_value": np.nan}
    observed = np.zeros(k)
    expected = np.zeros(k)
    cov = np.zeros((k, k))
    for t in np.unique(d[e]):
        at_risk = np.array([((d >= t) & (g == lab)).sum() for lab in labels], dtype=float)
        deaths = np.array([((d == t) & e & (g == lab)).sum() for lab in labels], dtype=float)
        n, dt = at_risk.sum(), deaths.sum()
        if n < 2:
            continue
        observed += deaths
        expected += dt * at_risk / n
        frac = at_risk / n
        cov += dt * (n - dt) / (n - 1) * (np.diag(frac) - np.outer(frac, frac))
    diff = (observed - expected)[:-1]
    v = cov[:-1, :-1]
    chi2 = float(diff @ np.linalg.pinv(v) @ diff)
    return {"chi2": chi2, "dof": k - 1, "p_value": float(stats.chi2.sf(chi2, k - 1)),
            "observed": dict(zip(labels.tolist(), observed.tolist(), strict=True)),
            "expected": dict(zip(labels.tolist(), expected.tolist(), strict=True))}


@dataclass
class SurvivalResult:
    curves: pd.DataFrame       # group, time, survival, ci_low, ci_high, at_risk
    milestones: pd.DataFrame   # group, weeks, survival, ci_low, ci_high, at_risk, creators
    tests: pd.DataFrame        # comparison, chi2, dof, p_value


def analyse(lifetime: pd.DataFrame, min_group: int = 20) -> SurvivalResult:
    """Curves for newcomers overall, newcomers by language group, and the
    founding cohort; log-rank tests for the language comparison."""
    if lifetime.empty:
        raise ValueError("no creator lifetimes yet (needs at least one complete week)")
    newcomers = lifetime[~lifetime["founding_cohort"]]
    groups: dict[str, pd.DataFrame] = {
        "All newcomers": newcomers,
        "Founding cohort": lifetime[lifetime["founding_cohort"]],
    }
    for name, part in newcomers.groupby("language_group"):
        groups[f"Newcomers: {name}"] = part

    curves, milestones = [], []
    for name, part in groups.items():
        if len(part) < min_group:
            continue
        km = kaplan_meier(part["duration_weeks"], part["churned"])
        start = pd.DataFrame([{"time": 0, "at_risk": len(part), "events": 0, "censored": 0,
                               "survival": 1.0, "ci_low": 1.0, "ci_high": 1.0}])
        curves.append(pd.concat([start, km], ignore_index=True).assign(group=name))
        for w in MILESTONES:
            milestones.append({"group": name, "weeks": w, "creators": len(part), **survival_at(km, w)})
        milestones.append({"group": name, "weeks": "median", "creators": len(part),
                           "survival": median_survival(km), "ci_low": np.nan, "ci_high": np.nan, "at_risk": np.nan})
    if not curves:
        raise ValueError(f"no group has {min_group}+ creators with a complete week yet")

    tests = []
    lang = newcomers[newcomers["language_group"].isin(["English", "EU/EEA languages"])]
    if lang["language_group"].nunique() == 2 and lang["language_group"].value_counts().min() >= min_group:
        tests.append({"comparison": "Newcomers: EU/EEA languages vs English",
                      **{k: v for k, v in logrank(lang["duration_weeks"], lang["churned"], lang["language_group"]).items()
                         if k in ("chi2", "dof", "p_value")}})
    multi = newcomers.groupby("language_group").filter(lambda g: len(g) >= min_group)
    if multi["language_group"].nunique() > 2:
        tests.append({"comparison": "Newcomers: all language groups",
                      **{k: v for k, v in logrank(multi["duration_weeks"], multi["churned"], multi["language_group"]).items()
                         if k in ("chi2", "dof", "p_value")}})

    ms = pd.DataFrame(milestones)
    ms["weeks"] = ms["weeks"].astype(str)
    return SurvivalResult(pd.concat(curves, ignore_index=True), ms, pd.DataFrame(tests))
