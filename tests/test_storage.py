from __future__ import annotations

import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from livescope.config import Settings
from livescope.storage import compact, maintain
from livescope.warehouse import build
from tests.test_warehouse import rec, write_hours

REPO = Path(__file__).resolve().parents[1]
CHECKS = {
    "creator_week": "select week_start, user_id, hours_live, avg_viewers, viewer_hours, wow_avg_viewers_growth, "
                    "streak_weeks, weeks_active_to_date, is_complete_week from creator_week order by 1, 2",
    "collector_weeks": "select * from collector_weeks order by 1",
    "category_week": "select * from category_week order by 1, 2",
    "platform_week": "select week_start, active_creators, viewer_hours, drop_off_rate from platform_week order by 1",
    "creator_lifetime": "select user_id, cohort_week, duration_weeks, churned from creator_lifetime order by 1",
}


def _store(tmp_path: Path, weeks: int = 4) -> Settings:
    """`weeks` weeks of hourly files. Creator a streams every week; b skips week 2."""
    s = Settings(tmp_path / "store", Path(":memory:"), tmp_path / "exports", 4, 10, 28, 30)
    start = pd.Timestamp("2026-01-05 00:07", tz="UTC")
    hours = {}
    for h in range(weeks * 168):
        ts = start + pd.Timedelta(hours=h)
        week = h // 168
        rows = [rec("filler", f"f{week}", 1)]
        if h % 168 < 10:
            rows.append(rec("a", f"a{week}", 100 * (week + 1)))
            if week != 1:
                rows.append(rec("b", f"b{week}", 50))
        hours[ts] = rows
    write_hours(s.raw_dir, hours)
    return s


def _snapshot(s: Settings) -> dict:
    con = build(s.raw_dir, ":memory:", s.panel_path, s.history_dir)
    out = {k: con.execute(q).df() for k, q in CHECKS.items()}
    con.close()
    return out


def _same(a: dict, b: dict) -> None:
    for k in CHECKS:
        pd.testing.assert_frame_equal(a[k].reset_index(drop=True), b[k].reset_index(drop=True), check_dtype=False, obj=k)


def test_compaction_keeps_results_and_today(tmp_path):
    s = _store(tmp_path, weeks=2)
    before = _snapshot(s)
    today = datetime(2026, 1, 18, tzinfo=timezone.utc).date()  # last day of week 2
    done = compact(s, today)
    assert len(done) == 13
    assert not list((s.raw_dir / "date=2026-01-05").glob("[0-9]*.parquet"))
    assert (s.raw_dir / "date=2026-01-05" / "day.parquet").exists()
    assert len(list((s.raw_dir / "date=2026-01-18").glob("[0-9]*.parquet"))) == 24  # today untouched
    day = pd.read_parquet(s.raw_dir / "date=2026-01-05" / "day.parquet")
    assert "tags" not in day and "user_name" not in day
    _same(before, _snapshot(s))
    assert compact(s, today) == []  # idempotent


def test_expiry_keeps_weekly_history(tmp_path):
    s = _store(tmp_path, weeks=4)
    before = _snapshot(s)
    # 2026-02-02 is the Monday after week 4; keep 10 days, so weeks 1-2 and part of week 3 go.
    s = Settings(s.datastore, s.warehouse, s.exports, 4, 10, 28, raw_retention_days=10)
    result = maintain(s, datetime(2026, 2, 2, 0, 30, tzinfo=timezone.utc))
    assert result["changed"] and result["expired"][0] == "2026-01-05" and result["expired"][-1] == "2026-01-22"
    assert sorted(p.name for p in s.history_dir.iterdir()) == ["category_week.parquet", "collector_weeks.parquet",
                                                              "creator_week_base.parquet"]
    con = build(s.raw_dir, ":memory:", s.panel_path, s.history_dir)
    assert str(con.execute("select first_full_week from raw_bounds").fetchone()[0]) == "2026-01-26"
    con.close()
    _same(before, _snapshot(s))


def test_retention_zero_keeps_everything(tmp_path):
    s = _store(tmp_path, weeks=2)
    s = Settings(s.datastore, s.warehouse, s.exports, 4, 10, 28, raw_retention_days=0)
    result = maintain(s, datetime(2026, 3, 1, tzinfo=timezone.utc))
    assert result["expired"] == [] and len(result["compacted"]) == 14


def test_squash_push_replaces_history(tmp_path):
    remote = tmp_path / "remote.git"
    subprocess.run(["git", "init", "-q", "--bare", str(remote)], check=True)
    env = {**os.environ, "DATA_REMOTE_URL": str(remote), "GIT_AUTHOR_NAME": "t", "GIT_COMMITTER_NAME": "t",
           "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_EMAIL": "t@t"}
    store = tmp_path / "store"
    subprocess.run([str(REPO / "scripts/checkout_data_branch.sh"), str(store)], check=True, env=env)
    for i in range(3):
        (store / f"f{i}.txt").write_text(str(i))
        subprocess.run([str(REPO / "scripts/push_data_branch.sh"), str(store), f"c{i}"], check=True, env=env,
                       capture_output=True)
    log = lambda: subprocess.run(["git", "--git-dir", str(remote), "log", "--format=%s", "data"],  # noqa: E731
                                 capture_output=True, text=True, check=True).stdout.split("\n")[:-1]
    assert len(log()) == 3
    (store / "f0.txt").unlink()
    subprocess.run([str(REPO / "scripts/push_data_branch.sh"), str(store), "squash"], check=True,
                   env={**env, "SQUASH": "true"}, capture_output=True)
    assert log() == ["squash (history reset after compaction)"]
    files = subprocess.run(["git", "--git-dir", str(remote), "ls-tree", "--name-only", "data"],
                           capture_output=True, text=True, check=True).stdout.split()
    assert files == ["README.md", "f1.txt", "f2.txt"]
