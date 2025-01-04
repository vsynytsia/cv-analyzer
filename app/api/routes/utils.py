from fastapi import APIRouter

router = APIRouter(prefix="/utils", tags=["Utils"])


@router.get("/healthcheck")
async def health_check() -> bool:
    return True
