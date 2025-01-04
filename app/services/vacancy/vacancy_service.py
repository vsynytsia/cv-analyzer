import logging
from collections.abc import Iterable
from typing import Callable

from httpx import AsyncClient

from app.core.config import settings
from app.schemas.vacancy import Vacancy, VacancySearchFilter, VacancySource
from app.services import html_service, http_service, language_service
from app.utils import execute_tasks_async, filter_out_exceptions, flatten_2d_list

from .converters import convert_vacancy_search_filter_to_http_request_params

logger = logging.getLogger(__name__)


async def standardize_vacancies_language(vacancies: list[Vacancy]) -> list[Vacancy]:
    ukrainian_vacancies, english_vacancies = [], []

    for vacancy in vacancies:
        vacancy_lang = language_service.detect_text_language(vacancy.description)
        if vacancy_lang == "uk":
            ukrainian_vacancies.append(vacancy)
        elif vacancy_lang == "en":
            english_vacancies.append(vacancy)
        else:
            logger.info(f"Skipping vacancy with unexpected language '{vacancy_lang}': {vacancy}")

    translated_descriptions = await language_service.translate_texts(
        texts=[vacancy.description for vacancy in ukrainian_vacancies], source_language="uk", target_language="en"
    )

    translated_ukrainian_vacancies = [
        Vacancy(**vacancy.model_dump(exclude={"description"}), description=translated_description)
        for vacancy, translated_description in zip(ukrainian_vacancies, translated_descriptions, strict=False)
    ]
    return english_vacancies + translated_ukrainian_vacancies


async def fetch_filtered_vacancies(httpx_client: AsyncClient, filters: Iterable[VacancySearchFilter]) -> list[Vacancy]:
    vacancies_urls = await fetch_vacancies_urls_with_filters(httpx_client, filters)
    filtered_vacancies = await execute_tasks_async(
        items=vacancies_urls,
        coro_factory=lambda url: fetch_vacancy_by_url(httpx_client, url),
        post_processor=lambda x: filter_out_exceptions(x),
    )
    return filtered_vacancies


async def fetch_vacancy_by_url(httpx_client: AsyncClient, url: str) -> Vacancy:
    response = await http_service.make_async_http_get_request_with_random_user_agent(client=httpx_client, url=url)
    return parse_vacancy_html(response.content, url)


def parse_vacancy_html(vacancy_html: bytes, vacancy_url: str) -> Vacancy:
    vacancy_source = _infer_vacancy_source_from_url(vacancy_url)
    parser = get_vacancy_html_parser(vacancy_source)
    return parser(vacancy_html, vacancy_url)


async def fetch_vacancies_urls_with_filters(
    httpx_client: AsyncClient, filters: Iterable[VacancySearchFilter]
) -> list[str]:
    urls = await execute_tasks_async(
        items=filters,
        coro_factory=lambda filter_: fetch_vacancies_urls_with_filter(httpx_client, filter_),
        post_processor=lambda x: flatten_2d_list(filter_out_exceptions(x)),
    )
    return urls


async def fetch_vacancies_urls_with_filter(httpx_client: AsyncClient, filter_: VacancySearchFilter) -> list[str]:
    base_url = get_vacancy_source_base_url(filter_.source)

    params = convert_vacancy_search_filter_to_http_request_params(filter_)
    response = await http_service.make_async_http_get_request_with_random_user_agent(
        client=httpx_client, url=base_url, params=params
    )

    extractor = get_urls_extractor(filter_.source)
    return extractor(response.content)[: settings.MAX_VACANCIES_PER_SOURCE]


def get_urls_extractor(source: VacancySource) -> Callable[[bytes], list[str]]:
    mapping = {
        VacancySource.DOU: _extract_vacancy_urls_from_dou_search_result,
        VacancySource.DJINNI: _extract_vacancy_urls_from_djinni_search_result,
    }
    return mapping[source]


def get_vacancy_html_parser(source: VacancySource) -> Callable[[bytes, str], Vacancy]:
    mapping = {VacancySource.DOU: _parse_dou_vacancy_html, VacancySource.DJINNI: _parse_djinni_vacancy_html}
    return mapping[source]


def get_vacancy_source_base_url(source: VacancySource) -> str:
    mapping = {
        VacancySource.DOU: settings.DOU_VACANCIES_BASE_URL,
        VacancySource.DJINNI: settings.DJINNI_VACANCIES_BASE_URL,
    }
    return mapping[source]


def _infer_vacancy_source_from_url(url: str) -> VacancySource:
    if VacancySource.DJINNI in url:
        return VacancySource.DJINNI
    elif VacancySource.DOU in url:
        return VacancySource.DOU


def _extract_vacancy_urls_from_dou_search_result(search_result: bytes) -> list[str]:
    soup = html_service.get_bs4_html_parser(search_result)
    return [link["href"] for link in soup.find_all("a", class_="vt")]


def _extract_vacancy_urls_from_djinni_search_result(search_result: bytes) -> list[str]:
    soup = html_service.get_bs4_html_parser(search_result)
    base_url = settings.DJINNI_VACANCIES_BASE_URL.replace("/jobs/", "")
    return [(base_url + link["href"]) for link in soup.find_all("a", class_="job-item__title-link")]


def _parse_dou_vacancy_html(vacancy_html: bytes, vacancy_url: str) -> Vacancy:
    parser = html_service.get_bs4_html_parser(vacancy_html)

    description = html_service.extract_element_text_unsafe(
        parser, "div", separator=" ", class_="b-typo vacancy-section"
    )
    job_title = html_service.extract_element_text_safe(parser, "h1", class_="g-h2")
    salary = html_service.extract_element_text_safe(parser, "span", class_="salary")
    company_name = html_service.extract_first_line_of_multiline_string_safe(parser, "div", class_="l-n")

    return Vacancy(
        url=vacancy_url, description=description, job_title=job_title, company_name=company_name, salary=salary
    )


def _parse_djinni_vacancy_html(vacancy_html: bytes, vacancy_url: str) -> Vacancy:
    parser = html_service.get_bs4_html_parser(vacancy_html)

    description = html_service.extract_element_text_unsafe(
        parser, "div", separator="\n", class_="job-post__description"
    )
    company_name = html_service.extract_element_text_safe(parser, "a", class_="text-reset")
    salary = html_service.extract_element_text_safe(parser, "span", class_="text-success text-nowrap")
    job_title = html_service.extract_first_line_of_multiline_string_safe(parser, "h1")

    return Vacancy(
        url=vacancy_url, description=description, job_title=job_title, company_name=company_name, salary=salary
    )
