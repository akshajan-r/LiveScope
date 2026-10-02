from __future__ import annotations

from pathlib import Path

import pandas as pd
import pytest

from livescope.ingest.snapshot import to_frame
from livescope.warehouse import build


def write_hours(raw: Path, rows_by_hour: dict[pd.Timestamp, list[dict]]) -> None:
    for ts, rows in rows_by_hour.items():
        df = to_frame([{**r, "source": "top", "rank": i + 1} for i, r in enumerate(rows)], ts.to_pydatetime())
        out = raw / f"date={ts:%Y-%m-%d}" / f"{ts:%H%M}.parquet"
        out.parent.mkdir(parents=True, exist_ok=True)
        df.to_parquet(out, index=False)


def rec(user, stream, viewers):
    return {"id": stream, "user_id": user, "user_login": user, "user_name": user, "game_id": "1",
            "game_name": "Art", "language": "en", "viewer_count": viewers,
            "started_at": "2026-01-05T00:00:00Z", "tags": [], "is_mature": False}


@pytest.fixture
def tiny(tmp_path):
    """Every hour of 3 weeks is captured. Creator `a` streams weeks 1, 2 and 3;
    `b` streams weeks 1 and 3 only, so `b` has no week-3 growth figure."""
    raw = tmp_path / "raw"
    start = pd.Timestamp("2026-01-05 00:07", tz="UTC")  # a Monday
    hours = {}
    for h in range(3 * 168):
        ts = start + pd.Timedelta(hours=h)
        week = h // 168
        rows = [rec("filler", f"f{week}", 1)]
        if h % 168 < 10:  # first 10 hours of each week
            rows.append(rec("a", f"a{week}", 100 * (week + 1)))
            if week != 1:
                rows.append(rec("b", f"b{week}", 50))
        hours[ts] = rows
    write_hours(raw, hours)
    # A re-run in the same hour must not double count: duplicate one capture.
    dup = start + pd.Timedelta(minutes=30)
    write_hours(raw, {dup: [rec("a", "a0", 100), rec("filler", "f0", 1)]})
    con = build(raw)
    yield con
    con.close()


def test_creator_week_values(tiny):
    cw = tiny.execute("select * from creator_week where user_id in ('a', 'b') order by user_id, week_start").df()
    a = cw[cw.user_id == "a"].reset_index(drop=True)
    assert list(a.hours_live) == [10, 10, 10]
    assert list(a.avg_viewers) == [100, 200, 300]
    assert a.wow_avg_viewers_growth.isna()[0]
    assert a.wow_avg_viewers_growth[1] == pytest.approx(1.0)
    assert a.wow_avg_viewers_growth[2] == pytest.approx(0.5)
    assert list(a.streak_weeks) == [1, 2, 3]
    assert list(a.viewer_hours) == [1000, 2000, 3000]

    b = cw[cw.user_id == "b"].reset_index(drop=True)
    assert len(b) == 2
    assert b.wow_avg_viewers_growth.isna().all()  # week 2 missing, so no week-on-week figure
    assert list(b.streak_weeks) == [1, 1]
    assert cw.is_complete_week.all()


def test_dedup_and_coverage(tiny):
    n = tiny.execute("select count(*) from stg_streams where stream_id = 'a0'").fetchone()[0]
    assert n == 10
    weeks = tiny.execute("select hours_observed, is_complete from collector_weeks order by week_start").fetchall()
    assert weeks == [(168, True), (168, True), (168, True)]


def test_peak_hours_has_six(tiny):
    assert tiny.execute("select count(*) from peak_hours where is_peak").fetchone()[0] == 6


def test_summary_one_row_per_creator(tiny):
    s = tiny.execute("select * from creator_summary where user_id = 'a'").df().iloc[0]
    assert s.weeks_active == 3 and s.longest_streak == 3 and s.current_streak == 3
    assert s.avg_viewers == pytest.approx(200)


def test_platform_week_kpis(tiny):
    pw = tiny.execute("select * from platform_week order by week_start").df()
    assert list(pw.active_creators) == [3, 2, 3]  # a, b, filler; b skips week 2
    assert pw.drop_off_rate[0] == pytest.approx(1 / 3)
    assert pw.drop_off_rate[1] == pytest.approx(0.0)
    assert pd.isna(pw.drop_off_rate[2])  # no following week yet
    assert pw.retention_4w.isna().all()
    assert pw.new_creators.tolist() == [3, 0, 0]
    assert pw.viewer_hours_wow[1] == pytest.approx((2000 + 168) / (1000 + 500 + 168) - 1)


def test_retention_tables(tiny):
    # Everyone joins the panel in week 1, the first collection week.
    pc = tiny.execute("select * from panel_creators").df()
    assert pc.founding_cohort.all() and len(pc) == 3
    cr = tiny.execute("select weeks_since, active, cohort_size from cohort_retention order by weeks_since").fetchall()
    assert cr == [(0, 3, 3), (1, 2, 3), (2, 3, 3)]
    lt = tiny.execute("select user_id, duration_weeks, churned from creator_lifetime order by user_id").fetchall()
    assert lt == [("a", 3, False), ("b", 3, False), ("filler", 3, False)]


def test_language_and_category_tables(tiny):
    assert tiny.execute("select language_group from creator_language where user_id = 'a'").fetchone()[0] == "English"
    lw = tiny.execute("select active_creators from language_week where language = 'en' order by week_start").fetchall()
    assert [r[0] for r in lw] == [3, 2, 3]
    co = tiny.execute("select * from category_opportunity where scope = 'All'").df()
    assert set(co.game_name) == {"Art"} and co.opportunity_index.iloc[0] == pytest.approx(1.0)
    assert set(tiny.execute("select distinct scope from category_opportunity").df().scope) == {"All", "English"}


def test_partial_week_is_incomplete(tmp_path):
    raw = tmp_path / "raw"
    start = pd.Timestamp("2026-01-05 00:07", tz="UTC")
    write_hours(raw, {start + pd.Timedelta(hours=h): [rec("a", "a", 5)] for h in range(100)})
    con = build(raw)
    assert con.execute("select is_complete from collector_weeks").fetchone()[0] is False
    con.close()


def test_missing_raw_dir(tmp_path):
    with pytest.raises(FileNotFoundError):
        build(tmp_path / "nothing")


def test_demo_store_builds(demo_creator_week):
    assert len(demo_creator_week) > 1000
    assert demo_creator_week["is_complete_week"].all()
