from __future__ import annotations

import pandas as pd
import pytest

from livescope.experiments.analyze import Guardrail
from livescope.experiments.posthog import PostHogClient, build_user_table, exposures_query, fetch
from livescope.experiments.readout import plan, readout, to_markdown


def test_build_user_table():
    exposures = pd.DataFrame([
        ("p1", "control", "2026-10-12T10:00:00Z"),
        ("p2", "test", "2026-10-12T11:00:00Z"),
        ("p3", "test", "2026-10-13T09:00:00Z"),
        ("p4", "control", "2026-10-12T09:00:00Z"),
        ("p4", "test", "2026-10-14T09:00:00Z"),  # saw both variants: dropped
    ], columns=["person_id", "variant", "first_exposure"])
    events = pd.DataFrame([
        ("p1", "2026-10-05T10:00:00Z"),  # pre-period
        ("p1", "2026-10-12T09:00:00Z"),  # before p1's first exposure: neither pre nor post
        ("p2", "2026-10-12T12:00:00Z"),
        ("p2", "2026-10-15T12:00:00Z"),
        ("p3", "2026-10-30T12:00:00Z"),  # after the end
        ("p4", "2026-10-13T12:00:00Z"),
    ], columns=["person_id", "timestamp"])
    users, quality = build_user_table(exposures, events, "2026-10-12", "2026-10-26", pre_days=14)
    u = users.set_index("person_id")
    assert quality == {"exposed_people": 4, "mixed_variant_people_dropped": 1, "analysed_people": 3}
    assert "p4" not in u.index
    assert u.loc["p1", ["converted", "metric_count", "pre_count"]].tolist() == [0, 0, 1]
    assert u.loc["p2", ["converted", "metric_count", "pre_count"]].tolist() == [1, 2, 0]
    assert u.loc["p3", "converted"] == 0


class FakeSession:
    def __init__(self, payloads):
        self.payloads = list(payloads)
        self.calls = []

    def post(self, url, headers, json, timeout):
        self.calls.append((url, headers, json))
        payload = self.payloads.pop(0)
        return type("R", (), {"status_code": 200, "json": lambda self: payload, "text": ""})()


def test_fetch_queries_posthog():
    session = FakeSession([
        {"columns": ["person_id", "variant", "first_exposure"], "results": [["a", "control", "2026-10-12T10:00:00Z"], ["b", "test", "2026-10-12T10:00:00Z"]]},
        {"columns": ["person_id", "timestamp"], "results": [["b", "2026-10-13T10:00:00Z"]]},
    ])
    client = PostHogClient("https://eu.posthog.com", "123", "phx_key", session)
    users, _ = fetch(client, "cta-copy", "booking_clicked", "2026-10-12", "2026-10-26")
    url, headers, body = session.calls[0]
    assert url == "https://eu.posthog.com/api/projects/123/query/"
    assert headers["Authorization"] == "Bearer phx_key"
    assert body["query"]["kind"] == "HogQLQuery" and "'cta-copy'" in body["query"]["query"]
    assert "2026-09-28" in session.calls[1][2]["query"]["query"]  # pre-period start
    assert users.set_index("person_id").loc["b", "converted"] == 1


def test_query_quotes_values():
    assert "'it\\'s'" in exposures_query("it's", "2026-01-01", "2026-01-02")


def test_plan_and_readout():
    p = plan(baseline=0.04, mde=0.25, daily_users=150)
    assert p["n_per_group"] == pytest.approx(6745, rel=0.01)
    assert p["weeks_to_run"] == 13
    assert p["mde_abs_4_weeks"] > p["mde_abs_2_weeks"] * 0 and p["mde_abs_4_weeks"] < p["mde_abs_2_weeks"]

    import numpy as np
    rng = np.random.default_rng(0)
    n = 4000
    users = pd.DataFrame({
        "person_id": range(2 * n),
        "variant": ["control"] * n + ["test"] * n,
        "converted": np.r_[rng.binomial(1, 0.05, n), rng.binomial(1, 0.07, n)],
        "pre_count": rng.poisson(0.3, 2 * n),
        "bounced": rng.binomial(1, 0.4, 2 * n),
    })
    out = readout(users, guardrails=[Guardrail("bounced", 0.05, higher_is_better=False)])
    assert out["decision"].startswith("ship")
    assert 0 < out["detectable_abs_lift"] < 0.02
    md = to_markdown("cta-copy", out, {"mixed_variant_people_dropped": 3}, "2026-10-12 to 2026-10-26")
    assert "Decision: ship" in md and "| bounced |" in md and "dropped: 3" in md


def test_cli_readout_from_csv(tmp_path, monkeypatch, capsys):
    import numpy as np

    from livescope.cli import main

    rng = np.random.default_rng(1)
    n = 1500
    pd.DataFrame({
        "person_id": range(2 * n),
        "variant": ["control"] * n + ["test"] * n,
        "converted": rng.binomial(1, 0.1, 2 * n),
        "pre_count": rng.poisson(0.5, 2 * n),
    }).to_csv(tmp_path / "users.csv", index=False)
    monkeypatch.setenv("LIVESCOPE_EXPORTS", str(tmp_path / "exports"))
    assert main(["experiment-readout", "--flag", "cta", "--start", "2026-10-12", "--end", "2026-10-26",
                 "--csv", str(tmp_path / "users.csv")]) == 0
    md = (tmp_path / "exports" / "experiments" / "cta" / "readout.md").read_text()
    assert "Decision:" in md and "CUPED" in md
    assert main(["experiment-readout", "--flag", "cta", "--start", "2026-10-12", "--end", "2026-10-26"]) == 2
