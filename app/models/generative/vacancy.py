from typing import Sequence, TypedDict

from pydantic import BaseModel

from app.models import Vacancy

__all__ = ["ScoredVacancyLlmResponse", "ScoredVacanciesLlmResponse", "VacancyScoringPromptParams"]


class VacancyScoringPromptParams(TypedDict):
    cv: str
    vacancies: Sequence[Vacancy]


class ScoredVacancyLlmResponse(BaseModel):
    vacancy_id: int
    reasoning: str
    relevance_score: float


class ScoredVacanciesLlmResponse(BaseModel):
    scored_vacancies: list[ScoredVacancyLlmResponse]
