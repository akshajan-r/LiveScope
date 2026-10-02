"""Minimal Twitch Helix client: app access token plus the Get Streams endpoint.

Docs: https://dev.twitch.tv/docs/api/reference/#get-streams
"""

from __future__ import annotations

import logging
import time
from collections.abc import Iterable, Iterator

import requests

log = logging.getLogger(__name__)

TOKEN_URL = "https://id.twitch.tv/oauth2/token"
STREAMS_URL = "https://api.twitch.tv/helix/streams"
PAGE_SIZE = 100  # Helix maximum for `first` and for repeated `user_id` filters


class HelixError(RuntimeError):
    pass


class HelixClient:
    def __init__(
        self,
        client_id: str,
        client_secret: str,
        session: requests.Session | None = None,
        max_retries: int = 5,
        sleep=time.sleep,
    ) -> None:
        if not client_id or not client_secret:
            raise HelixError("TWITCH_CLIENT_ID and TWITCH_CLIENT_SECRET must be set")
        self.client_id = client_id
        self.client_secret = client_secret
        self.session = session or requests.Session()
        self.max_retries = max_retries
        self._sleep = sleep
        self._token: str | None = None

    # -- auth -------------------------------------------------------------
    def _authenticate(self) -> str:
        resp = self.session.post(
            TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "client_credentials",
            },
            timeout=30,
        )
        if resp.status_code != 200:
            raise HelixError(f"token request failed: HTTP {resp.status_code}")
        self._token = resp.json()["access_token"]
        return self._token

    def _headers(self) -> dict[str, str]:
        token = self._token or self._authenticate()
        return {"Client-Id": self.client_id, "Authorization": f"Bearer {token}"}

    # -- requests ---------------------------------------------------------
    def _get(self, url: str, params: list[tuple[str, str]]) -> dict:
        for attempt in range(self.max_retries + 1):
            resp = self.session.get(url, headers=self._headers(), params=params, timeout=30)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 401 and attempt < self.max_retries:
                # Token expired or revoked: get a new one and retry.
                self._authenticate()
                continue
            if resp.status_code == 429 and attempt < self.max_retries:
                reset = resp.headers.get("Ratelimit-Reset")
                wait = max(1.0, float(reset) - time.time()) if reset else 2.0**attempt
                log.warning("rate limited; sleeping %.1fs", wait)
                self._sleep(min(wait, 60.0))
                continue
            if resp.status_code >= 500 and attempt < self.max_retries:
                self._sleep(2.0**attempt)
                continue
            raise HelixError(f"GET {url} failed: HTTP {resp.status_code}: {resp.text[:200]}")
        raise HelixError(f"GET {url} failed after {self.max_retries} retries")

    def top_streams(self, limit: int) -> list[dict]:
        """Live streams ordered by current viewer count (Helix default order).

        Rankings shift while we page, so a stream can appear on two pages; we keep
        the first occurrence. Each record gets its 1-based `rank`.
        """
        seen: set[str] = set()
        out: list[dict] = []
        cursor: str | None = None
        while len(out) < limit:
            params = [("first", str(PAGE_SIZE))]
            if cursor:
                params.append(("after", cursor))
            payload = self._get(STREAMS_URL, params)
            page = payload.get("data", [])
            for item in page:
                if item["id"] in seen:
                    continue
                seen.add(item["id"])
                item["rank"] = len(out) + 1
                out.append(item)
                if len(out) >= limit:
                    break
            cursor = (payload.get("pagination") or {}).get("cursor")
            if not page or not cursor:
                break
        return out

    def streams_for_users(self, user_ids: Iterable[str]) -> Iterator[dict]:
        """Live streams for specific broadcasters (offline users return nothing)."""
        ids = list(dict.fromkeys(user_ids))
        for i in range(0, len(ids), PAGE_SIZE):
            batch = ids[i : i + PAGE_SIZE]
            params = [("first", str(PAGE_SIZE))] + [("user_id", uid) for uid in batch]
            payload = self._get(STREAMS_URL, params)
            yield from payload.get("data", [])
