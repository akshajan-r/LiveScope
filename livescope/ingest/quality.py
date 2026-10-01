"""Data-quality checks run on every snapshot before it is written."""

from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

REQUIRED_COLUMNS = [
    "snapshot_at",
    "snapshot_hour",
    "stream_id",
    "user_id",
    "user_login",
    "game_id",
    "game_name",
    "language",
    "viewer_count",
    "started_at",
    "source",
]

# A started_at slightly after the snapshot time can happen with clock skew.
CLOCK_SKEW = pd.Timedelta(minutes=5)


@dataclass
class QualityReport:
    rows: int
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors

    def as_dict(self) -> dict:
        return {"rows": self.rows, "errors": self.errors, "warnings": self.warnings}


def check_snapshot(df: pd.DataFrame, min_rows: int = 1) -> QualityReport:
    """Errors block the write; warnings are logged in the run manifest."""
    report = QualityReport(rows=len(df))

    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        report.errors.append(f"missing columns: {missing}")
        return report

    if len(df) < min_rows:
        report.errors.append(f"only {len(df)} rows (minimum {min_rows})")
        if df.empty:
            return report

    for col in ("stream_id", "user_id", "snapshot_at"):
        n = int(df[col].isna().sum())
        if n:
            report.errors.append(f"{n} null values in {col}")

    dupes = int(df["stream_id"].duplicated().sum())
    if dupes:
        report.errors.append(f"{dupes} duplicate stream_id values")

    negative = int((df["viewer_count"] < 0).sum())
    if negative:
        report.errors.append(f"{negative} negative viewer counts")

    if df["snapshot_hour"].nunique() != 1:
        report.errors.append("snapshot spans more than one snapshot_hour")

    future = int((df["started_at"] > df["snapshot_at"] + CLOCK_SKEW).sum())
    if future:
        report.warnings.append(f"{future} streams start after the snapshot time")

    dupe_users = int(df["user_id"].duplicated().sum())
    if dupe_users:
        report.warnings.append(f"{dupe_users} users with more than one live stream")

    null_game = int((df["game_name"].fillna("") == "").sum())
    if null_game / max(len(df), 1) > 0.2:
        report.warnings.append(f"{null_game} streams without a category")

    bad_source = set(df["source"].unique()) - {"top", "panel"}
    if bad_source:
        report.errors.append(f"unexpected source values: {sorted(bad_source)}")

    return report
