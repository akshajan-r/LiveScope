from __future__ import annotations

import json
from datetime import datetime, timezone

import pandas as pd

from livescope.cli import main
from livescope.status import captured_this_hour, summary, to_markdown


def _log(settings, *records):
    settings.runs_log.parent.mkdir(parents=True, exist_ok=True)
    settings.runs_log.write_text("".join(json.dumps(r) + "\n" for r in records))


def _rec(ts, status="ok", **kw):
    return {"snapshot_at": ts, "status": status, "top_rows": 4, "panel_rows": 1, "panel_size": 5, "rows": 5,
            "errors": [], "warnings": [], **kw}


def test_captured_this_hour(settings):
    now = datetime(2026, 10, 2, 13, 53, tzinfo=timezone.utc)
    assert not captured_this_hour(settings, now)
    f = settings.raw_dir / "date=2026-10-02" / "1323.parquet"
    f.parent.mkdir(parents=True)
    f.write_bytes(b"")
    assert captured_this_hour(settings, now)
    assert not captured_this_hour(settings, now.replace(hour=14, minute=23))


def test_summary_and_markdown(settings):
    _log(settings, _rec("2026-10-02T10:42:00+00:00"), _rec("2026-10-02T11:23:00+00:00"),
         _rec("2026-10-02T12:23:00+00:00", status="failed", errors=["only 1 rows"]))
    now = datetime(2026, 10, 2, 15, 0, tzinfo=timezone.utc)
    s = summary(settings, now)
    assert s["snapshots"] == 2 and s["failed_runs"] == 1
    assert s["hours_captured"] == 2 and s["hours_since_start"] == 6
    md = to_markdown(settings, now)
    assert "**2**" in md and "only 1 rows" in md
    assert "No snapshot for 4 hours" in md  # last success 11:23, now 15:00


def test_empty_status(settings):
    assert "No successful snapshots yet" in to_markdown(settings)


def test_ingest_skips_when_hour_captured(settings, monkeypatch, tmp_path):
    now = pd.Timestamp.now(tz="UTC")
    f = settings.raw_dir / f"date={now:%Y-%m-%d}" / f"{now:%H}00.parquet"
    f.parent.mkdir(parents=True)
    f.write_bytes(b"")
    out = tmp_path / "gh_output"
    monkeypatch.setenv("GITHUB_OUTPUT", str(out))
    monkeypatch.setenv("LIVESCOPE_DATASTORE", str(settings.datastore))
    # No Twitch credentials are set, so this would fail if it tried to ingest.
    monkeypatch.delenv("TWITCH_CLIENT_ID", raising=False)
    assert main(["ingest", "--skip-if-captured"]) == 0
    assert out.read_text().strip() == "captured=false"


def test_status_command_writes_readme(settings, monkeypatch, tmp_path):
    _log(settings, _rec("2026-10-02T10:42:00+00:00"))
    monkeypatch.setenv("LIVESCOPE_DATASTORE", str(settings.datastore))
    monkeypatch.setenv("GITHUB_STEP_SUMMARY", str(tmp_path / "summary.md"))
    assert main(["status", "--write"]) == 0
    assert "Collection status" in (settings.datastore / "README.md").read_text()
    assert "## Layout" not in (tmp_path / "summary.md").read_text()
