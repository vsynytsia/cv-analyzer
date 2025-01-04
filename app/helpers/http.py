from typing import Any

import httpx
from fake_useragent import UserAgent


class AsyncHTTPClient:
    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self._client = httpx.AsyncClient(timeout=timeout)

    async def get(
        self,
        url: httpx.URL | str,
        headers: dict[str, str] | None = None,
        params: dict[str, Any] | None = None,
    ) -> httpx.Response:
        headers = self.prepare_headers(headers)
        response = await self._client.get(url, headers=headers, params=params)
        return response.raise_for_status()

    @staticmethod
    def prepare_headers(headers: dict[str, str] | None) -> dict[str, str]:
        headers = headers or {}
        if headers.get("User-Agent") is None:
            headers["User-Agent"] = UserAgent().random
        return headers

    async def close(self) -> None:
        await self._client.aclose()

    async def __aenter__(self) -> "AsyncHTTPClient":
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        await self.close()
