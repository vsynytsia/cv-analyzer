from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, UploadFile

from app.api.serializers import MatchVacanciesSerializer
from app.containers import Containers
from app.services import CVOperationsService

__all__ = ["cv_operations_router"]

cv_operations_router = APIRouter(prefix="/cv-operations", tags=["CVOperations"])


@cv_operations_router.post("/match-vacancies", response_model=MatchVacanciesSerializer)
@inject
async def match_vacancies(
    cv: UploadFile, cv_operations_service: CVOperationsService = Depends(Provide[Containers.cv_operations_service])
):
    matched_vacancies = await cv_operations_service.match_vacancies(cv)
    return MatchVacanciesSerializer(matched_vacancies=matched_vacancies)
