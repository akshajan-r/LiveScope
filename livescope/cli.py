"""Command line entry point: `python -m livescope <command>`."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from livescope.config import get_settings


def cmd_ingest(args, settings) -> int:
    from livescope.ingest.snapshot import QualityError, run_snapshot
    from livescope.ingest.twitch import HelixClient, HelixError

    try:
        client = HelixClient(os.environ.get("TWITCH_CLIENT_ID", ""), os.environ.get("TWITCH_CLIENT_SECRET", ""))
        record = run_snapshot(client, settings)
    except QualityError as exc:
        print(f"quality checks failed, nothing written: {exc}", file=sys.stderr)
        return 1
    except HelixError as exc:
        print(f"Twitch API error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(record, indent=2))
    return 0


def cmd_build(args, settings) -> int:
    from livescope import pipeline

    meta = pipeline.run(settings)
    print(json.dumps(meta, indent=2, default=str))
    return 0


def cmd_demo(args, settings) -> int:
    from livescope.demo import write_demo_store

    if (settings.raw_dir.exists() and any(settings.raw_dir.iterdir())
            and not (settings.datastore / "SYNTHETIC").exists()):
        print(f"{settings.datastore} already holds collected data; use a different LIVESCOPE_DATASTORE", file=sys.stderr)
        return 1
    n = write_demo_store(settings.datastore, n_creators=args.creators, weeks=args.weeks, seed=args.seed)
    print(f"wrote {n} synthetic snapshot rows to {settings.raw_dir}")
    return 0


def cmd_ucsd(args, settings) -> int:
    from livescope import ucsd, warehouse

    path = Path(args.file) if args.file else ucsd.download(settings.ucsd_dir, args.variant, args.file_id)
    con = warehouse.connect(args.warehouse or ":memory:")
    ucsd.load(con, path)
    print(json.dumps(ucsd.build_profiles(con)))
    out = settings.exports / "ucsd"
    out.mkdir(parents=True, exist_ok=True)
    for table in ("ucsd_streamer", "ucsd_daily", "ucsd_concentration"):
        con.execute(f"copy {table} to '{out / table}.parquet' (format parquet)")
        con.execute(f"copy {table} to '{out / table}.csv' (header)")
    if not args.skip_model:
        res = ucsd.evaluate_returns(con, sample_rows=args.sample_rows)
        res["metrics"].to_csv(out / "return_model_metrics.csv", index=False)
        if res["importance"] is not None:
            res["importance"].to_csv(out / "return_feature_importance.csv", index=False)
        print(res["metrics"].to_string(index=False))
        print({k: v for k, v in res.items() if k not in ("metrics", "importance")})
    return 0


def cmd_abtest(args, settings) -> int:
    from livescope.experiments.simulate import validate

    print(validate(n_sims=args.sims, seed=args.seed).to_string(index=False))
    return 0


def cmd_bigquery(args, settings) -> int:
    from livescope.bigquery import load_exports

    for line in load_exports(settings.exports / "parquet", args.project, args.dataset, args.location):
        print(line)
    return 0


def main(argv: list[str] | None = None) -> int:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(name)s: %(message)s")
    parser = argparse.ArgumentParser(prog="livescope")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("ingest", help="capture one snapshot of live Twitch streams")
    sub.add_parser("build", help="build the warehouse, run analyses, export tables")

    p = sub.add_parser("demo", help="write synthetic snapshots for local development")
    p.add_argument("--creators", type=int, default=400)
    p.add_argument("--weeks", type=int, default=8)
    p.add_argument("--seed", type=int, default=7)

    p = sub.add_parser("ucsd", help="download and process the UCSD Twitch dataset")
    p.add_argument("--variant", choices=["100k", "full"], default="100k")
    p.add_argument("--file", help="use an already downloaded CSV instead of downloading")
    p.add_argument("--file-id", help="Google Drive file id, if folder listing fails")
    p.add_argument("--warehouse", help="DuckDB file to keep the tables in (default: in memory)")
    p.add_argument("--sample-rows", type=int, default=1_000_000, help="pairs sampled per split for the return model")
    p.add_argument("--skip-model", action="store_true")

    p = sub.add_parser("abtest-validate", help="validate the A/B toolkit on simulated experiments")
    p.add_argument("--sims", type=int, default=1000)
    p.add_argument("--seed", type=int, default=42)

    p = sub.add_parser("bigquery", help="load exported tables into BigQuery")
    p.add_argument("--project", required=True)
    p.add_argument("--dataset", default="livescope")
    p.add_argument("--location", default="US")

    args = parser.parse_args(argv)
    settings = get_settings()
    handler = {
        "ingest": cmd_ingest, "build": cmd_build, "demo": cmd_demo, "ucsd": cmd_ucsd,
        "abtest-validate": cmd_abtest, "bigquery": cmd_bigquery,
    }[args.command]
    return handler(args, settings)


if __name__ == "__main__":
    sys.exit(main())
