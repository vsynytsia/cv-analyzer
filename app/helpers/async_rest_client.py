import abc

import httpx
from fake_useragent import UserAgent

__all__ = ["AsyncRESTClient"]


class AsyncRESTClient(abc.ABC):  # noqa: B024
    def __init__(self, timeout_seconds: int = 60) -> None:
        self._timeout = httpx.Timeout(timeout_seconds)
        self._headers = {"User-Agent": UserAgent().random}

        self._session = httpx.AsyncClient(timeout=self._timeout, headers=self._headers)
