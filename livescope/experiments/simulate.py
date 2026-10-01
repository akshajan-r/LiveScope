"""Simulated experiments used to validate the toolkit.

If the tests are implemented correctly then, over many simulated A/A tests,
about `alpha` of them come out significant (false-positive rate), and over many
A/B tests sized with `power.py`, about `power` of them do (empirical power).
CUPED should keep the false-positive rate and raise the power.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

from livescope.experiments.cuped import cuped_ttest
from livescope.experiments.power import sample_size_means, sample_size_proportions
from livescope.experiments.significance import two_proportion_ztest, welch_ttest


def simulate_continuous(
    n_per_group: int, effect: float = 0.0, mean: float = 30.0, sd: float = 10.0, rho: float = 0.6, rng=None
) -> pd.DataFrame:
    """Users with a pre-period metric `pre` and an in-experiment metric `post`
    (think: minutes watched per user) correlated at `rho`."""
    rng = rng or np.random.default_rng()
    n = 2 * n_per_group
    group = np.repeat(["control", "treatment"], n_per_group)
    pre = rng.normal(mean, sd, n)
    noise = rng.normal(0, sd * np.sqrt(1 - rho**2), n)
    post = mean + rho * (pre - mean) + noise + effect * (group == "treatment")
    return pd.DataFrame({"group": group, "pre": pre, "post": post})


def simulate_binary(n_per_group: int, p_control: float, p_treatment: float, rng=None) -> tuple[int, int]:
    rng = rng or np.random.default_rng()
    return int(rng.binomial(n_per_group, p_control)), int(rng.binomial(n_per_group, p_treatment))


def validate(n_sims: int = 1000, alpha: float = 0.05, power: float = 0.8, seed: int = 42) -> pd.DataFrame:
    """Return empirical vs nominal rates for each test."""
    rng = np.random.default_rng(seed)
    rows = []

    # Continuous metric: effect = 1 unit on sd = 10, rho = 0.6.
    sd, effect, rho = 10.0, 1.0, 0.6
    n, _ = sample_size_means(sd, effect, alpha, power)
    hits = {"aa_raw": 0, "aa_cuped": 0, "ab_raw": 0, "ab_cuped": 0}
    reductions = []
    for _ in range(n_sims):
        for kind, eff in (("aa", 0.0), ("ab", effect)):
            d = simulate_continuous(n, eff, sd=sd, rho=rho, rng=rng)
            c, t = d[d.group == "control"], d[d.group == "treatment"]
            hits[f"{kind}_raw"] += welch_ttest(c.post, t.post, alpha).significant
            res, red = cuped_ttest(c.post, c.pre, t.post, t.pre, alpha)
            hits[f"{kind}_cuped"] += res.significant
            reductions.append(red)
    rows += [
        {"test": "welch t-test", "scenario": "A/A", "nominal": alpha, "empirical": hits["aa_raw"] / n_sims, "n_per_group": n},
        {"test": "welch t-test", "scenario": "A/B", "nominal": power, "empirical": hits["ab_raw"] / n_sims, "n_per_group": n},
        {"test": "CUPED t-test", "scenario": "A/A", "nominal": alpha, "empirical": hits["aa_cuped"] / n_sims, "n_per_group": n},
        {"test": "CUPED t-test", "scenario": "A/B", "nominal": None, "empirical": hits["ab_cuped"] / n_sims, "n_per_group": n},
        {"test": "CUPED variance reduction", "scenario": "both", "nominal": rho**2, "empirical": float(np.mean(reductions)), "n_per_group": n},
    ]

    # Binary metric: 10% -> 11% conversion.
    p1, p2 = 0.10, 0.11
    nb, _ = sample_size_proportions(p1, p2 - p1, alpha, power)
    aa = ab = 0
    for _ in range(n_sims):
        x1, x2 = simulate_binary(nb, p1, p1, rng)
        aa += two_proportion_ztest(x1, nb, x2, nb, alpha).significant
        x1, x2 = simulate_binary(nb, p1, p2, rng)
        ab += two_proportion_ztest(x1, nb, x2, nb, alpha).significant
    rows += [
        {"test": "two-proportion z-test", "scenario": "A/A", "nominal": alpha, "empirical": aa / n_sims, "n_per_group": nb},
        {"test": "two-proportion z-test", "scenario": "A/B", "nominal": power, "empirical": ab / n_sims, "n_per_group": nb},
    ]
    return pd.DataFrame(rows)
