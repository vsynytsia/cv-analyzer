from pydantic import BaseModel

from app.models.domain import ScoredVacancy

__all__ = ["MatchVacanciesSerializer"]


class MatchVacanciesSerializer(BaseModel):
    matched_vacancies: list[ScoredVacancy]
