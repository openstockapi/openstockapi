import httpx
import random
import time
from typing import Any, Dict, Optional
from openstockapi.core.exceptions import OpenStockAPIError

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
]

class RobustHTTPClient:
    def __init__(self) -> None:
        self.client = httpx.Client(
            timeout=httpx.Timeout(2.0, connect=2.0),
            follow_redirects=True
        )
        self._async_client = None

    def get_async_client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(
            timeout=httpx.Timeout(2.0, connect=2.0),
            follow_redirects=True
        )


    def request(self, method: str, url: str, retries: int = 1, backoff_factor: float = 0.5, **kwargs: Any) -> httpx.Response:
        headers = kwargs.get("headers", {})
        if "User-Agent" not in headers:
            headers["User-Agent"] = random.choice(USER_AGENTS)
        kwargs["headers"] = headers

        last_err = None
        for attempt in range(retries):
            try:
                response = self.client.request(method, url, **kwargs)
                if response.status_code == 429:
                    try:
                        err_json = response.json()
                        error_code = err_json.get("error", "RateLimitExceeded")
                        message = err_json.get("message", "Rate limit exceeded.")
                        retry_after = int(err_json.get("retry_after_seconds", 30))
                    except Exception:
                        error_code = "RateLimitExceeded"
                        message = "Rate limit exceeded. Please reduce your request frequency."
                        retry_after = 30
                    from openstockapi.core.exceptions import RateLimitError
                    raise RateLimitError(error_code, message, retry_after)
                response.raise_for_status()
                return response
            except (httpx.HTTPError, httpx.NetworkError) as e:
                # If we manually raised RateLimitError, do not retry or suppress it
                if isinstance(e, OpenStockAPIError) or type(e).__name__ == "RateLimitError":
                    raise e
                last_err = e
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2 ** attempt))
                    continue
        raise last_err or httpx.HTTPError("Request failed after retries")

    async def async_request(self, method: str, url: str, retries: int = 1, backoff_factor: float = 0.5, **kwargs: Any) -> httpx.Response:
        import asyncio
        headers = kwargs.get("headers", {})
        if "User-Agent" not in headers:
            headers["User-Agent"] = random.choice(USER_AGENTS)
        kwargs["headers"] = headers

        for attempt in range(retries):
            try:
                async with self.get_async_client() as client:
                    response = await client.request(method, url, **kwargs)
                if response.status_code == 429:
                    try:
                        err_json = response.json()
                        error_code = err_json.get("error", "RateLimitExceeded")
                        message = err_json.get("message", "Rate limit exceeded.")
                        retry_after = int(err_json.get("retry_after_seconds", 30))
                    except Exception:
                        error_code = "RateLimitExceeded"
                        message = "Rate limit exceeded. Please reduce your request frequency."
                        retry_after = 30
                    from openstockapi.core.exceptions import RateLimitError
                    raise RateLimitError(error_code, message, retry_after)
                response.raise_for_status()
                return response
            except (httpx.HTTPError, httpx.NetworkError) as e:
                if isinstance(e, OpenStockAPIError) or type(e).__name__ == "RateLimitError":
                    raise e
                last_err = e
                if attempt < retries - 1:
                    await asyncio.sleep(backoff_factor * (2 ** attempt))
                    continue
        raise last_err or httpx.HTTPError("Async request failed after retries")

http_client = RobustHTTPClient()
