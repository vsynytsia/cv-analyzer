import logging

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.api.middleware import handle_uncaught_exceptions_middleware
from app.core.config import settings

logger = logging.getLogger(__name__)


def initialize_app() -> FastAPI:
    application = FastAPI(
        title=settings.PROJECT_NAME, description=settings.PROJECT_DESCRIPTION, version=settings.PROJECT_VERSION
    )
    application.middleware("http")(handle_uncaught_exceptions_middleware)
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    application.include_router(api_router, prefix=settings.API_V1_STR)
    return application


logging.info("Started initializing app")
app = initialize_app()
logging.info("Finished initializing app")
