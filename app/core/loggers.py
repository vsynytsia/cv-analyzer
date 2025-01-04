import logging

from app.core.settings import settings

__all__ = ["setup_logging"]


def setup_logging() -> None:
    logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)
    for _ in ["httpx"]:
        logging.getLogger(_).setLevel(logging.CRITICAL + 1)
