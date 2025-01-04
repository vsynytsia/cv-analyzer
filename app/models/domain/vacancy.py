from pydantic import BaseModel, field_validator

__all__ = ["Vacancy", "ScoredVacancy"]


class Vacancy(BaseModel):
    url: str
    description: str
    job_title: str | None
    company_name: str | None
    salary: str | None


class ScoredVacancy(Vacancy):
    relevance: float
    reasoning: str

    @field_validator("relevance")
    def round_float(cls, v: float) -> float:
        return round(v, 2)
