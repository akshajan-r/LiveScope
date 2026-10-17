"""Keep the data branch small.

Run after each snapshot (it only does work once a day):

1. Compact: every finished UTC day's hourly files become one `day.parquet`,
   deduplicated, with only the columns the models use, sorted and compressed
   (about 6x smaller than the hourly files).
2. Save history: weekly summaries (`creator_week_base`, `collector_weeks`,
   `category_week`) for every week that has ended are written to `history/`.
   They are small and kept forever, so retention, cohort and model analyses
   keep their full history after raw snapshots are deleted.
3. Expire: raw days older than `raw_retention_days` are deleted.

Git keeps deleted files in history, so the workflow also replaces the data
branch with a single fresh commit whenever this step changed anything (see
scripts/push_data_branch.sh).
"""

from __future__ import annotations

import logging
import shutil
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import duckdb
import pandas as pd

from livescope.config import Settings
from livescope.warehouse import HISTORY_TABLES, build

log = logging.getLogger(__name__)

# Columns read by the SQL models. Dropped: user_name (same as login), is_mature, tags.
KEEP_COLUMNS = ["snapshot_at", "snapshot_hour", "stream_id", "user_id", "user_login", "game_id", "game_name",
                "language", "viewer_count", "started_at", "source", "rank"]
HOURLY_GLOB = "[0-2][0-9][0-5][0-9].parquet"
DAY_FILE = "day.parquet"


def _day_dirs(raw_dir: Path) -> list[tuple[date, Path]]:
    out = []
    for d in sorted(raw_dir.glob("date=*")):
        try:
            out.append((date.fromisoformat(d.name.removeprefix("date=")), d))
        except ValueError:
            continue
    return out


def compact_day(day_dir: Path) -> bool:
    """Merge a day's hourly files (and any earlier day.parquet) into one file."""
    hourly = sorted(day_dir.glob(HOURLY_GLOB))
    if not hourly:
        return False
    sources = [str(p) for p in hourly]
    existing = day_dir / DAY_FILE
    if existing.exists():
        sources.append(str(existing))
    cols = ", ".join(KEEP_COLUMNS)
    tmp = day_dir / f".{DAY_FILE}.tmp"
    con = duckdb.connect()
    con.execute("set TimeZone = 'UTC'")
    con.execute(f"""
        copy (
            select {cols} from read_parquet({sources!r}, union_by_name = true, hive_partitioning = false)
            qualify row_number() over (partition by stream_id, snapshot_hour order by snapshot_at desc) = 1
            order by user_id, snapshot_hour
        ) to '{tmp}' (format parquet, compression zstd, compression_level 9)
    """)
    con.close()
    tmp.replace(existing)
    for p in hourly:
        p.unlink()
    return True


def compact(settings: Settings, today: date) -> list[str]:
    done = []
    for d, path in _day_dirs(settings.raw_dir):
        if d < today and compact_day(path):
            done.append(d.isoformat())
    return done


def save_history(settings: Settings) -> dict[str, int]:
    """Write weekly summaries for every week that has ended (raw merged with existing history)."""
    con = build(settings.raw_dir, ":memory:", settings.panel_path, settings.history_dir)
    ended = "week_start + interval 7 day <= (select last_hour + interval 1 hour from raw_bounds)"
    queries = {
        "collector_weeks": f"select week_start, hours_observed from collector_weeks where {ended}",
        "creator_week_base": f"select * from creator_week_base where {ended}",
        "category_week": f"select * from category_week where {ended}",
    }
    settings.history_dir.mkdir(parents=True, exist_ok=True)
    counts = {}
    for name, sql in queries.items():
        assert name in HISTORY_TABLES
        out = settings.history_dir / f"{name}.parquet"
        tmp = settings.history_dir / f".{name}.parquet.tmp"
        con.execute(f"copy ({sql} order by week_start) to '{tmp}' (format parquet, compression zstd)")
        tmp.replace(out)
        counts[name] = con.execute(f"select count(*) from ({sql})").fetchone()[0]
    con.close()
    return counts


def expire(settings: Settings, today: date) -> list[str]:
    if settings.raw_retention_days <= 0:
        return []
    cutoff = today - timedelta(days=settings.raw_retention_days)
    removed = []
    for d, path in _day_dirs(settings.raw_dir):
        if d < cutoff:
            shutil.rmtree(path)
            removed.append(d.isoformat())
    return removed


def maintain(settings: Settings, now: datetime | None = None) -> dict:
    """Compact, save history, expire. `changed` tells the caller to squash git history."""
    now = pd.Timestamp(now or datetime.now(timezone.utc)).tz_convert("UTC")
    today = now.date()
    compacted = compact(settings, today)
    cutoff = today - timedelta(days=settings.raw_retention_days)
    due = settings.raw_retention_days > 0 and any(d < cutoff for d, _ in _day_dirs(settings.raw_dir))
    history = {}
    expired = []
    if compacted or due:
        # Save history before deleting anything it is built from.
        history = save_history(settings)
        expired = expire(settings, today)
    return {"compacted": compacted, "expired": expired, "history_rows": history,
            "changed": bool(compacted or expired)}


def disk_usage(path: Path) -> int:
    return sum(p.stat().st_size for p in Path(path).rglob("*") if p.is_file())
