from typing import TypedDict

from pydantic import BaseModel

from app.models.domain.category import DjinniCategory, DouCategory

__all__ = ["ExtractVacancyFiltersLlmResponse", "ExtractVacancyFiltersPromptParams"]


class ExtractVacancyFiltersPromptParams(TypedDict):
    cv: str


class ExtractVacancyFiltersLlmResponse(BaseModel):
    years_of_experience: int
    dou_category: DouCategory
    djinni_category: DjinniCategory
