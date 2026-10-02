from __future__ import annotations

from pathlib import Path

import pytest

from livescope.config import Settings
from livescope.demo import write_demo_store
from livescope.warehouse import build


@pytest.fixture
def settings(tmp_path: Path) -> Settings:
    return Settings(
        datastore=tmp_path / "store",
        warehouse=tmp_path / "wh.duckdb",
        exports=tmp_path / "exports",
        max_streams=4,
        panel_max=10,
    )


@pytest.fixture(scope="session")
def demo_store(tmp_path_factory) -> Path:
    root = tmp_path_factory.mktemp("demo")
    write_demo_store(root, n_creators=250, weeks=8, seed=3)
    return root


@pytest.fixture(scope="session")
def demo_creator_week(demo_store):
    con = build(demo_store / "raw" / "twitch_streams")
    df = con.execute("select * from creator_week").df()
    con.close()
    return df
