from pydantic import BaseModel

from app.schemas.vacancy import DjinniCategory, DouCategory


class VacancySearchFilterLlmResponse(BaseModel):
    years_of_experience: int
    dou_category: DouCategory
    djinni_category: DjinniCategory
