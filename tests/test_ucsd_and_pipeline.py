from __future__ import annotations

import json
from types import SimpleNamespace

import duckdb
import pandas as pd
import pytest

from livescope import pipeline, ucsd
from livescope.demo import write_demo_store


@pytest.fixture
def ucsd_con(tmp_path):
    con = duckdb.connect()
    ucsd.load(con, ucsd.synthetic_csv(tmp_path / "x.csv", n_users=300, n_streamers=40))
    yield con
    con.close()


def test_ucsd_profiles(ucsd_con):
    counts = ucsd.build_profiles(ucsd_con)
    assert counts["ucsd_streamer"] > 0 and counts["ucsd_concentration"] == 3
    shares = [r[0] for r in ucsd_con.execute("select watch_share from ucsd_concentration order by pct").fetchall()]
    assert shares == sorted(shares) and 0 < shares[-1] <= 1


def test_return_labels(tmp_path):
    rows = [
        (1, 1, "alice", 10, 12),                          # day 0
        (1, 2, "alice", 5 * 144, 5 * 144 + 3),            # day 5: inside the 7-day horizon from cutoff day 2
        (2, 3, "alice", 20, 21),                          # never returns
        (2, 4, "bob", 30, 31),
        (2, 5, "bob", 12 * 144, 12 * 144 + 1),            # day 12: after the horizon
    ]
    path = tmp_path / "t.csv"
    pd.DataFrame(rows).to_csv(path, header=False, index=False)
    con = duckdb.connect()
    ucsd.load(con, path)
    df = ucsd.return_dataset(con, cutoff_day=2, horizon_days=7).set_index(["user_id", "streamer"])
    assert df.loc[(1, "alice"), "returned"] == 1
    assert df.loc[(2, "alice"), "returned"] == 0
    assert df.loc[(2, "bob"), "returned"] == 0
    assert df.loc[(2, "alice"), "user_streamers"] == 2
    assert len(df) == 3  # pairs first seen after the cutoff are not included


def test_return_model_runs(ucsd_con):
    res = ucsd.evaluate_returns(ucsd_con, sample_rows=5000)
    assert set(res["metrics"]["model"]) >= {"recency_rule", "logistic_regression"}
    assert res["metrics"]["roc_auc"].between(0, 1).all()
    with pytest.raises(ValueError):
        ucsd.evaluate_returns(ucsd_con, train_cutoff=21, test_cutoff=25)


def test_download_picks_file_from_folder(tmp_path, monkeypatch):
    calls = {}
    fake = SimpleNamespace(
        download_folder=lambda **kw: [SimpleNamespace(id="ID_FULL", path="full_a.csv.gz"), SimpleNamespace(id="ID_100K", path="100k_a.csv")],
        download=lambda id, output, quiet: calls.update(id=id, output=output) or output,
    )
    monkeypatch.setitem(__import__("sys").modules, "gdown", fake)
    out = ucsd.download(tmp_path, "100k")
    assert calls["id"] == "ID_100K" and out.name == "100k_a.csv"


def test_pipeline_end_to_end(tmp_path, settings):
    write_demo_store(settings.datastore, n_creators=150, weeks=7, seed=11)
    meta = pipeline.run(settings, abtest_sims=50)
    assert meta["source"] == "synthetic"
    assert meta["complete_weeks"] == 7
    assert meta["analyses"]["segmentation"]["status"] == "ok"
    assert meta["analyses"]["predict_growth"]["status"] == "ok"
    dash = settings.exports / "dashboard"
    for name in pipeline.EXPORT_TABLES:
        assert (dash / f"{name}.arrow").exists()
        assert (settings.exports / "tableau" / f"{name}.csv").exists()
        assert (settings.exports / "parquet" / f"{name}.parquet").exists()
    results = json.loads((dash / "analyses.json").read_text())
    assert "abtest_validation" in results and "segment_profiles" in results
    assert meta["analyses"]["survival"]["status"] == "ok"
    assert {"survival_curves", "survival_milestones", "segment_language_mix", "findings"} <= set(results)
    assert all(f["status"] in ("measured", "pending") for f in results["findings"])
    assert (settings.exports / "findings.md").read_text().startswith("# Measured facts")
    import pyarrow as pa
    with pa.OSFile(str(dash / "creator_week.arrow"), "rb") as f:
        assert pa.ipc.open_stream(f).read_all().num_rows > 0


def test_pipeline_with_little_data_skips_analyses(settings):
    write_demo_store(settings.datastore, n_creators=30, weeks=1, seed=1)
    meta = pipeline.run(settings, abtest_sims=20)
    assert meta["analyses"]["segmentation"]["status"] == "skipped"
    assert meta["analyses"]["predict_growth"]["status"] == "skipped"
    assert meta["analyses"]["did_peak_hours"]["status"] == "skipped"
