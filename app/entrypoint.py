import logging
from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

import uvicorn
from fastapi import FastAPI
from google import generativeai as genai
from starlette.middleware.cors import CORSMiddleware

from app import api
from app.api.endpoints import cv_operations_router
from app.api.error_handlers import register_error_handlers
from app.containers import Containers
from app.core.loggers import setup_logging
from app.core.settings import settings

logger = logging.getLogger(__name__)


def run_api() -> None:
    app = create_app()
    uvicorn.run(app, host="0.0.0.0", port=8080)


def create_app() -> FastAPI:
    containers = init_containers()

    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
        lifespan=lifespan,
    )
    app = apply_routes(apply_middleware(app))
    register_error_handlers(app)
    app.containers = containers
    return app


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    setup_logging()
    genai.configure(api_key=settings.GOOGLE_GENAI_API_KEY)
    yield


def apply_routes(app: FastAPI) -> FastAPI:
    app.include_router(cv_operations_router)
    return app


def apply_middleware(app: FastAPI) -> FastAPI:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return app


def init_containers() -> Containers:
    containers = Containers()
    containers.init_resources()
    containers.wire(packages=[api])
    return containers
