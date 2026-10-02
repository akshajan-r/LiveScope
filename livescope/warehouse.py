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


def build(raw_dir: Path, warehouse: Path | str = ":memory:", panel_path: Path | None = None) -> duckdb.DuckDBPyConnection:
    """Run every SQL model over the snapshots in `raw_dir`.

    `panel_path` is the collector's panel file (creators tracked outside the
    top list). Without it, every creator is treated as tracked, which is right
    for synthetic data where every live creator is observed.
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
    if panel_path is not None and Path(panel_path).exists():
        con.execute(
            f"create or replace table panel as "
            f"select user_id, first_seen_at::timestamp as first_seen_at from read_parquet('{panel_path}')"
        )
    else:
        con.execute(
            "create or replace table panel as "
            "select user_id, min(snapshot_hour::timestamp) as first_seen_at from raw_snapshots group by user_id"
        )
    for name, sql in sql_models():
        log.info("running %s", name)
        con.execute(sql)
    return con


def table_counts(con: duckdb.DuckDBPyConnection) -> dict[str, int]:
    tables = [r[0] for r in con.execute("select table_name from information_schema.tables where table_type = 'BASE TABLE' order by 1").fetchall()]
    return {t: con.execute(f"select count(*) from {t}").fetchone()[0] for t in tables}
