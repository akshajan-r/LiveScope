"""Checks the PySpark job against the DuckDB path. Skipped without pyspark/Java."""

from __future__ import annotations

import importlib.util
import shutil
import sys
from pathlib import Path

import duckdb
import pytest

from livescope import ucsd

pytest.importorskip("pyspark")
if shutil.which("java") is None:
    pytest.skip("Java not installed", allow_module_level=True)

spec = importlib.util.spec_from_file_location("ucsd_spark", Path(__file__).parents[1] / "spark" / "ucsd_spark.py")
ucsd_spark = importlib.util.module_from_spec(spec)
sys.modules["ucsd_spark"] = ucsd_spark
spec.loader.exec_module(ucsd_spark)


def test_spark_matches_duckdb(tmp_path):
    path = ucsd.synthetic_csv(tmp_path / "x.csv", n_users=200, n_streamers=30)
    con = duckdb.connect()
    ucsd.load(con, path)
    ucsd.build_profiles(con)
    expected = con.execute("select * from ucsd_streamer order by streamer").df()
    conc = con.execute("select pct::double, watch_share from ucsd_concentration order by pct").fetchall()

    spark = ucsd_spark.spark_session("1g")
    try:
        df = spark.read.csv(str(path), schema=ucsd_spark.SCHEMA, header=False)
        profile = ucsd_spark.streamer_profile(df)
        got = profile.toPandas().sort_values("streamer").reset_index(drop=True)
        spark_conc = ucsd_spark.concentration(profile)
    finally:
        spark.stop()

    cols = ["interactions", "unique_viewers", "streams", "watch_hours", "avg_session_minutes", "active_days", "return_rate"]
    assert list(got["streamer"]) == list(expected["streamer"])
    for col in cols:
        assert got[col].astype(float).round(6).tolist() == expected[col].astype(float).round(6).tolist(), col
    for (p1, s1), (p2, s2) in zip(conc, spark_conc, strict=True):
        assert p1 == pytest.approx(p2) and s1 == pytest.approx(s2)
