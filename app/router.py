from fastapi import FastAPI

from app.api.routes import cv, root, utils


def apply_routes(app: FastAPI) -> FastAPI:
    app.include_router(root.router)
    app.include_router(utils.router)
    app.include_router(cv.router)
    return app
