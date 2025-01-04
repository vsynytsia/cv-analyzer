from typing import TypedDict

from pydantic import BaseModel

from app.models.domain.category import DjinniCategory, DouCategory

__all__ = ["VacancySearchFilterLlmResponse", "VacancySearchFiltersPromptParams"]


class VacancySearchFiltersPromptParams(TypedDict):
    cv: str


class VacancySearchFilterLlmResponse(BaseModel):
    years_of_experience: int
    dou_category: DouCategory
    djinni_category: DjinniCategory
