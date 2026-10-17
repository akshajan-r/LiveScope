"""Week-to-date report: this week so far vs the same hours of last week.

Weekly KPIs only use complete weeks, so they lag by up to a week. This report
fills the gap. To compare like with like it uses only top-list rows (the top
`max_streams` streams of each snapshot): that population has a fixed size, so
growth in the tracking panel cannot inflate it. Last week's window covers the
same elapsed hours (Monday 00:00 UTC to the same weekday and hour).

Rebuilt with every dashboard build; nothing is stored between runs.
"""

from __future__ import annotations

import math

import duckdb
import pandas as pd

from livescope.experiments.significance import two_proportion_ztest

WINDOWS = """
with b as (select max(snapshot_hour) as last_hour from creator_hour),
w as (select date_trunc('week', last_hour) as this_start, last_hour from b),
x as (
    select case when ch.snapshot_hour >= w.this_start then 'this' else 'last' end as wk,
           ch.*, coalesce(cl.language_group, 'Other') as language_group,
           coalesce(cl.language_name, ch.language) as language_name
    from creator_hour ch
    cross join w
    left join creator_language cl using (user_id)
    where ch.source = 'top'
      and ((ch.snapshot_hour >= w.this_start and ch.snapshot_hour <= w.last_hour)
        or (ch.snapshot_hour >= w.this_start - interval 7 day and ch.snapshot_hour <= w.last_hour - interval 7 day))
)
"""


def _records(df: pd.DataFrame) -> list[dict]:
    return [{k: (None if isinstance(v, float) and math.isnan(v) else v) for k, v in r.items()}
            for r in df.to_dict(orient="records")]


def _change(this, last):
    return None if not last else this / last - 1


