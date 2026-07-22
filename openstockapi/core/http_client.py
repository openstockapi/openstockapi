import httpx
import random
import time
from typing import Any, Dict, Optional

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]

class RobustHTTPClient:
    def __init__(self) -> None:
        self.client = httpx.Client(
            timeout=httpx.Timeout(30.0, connect=10.0),
            follow_redirects=True
        )
        self.async_client = httpx.AsyncClient(
            timeout=httpx.Timeout(30.0, connect=10.0),
            follow_redirects=True
        )


    def request(self, method: str, url: str, retries: int = 3, backoff_factor: float = 0.5, **kwargs: Any) -> httpx.Response:
        headers = kwargs.get("headers", {})
        if "User-Agent" not in headers:
            headers["User-Agent"] = random.choice(USER_AGENTS)
        kwargs["headers"] = headers

        last_err = None
        for attempt in range(retries):
            try:
                response = self.client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.HTTPError, httpx.NetworkError) as e:
                last_err = e
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                    continue
        raise last_err or httpx.HTTPError("Request failed after retries")

    async def async_request(self, method: str, url: str, retries: int = 3, backoff_factor: float = 0.5, **kwargs: Any) -> httpx.Response:
        import asyncio
        headers = kwargs.get("headers", {})
        if "User-Agent" not in headers:
            headers["User-Agent"] = random.choice(USER_AGENTS)
        kwargs["headers"] = headers

        last_err = None
        for attempt in range(retries):
            try:
                response = await self.async_client.request(method, url, **kwargs)
                response.raise_for_status()
                return response
            except (httpx.HTTPError, httpx.NetworkError) as e:
                last_err = e
                if attempt < retries - 1:
                    await asyncio.sleep(backoff_factor * (2 ** attempt))
                    continue
        raise last_err or httpx.HTTPError("Async request failed after retries")

http_client = RobustHTTPClient()
