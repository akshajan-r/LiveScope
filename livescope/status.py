"""Collection status: how many snapshots exist, when they ran, what failed.

Written to the `data` branch README after every run (so progress is visible on
GitHub without waiting for a dashboard rebuild) and to the Actions job summary.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from livescope.config import Settings


def captured_this_hour(settings: Settings, now: datetime | None = None) -> bool:
    """True if a snapshot file already exists for the current UTC hour."""
    now = pd.Timestamp(now or datetime.now(timezone.utc)).tz_convert("UTC")
    day_dir = settings.raw_dir / f"date={now:%Y-%m-%d}"
    return any(day_dir.glob(f"{now:%H}[0-5][0-9].parquet"))


def _size(path: Path) -> int:
    return sum(p.stat().st_size for p in path.rglob("*") if p.is_file()) if path.exists() else 0


def load_runs(path: Path) -> pd.DataFrame:
    if not path.exists():
        return pd.DataFrame(columns=["snapshot_at", "status", "top_rows", "panel_rows", "panel_size", "rows", "errors", "warnings"])
    runs = pd.DataFrame([json.loads(line) for line in path.read_text().splitlines() if line.strip()])
    runs["snapshot_at"] = pd.to_datetime(runs["snapshot_at"], utc=True)
    return runs.sort_values("snapshot_at").reset_index(drop=True)


def summary(settings: Settings, now: datetime | None = None) -> dict:
    now = pd.Timestamp(now or datetime.now(timezone.utc)).tz_convert("UTC")
    runs = load_runs(settings.runs_log)
    ok = runs[runs["status"] == "ok"]
    raw_days = [d for d in settings.raw_dir.glob("date=*") if d.is_dir()] if settings.raw_dir.exists() else []
    out = {
        "raw_mb": _size(settings.raw_dir) / 1e6,
        "raw_days": len(raw_days),
        "history_kb": _size(settings.history_dir) / 1e3,
        "updated_at": f"{now:%Y-%m-%d %H:%M}",
        "snapshots": len(ok),
        "failed_runs": int((runs["status"] != "ok").sum()),
        "rows": int(ok["rows"].sum()) if len(ok) else 0,
    }
    if len(ok):
        first, last = ok["snapshot_at"].min(), ok["snapshot_at"].max()
        hours_ok = ok["snapshot_at"].dt.floor("h").nunique()
        expected = int((now.floor("h") - first.floor("h")) / pd.Timedelta(hours=1)) + 1
        out.update(
            first_snapshot=f"{first:%Y-%m-%d %H:%M}",
            last_snapshot=f"{last:%Y-%m-%d %H:%M}",
            hours_since_last=round((now - last) / pd.Timedelta(hours=1), 1),
            hours_captured=int(hours_ok),
            hours_since_start=expected,
            coverage=hours_ok / expected if expected else 1.0,
            panel_size=int(ok["panel_size"].iloc[-1]),
            panel_evicted=int(ok["panel_evicted"].iloc[-1]) if "panel_evicted" in ok and pd.notna(ok["panel_evicted"].iloc[-1]) else 0,
        )
    return out


def to_markdown(settings: Settings, now: datetime | None = None, recent: int = 24) -> str:
    s = summary(settings, now)
    lines = ["# LiveScope data branch", "",
             "Written by the `Collect and publish` workflow; do not edit by hand.", "",
             "## Collection status", "", f"_Updated {s['updated_at']} UTC._", ""]
    if not s["snapshots"]:
        lines.append("No successful snapshots yet.")
    else:
        lines += [
            "| | |", "|---|---|",
            f"| Snapshots collected | **{s['snapshots']:,}** ({s['rows']:,} rows) |",
            f"| First / latest | {s['first_snapshot']} / {s['last_snapshot']} UTC |",
            f"| Hours captured since the first snapshot | {s['hours_captured']:,} of {s['hours_since_start']:,} ({s['coverage']:.0%}) |",
            f"| Creators in the tracking panel | {s['panel_size']:,} active"
            + (f", {s['panel_evicted']:,} dropped after 4 weeks offline" if s["panel_evicted"] else "") + " |",
            f"| Raw snapshots on disk | {s['raw_mb']:.1f} MB, {s['raw_days']} days "
            f"({'all kept' if not settings.raw_retention_days else f'last {settings.raw_retention_days} kept'}) |",
            f"| Weekly history | {s['history_kb']:,.0f} KB |",
            f"| Failed runs | {s['failed_runs']} |",
        ]
        if s["hours_since_last"] > 2:
            lines += ["", f"> **No snapshot for {s['hours_since_last']:.0f} hours.** Check the Actions tab for failed or "
                          "skipped runs; GitHub occasionally drops scheduled runs at busy times."]
    runs = load_runs(settings.runs_log).tail(recent).iloc[::-1]
    if len(runs):
        lines += ["", f"### Last {len(runs)} runs", "", "| Time (UTC) | Status | Top-list rows | Panel rows | Panel size | Notes |",
                  "|---|---|---|---|---|---|"]
        for r in runs.itertuples():
            notes = "; ".join((r.errors or []) + (r.warnings or [])) if isinstance(r.errors, list) else ""
            lines.append(f"| {r.snapshot_at:%Y-%m-%d %H:%M} | {r.status} | {int(r.top_rows):,} | {int(r.panel_rows):,} | "
                         f"{int(r.panel_size):,} | {notes} |")
    lines += ["", "## Layout", "",
              "- `raw/twitch_streams/date=YYYY-MM-DD/HHMM.parquet`: one file per hourly snapshot",
              "- `state/panel.parquet`: the creators tracked outside the top list",
              "- `manifest/runs.jsonl`: one line per run, with row counts and data-quality results"]
    return "\n".join(lines) + "\n"
