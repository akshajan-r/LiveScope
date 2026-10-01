"""Significance tests, sample-ratio-mismatch check and guardrail tests."""

from __future__ import annotations

import math
from dataclasses import asdict, dataclass

import numpy as np
from scipy import stats


@dataclass
class Comparison:
    metric: str
    control: float
    treatment: float
    diff: float
    rel_lift: float
    stat: float
    p_value: float
    ci_low: float
    ci_high: float
    alpha: float

    def __post_init__(self) -> None:
        # Plain floats, so results serialise cleanly (numpy scalars leak in otherwise).
        for name in ("control", "treatment", "diff", "rel_lift", "stat", "p_value", "ci_low", "ci_high", "alpha"):
            setattr(self, name, float(getattr(self, name)))

    @property
    def significant(self) -> bool:
        return bool(self.p_value < self.alpha)

    def as_dict(self) -> dict:
        return {**asdict(self), "significant": self.significant}


def two_proportion_ztest(
    x_control: int, n_control: int, x_treatment: int, n_treatment: int, alpha: float = 0.05, metric: str = "conversion"
) -> Comparison:
    """Two-sided z-test with pooled SE for the p-value and unpooled SE for the CI."""
    p1, p2 = x_control / n_control, x_treatment / n_treatment
    pooled = (x_control + x_treatment) / (n_control + n_treatment)
    se0 = math.sqrt(pooled * (1 - pooled) * (1 / n_control + 1 / n_treatment))
    se1 = math.sqrt(p1 * (1 - p1) / n_control + p2 * (1 - p2) / n_treatment)
    diff = p2 - p1
    z = diff / se0 if se0 > 0 else 0.0
    p = 2 * stats.norm.sf(abs(z))
    half = stats.norm.ppf(1 - alpha / 2) * se1
    return Comparison(metric, p1, p2, diff, diff / p1 if p1 else math.nan, z, p, diff - half, diff + half, alpha)


def welch_ttest(control: np.ndarray, treatment: np.ndarray, alpha: float = 0.05, metric: str = "mean") -> Comparison:
    """Welch's t-test for a difference in means, with a Welch-Satterthwaite CI."""
    a, b = np.asarray(control, float), np.asarray(treatment, float)
    va, vb = a.var(ddof=1) / len(a), b.var(ddof=1) / len(b)
    se = math.sqrt(va + vb)
    dof = (va + vb) ** 2 / (va**2 / (len(a) - 1) + vb**2 / (len(b) - 1))
    diff = b.mean() - a.mean()
    t = diff / se
    p = 2 * stats.t.sf(abs(t), dof)
    half = stats.t.ppf(1 - alpha / 2, dof) * se
    return Comparison(metric, a.mean(), b.mean(), diff, diff / a.mean() if a.mean() else math.nan, t, p, diff - half, diff + half, alpha)


def srm_check(n_control: int, n_treatment: int, expected_share_treatment: float = 0.5, threshold: float = 0.001) -> dict:
    """Sample ratio mismatch: chi-square goodness-of-fit on the assignment counts.

    A tiny p-value means the split is not what was configured, which usually
    signals a bug in assignment or logging; results should not be trusted.
    """
    total = n_control + n_treatment
    expected = [total * (1 - expected_share_treatment), total * expected_share_treatment]
    chi2, p = stats.chisquare([n_control, n_treatment], expected)
    return {"chi2": float(chi2), "p_value": float(p), "mismatch": bool(p < threshold)}


def non_inferiority(result: Comparison, margin: float, higher_is_better: bool = True) -> dict:
    """Guardrail check: is the treatment no worse than control by more than `margin`?

    Uses the two-sided (1 - alpha) CI, i.e. a one-sided test at alpha/2, which
    is the conservative convention. `margin` is in the metric's absolute units.
    """
    if higher_is_better:
        passed = result.ci_low > -margin
    else:
        passed = result.ci_high < margin
    return {"metric": result.metric, "margin": margin, "higher_is_better": higher_is_better, "passed": bool(passed),
            "ci_low": result.ci_low, "ci_high": result.ci_high}
