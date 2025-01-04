from pydantic import BaseModel


class ScoredVacancyLlmResponse(BaseModel):
    vacancy_id: int
    reasoning: str
    relevancy_score: float


class ScoredVacanciesLlmResponse(BaseModel):
    scored_vacancies: list[ScoredVacancyLlmResponse]
