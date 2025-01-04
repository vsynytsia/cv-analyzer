from app.schemas.vacancy import ScoredVacancy, Vacancy


def convert_vacancy_to_scored_vacancy(vacancy: Vacancy, relevancy_score: float, reasoning: str) -> ScoredVacancy:
    return ScoredVacancy(
        url=vacancy.url,
        job_title=vacancy.job_title,
        company_name=vacancy.company_name,
        salary=vacancy.salary,
        relevancy_score=relevancy_score,
        reasoning=reasoning,
    )
