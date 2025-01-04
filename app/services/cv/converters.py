from app.schemas.filters import DjinniSearchFilter, DouSearchFilter, JobSearchFilter
from app.services.cv.schemas import VacancySearchFilterLlmResponse


def llm_response_to_job_search_filters(response: VacancySearchFilterLlmResponse) -> list[JobSearchFilter]:
    return [
        DouSearchFilter(experience_years=response.years_of_experience, category=response.dou_category),
        DjinniSearchFilter(experience_years=response.years_of_experience, category=response.djinni_category),
    ]
