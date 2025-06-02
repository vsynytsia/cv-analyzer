import abc
import logging

import httpx
import tenacity
from fake_useragent import UserAgent

__all__ = ["AsyncRESTClient"]


retry_logger = logging.getLogger("HTTPRetryer")


RETRYABLE_STATUS_CODES = (429, 500, 502, 503, 504)


def is_http_exception_retryable(exception: BaseException) -> bool:
    return isinstance(exception, httpx.HTTPStatusError) and exception.response.status_code in RETRYABLE_STATUS_CODES


retry_on_http_error = tenacity.retry(
    stop=tenacity.stop_after_attempt(7),
    wait=tenacity.wait_exponential(multiplier=1, min=0),
    retry=tenacity.retry_if_exception(is_http_exception_retryable),
    before_sleep=tenacity.before_sleep_log(retry_logger, log_level=logging.WARNING),
    reraise=True,
)


class AsyncRESTClient(abc.ABC):  # noqa: B024
    def __init__(self, timeout_seconds: int = 60) -> None:
        self._timeout = httpx.Timeout(timeout_seconds)
        self._headers = {"User-Agent": UserAgent().random}

        self._session = httpx.AsyncClient(timeout=self._timeout, headers=self._headers)

    @retry_on_http_error
    async def get(self, *args, **kwargs) -> httpx.Response:
        return await self._session.get(*args, **kwargs)
