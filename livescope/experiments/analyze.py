"""One-call analysis of a two-group experiment: SRM, primary metric (raw and
CUPED), guardrails, and a ship / don't ship / inconclusive call."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd

from livescope.experiments.cuped import cuped_ttest
from livescope.experiments.significance import non_inferiority, srm_check, two_proportion_ztest, welch_ttest


@dataclass
class Guardrail:
    metric: str
    margin: float  # largest acceptable harm, in the metric's absolute units
    higher_is_better: bool = True


def analyze_experiment(
    df: pd.DataFrame,
    primary: str,
    group_col: str = "group",
    control: str = "control",
    treatment: str = "treatment",
    pre_period: str | None = None,
    binary: bool = False,
    guardrails: list[Guardrail] | None = None,
    expected_share_treatment: float = 0.5,
    alpha: float = 0.05,
) -> dict:
    c = df[df[group_col] == control]
    t = df[df[group_col] == treatment]
    out: dict = {"n_control": len(c), "n_treatment": len(t)}
    out["srm"] = srm_check(len(c), len(t), expected_share_treatment)

    if binary:
        res = two_proportion_ztest(int(c[primary].sum()), len(c), int(t[primary].sum()), len(t), alpha, primary)
    else:
        res = welch_ttest(c[primary].to_numpy(), t[primary].to_numpy(), alpha, primary)
    out["primary"] = res.as_dict()

    decisive = res
    if pre_period is not None and not binary:
        adj, reduction = cuped_ttest(
            c[primary].to_numpy(), c[pre_period].to_numpy(), t[primary].to_numpy(), t[pre_period].to_numpy(), alpha,
            f"{primary} (CUPED)",
        )
        out["primary_cuped"] = {**adj.as_dict(), "variance_reduction": reduction}
        decisive = adj

    out["guardrails"] = []
    for g in guardrails or []:
        values = df[g.metric].dropna()
        is_binary = set(np.unique(values)) <= {0, 1}
        if is_binary:
            gr = two_proportion_ztest(int(c[g.metric].sum()), len(c), int(t[g.metric].sum()), len(t), alpha, g.metric)
        else:
            gr = welch_ttest(c[g.metric].to_numpy(), t[g.metric].to_numpy(), alpha, g.metric)
        out["guardrails"].append(non_inferiority(gr, g.margin, g.higher_is_better))

    if out["srm"]["mismatch"]:
        decision = "invalid: sample ratio mismatch, fix assignment before reading results"
    elif any(not g["passed"] for g in out["guardrails"]):
        decision = "don't ship: a guardrail could not rule out harm"
    elif decisive.significant and decisive.diff > 0:
        decision = "ship: primary metric improved and guardrails held"
    elif decisive.significant and decisive.diff < 0:
        decision = "don't ship: primary metric got worse"
    else:
        decision = "inconclusive: no significant change in the primary metric"
    out["decision"] = decision
    return out
