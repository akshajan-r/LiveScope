"""CUPED (Deng et al., 2013): reduce metric variance with a pre-experiment covariate.

    y_adj = y - theta * (x - mean(x)),  theta = cov(x, y) / var(x)

theta is estimated on control and treatment pooled, which keeps the estimator
unbiased because assignment is independent of the pre-period covariate. The
variance falls by a factor of (1 - rho^2), where rho = corr(x, y).
"""

from __future__ import annotations

import numpy as np

from livescope.experiments.significance import Comparison, welch_ttest


def theta(y: np.ndarray, x: np.ndarray) -> float:
    x, y = np.asarray(x, float), np.asarray(y, float)
    var = x.var(ddof=1)
    return float(np.cov(x, y, ddof=1)[0, 1] / var) if var > 0 else 0.0


def adjust(y: np.ndarray, x: np.ndarray, th: float | None = None, x_mean: float | None = None) -> np.ndarray:
    x, y = np.asarray(x, float), np.asarray(y, float)
    th = theta(y, x) if th is None else th
    x_mean = x.mean() if x_mean is None else x_mean
    return y - th * (x - x_mean)


def cuped_ttest(
    y_control: np.ndarray,
    x_control: np.ndarray,
    y_treatment: np.ndarray,
    x_treatment: np.ndarray,
    alpha: float = 0.05,
    metric: str = "mean (CUPED)",
) -> tuple[Comparison, float]:
    """Welch test on CUPED-adjusted values. Returns (result, variance reduction)."""
    y = np.concatenate([y_control, y_treatment]).astype(float)
    x = np.concatenate([x_control, x_treatment]).astype(float)
    th, x_mean = theta(y, x), x.mean()
    adj_c = adjust(y_control, x_control, th, x_mean)
    adj_t = adjust(y_treatment, x_treatment, th, x_mean)
    raw_var = np.var(y_control, ddof=1) + np.var(y_treatment, ddof=1)
    adj_var = np.var(adj_c, ddof=1) + np.var(adj_t, ddof=1)
    reduction = 1 - adj_var / raw_var if raw_var > 0 else 0.0
    return welch_ttest(adj_c, adj_t, alpha=alpha, metric=metric), float(reduction)
