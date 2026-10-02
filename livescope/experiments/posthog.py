"""Pull a PostHog feature-flag experiment and turn it into one row per user.

Exposure is PostHog's `$feature_flag_called` event, which posthog-js sends the
first time a page evaluates the flag. Each person's variant is the flag value
they were shown; people who were shown more than one variant are dropped and
counted (they usually mean a flag change mid-test or a shared device).

Outcomes, per person:
  converted     1 if they triggered the metric event after first exposure
  metric_count  how many times they triggered it after first exposure
  pre_count     how many times they triggered it in the `pre_days` before the
                experiment started (the CUPED covariate; 0 for new visitors)

The user table contains PostHog person ids, so keep it out of the repository;
publish only the readout.
"""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd
import requests

ROW_LIMIT = 50_000


def _quote(value: str) -> str:
    return "'" + str(value).replace("\\", "\\\\").replace("'", "\\'") + "'"


@dataclass
class PostHogClient:
    host: str          # e.g. https://eu.posthog.com for PostHog's EU cloud
    project_id: str
    api_key: str       # personal API key with query:read access
    session: requests.Session | None = None

    def query(self, hogql: str) -> pd.DataFrame:
        sess = self.session or requests.Session()
        resp = sess.post(
            f"{self.host.rstrip('/')}/api/projects/{self.project_id}/query/",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"query": {"kind": "HogQLQuery", "query": hogql}},
            timeout=120,
        )
        if resp.status_code != 200:
            raise RuntimeError(f"PostHog query failed: HTTP {resp.status_code}: {resp.text[:300]}")
        payload = resp.json()
        df = pd.DataFrame(payload.get("results", []), columns=payload.get("columns"))
        if len(df) >= ROW_LIMIT:
            raise RuntimeError(f"query hit the {ROW_LIMIT:,}-row limit; narrow the date range or aggregate first")
        return df


def exposures_query(flag: str, start: str, end: str) -> str:
    return f"""
        SELECT person_id, properties.$feature_flag_response AS variant, min(timestamp) AS first_exposure
        FROM events
        WHERE event = '$feature_flag_called'
          AND properties.$feature_flag = {_quote(flag)}
          AND timestamp >= toDateTime({_quote(start)}) AND timestamp < toDateTime({_quote(end)})
        GROUP BY person_id, variant
        LIMIT {ROW_LIMIT}
    """


def events_query(event: str, start: str, end: str) -> str:
    return f"""
        SELECT person_id, timestamp
        FROM events
        WHERE event = {_quote(event)}
          AND timestamp >= toDateTime({_quote(start)}) AND timestamp < toDateTime({_quote(end)})
        LIMIT {ROW_LIMIT}
    """


def build_user_table(exposures: pd.DataFrame, events: pd.DataFrame, start: str, end: str, pre_days: int = 14) -> tuple[pd.DataFrame, dict]:
    """One row per exposed person. Returns (users, data-quality counts)."""
    exp = exposures.copy()
    exp["first_exposure"] = pd.to_datetime(exp["first_exposure"], utc=True)
    exp["variant"] = exp["variant"].astype(str)
    variants_per_person = exp.groupby("person_id")["variant"].nunique()
    mixed = variants_per_person[variants_per_person > 1].index
    exp = exp[~exp["person_id"].isin(mixed)]
    users = exp.groupby("person_id").agg(variant=("variant", "first"), first_exposure=("first_exposure", "min")).reset_index()

    ev = events.copy()
    ev["timestamp"] = pd.to_datetime(ev["timestamp"], utc=True)
    start_ts, end_ts = pd.Timestamp(start, tz="UTC"), pd.Timestamp(end, tz="UTC")
    pre = ev[(ev["timestamp"] >= start_ts - pd.Timedelta(days=pre_days)) & (ev["timestamp"] < start_ts)]
    pre_counts = pre.groupby("person_id").size().rename("pre_count")

    during = ev.merge(users[["person_id", "first_exposure"]], on="person_id")
    during = during[(during["timestamp"] >= during["first_exposure"]) & (during["timestamp"] < end_ts)]
    post_counts = during.groupby("person_id").size().rename("metric_count")

    users = users.merge(post_counts, on="person_id", how="left").merge(pre_counts, on="person_id", how="left")
    users[["metric_count", "pre_count"]] = users[["metric_count", "pre_count"]].fillna(0).astype(int)
    users["converted"] = (users["metric_count"] > 0).astype(int)
    quality = {"exposed_people": int(exposures["person_id"].nunique()), "mixed_variant_people_dropped": int(len(mixed)),
               "analysed_people": len(users)}
    return users, quality


def fetch(client: PostHogClient, flag: str, event: str, start: str, end: str, pre_days: int = 14) -> tuple[pd.DataFrame, dict]:
    pre_start = (pd.Timestamp(start) - pd.Timedelta(days=pre_days)).strftime("%Y-%m-%d %H:%M:%S")
    exposures = client.query(exposures_query(flag, start, end))
    events = client.query(events_query(event, pre_start, end))
    return build_user_table(exposures, events, start, end, pre_days)
