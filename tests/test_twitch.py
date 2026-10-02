from __future__ import annotations

import pytest

from livescope.ingest.twitch import HelixClient, HelixError


class FakeResponse:
    def __init__(self, status=200, payload=None, headers=None):
        self.status_code = status
        self._payload = payload or {}
        self.headers = headers or {}
        self.text = str(payload)

    def json(self):
        return self._payload


class FakeSession:
    """Replays queued GET responses and records requests."""

    def __init__(self, gets):
        self.gets = list(gets)
        self.get_calls = []
        self.token_calls = 0

    def post(self, url, data, timeout):
        self.token_calls += 1
        return FakeResponse(200, {"access_token": f"tok{self.token_calls}", "expires_in": 3600})

    def get(self, url, headers, params, timeout):
        self.get_calls.append((headers, params))
        return self.gets.pop(0)


def stream(i, viewers=100, user=None):
    return {"id": f"s{i}", "user_id": user or f"u{i}", "viewer_count": viewers}


def test_top_streams_pages_dedupes_and_ranks():
    session = FakeSession([
        FakeResponse(200, {"data": [stream(1), stream(2)], "pagination": {"cursor": "c1"}}),
        # s2 shifted onto the second page while paging; it must not be counted twice.
        FakeResponse(200, {"data": [stream(2), stream(3), stream(4)], "pagination": {"cursor": "c2"}}),
    ])
    client = HelixClient("id", "secret", session=session)
    out = client.top_streams(limit=3)
    assert [s["id"] for s in out] == ["s1", "s2", "s3"]
    assert [s["rank"] for s in out] == [1, 2, 3]
    assert ("after", "c1") in session.get_calls[1][1]
    assert session.get_calls[0][0]["Authorization"] == "Bearer tok1"


def test_top_streams_stops_without_cursor():
    session = FakeSession([FakeResponse(200, {"data": [stream(1)], "pagination": {}})])
    out = HelixClient("id", "secret", session=session).top_streams(limit=500)
    assert len(out) == 1


def test_refreshes_token_on_401_and_retries_429():
    sleeps = []
    session = FakeSession([
        FakeResponse(401),
        FakeResponse(429, headers={}),
        FakeResponse(200, {"data": [stream(1)], "pagination": {}}),
    ])
    client = HelixClient("id", "secret", session=session, sleep=sleeps.append)
    assert len(client.top_streams(10)) == 1
    assert session.token_calls == 2
    assert len(sleeps) == 1


def test_gives_up_on_client_error():
    session = FakeSession([FakeResponse(400, {"message": "bad"})])
    with pytest.raises(HelixError):
        HelixClient("id", "secret", session=session).top_streams(10)


def test_streams_for_users_batches_by_100():
    ids = [f"u{i}" for i in range(250)]
    session = FakeSession([FakeResponse(200, {"data": [stream(i)]}) for i in range(3)])
    out = list(HelixClient("id", "secret", session=session).streams_for_users(ids))
    assert len(out) == 3
    sizes = [sum(1 for k, _ in params if k == "user_id") for _, params in session.get_calls]
    assert sizes == [100, 100, 50]


def test_requires_credentials():
    with pytest.raises(HelixError):
        HelixClient("", "")