def weekly_report(con: duckdb.DuckDBPyConnection, top_n: int = 8) -> dict:
    meta = con.execute("""
        with b as (select max(snapshot_hour) as last_hour from creator_hour)
        select date_trunc('week', last_hour) as this_start, last_hour,
               (select count(distinct snapshot_hour) from collector_hours, b
                 where snapshot_hour >= date_trunc('week', b.last_hour)) as hours_this,
               (select count(distinct snapshot_hour) from collector_hours, b
                 where snapshot_hour >= date_trunc('week', b.last_hour) - interval 7 day
                   and snapshot_hour <= b.last_hour - interval 7 day) as hours_last
        from b
    """).df().iloc[0]
    report = {
        "this_start": f"{meta.this_start:%Y-%m-%d}",
        "through": f"{meta.last_hour:%Y-%m-%d %H:00}",
        "last_start": f"{meta.this_start - pd.Timedelta(days=7):%Y-%m-%d}",
        "last_through": f"{meta.last_hour - pd.Timedelta(days=7):%Y-%m-%d %H:00}",
        "hours_this": int(meta.hours_this),
        "hours_last": int(meta.hours_last),
    }
    if report["hours_last"] == 0:
        report["status"] = "needs a previous week to compare with"
        return report
    if report["hours_last"] < 0.9 * report["hours_this"]:
        report["status"] = (f"last week's comparison window is incomplete ({report['hours_last']} of "
                            f"{report['hours_this']} hours captured), so the comparison would be misleading")
        return report
    report["status"] = "ok"

    head = con.execute(WINDOWS + """
        select wk, sum(viewer_count) as viewer_hours, count(distinct user_id) as creators,
               count(*) as creator_hours, sum(viewer_count) / count(distinct snapshot_hour) as avg_concurrent
        from x group by wk
    """).df().set_index("wk")
    t, l = head.loc["this"], head.loc["last"]
    report["headline"] = {
        "viewer_hours": float(t.viewer_hours), "viewer_hours_last": float(l.viewer_hours),
        "viewer_hours_change": _change(t.viewer_hours, l.viewer_hours),
        "avg_concurrent": float(t.avg_concurrent), "avg_concurrent_last": float(l.avg_concurrent),
        "avg_concurrent_change": _change(t.avg_concurrent, l.avg_concurrent),
        "creators": int(t.creators), "creators_last": int(l.creators),
    }

    groups = con.execute(WINDOWS + """
        select language_group,
               sum(viewer_count) filter (where wk = 'this') as this_vh,
               sum(viewer_count) filter (where wk = 'last') as last_vh
        from x group by language_group
    """).df()
    groups["share_this"] = groups.this_vh / groups.this_vh.sum()
    groups["share_last"] = groups.last_vh / groups.last_vh.sum()
    groups["change"] = groups.this_vh / groups.last_vh - 1
    report["language_groups"] = _records(groups.sort_values("this_vh", ascending=False))

    langs = con.execute(WINDOWS + """
        select language_name,
               sum(viewer_count) filter (where wk = 'this') as this_vh,
               sum(viewer_count) filter (where wk = 'last') as last_vh
        from x where language_group = 'EU/EEA languages' group by language_name
        order by this_vh desc nulls last
    """).df()
    langs["change"] = langs.this_vh / langs.last_vh - 1
    report["eu_languages"] = _records(langs.head(top_n))

    cats = con.execute(WINDOWS + """
        select game_name,
               coalesce(sum(viewer_count) filter (where wk = 'this'), 0) as this_vh,
               coalesce(sum(viewer_count) filter (where wk = 'last'), 0) as last_vh,
               count(distinct user_id) filter (where wk = 'this') as creators_this,
               count(distinct user_id) filter (where wk = 'last') as creators_last
        from x group by game_name
    """).df()
    cats["delta"] = cats.this_vh - cats.last_vh
    report["categories_up"] = _records(cats.sort_values("delta", ascending=False).head(top_n))
    report["categories_down"] = _records(cats.sort_values("delta").head(5))

    # Where the EU growth came from: language x category.
    eu_cats = con.execute(WINDOWS + """
        select language_name, game_name,
               coalesce(sum(viewer_count) filter (where wk = 'this'), 0) as this_vh,
               coalesce(sum(viewer_count) filter (where wk = 'last'), 0) as last_vh,
               count(distinct user_id) filter (where wk = 'this') as creators_this
        from x where language_group = 'EU/EEA languages' group by all
    """).df()
    eu_cats["delta"] = eu_cats.this_vh - eu_cats.last_vh
    report["eu_drivers"] = _records(eu_cats.sort_values("delta", ascending=False).head(5))

    creators = con.execute(WINDOWS + """
        select user_login, any_value(language_name) as language_name,
               mode(game_name) filter (where wk = 'this') as main_category,
               coalesce(sum(viewer_count) filter (where wk = 'this'), 0) as this_vh,
               coalesce(sum(viewer_count) filter (where wk = 'last'), 0) as last_vh
        from x group by user_login
    """).df()
    creators["delta"] = creators.this_vh - creators.last_vh
    report["creators_up"] = _records(creators.sort_values("delta", ascending=False).head(10))

    # Return rate: creators live last week (whole week up to Monday) who have
    # been live again this week so far. Panel creators only, newcomers vs
    # founding cohort, by language group.
    ret = con.execute("""
        with b as (select max(snapshot_hour) as last_hour from creator_hour),
        w as (select date_trunc('week', last_hour) as ts from b),
        live_this as (select distinct user_id from creator_hour, w where snapshot_hour >= w.ts),
        live_last as (select distinct user_id from creator_hour, w
                      where snapshot_hour >= w.ts - interval 7 day and snapshot_hour < w.ts)
        select case when pc.founding_cohort then 'Founding cohort' else 'Newcomers' end as cohort,
               pc.language_group, count(*) as live_last_week,
               count(lt.user_id) as live_again
        from panel_creators pc
        join live_last using (user_id)
        left join live_this lt using (user_id)
        group by all
    """).df()
    ret["return_rate"] = ret.live_again / ret.live_last_week
    report["returns"] = _records(ret.sort_values(["cohort", "language_group"]))
    new = ret[ret.cohort == "Newcomers"].set_index("language_group")
    if {"English", "EU/EEA languages"} <= set(new.index):
        en, eu = new.loc["English"], new.loc["EU/EEA languages"]
        z = two_proportion_ztest(int(en.live_again), int(en.live_last_week), int(eu.live_again), int(eu.live_last_week),
                                 metric="return rate, EU vs English newcomers")
        report["returns_test"] = {"english": float(en.return_rate), "eu": float(eu.return_rate),
                                  "diff": z.diff, "ci_low": z.ci_low, "ci_high": z.ci_high, "p_value": z.p_value,
                                  "n_english": int(en.live_last_week), "n_eu": int(eu.live_last_week)}
    return report


