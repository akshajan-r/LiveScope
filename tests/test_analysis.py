from __future__ import annotations

import numpy as np
import pandas as pd
import pytest

from livescope.causal.did import did_2x2, peak_hours_did
from livescope.predict import FEATURES, build_dataset, evaluate, time_split
from livescope.segmentation import FEATURES as SEG_FEATURES
from livescope.segmentation import creator_features, name_segments, segment


def test_segmentation_on_demo(demo_creator_week):
    feats = creator_features(demo_creator_week)
    assert feats["weeks_active"].min() >= 2
    res = segment(feats)
    assert res.k == max(res.silhouette_by_k, key=res.silhouette_by_k.get)
    assert res.assignments["segment"].nunique() == res.k
    assert res.profiles["creators"].sum() == len(feats)


def test_segment_names_follow_centres():
    z = pd.DataFrame(0.0, index=range(3), columns=SEG_FEATURES)
    z.loc[0, ["viewer_trend", "active_share"]] = [-1.0, -1.0]
    z.loc[1, "viewer_trend"] = 1.2
    names = name_segments(z)
    assert names[0] == "At risk" and names[1] == "Rising stars"
    assert len(set(names.values())) == 3


def test_prediction_dataset_has_no_lookahead(demo_creator_week):
    df = build_dataset(demo_creator_week)
    # Labels come from week t+1; features must equal the creator's own week-t row.
    row = df.iloc[0]
    src = demo_creator_week[(demo_creator_week.user_id == row.user_id) & (demo_creator_week.week_index == row.week_index)].iloc[0]
    assert row.hours_live == src.hours_live
    nxt = demo_creator_week[(demo_creator_week.user_id == row.user_id) & (demo_creator_week.week_index == row.week_index + 1)]
    expected_next = nxt.viewer_hours.iloc[0] if len(nxt) else 0.0
    assert row.next_viewer_hours == expected_next
    assert row.churn == int(len(nxt) == 0)
    assert df[FEATURES].notna().all().all()
    train, test = time_split(df)
    assert train.week_index.max() < test.week_index.min()


def test_models_beat_base_rate_on_demo(demo_creator_week):
    rep = evaluate(build_dataset(demo_creator_week), target="growth")
    m = rep.metrics.set_index("model")
    assert m.loc["base_rate", "roc_auc"] == pytest.approx(0.5)
    assert m.loc["logistic_regression", "roc_auc"] > 0.6
    assert len(rep.importance) == len(FEATURES)


def _panel(effect, pre_trend=0.0, n=300, seed=0):
    rng = np.random.default_rng(seed)
    rows = []
    for u in range(n):
        treated = u < n // 3
        base = rng.normal(4, 1)
        for w in range(6):
            post = w >= 3
            share = (0.7 if treated and post else 0.2) + rng.normal(0, 0.01)
            y = base + 0.02 * w + (pre_trend * w if treated else 0) + (effect if treated and post else 0) + rng.normal(0, 0.2)
            rows.append({"user_id": str(u), "week_index": w, "is_complete_week": True,
                         "peak_hour_share": share, "avg_viewers": np.expm1(y)})
    return pd.DataFrame(rows)


def test_did_recovers_planted_effect():
    res = peak_hours_did(_panel(0.15), event_week_index=3)
    assert res.n_treated == 100 and res.n_control == 200
    assert res.did["ci_low"] < 0.15 < res.did["ci_high"]
    assert res.pretrend_p_value > 0.01
    pre = res.event_study[res.event_study.rel_week < -1]
    assert (pre.ci_low < 0).all() and (pre.ci_high > 0).all()


def test_did_null_effect_and_pretrend_detection():
    res = peak_hours_did(_panel(0.0), event_week_index=3)
    assert res.did["ci_low"] < 0 < res.did["ci_high"]
    trending = peak_hours_did(_panel(0.0, pre_trend=0.1), event_week_index=3)
    assert trending.pretrend_p_value < 0.01


def test_did_2x2_exact_on_noiseless_data():
    df = pd.DataFrame({
        "unit": ["a", "a", "b", "b", "c", "c", "d", "d"],
        "treated": [True, True, True, True, False, False, False, False],
        "post": [False, True] * 4,
        "y": [1.0, 3.0, 2.0, 4.0, 1.0, 2.0, 3.0, 4.0],
    })
    assert did_2x2(df, "y", "unit", "treated", "post")["estimate"] == pytest.approx(1.0)
