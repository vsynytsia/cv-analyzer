from fastapi import APIRouter

from app.api.routes import cv, root, utils

api_router = APIRouter()
api_router.include_router(root.router)
api_router.include_router(utils.router)
api_router.include_router(cv.router)
