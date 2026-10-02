"""Pre-registration numbers and the final readout for a real A/B test."""

from __future__ import annotations

import math

import pandas as pd

from livescope.experiments.analyze import Guardrail, analyze_experiment
from livescope.experiments.power import mde_proportions, sample_size_proportions


def plan(baseline: float, mde: float, daily_users: float, relative: bool = True, alpha: float = 0.05,
         power: float = 0.8, traffic_share: float = 1.0) -> dict:
    """Sample size and duration for a conversion-rate test, rounded up to whole weeks,
    plus the effect that is detectable if the test is capped at 2 or 4 weeks."""
    n, _ = sample_size_proportions(baseline, mde, alpha, power, relative=relative)
    per_day = daily_users * traffic_share
    days = math.ceil(2 * n / per_day)
    weeks = max(2, math.ceil(days / 7))
    capped = {}
    for w in (2, 4):
        n_w = int(per_day * 7 * w / 2)
        try:
            capped[f"mde_abs_{w}_weeks"] = mde_proportions(baseline, n_w, alpha, power) if n_w > 0 else math.nan
        except ValueError:
            capped[f"mde_abs_{w}_weeks"] = math.nan
    return {"baseline": baseline, "mde": mde, "relative": relative, "n_per_group": n, "days_needed": days,
            "weeks_to_run": weeks, "daily_users_in_test": per_day, **capped}


def readout(users: pd.DataFrame, control: str = "control", treatment: str = "test", primary: str = "converted",
            guardrails: list[Guardrail] | None = None, alpha: float = 0.05) -> dict:
    df = users.rename(columns={"variant": "group"})
    binary = set(df[primary].unique()) <= {0, 1}
    use_pre = "pre_count" in df and df["pre_count"].var() > 0
    out = analyze_experiment(df, primary, control=control, treatment=treatment, binary=binary,
                             pre_period="pre_count" if use_pre else None, guardrails=guardrails, alpha=alpha)
    if binary:
        n = min(out["n_control"], out["n_treatment"])
        p = out["primary"]["control"]
        try:
            out["detectable_abs_lift"] = mde_proportions(p, n, alpha) if 0 < p < 1 and n > 0 else math.nan
        except ValueError:
            out["detectable_abs_lift"] = math.nan
    return out


def to_markdown(name: str, out: dict, quality: dict | None = None, period: str = "") -> str:
    p = out["primary"]
    pct = lambda x: f"{x * 100:.2f}%"  # noqa: E731
    lines = [f"# Experiment readout: {name}", ""]
    if period:
        lines += [f"Period: {period}", ""]
    lines += [f"**Decision: {out['decision']}**", "", "## Sample", "",
              f"- Control: {out['n_control']:,} people; treatment: {out['n_treatment']:,} people",
              f"- Sample ratio check: p = {out['srm']['p_value']:.3f} ({'MISMATCH' if out['srm']['mismatch'] else 'ok'})"]
    if quality:
        lines.append(f"- People shown both variants and dropped: {quality['mixed_variant_people_dropped']:,}")
    lines += ["", "## Primary metric", "", "| | Control | Treatment | Difference | 95% CI | p-value |", "|---|---|---|---|---|---|",
              f"| {p['metric']} | {pct(p['control'])} | {pct(p['treatment'])} | {pct(p['diff'])} | {pct(p['ci_low'])} to {pct(p['ci_high'])} | {p['p_value']:.3f} |"]
    if "primary_cuped" in out:
        c = out["primary_cuped"]
        lines.append(f"| {c['metric']} | | | {pct(c['diff'])} | {pct(c['ci_low'])} to {pct(c['ci_high'])} | {c['p_value']:.3f} |")
        lines += ["", f"CUPED used each person's pre-period count as the covariate and removed {c['variance_reduction'] * 100:.0f}% of the variance."]
    if not math.isnan(out.get("detectable_abs_lift", math.nan)):
        lines += ["", f"With this sample the test could detect an absolute change of about {pct(out['detectable_abs_lift'])} "
                      f"(80% power). Smaller true effects would usually come out inconclusive."]
    if out["guardrails"]:
        lines += ["", "## Guardrails", "", "| Metric | Margin | 95% CI of difference | Result |", "|---|---|---|---|"]
        for g in out["guardrails"]:
            lines.append(f"| {g['metric']} | {g['margin']} | {g['ci_low']:.4f} to {g['ci_high']:.4f} | {'pass' if g['passed'] else 'FAIL'} |")
    return "\n".join(lines) + "\n"
