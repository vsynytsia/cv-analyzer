from pydantic import BaseModel, field_validator

__all__ = ["VacancyDetails", "VacancyScore", "Vacancy", "ScoredVacancy"]


class VacancyDetails(BaseModel):
    description: str
    job_title: str | None
    company_name: str | None
    salary: str | None


class VacancyScore(BaseModel):
    score: float
    reasoning: str

    @field_validator("score")
    def round_float(cls, v: float) -> float:
        return round(v, 2)


class Vacancy(BaseModel):
    url: str
    details: VacancyDetails


class ScoredVacancy(Vacancy):
    score: VacancyScore
