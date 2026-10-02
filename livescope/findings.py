"""Measured facts for the findings write-up.

Each fact is a sentence built from the latest build's numbers, or a "pending"
line saying what data it still needs. Nothing here makes a recommendation:
turning facts into advice is a judgement call left to the write-up in the
README, so the dashboard never states a conclusion the data has not earned.
"""

from __future__ import annotations

import math

import duckdb
import pandas as pd

MIN_CATEGORY_DAYS = 7


def _pct(x: float, digits: int = 0) -> str:
    return f"{x * 100:.{digits}f}%"


def _signed(x: float, digits: int = 0) -> str:
    return f"{'+' if x >= 0 else '−'}{abs(x) * 100:.{digits}f}%"


def _ok(x) -> bool:
    return x is not None and not (isinstance(x, float) and math.isnan(x))


def _fact(topic: str, text: str, page: str, measured: bool = True) -> dict:
    return {"topic": topic, "status": "measured" if measured else "pending", "text": text, "page": page}


def measured_facts(con: duckdb.DuckDBPyConnection, results: dict, analyses: dict) -> list[dict]:
    facts = []

    # North star.
    pw = con.execute("select * from platform_week order by week_start").df()
    if len(pw):
        last = pw.iloc[-1]
        wow = f", {_signed(last.viewer_hours_wow, 1)} on the week before" if _ok(last.viewer_hours_wow) else ""
        facts.append(_fact("North star",
                           f"Tracked creators drew {last.viewer_hours:,.0f} hours watched in the week of "
                           f"{pd.Timestamp(last.week_start):%d %b %Y}{wow}, across {last.active_creators:,} live creators.",
                           "/"))
    else:
        facts.append(_fact("North star", "Needs one complete week of collection.", "/", measured=False))

    # Retention / survival.
    ms = pd.DataFrame(results.get("survival_milestones", []))
    if not ms.empty:
        new = ms[(ms["group"] == "All newcomers")]
        shown = [r for _, r in new.iterrows() if r["weeks"] != "median" and _ok(r["survival"])]
        if shown:
            r = shown[-1]
            facts.append(_fact("Creator retention",
                               f"Of {int(r['creators']):,} creators who broke into the top list after collection began, "
                               f"{_pct(r['survival'])} (95% CI {_pct(r['ci_low'])}–{_pct(r['ci_high'])}) were still streaming "
                               f"{r['weeks']} week{'s' if r['weeks'] != '1' else ''} later (Kaplan–Meier; churn = two complete weeks without going live).",
                               "/retention"))
        eu = ms[(ms["group"] == "Newcomers: EU/EEA languages")]
        en = ms[(ms["group"] == "Newcomers: English")]
        common = sorted(set(eu.loc[eu["survival"].notna() & (eu["weeks"] != "median"), "weeks"])
                        & set(en.loc[en["survival"].notna() & (en["weeks"] != "median"), "weeks"]), key=int)
        tests = pd.DataFrame(results.get("survival_tests", []))
        if common:
            w = common[-1]
            a = eu[eu["weeks"] == w].iloc[0]
            b = en[en["weeks"] == w].iloc[0]
            p = tests.loc[tests["comparison"].str.contains("EU/EEA languages vs English"), "p_value"]
            ptxt = f" Log-rank p = {p.iloc[0]:.3f}." if len(p) else ""
            facts.append(_fact("EU vs English",
                               f"{w}-week survival of newcomers: {_pct(a['survival'])} for EU/EEA-language creators "
                               f"(n = {int(a['creators']):,}) vs {_pct(b['survival'])} for English (n = {int(b['creators']):,}).{ptxt}",
                               "/europe"))
        else:
            facts.append(_fact("EU vs English", "Needs at least 20 newcomers in each language group with a complete week.",
                               "/europe", measured=False))
    else:
        reason = analyses.get("survival", {}).get("reason", "needs complete weeks")
        facts.append(_fact("Creator retention", f"{reason[0].upper()}{reason[1:]}.", "/retention", measured=False))

    # EU share of the north star.
    lw = con.execute("""
        select language_group, sum(viewer_hours) as vh, sum(creator_hours) as ch
        from language_week
        where week_start = (select max(week_start) from language_week)
        group by 1
    """).df()
    if len(lw):
        total = lw["vh"].sum()
        eu = lw[lw["language_group"] == "EU/EEA languages"]
        en = lw[lw["language_group"] == "English"]
        if len(eu) and len(en) and total:
            facts.append(_fact("EU audience",
                               f"EU/EEA-language streams were {_pct(eu.vh.iloc[0] / total)} of hours watched in the latest complete week, "
                               f"averaging {eu.vh.iloc[0] / eu.ch.iloc[0]:,.0f} viewers per live hour vs {en.vh.iloc[0] / en.ch.iloc[0]:,.0f} for English.",
                               "/europe"))

    # Category opportunity. A few hours of data would rank categories on noise,
    # so wait for a full week.
    days = con.execute("select count(distinct snapshot_hour) / 24.0 from collector_hours").fetchone()[0]
    if days < MIN_CATEGORY_DAYS:
        facts.append(_fact("Category opportunity", f"Needs {MIN_CATEGORY_DAYS} days of collection, have {days:.1f}.",
                           "/categories", measured=False))
    co = con.execute("""
        select scope, game_name, creators, opportunity_index, median_creator_viewers, top_creator_share
        from category_opportunity
        where enough_creators and top_creator_share < 0.5 and scope in ('All', 'EU/EEA languages')
        order by scope, opportunity_index desc
    """).df()
    for scope, label in (("All", "all languages"), ("EU/EEA languages", "EU/EEA languages")):
        part = co[co["scope"] == scope].head(3)
        if len(part) and days >= MIN_CATEGORY_DAYS:
            items = "; ".join(f"{r.game_name} ({r.opportunity_index:.1f}× the median, {r.creators} creators)" for r in part.itertuples())
            facts.append(_fact(f"Category opportunity ({label})",
                               f"Highest median viewers per creator in the last 28 days, among categories with 5+ creators and no single creator "
                               f"holding half the audience: {items}.", "/categories"))

    # Growth model.
    mm = pd.DataFrame(results.get("model_metrics_growth", []))
    if not mm.empty:
        best = mm[~mm["model"].isin(["base_rate", "momentum_rule"])].sort_values("roc_auc", ascending=False).iloc[0]
        mom = mm[mm["model"] == "momentum_rule"].iloc[0]
        imp = pd.DataFrame(results.get("feature_importance_growth", []))
        top = ", ".join(imp["feature"].head(3).str.replace("_", " ")) if not imp.empty else "n/a"
        facts.append(_fact("Growth drivers",
                           f"Predicting a 10%+ rise in next week's hours watched: {best['model'].replace('_', ' ')} scores ROC AUC "
                           f"{best['roc_auc']:.2f} on held-out weeks vs {mom['roc_auc']:.2f} for last week's trend. Most informative features: {top}.",
                           "/models"))
    else:
        reason = analyses.get("predict_growth", {}).get("reason", "needs more weeks")
        facts.append(_fact("Growth drivers", f"{reason[0].upper()}{reason[1:]}.",
                           "/models", measured=False))

    # Peak hours natural experiment.
    did = results.get("did_summary")
    if did:
        d = did[0]
        facts.append(_fact("Peak hours",
                           f"Creators who moved into peak hours saw average viewers change by {_signed(d['pct_effect'])} relative to "
                           f"creators who did not (95% CI {_signed(math.expm1(d['ci_low']))} to {_signed(math.expm1(d['ci_high']))}; "
                           f"{d['n_treated']} vs {d['n_control']} creators; pre-trend p = {d['pretrend_p_value']:.2f}). Observational.",
                           "/experiments"))
    else:
        reason = analyses.get("did_peak_hours", {}).get("reason", "needs more weeks")
        facts.append(_fact("Peak hours", f"{reason[0].upper()}{reason[1:]}.",
                           "/experiments", measured=False))
    return facts


def to_markdown(facts: list[dict], meta: dict) -> str:
    lines = [
        "# Measured facts",
        "",
        f"Generated {meta['generated_at']} from {meta['snapshot_rows']:,} snapshot rows "
        f"({meta['first_snapshot']} to {meta['last_snapshot']} UTC, {meta['complete_weeks']} complete weeks). "
        f"Source: {meta['source']}.",
        "",
    ]
    for f in facts:
        mark = "" if f["status"] == "measured" else " _(pending)_"
        lines.append(f"- **{f['topic']}**{mark}: {f['text']}")
    return "\n".join(lines) + "\n"
