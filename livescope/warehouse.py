"""Build the DuckDB warehouse from raw snapshot files by running sql/*.sql in order."""

from __future__ import annotations

import logging
from importlib import resources
from pathlib import Path

import duckdb

log = logging.getLogger(__name__)


def sql_models() -> list[tuple[str, str]]:
    files = sorted(
        (f for f in resources.files("livescope.sql").iterdir() if f.name.endswith(".sql")),
        key=lambda f: f.name,
    )
    return [(f.name, f.read_text()) for f in files]


def connect(warehouse: Path | str = ":memory:") -> duckdb.DuckDBPyConnection:
    if warehouse != ":memory:":
        Path(warehouse).parent.mkdir(parents=True, exist_ok=True)
    con = duckdb.connect(str(warehouse))
    con.execute("set TimeZone = 'UTC'")
    return con


# Weekly summaries saved by livescope.storage before old raw snapshots are
# deleted. Empty tables with these schemas stand in when no history exists.
HISTORY_TABLES = {
    "collector_weeks": "week_start DATE, hours_observed BIGINT",
    "creator_week_base": (
        "user_id VARCHAR, week_start DATE, user_login VARCHAR, hours_live BIGINT, streams BIGINT, "
        "days_live BIGINT, avg_viewers DOUBLE, peak_viewers BIGINT, median_viewers DOUBLE, viewer_hours DOUBLE, "
        "categories BIGINT, main_category VARCHAR, language VARCHAR, peak_hour_share DOUBLE, "
        "top_list_share DOUBLE, best_rank BIGINT"
    ),
    "category_week": (
        "week_start DATE, game_name VARCHAR, creators BIGINT, creator_hours BIGINT, viewer_hours DOUBLE, "
        "viewers_per_live_hour DOUBLE"
    ),
}


def load_history(con: duckdb.DuckDBPyConnection, history_dir: Path | None) -> None:
    for name, ddl in HISTORY_TABLES.items():
        path = Path(history_dir) / f"{name}.parquet" if history_dir else None
        if path is not None and path.exists():
            con.execute(f"create or replace table history_{name} as select * from read_parquet('{path}')")
        else:
            con.execute(f"create or replace table history_{name} ({ddl})")


def build(raw_dir: Path, warehouse: Path | str = ":memory:", panel_path: Path | None = None,
          history_dir: Path | None = None) -> duckdb.DuckDBPyConnection:
    """Run every SQL model over the snapshots in `raw_dir`.

    `panel_path` is the collector's panel file (creators tracked outside the
    top list). Without it, every creator is treated as tracked, which is right
    for synthetic data where every live creator is observed. `history_dir`
    holds weekly summaries of weeks whose raw snapshots have been deleted.
    """
    files = sorted(Path(raw_dir).glob("**/*.parquet"))
    if not files:
        raise FileNotFoundError(f"no snapshot files under {raw_dir}")
    con = connect(warehouse)
    glob = str(Path(raw_dir) / "**" / "*.parquet")
    con.execute(
        f"create or replace view raw_snapshots as "
        f"select * from read_parquet('{glob}', union_by_name = true, hive_partitioning = false)"
    )
    load_history(con, history_dir)
    if panel_path is not None and Path(panel_path).exists():
        con.execute(
            f"create or replace table panel as "
            f"select user_id, first_seen_at::timestamp as first_seen_at from read_parquet('{panel_path}')"
        )
    else:
        # First seen = earliest of the raw snapshots and the saved weekly history,
        # so deleting old raw days does not move it.
        con.execute(
            "create or replace table panel as "
            "select user_id, min(t) as first_seen_at from ("
            "  select user_id, snapshot_hour::timestamp as t from raw_snapshots"
            "  union all select user_id, week_start::timestamp from history_creator_week_base"
            ") group by user_id"
        )
    for name, sql in sql_models():
        log.info("running %s", name)
        con.execute(sql)
    return con


def table_counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    tables = [r[0] for r in con.execute("select table_name from information_schema.tables where table_type = 'BASE TABLE' order by 1").fetchall()]
    return {t: con.execute(f"select count(*) from {t}").fetchone()[0] for t in tables}
