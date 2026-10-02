from __future__ import annotations

import numpy as np
import pandas as pd
import pytest
from statsmodels.stats.power import NormalIndPower
from statsmodels.stats.proportion import proportion_effectsize, proportions_ztest

from livescope.experiments.analyze import Guardrail, analyze_experiment
from livescope.experiments.cuped import cuped_ttest, theta
from livescope.experiments.power import (
    duration_days, mde_proportions, power_proportions, sample_size_means, sample_size_proportions,
)
from livescope.experiments.significance import non_inferiority, srm_check, two_proportion_ztest, welch_ttest
from livescope.experiments.simulate import simulate_continuous, validate


def test_ztest_matches_statsmodels():
    res = two_proportion_ztest(480, 5000, 545, 5000)
    z, p = proportions_ztest([545, 480], [5000, 5000])
    assert res.stat == pytest.approx(z)
    assert res.p_value == pytest.approx(p)
    assert res.ci_low < res.diff < res.ci_high


def test_welch_matches_scipy():
    from scipy import stats

    rng = np.random.default_rng(0)
    a, b = rng.normal(10, 2, 300), rng.normal(10.4, 3, 250)
    res = welch_ttest(a, b)
    t, p = stats.ttest_ind(b, a, equal_var=False)
    assert res.stat == pytest.approx(t) and res.p_value == pytest.approx(p)


def test_sample_size_proportions_close_to_statsmodels():
    n, n2 = sample_size_proportions(0.10, 0.01)
    es = proportion_effectsize(0.11, 0.10)
    sm_n = NormalIndPower().solve_power(es, alpha=0.05, power=0.8)
    assert n == n2
    assert abs(n - sm_n) / sm_n < 0.02  # arcsine vs. Wald approximations differ slightly
    assert power_proportions(0.10, 0.11, n, n) == pytest.approx(0.8, abs=0.01)
    assert sample_size_proportions(0.10, 0.10, relative=True) == (n, n)


def test_unequal_split_and_mde():
    n1, n2 = sample_size_proportions(0.2, 0.02, ratio=2)
    assert n2 == pytest.approx(2 * n1, abs=1)
    mde = mde_proportions(0.10, 14751)
    assert mde == pytest.approx(0.01, rel=0.02)


def test_sample_size_means_and_cuped_reduction():
    n, _ = sample_size_means(sd=10, mde=1)
    assert n == 1570
    n_cuped, _ = sample_size_means(sd=10, mde=1, variance_reduction=0.36)
    assert n_cuped == pytest.approx(n * 0.64, rel=0.01)
    assert duration_days(10_000, daily_eligible_users=1000, traffic_share=0.5) == 20


def test_cuped_reduces_variance_and_stays_unbiased():
    rng = np.random.default_rng(1)
    d = simulate_continuous(5000, effect=0.5, rho=0.7, rng=rng)
    c, t = d[d.group == "control"], d[d.group == "treatment"]
    raw = welch_ttest(c.post, t.post)
    adj, reduction = cuped_ttest(c.post, c.pre, t.post, t.pre)
    assert reduction == pytest.approx(0.49, abs=0.05)
    assert adj.ci_high - adj.ci_low < raw.ci_high - raw.ci_low
    assert adj.ci_low < 0.5 < adj.ci_high
    assert theta(d.post, d.pre) == pytest.approx(0.7, abs=0.05)


def test_srm_and_guardrail():
    assert srm_check(5000, 5000)["mismatch"] is False
    assert srm_check(5000, 5400)["mismatch"] is True
    res = welch_ttest(np.r_[np.zeros(500), np.ones(500)], np.r_[np.zeros(510), np.ones(490)])
    assert non_inferiority(res, margin=0.1)["passed"] is True
    assert non_inferiority(res, margin=0.001)["passed"] is False


def test_analyze_experiment_decisions():
    rng = np.random.default_rng(2)
    d = simulate_continuous(4000, effect=1.0, rng=rng)
    d["crash"] = rng.binomial(1, 0.02, len(d))
    out = analyze_experiment(d, "post", pre_period="pre", guardrails=[Guardrail("crash", 0.01, higher_is_better=False)])
    assert out["decision"].startswith("ship")
    assert out["primary_cuped"]["variance_reduction"] > 0.2

    bad = pd.concat([d, d[d.group == "treatment"].head(400)])
    assert analyze_experiment(bad, "post")["decision"].startswith("invalid")


def test_simulation_validation_rates():
    v = validate(n_sims=300, seed=5).set_index(["test", "scenario"])
    for test in ("welch t-test", "CUPED t-test", "two-proportion z-test"):
        assert v.loc[(test, "A/A"), "empirical"] < 0.10
    assert v.loc[("welch t-test", "A/B"), "empirical"] == pytest.approx(0.8, abs=0.08)
    assert v.loc[("two-proportion z-test", "A/B"), "empirical"] == pytest.approx(0.8, abs=0.08)
    assert v.loc[("CUPED t-test", "A/B"), "empirical"] > v.loc[("welch t-test", "A/B"), "empirical"]
