"""One ingestion run: fetch live streams, check them, append a Parquet file.

Each run captures
  * the top `max_streams` live streams by concurrent viewers (source="top"), and
  * every live stream of creators in the tracking panel who are not already in
    the top list (source="panel").

The panel is the first `panel_max` creators ever seen in a top list. Tracking
them outside the top list means a creator whose audience shrinks is still
observed, so declines and drop-off can be measured rather than looking like the
creator simply vanished. See docs/data.md for the sampling caveats.
"""

from __future__ import annotations

import json
import logging
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from livescope.config import Settings
from livescope.ingest.quality import QualityReport, check_snapshot
from livescope.ingest.twitch import HelixClient

log = logging.getLogger(__name__)

SNAPSHOT_COLUMNS = [
    "snapshot_at",
    "snapshot_hour",
    "stream_id",
    "user_id",
    "user_login",
    "user_name",
    "game_id",
    "game_name",
    "language",
    "viewer_count",
    "started_at",
    "is_mature",
    "tags",
    "source",
    "rank",
]


class QualityError(RuntimeError):
    def __init__(self, report: QualityReport):
        super().__init__("; ".join(report.errors))
        self.report = report


def to_frame(records: list[dict], snapshot_at: datetime) -> pd.DataFrame:
    snapshot_at = pd.Timestamp(snapshot_at).tz_convert("UTC")
    df = pd.DataFrame.from_records(records)
    if df.empty:
        df = pd.DataFrame(columns=[c for c in SNAPSHOT_COLUMNS if c not in ("snapshot_at", "snapshot_hour")])
    df = df.rename(columns={"id": "stream_id"})
    for col in SNAPSHOT_COLUMNS:
        if col not in df.columns:
            df[col] = None
    df["snapshot_at"] = snapshot_at
    df["snapshot_hour"] = snapshot_at.floor("h")
    df["started_at"] = pd.to_datetime(df["started_at"], utc=True)
    df["viewer_count"] = pd.to_numeric(df["viewer_count"]).astype("int64")
    df["rank"] = pd.to_numeric(df["rank"]).astype("Int64")
    df["is_mature"] = df["is_mature"].astype("boolean")
    df["tags"] = df["tags"].apply(lambda t: list(t) if isinstance(t, (list, tuple)) else [])
    for col in ("stream_id", "user_id", "user_login", "user_name", "game_id", "game_name", "language", "source"):
        df[col] = df[col].astype("string")
    return df[SNAPSHOT_COLUMNS].reset_index(drop=True)


def load_panel(path: Path) -> pd.DataFrame:
    if path.exists():
        return pd.read_parquet(path)
    return pd.DataFrame(
        {
            "user_id": pd.Series(dtype="string"),
            "user_login": pd.Series(dtype="string"),
            "first_seen_at": pd.Series(dtype="datetime64[ns, UTC]"),
        }
    )


def update_panel(panel: pd.DataFrame, top: pd.DataFrame, panel_max: int, now: datetime) -> pd.DataFrame:
    """Add creators from the top list (best-ranked first) until the panel is full."""
    room = panel_max - len(panel)
    if room <= 0 or top.empty:
        return panel
    known = set(panel["user_id"])
    new = top.loc[~top["user_id"].isin(known)].sort_values("rank").drop_duplicates("user_id").head(room)
    if new.empty:
        return panel
    additions = pd.DataFrame(
        {
            "user_id": new["user_id"].astype("string"),
            "user_login": new["user_login"].astype("string"),
            "first_seen_at": pd.Timestamp(now).tz_convert("UTC"),
        }
    )
    return pd.concat([panel, additions], ignore_index=True)


def snapshot_path(raw_dir: Path, snapshot_at: datetime) -> Path:
    ts = pd.Timestamp(snapshot_at).tz_convert("UTC")
    return raw_dir / f"date={ts:%Y-%m-%d}" / f"{ts:%H%M}.parquet"


def run_snapshot(client: HelixClient, settings: Settings, now: datetime | None = None) -> dict:
    now = now or datetime.now(timezone.utc)
    panel = load_panel(settings.panel_path)

    top_records = client.top_streams(settings.max_streams)
    for r in top_records:
        r["source"] = "top"
    top_users = {r["user_id"] for r in top_records}

    panel_ids = [uid for uid in panel["user_id"] if uid not in top_users]
    panel_records = []
    for r in client.streams_for_users(panel_ids):
        if r["user_id"] in top_users:
            continue
        r["source"] = "panel"
        r["rank"] = None
        panel_records.append(r)

    df = to_frame(top_records + panel_records, now)
    # Paging and the panel lookup are separate requests, so a stream can occasionally
    # be returned twice; keep the top-list copy.
    df = df.drop_duplicates("stream_id", keep="first").reset_index(drop=True)

    min_rows = max(1, int(settings.max_streams * 0.5))
    report = check_snapshot(df, min_rows=min_rows)
    record = {
        "snapshot_at": pd.Timestamp(now).isoformat(),
        "top_rows": int((df["source"] == "top").sum()),
        "panel_rows": int((df["source"] == "panel").sum()),
        "panel_size": len(panel),
        **report.as_dict(),
    }
    if not report.ok:
        _append_log(settings.runs_log, {**record, "status": "failed"})
        raise QualityError(report)

    out = snapshot_path(settings.raw_dir, now)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False, compression="zstd")

    panel = update_panel(panel, df[df["source"] == "top"], settings.panel_max, now)
    settings.panel_path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(settings.panel_path, index=False)

    record.update(status="ok", path=str(out.relative_to(settings.datastore)), panel_size=len(panel))
    _append_log(settings.runs_log, record)
    for w in report.warnings:
        log.warning(w)
    return record


def _append_log(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(record) + "\n")
