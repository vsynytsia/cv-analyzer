from app.schemas.vacancy import VacancySearchFilter, VacancySource

from .schemas import VacancySearchFilterLlmResponse


def convert_llm_response_to_vacancy_search_filters(
    response: VacancySearchFilterLlmResponse,
) -> list[VacancySearchFilter]:
    return [
        VacancySearchFilter(
            source=VacancySource.DOU, years_of_experience=response.years_of_experience, category=response.dou_category
        ),
        VacancySearchFilter(
            source=VacancySource.DJINNI,
            years_of_experience=response.years_of_experience,
            category=response.djinni_category,
        ),
    ]
