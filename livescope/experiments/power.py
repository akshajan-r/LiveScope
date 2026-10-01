"""Power and sample-size calculations for two-group experiments (normal approximation)."""

from __future__ import annotations

import math

from scipy import optimize, stats


def _z(alpha: float, two_sided: bool) -> float:
    return stats.norm.ppf(1 - alpha / 2) if two_sided else stats.norm.ppf(1 - alpha)


def sample_size_proportions(
    p_control: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.8,
    ratio: float = 1.0,
    relative: bool = False,
    two_sided: bool = True,
) -> tuple[int, int]:
    """Users needed per group to detect a change of `mde` in a conversion rate.

    `mde` is absolute (0.01 = +1 percentage point) unless `relative=True`
    (0.05 = +5% of p_control). `ratio` = n_treatment / n_control.
    Returns (n_control, n_treatment), rounded up.
    """
    p2 = p_control * (1 + mde) if relative else p_control + mde
    if not 0 < p_control < 1 or not 0 < p2 < 1:
        raise ValueError("rates must be strictly between 0 and 1")
    delta = abs(p2 - p_control)
    p_bar = (p_control + ratio * p2) / (1 + ratio)
    z_a, z_b = _z(alpha, two_sided), stats.norm.ppf(power)
    num = z_a * math.sqrt(p_bar * (1 - p_bar) * (1 + 1 / ratio)) + z_b * math.sqrt(
        p_control * (1 - p_control) + p2 * (1 - p2) / ratio
    )
    n1 = math.ceil((num / delta) ** 2)
    return n1, math.ceil(n1 * ratio)


def sample_size_means(
    sd: float,
    mde: float,
    alpha: float = 0.05,
    power: float = 0.8,
    ratio: float = 1.0,
    two_sided: bool = True,
    variance_reduction: float = 0.0,
) -> tuple[int, int]:
    """Users per group to detect an absolute difference `mde` in a mean.

    `variance_reduction` is the expected CUPED reduction (rho^2 between the
    pre-period covariate and the metric); it shrinks the variance accordingly.
    """
    var = sd**2 * (1 - variance_reduction)
    z = _z(alpha, two_sided) + stats.norm.ppf(power)
    n1 = math.ceil(z**2 * var * (1 + 1 / ratio) / mde**2)
    return n1, math.ceil(n1 * ratio)


def power_proportions(p_control: float, p_treatment: float, n_control: int, n_treatment: int, alpha: float = 0.05) -> float:
    """Power of a two-sided two-proportion z-test."""
    se1 = math.sqrt(p_control * (1 - p_control) / n_control + p_treatment * (1 - p_treatment) / n_treatment)
    p_bar = (p_control * n_control + p_treatment * n_treatment) / (n_control + n_treatment)
    se0 = math.sqrt(p_bar * (1 - p_bar) * (1 / n_control + 1 / n_treatment))
    z_a = _z(alpha, True)
    d = abs(p_treatment - p_control)
    return float(stats.norm.cdf((d - z_a * se0) / se1) + stats.norm.cdf((-d - z_a * se0) / se1))


def mde_proportions(p_control: float, n_per_group: int, alpha: float = 0.05, power: float = 0.8) -> float:
    """Smallest absolute uplift detectable with `n_per_group` users per group."""
    f = lambda d: power_proportions(p_control, p_control + d, n_per_group, n_per_group, alpha) - power  # noqa: E731
    return float(optimize.brentq(f, 1e-9, 1 - p_control - 1e-9))


def duration_days(n_total: int, daily_eligible_users: float, traffic_share: float = 1.0) -> int:
    """Days needed to enrol `n_total` users. Round up to whole weeks in practice."""
    return math.ceil(n_total / (daily_eligible_users * traffic_share))
