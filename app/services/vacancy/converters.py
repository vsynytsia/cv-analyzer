from collections.abc import Callable

from app.schemas.vacancy import VacancySearchFilter, VacancySource


def convert_vacancy_search_filter_to_http_request_params(filter_: VacancySearchFilter) -> dict:
    converter = _get_vacancy_search_filters_converter(filter_.source)
    return converter(filter_)


def _get_vacancy_search_filters_converter(website: VacancySource) -> Callable[[VacancySearchFilter], dict]:
    website_to_converter = {
        VacancySource.DOU: _convert_dou_vacancy_search_filters_to_http_request_params,
        VacancySource.DJINNI: _convert_djinni_vacancy_search_filters_to_http_request_params,
    }

    return website_to_converter[website]


def _convert_dou_vacancy_search_filters_to_http_request_params(filter_: VacancySearchFilter) -> dict:
    converted_experience = _convert_dou_experience_to_http_request_experience(filter_.years_of_experience)

    return {"category": filter_.category, "exp": converted_experience}


def _convert_djinni_vacancy_search_filters_to_http_request_params(filter_: VacancySearchFilter) -> dict:
    converted_experience = _convert_djinni_experience_to_http_request_experience(filter_.years_of_experience)

    return {"primary_keyword": filter_.category, "exp_level": converted_experience}


def _convert_dou_experience_to_http_request_experience(experience: float) -> str:
    if 0 <= experience < 1:
        request_param_experience = "0-1"
    elif 1 <= experience < 3:
        request_param_experience = "1-3"
    elif 3 <= experience < 5:
        request_param_experience = "3-5"
    else:
        request_param_experience = "5plus"

    return request_param_experience


def _convert_djinni_experience_to_http_request_experience(experience: int) -> str:
    if experience == 0:
        return "no_exp"
    else:
        return f"{min(experience, 10)}y"
