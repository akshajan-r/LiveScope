from __future__ import annotations

import json
from datetime import datetime, timezone

from pathlib import Path

import pandas as pd
import pytest

from livescope.ingest.quality import check_snapshot
from livescope.ingest.snapshot import QualityError, run_snapshot, snapshot_path, to_frame

NOW = datetime(2026, 10, 1, 20, 7, tzinfo=timezone.utc)


def record(i, viewers, user=None, **kw):
    return {
        "id": f"s{i}", "user_id": user or f"u{i}", "user_login": f"login{i}", "user_name": f"Name{i}",
        "game_id": "1", "game_name": "Just Chatting", "type": "live", "title": "hi",
        "viewer_count": viewers, "started_at": "2026-10-01T18:00:00Z", "language": "en",
        "tags": ["English"], "is_mature": False, **kw,
    }


class FakeClient:
    def __init__(self, top, live_users):
        self.top = top
        self.live_users = live_users
        self.requested = []

    def top_streams(self, limit):
        return [{**r, "rank": i + 1} for i, r in enumerate(self.top[:limit])]

    def streams_for_users(self, ids):
        self.requested.extend(ids)
        return [dict(r) for r in self.live_users if r["user_id"] in set(ids)]


def test_first_run_writes_snapshot_and_seeds_panel(settings):
    client = FakeClient([record(i, 1000 - i) for i in range(4)], [])
    rec = run_snapshot(client, settings, now=NOW)
    assert rec["status"] == "ok" and rec["top_rows"] == 4
    df = pd.read_parquet(snapshot_path(settings.raw_dir, NOW))
    assert list(df["rank"]) == [1, 2, 3, 4]
    assert (df["snapshot_hour"] == pd.Timestamp("2026-10-01 20:00", tz="UTC")).all()
    panel = pd.read_parquet(settings.panel_path)
    assert list(panel["user_id"]) == ["u0", "u1", "u2", "u3"]
    log = [json.loads(line) for line in settings.runs_log.read_text().splitlines()]
    assert log[-1]["status"] == "ok"


def test_panel_members_outside_top_list_are_tracked(settings):
    run_snapshot(FakeClient([record(i, 1000 - i) for i in range(4)], []), settings, now=NOW)
    # Next hour u0 dropped out of the top list but is still live.
    later = NOW.replace(hour=21)
    top = [record(i, 900 - i) for i in range(1, 5)]
    client = FakeClient(top, [record(0, 12)])
    rec = run_snapshot(client, settings, now=later)
    assert rec["panel_rows"] == 1
    df = pd.read_parquet(snapshot_path(settings.raw_dir, later))
    row = df[df["user_id"] == "u0"].iloc[0]
    assert row["source"] == "panel" and pd.isna(row["rank"])
    # Users already in the top list are not looked up again.
    assert set(client.requested) == {"u0"}


def test_panel_is_capped(settings):
    run_snapshot(FakeClient([record(i, 1000 - i) for i in range(4)], []), settings, now=NOW)
    for h in range(21, 24):
        top = [record(10 * h + i, 500 - i) for i in range(4)]
        run_snapshot(FakeClient(top, []), settings, now=NOW.replace(hour=h))
    assert len(pd.read_parquet(settings.panel_path)) == settings.panel_max


def test_quality_failure_writes_nothing(settings):
    client = FakeClient([record(1, 10), record(2, 5, id="s1")], [])  # duplicate stream id, too few rows
    with pytest.raises(QualityError):
        run_snapshot(client, settings, now=NOW)
    assert not settings.raw_dir.exists()
    assert json.loads(settings.runs_log.read_text().splitlines()[-1])["status"] == "failed"


def test_quality_checks():
    df = to_frame([{**record(1, 10), "rank": 1, "source": "top"}, {**record(2, -3), "rank": 2, "source": "top"}], NOW)
    report = check_snapshot(df)
    assert any("negative" in e for e in report.errors)
    df = to_frame([{**record(1, 10, started_at="2026-10-01T23:00:00Z"), "rank": 1, "source": "top"}], NOW)
    report = check_snapshot(df)
    assert report.ok and any("start after" in w for w in report.warnings)
    assert not check_snapshot(df.drop(columns=["language"])).ok


def test_panel_eviction_and_reactivation():
    from livescope.ingest.snapshot import active_ids, load_panel, update_panel

    t0 = pd.Timestamp("2026-10-01 00:00", tz="UTC")
    snap = lambda users, source="top": pd.DataFrame({  # noqa: E731
        "user_id": users, "user_login": users, "source": source, "rank": range(1, len(users) + 1)})
    panel = load_panel(Path("/nonexistent"))
    panel = update_panel(panel, snap(["a", "b", "c"]), panel_max=3, now=t0)
    assert active_ids(panel) == ["a", "b", "c"]
    # Full: d cannot join.
    panel = update_panel(panel, snap(["a", "d"]), panel_max=3, now=t0 + pd.Timedelta(days=1))
    assert "d" not in set(panel.user_id)
    # 30 days later only a has been seen recently: b and c are evicted, which makes room for d.
    panel = update_panel(panel, snap(["a"], "panel"), panel_max=3, now=t0 + pd.Timedelta(days=29))
    panel = update_panel(panel, snap(["d"]), panel_max=3, now=t0 + pd.Timedelta(days=30))
    assert set(active_ids(panel)) == {"a", "d"}
    assert set(panel.user_id) == {"a", "b", "c", "d"}  # evicted creators stay in the file
    # b re-enters the top list and is reactivated.
    panel = update_panel(panel, snap(["b"]), panel_max=3, now=t0 + pd.Timedelta(days=31))
    assert set(active_ids(panel)) == {"a", "b", "d"}


def test_old_panel_files_get_new_columns(tmp_path):
    from livescope.ingest.snapshot import load_panel

    path = tmp_path / "panel.parquet"
    pd.DataFrame({"user_id": ["a"], "user_login": ["a"], "first_seen_at": [pd.Timestamp("2026-10-01", tz="UTC")]}).to_parquet(path)
    panel = load_panel(path)
    assert panel.evicted_at.isna().all() and panel.last_seen_at.notna().all()
