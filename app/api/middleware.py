import logging
from typing import Callable

from fastapi import HTTPException, Request, status

logger = logging.getLogger(__name__)


async def handle_uncaught_exceptions_middleware(request: Request, call_next: Callable):
    try:
        return await call_next(request)
    except Exception as ex:
        logging.exception(f"Unknown server error: {ex}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal server error.")
