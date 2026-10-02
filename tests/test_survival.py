from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from livescope.survival import analyse, kaplan_meier, logrank, median_survival, survival_at


def test_kaplan_meier_textbook_example():
    # Durations 1,2,2,3,4 with the second 2 and the 4 censored.
    km = kaplan_meier([1, 2, 2, 3, 4], [1, 1, 0, 1, 0])
    s = dict(zip(km.time, km.survival, strict=True))
    assert s[1] == pytest.approx(4 / 5)
    assert s[2] == pytest.approx(4 / 5 * 3 / 4)
    assert s[3] == pytest.approx(4 / 5 * 3 / 4 * 1 / 2)
    assert s[4] == pytest.approx(s[3])  # censoring does not drop the curve
    assert survival_at(km, 2.5)["survival"] == pytest.approx(0.6)
    assert np.isnan(survival_at(km, 10)["survival"])
    assert median_survival(km) == 3


def test_matches_lifelines():
    lifelines = pytest.importorskip("lifelines")
    rng = np.random.default_rng(0)
    d, e = rng.integers(1, 10, 400), rng.random(400) < 0.6
    km = kaplan_meier(d, e)
    ref = lifelines.KaplanMeierFitter().fit(d, e)
    expected = ref.survival_function_.loc[km.time].to_numpy().ravel()
    assert np.allclose(km.survival, expected)
    ci = ref.confidence_interval_.loc[km.time].to_numpy()
    assert np.allclose(km.ci_low, ci[:, 0]) and np.allclose(km.ci_high, ci[:, 1])


def test_logrank_matches_lifelines():
    stats_mod = pytest.importorskip("lifelines.statistics")
    rng = np.random.default_rng(1)
    d, e = rng.integers(1, 10, 300), rng.random(300) < 0.6
    g = rng.choice(["a", "b", "c"], 300)
    assert logrank(d, e, g)["p_value"] == pytest.approx(stats_mod.multivariate_logrank_test(d, g, e).p_value)


def test_logrank_detects_difference():
    rng = np.random.default_rng(2)
    fast = rng.geometric(0.5, 300)
    slow = rng.geometric(0.15, 300)
    d = np.r_[fast, slow]
    e = np.ones(600, bool)
    g = np.r_[["fast"] * 300, ["slow"] * 300]
    assert logrank(d, e, g)["p_value"] < 1e-6


def _lifetimes(n=200, seed=3):
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "user_id": [str(i) for i in range(n)],
        "founding_cohort": rng.random(n) < 0.3,
        "language_group": rng.choice(["English", "EU/EEA languages"], n),
        "duration_weeks": rng.integers(1, 9, n),
        "churned": rng.random(n) < 0.5,
    })


def test_analyse_groups_and_tests():
    res = analyse(_lifetimes())
    groups = set(res.curves.group)
    assert {"All newcomers", "Founding cohort", "Newcomers: English", "Newcomers: EU/EEA languages"} <= groups
    assert (res.curves.groupby("group").survival.first() == 1.0).all()  # every curve starts at 100%
    assert res.tests.comparison.str.contains("vs English").any()
    m = res.milestones[(res.milestones.group == "All newcomers") & (res.milestones.weeks == "4")]
    assert len(m) == 1 and 0 <= m.survival.iloc[0] <= 1


def test_analyse_without_data():
    with pytest.raises(ValueError):
        analyse(pd.DataFrame(columns=["founding_cohort", "language_group", "duration_weeks", "churned"]))
