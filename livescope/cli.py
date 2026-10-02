"""Command line entry point: `python -m livescope <command>`."""

from __future__ import annotations

import argparse
import json
import logging
import os
import sys
from pathlib import Path

from livescope.config import get_settings


def _set_output(name: str, value: str) -> None:
    """Expose a value to later GitHub Actions steps (no-op outside Actions)."""
    path = os.environ.get("GITHUB_OUTPUT")
    if path:
        with open(path, "a") as fh:
            fh.write(f"{name}={value}\n")


def cmd_ingest(args, settings) -> int:
    from livescope.ingest.snapshot import QualityError, run_snapshot
    from livescope.ingest.twitch import HelixClient, HelixError
    from livescope.status import captured_this_hour

    if args.skip_if_captured and captured_this_hour(settings):
        print("a snapshot for this hour already exists; skipping")
        _set_output("captured", "false")
        return 0
    _set_output("captured", "true")
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


def cmd_status(args, settings) -> int:
    from livescope.status import to_markdown

    md = to_markdown(settings)
    if args.write:
        (settings.datastore / "README.md").write_text(md)
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary_path:
        with open(summary_path, "a") as fh:
            fh.write(md.split("## Layout")[0])
    print(md)
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


def cmd_experiment_plan(args, settings) -> int:
    from livescope.experiments.readout import plan

    p = plan(args.baseline, args.mde, args.daily_users, relative=not args.absolute, traffic_share=args.traffic_share)
    lift = f"{args.mde:.0%} relative" if not args.absolute else f"{args.mde * 100:.2f} percentage points"
    print(f"Baseline conversion {args.baseline:.2%}, detecting a {lift} change at alpha 0.05, power 0.8:")
    print(f"  {p['n_per_group']:,} people per group, {p['days_needed']} days at {p['daily_users_in_test']:,.0f} people/day "
          f"-> run {p['weeks_to_run']} full weeks")
    for w in (2, 4):
        v = p[f"mde_abs_{w}_weeks"]
        if v == v:
            print(f"  If capped at {w} weeks: smallest detectable change {v * 100:.2f} pp ({v / args.baseline:.0%} relative)")
    return 0


def cmd_experiment_readout(args, settings) -> int:
    import pandas as pd

    from livescope.experiments.analyze import Guardrail
    from livescope.experiments.readout import readout, to_markdown

    quality = None
    if args.csv:
        users = pd.read_csv(args.csv)
    elif not args.event:
        print("--event is required when reading from PostHog", file=sys.stderr)
        return 2
    else:
        from livescope.experiments.posthog import PostHogClient, fetch

        client = PostHogClient(os.environ.get("POSTHOG_HOST", "https://eu.posthog.com"),
                               os.environ["POSTHOG_PROJECT_ID"], os.environ["POSTHOG_API_KEY"])
        users, quality = fetch(client, args.flag, args.event, args.start, args.end, args.pre_days)
    guardrails = [Guardrail(m, args.guardrail_margin, higher_is_better=False) for m in args.guardrail]
    out = readout(users, control=args.control, treatment=args.treatment, guardrails=guardrails)
    md = to_markdown(args.flag, out, quality, f"{args.start} to {args.end} (UTC)")
    dest = settings.exports / "experiments" / args.flag
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "readout.md").write_text(md)
    print(md)
    print(f"written to {dest / 'readout.md'} (user-level data was not saved)")
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

    p = sub.add_parser("ingest", help="capture one snapshot of live Twitch streams")
    p.add_argument("--skip-if-captured", action="store_true", help="do nothing if this UTC hour already has a snapshot")

    p = sub.add_parser("status", help="summarise collected snapshots and recent runs")
    p.add_argument("--write", action="store_true", help="also write the summary to the data store's README.md")
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

    p = sub.add_parser("experiment-plan", help="sample size and duration for a conversion A/B test")
    p.add_argument("--baseline", type=float, required=True, help="current conversion rate, e.g. 0.04")
    p.add_argument("--mde", type=float, required=True, help="smallest change worth detecting (relative unless --absolute)")
    p.add_argument("--absolute", action="store_true", help="treat --mde as percentage points (0.01 = 1pp)")
    p.add_argument("--daily-users", type=float, required=True, help="eligible visitors per day")
    p.add_argument("--traffic-share", type=float, default=1.0, help="share of traffic in the test")

    p = sub.add_parser("experiment-readout", help="analyse a PostHog feature-flag experiment")
    p.add_argument("--flag", required=True, help="feature flag key")
    p.add_argument("--event", help="metric event name (required unless --csv)")
    p.add_argument("--start", required=True, help="experiment start, e.g. 2026-10-12")
    p.add_argument("--end", required=True, help="experiment end (exclusive)")
    p.add_argument("--control", default="control")
    p.add_argument("--treatment", default="test")
    p.add_argument("--pre-days", type=int, default=14)
    p.add_argument("--guardrail", action="append", default=[], help="column in --csv that must not get worse (lower is better)")
    p.add_argument("--guardrail-margin", type=float, default=0.01)
    p.add_argument("--csv", help="user table instead of querying PostHog (person_id, variant, converted, pre_count, ...)")

    p = sub.add_parser("bigquery", help="load exported tables into BigQuery")
    p.add_argument("--project", required=True)
    p.add_argument("--dataset", default="livescope")
    p.add_argument("--location", default="US")

    args = parser.parse_args(argv)
    settings = get_settings()
    handler = {
        "ingest": cmd_ingest, "status": cmd_status, "build": cmd_build, "demo": cmd_demo, "ucsd": cmd_ucsd,
        "abtest-validate": cmd_abtest, "bigquery": cmd_bigquery,
        "experiment-plan": cmd_experiment_plan, "experiment-readout": cmd_experiment_readout,
    }[args.command]
    return handler(args, settings)


if __name__ == "__main__":
    sys.exit(main())
