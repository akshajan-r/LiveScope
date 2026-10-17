"""Paths and settings, overridable through environment variables."""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


def _env_int(name: str, default: int) -> int:
    value = os.environ.get(name, "").strip()
    return int(value) if value else default


@dataclass(frozen=True)
class Settings:
    # Root of the data store. In CI this is a checkout of the `data` branch.
    datastore: Path
    # DuckDB warehouse file built from the raw snapshots.
    warehouse: Path
    # Where exported tables (Parquet/CSV for the dashboard and Tableau) go.
    exports: Path
    # Number of top live streams (by concurrent viewers) captured per snapshot.
    max_streams: int
    # Maximum number of creators actively tracked in the panel (see docs/data.md).
    panel_max: int
    # Creators not seen live for this many days stop being looked up (they
    # stay in the panel file, marked evicted, so retention analysis keeps them).
    panel_evict_days: int = 28
    # Days of raw snapshots kept on the data branch; older days are deleted
    # after their weekly summaries are saved to history/. 0 keeps everything.
    raw_retention_days: int = 30

    @property
    def raw_dir(self) -> Path:
        return self.datastore / "raw" / "twitch_streams"

    @property
    def panel_path(self) -> Path:
        return self.datastore / "state" / "panel.parquet"

    @property
    def history_dir(self) -> Path:
        return self.datastore / "history"

    @property
    def runs_log(self) -> Path:
        return self.datastore / "manifest" / "runs.jsonl"

    @property
    def ucsd_dir(self) -> Path:
        return self.datastore / "ucsd"


def get_settings() -> Settings:
    datastore = Path(os.environ.get("LIVESCOPE_DATASTORE", "datastore"))
    return Settings(
        datastore=datastore,
        warehouse=Path(os.environ.get("LIVESCOPE_WAREHOUSE", "build/livescope.duckdb")),
        exports=Path(os.environ.get("LIVESCOPE_EXPORTS", "exports")),
        max_streams=_env_int("LIVESCOPE_MAX_STREAMS", 2000),
        panel_max=_env_int("LIVESCOPE_PANEL_MAX", 60000),
        panel_evict_days=_env_int("LIVESCOPE_PANEL_EVICT_DAYS", 28),
        raw_retention_days=_env_int("LIVESCOPE_RAW_RETENTION_DAYS", 30),
    )
