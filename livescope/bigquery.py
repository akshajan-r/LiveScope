"""Load exported Parquet tables into BigQuery (works in the free sandbox).

Authentication uses Application Default Credentials: in GitHub Actions,
google-github-actions/auth sets them from a service-account key or workload
identity federation. Sandbox tables expire after 60 days, so the workflow
reloads them on every run (WRITE_TRUNCATE).
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path


def load_exports(export_dir: Path, project: str, dataset: str = "livescope", location: str = "US") -> Iterator[str]:
    from google.cloud import bigquery

    client = bigquery.Client(project=project)
    ds = bigquery.Dataset(f"{project}.{dataset}")
    ds.location = location
    client.create_dataset(ds, exists_ok=True)
    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.PARQUET,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )
    for path in sorted(Path(export_dir).glob("*.parquet")):
        table_id = f"{project}.{dataset}.{path.stem}"
        with path.open("rb") as fh:
            client.load_table_from_file(fh, table_id, job_config=job_config).result()
        yield f"loaded {path.name} -> {table_id} ({client.get_table(table_id).num_rows} rows)"