def _pct(x, digits=1):
    return "–" if x is None else f"{x * 100:.{digits}f}%"


def _signed(x, digits=1):
    return "–" if x is None else f"{'+' if x >= 0 else '−'}{abs(x) * 100:.{digits}f}%"


def _m(x):
    return f"{x / 1e6:.1f}M"


def _pp(x):
    return "–" if x is None else f"{'+' if x >= 0 else '−'}{abs(x) * 100:.1f} pp"


def _vs_last(this, last, digits=0):
    """Percentage change, or "new" when last week's base was negligible."""
    if not last or last < 0.05 * (this or 0):
        return "new or relaunched"
    return _signed(this / last - 1, digits)


def to_markdown(r: dict) -> str:
    lines = [f"# Week to date: {r['this_start']} to {r['through']} UTC", ""]
    if r.get("status") != "ok":
        return "\n".join(lines + [f"Not available: {r.get('status')}."]) + "\n"
    h = r["headline"]
    lines += [f"Compared with the same hours last week ({r['last_start']} to {r['last_through']}). Top-list streams only, "
              f"so the comparison is like for like. Hours captured: {r['hours_this']} this week, {r['hours_last']} last week.", "",
              "## Headline", "",
              f"- Hours watched: **{_m(h['viewer_hours'])}** vs {_m(h['viewer_hours_last'])} ({_signed(h['viewer_hours_change'])})",
              f"- Average concurrent viewers across the top list: {h['avg_concurrent']:,.0f} vs {h['avg_concurrent_last']:,.0f} "
              f"({_signed(h['avg_concurrent_change'])})",
              f"- Distinct creators in the top list: {h['creators']:,} vs {h['creators_last']:,}", "",
              "## By language group", "", "| Group | Share this week | Share last week | Hours watched change |", "|---|---|---|---|"]
    for g in r["language_groups"]:
        lines.append(f"| {g['language_group']} | {_pct(g['share_this'])} | {_pct(g['share_last'])} | {_signed(g['change'])} |")
    lines += ["", "EU/EEA languages: " + "; ".join(f"{x['language_name']} {_m(x['this_vh'] or 0)} ({_vs_last(x['this_vh'], x['last_vh'], 1)})"
                                                  for x in r["eu_languages"][:5]), ""]
    lines += ["Biggest EU increases by language and category: " + "; ".join(
        f"{x['language_name']} {x['game_name']} {_m(x['last_vh'])} → {_m(x['this_vh'])}" for x in r["eu_drivers"][:3]), ""]
    lines += ["## Categories", "", "Rising: " + "; ".join(
        f"{c['game_name']} {_m(c['this_vh'])} ({_vs_last(c['this_vh'], c['last_vh'])})"
        for c in r["categories_up"][:6]), "",
        "Falling: " + "; ".join(f"{c['game_name']} {_m(c['this_vh'])} ({_signed(c['this_vh'] / c['last_vh'] - 1, 0)})"
                                for c in r["categories_down"] if c["last_vh"]), ""]
    lines += ["## Creators gaining the most hours watched", "",
              "| Creator | Language | Main category this week | This week | Last week |", "|---|---|---|---|---|"]
    for c in r["creators_up"][:8]:
        lines.append(f"| {c['user_login']} | {c['language_name']} | {c['main_category'] or '–'} | {_m(c['this_vh'])} | {_m(c['last_vh'])} |")
    if "returns_test" in r:
        t = r["returns_test"]
        lines += ["", "## Are last week's newcomers back?", "",
                  f"Of newcomers who were live last week, {_pct(t['english'])} of English-language creators (n = {t['n_english']:,}) "
                  f"and {_pct(t['eu'])} of EU/EEA-language creators (n = {t['n_eu']:,}) have been live again this week so far "
                  f"(EU minus English: {_pp(t['diff'])}, 95% CI {_pp(t['ci_low'])} to {_pp(t['ci_high'])}, p = {t['p_value']:.2g}). "
                  "The week is not over, so both rates will rise."]
    return "\n".join(lines) + "\n"
