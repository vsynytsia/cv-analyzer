import logging

from app.core.settings import settings


def set_logging() -> None:
    logging.basicConfig(level=settings.LOG_LEVEL, format=settings.LOG_FORMAT)
    for _ in ["httpx"]:
        logging.getLogger(_).setLevel(logging.CRITICAL)
