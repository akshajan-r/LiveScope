"""One ingestion run: fetch live streams, check them, append a Parquet file.

Each run captures
  * the top `max_streams` live streams by concurrent viewers (source="top"), and
  * every live stream of creators in the tracking panel who are not already in
    the top list (source="panel").

Every creator who appears in a top list joins the panel while it has room
(`panel_max` active members). Tracking them outside the top list means a
creator whose audience shrinks is still observed, so declines and drop-off can
be measured rather than looking like the creator simply vanished. Creators not
seen live for `panel_evict_days` are evicted to make room for newcomers; they
stay in the panel file so retention analysis still counts them. See
docs/data.md for the sampling caveats.
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


PANEL_COLUMNS = ["user_id", "user_login", "first_seen_at", "last_seen_at", "evicted_at"]


def load_panel(path: Path) -> pd.DataFrame:
    if path.exists():
        panel = pd.read_parquet(path)
    else:
        panel = pd.DataFrame({"user_id": pd.Series(dtype="string"), "user_login": pd.Series(dtype="string"),
                              "first_seen_at": pd.Series(dtype="datetime64[ns, UTC]")})
    # Panels written before eviction existed have no last_seen_at: give every
    # member a full grace period from the first run that reads them.
    if "last_seen_at" not in panel:
        panel["last_seen_at"] = pd.Timestamp.now(tz="UTC") if len(panel) else pd.Series(dtype="datetime64[ns, UTC]")
    if "evicted_at" not in panel:
        panel["evicted_at"] = pd.Series(pd.NaT, index=panel.index, dtype="datetime64[ns, UTC]")
    for col in ("first_seen_at", "last_seen_at", "evicted_at"):
        panel[col] = pd.to_datetime(panel[col], utc=True)
    return panel[PANEL_COLUMNS].reset_index(drop=True)


def active_ids(panel: pd.DataFrame) -> list[str]:
    return panel.loc[panel["evicted_at"].isna(), "user_id"].tolist()


def update_panel(panel: pd.DataFrame, snapshot: pd.DataFrame, panel_max: int, now: datetime,
                 evict_days: int = 28) -> pd.DataFrame:
    """Refresh the panel after a snapshot.

    1. Everyone live in the snapshot gets last_seen_at = now; evicted creators
       who are live again (they re-entered the top list) are reactivated.
    2. Active creators not seen for `evict_days` are evicted: no longer looked
       up, but kept in the file so their history stays in the analysis.
    3. New top-list creators are added, best-ranked first, while the number of
       active creators is below `panel_max`.
    """
    now = pd.Timestamp(now).tz_convert("UTC")
    panel = panel.copy()
    live = set(snapshot["user_id"])
    seen = panel["user_id"].isin(live)
    panel.loc[seen, "last_seen_at"] = now
    panel.loc[seen, "evicted_at"] = pd.NaT

    stale = panel["evicted_at"].isna() & (panel["last_seen_at"] < now - pd.Timedelta(days=evict_days))
    panel.loc[stale, "evicted_at"] = now

    room = panel_max - int(panel["evicted_at"].isna().sum())
    top = snapshot[snapshot["source"] == "top"]
    if room <= 0 or top.empty:
        return panel
    new = top.loc[~top["user_id"].isin(set(panel["user_id"]))].sort_values("rank").drop_duplicates("user_id").head(room)
    if new.empty:
        return panel
    additions = pd.DataFrame({
        "user_id": new["user_id"].astype("string"),
        "user_login": new["user_login"].astype("string"),
        "first_seen_at": now,
        "last_seen_at": now,
        "evicted_at": pd.Series(pd.NaT, index=new.index, dtype="datetime64[ns, UTC]"),
    })
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

    panel_ids = [uid for uid in active_ids(panel) if uid not in top_users]
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
        "panel_size": int(panel["evicted_at"].isna().sum()),
        **report.as_dict(),
    }
    if not report.ok:
        _append_log(settings.runs_log, {**record, "status": "failed"})
        raise QualityError(report)

    out = snapshot_path(settings.raw_dir, now)
    out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(out, index=False, compression="zstd")

    panel = update_panel(panel, df, settings.panel_max, now, settings.panel_evict_days)
    settings.panel_path.parent.mkdir(parents=True, exist_ok=True)
    panel.to_parquet(settings.panel_path, index=False)

    active = int(panel["evicted_at"].isna().sum())
    record.update(status="ok", path=str(out.relative_to(settings.datastore)), panel_size=active,
                  panel_evicted=int(len(panel) - active))
    _append_log(settings.runs_log, record)
    for w in report.warnings:
        log.warning(w)
    return record


def _append_log(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a") as fh:
        fh.write(json.dumps(record) + "\n")
