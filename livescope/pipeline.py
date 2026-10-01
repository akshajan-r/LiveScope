"""Build the warehouse, run the analyses that the data supports, export tables.

Outputs (in `exports/`):
  dashboard/  Arrow IPC tables, analyses.json (small result tables) and meta.json,
              read by the Observable Framework dashboard
  tableau/    CSV files for Tableau Public / Power BI
  parquet/    the same tables as Parquet (BigQuery loads these)

Analyses that need more history than exists yet (segmentation needs complete
weeks, prediction and the natural experiment need several) are skipped with a
reason recorded in meta.json, so the pipeline works from the first snapshot on.
"""

from __future__ import annotations

import json
import logging
import shutil
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import pyarrow as pa

from livescope import warehouse
from livescope.causal.did import peak_hours_did
from livescope.config import Settings
from livescope.experiments.simulate import validate
from livescope.predict import build_dataset, evaluate
from livescope.segmentation import creator_features, segment

log = logging.getLogger(__name__)

EXPORT_TABLES = {
    "creator_week": "select * from creator_week",
    "creator_summary": "select * from creator_summary",
    "platform_hour": "select * from platform_hour order by snapshot_hour",
    "category_week": "select * from category_week",
    "peak_hours": "select * from peak_hours order by hour_utc",
    "collector_weeks": "select * from collector_weeks order by week_start",
    "platform_week": "select * from platform_week order by week_start",
}


def _write(df: pd.DataFrame, name: str, exports: Path) -> None:
    for sub in ("dashboard", "tableau", "parquet"):
        (exports / sub).mkdir(parents=True, exist_ok=True)
    df.to_parquet(exports / "parquet" / f"{name}.parquet", index=False)
    # Uncompressed Arrow IPC stream: DuckDB-wasm in the dashboard reads it without
    # extensions, and apache-arrow JS cannot decode compressed IPC buffers.
    table = pa.Table.from_pandas(df, preserve_index=False)
    with pa.OSFile(str(exports / "dashboard" / f"{name}.arrow"), "wb") as sink:
        with pa.ipc.new_stream(sink, table.schema) as writer:
            writer.write_table(table)
    flat = df.copy()
    for col in flat.columns:
        if flat[col].dtype == object and flat[col].map(lambda v: isinstance(v, (list, tuple))).any():
            flat[col] = flat[col].map(lambda v: "|".join(map(str, v)) if isinstance(v, (list, tuple)) else v)
    flat.to_csv(exports / "tableau" / f"{name}.csv", index=False)


def run(settings: Settings, exports: Path | None = None, abtest_sims: int = 500) -> dict:
    exports = exports or settings.exports
    if exports.exists():
        shutil.rmtree(exports)
    con = warehouse.build(settings.raw_dir, settings.warehouse)

    for name, sql in EXPORT_TABLES.items():
        _write(con.execute(sql).df(), name, exports)

    cw = con.execute("select * from creator_week").df()
    analyses: dict[str, dict] = {}
    # Small result tables go into one JSON file that always exists, so the
    # dashboard builds even when an analysis is skipped for lack of history.
    results: dict[str, list[dict]] = {}

    def keep(name: str, df: pd.DataFrame, tableau: bool = True) -> None:
        results[name] = json.loads(df.to_json(orient="records", date_format="iso"))
        if tableau:
            (exports / "tableau").mkdir(parents=True, exist_ok=True)
            df.to_csv(exports / "tableau" / f"{name}.csv", index=False)

    try:
        res = segment(creator_features(cw))
        keep("segments", res.assignments)
        keep("segment_profiles", res.profiles)
        keep("segment_k_selection", pd.DataFrame({
            "k": list(res.silhouette_by_k), "silhouette": list(res.silhouette_by_k.values()),
            "gmm_bic": [res.bic_by_k[k] for k in res.silhouette_by_k]}))
        analyses["segmentation"] = {"status": "ok", "k": res.k, "creators": len(res.assignments)}
    except ValueError as exc:
        analyses["segmentation"] = {"status": "skipped", "reason": str(exc)}

    for target in ("growth", "churn"):
        try:
            rep = evaluate(build_dataset(cw), target=target)
            keep(f"model_metrics_{target}", rep.metrics)
            keep(f"feature_importance_{target}", rep.importance)
            weeks = cw.drop_duplicates("week_index").set_index("week_index")["week_start"].dt.strftime("%Y-%m-%d")
            analyses[f"predict_{target}"] = {
                "status": "ok", "train_rows": rep.train_rows, "test_rows": rep.test_rows,
                "train_weeks": [weeks[w] for w in rep.train_weeks],
                "test_weeks": [weeks[w] for w in rep.test_weeks],
                "base_rate_test": rep.base_rate_test,
            }
        except ValueError as exc:
            analyses[f"predict_{target}"] = {"status": "skipped", "reason": str(exc)}

    try:
        did = peak_hours_did(cw)
        keep("did_event_study", did.event_study)
        keep("did_summary", pd.DataFrame([{
            **did.did, "n_treated": did.n_treated, "n_control": did.n_control,
            "event_week_start": cw.loc[cw["week_index"] == did.event_week_index, "week_start"].iloc[0].strftime("%Y-%m-%d"),
            "pretrend_p_value": did.pretrend_p_value}]))
        analyses["did_peak_hours"] = {"status": "ok", "n_treated": did.n_treated, "n_control": did.n_control}
    except ValueError as exc:
        analyses["did_peak_hours"] = {"status": "skipped", "reason": str(exc)}

    keep("abtest_validation", validate(n_sims=abtest_sims, seed=42))
    analyses["abtest_validation"] = {"status": "ok", "simulations": abtest_sims}

    stats = con.execute(
        """
        select count(*) as snapshot_rows, count(distinct user_id) as creators,
               min(snapshot_hour) as first_snapshot, max(snapshot_hour) as last_snapshot,
               count(distinct snapshot_hour) as snapshot_hours
        from stg_streams
        """
    ).df().iloc[0]
    meta = {
        "source": "synthetic" if (settings.datastore / "SYNTHETIC").exists() else "twitch",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "snapshot_rows": int(stats.snapshot_rows),
        "creators": int(stats.creators),
        "snapshot_hours": int(stats.snapshot_hours),
        "first_snapshot": str(stats.first_snapshot),
        "last_snapshot": str(stats.last_snapshot),
        "complete_weeks": int(con.execute("select count(*) from collector_weeks where is_complete").fetchone()[0]),
        "max_streams_per_snapshot": settings.max_streams,
        "panel_max": settings.panel_max,
        "analyses": analyses,
    }
    (exports / "dashboard" / "meta.json").write_text(json.dumps(meta, indent=2, default=str))
    (exports / "dashboard" / "analyses.json").write_text(json.dumps(results, default=str))
    (exports / "tableau" / "meta.json").write_text(json.dumps(meta, indent=2, default=str))
    con.close()
    return meta
