from fastapi import APIRouter, UploadFile

from app.api.dependencies import CVOperationsServiceDep
from app.api.serializers import MatchVacanciesSerializer

__all__ = ["cv_operations_router"]

cv_operations_router = APIRouter(prefix="/cv-operations", tags=["CVOperations"])


@cv_operations_router.post("/match-vacancies", response_model=MatchVacanciesSerializer)
async def match_vacancies(cv: UploadFile, cv_operations_service: CVOperationsServiceDep):
    matched_vacancies = await cv_operations_service.match_vacancies(cv)
    return MatchVacanciesSerializer(matched_vacancies=matched_vacancies)
