import logging
from collections.abc import Iterable
from typing import Callable

from app.core.config import settings
from app.helpers import concurrency, http, language, utils
from app.schemas.filters import DjinniSearchFilter, DouSearchFilter, JobSearchFilter
from app.schemas.vacancies import Vacancy
from app.services.vacancy.djinni import parsers as djinni_parsers
from app.services.vacancy.dou import parsers as dou_parsers

logger = logging.getLogger(__name__)


async def standardize_vacancies_language(vacancies: list[Vacancy]) -> list[Vacancy]:
    ukrainian_vacancies, english_vacancies = [], []

    for vacancy in vacancies:
        vacancy_lang = language.detect_text_language(vacancy.description)
        if vacancy_lang == "uk":
            ukrainian_vacancies.append(vacancy)
        elif vacancy_lang == "en":
            english_vacancies.append(vacancy)
        else:
            logger.info(f"Skipping vacancy with unexpected language '{vacancy_lang}': {vacancy}")

    translated_descriptions = await language.translate_texts(
        texts=[vacancy.description for vacancy in ukrainian_vacancies], source_language="uk", target_language="en"
    )

    translated_ukrainian_vacancies = [
        Vacancy(**vacancy.model_dump(exclude={"description"}), description=translated_description)
        for vacancy, translated_description in zip(ukrainian_vacancies, translated_descriptions, strict=False)
    ]
    return english_vacancies + translated_ukrainian_vacancies


async def fetch_filtered_vacancies(
    http_client: http.AsyncHTTPClient, filters: Iterable[JobSearchFilter]
) -> list[Vacancy]:
    urls = await concurrency.gather(
        items=filters,
        coro_factory=lambda filter_: fetch_vacancies_urls_with_filter(http_client, filter_),
        post_processor=lambda x: utils.flatten_list(utils.filter_exceptions(x)),
    )

    filtered_vacancies = await concurrency.gather(
        items=urls,
        coro_factory=lambda url: fetch_vacancy_by_url(http_client, url),
        post_processor=lambda x: utils.filter_exceptions(x),
    )
    return filtered_vacancies


async def fetch_vacancy_by_url(http_client: http.AsyncHTTPClient, url: str) -> Vacancy:
    response = await http_client.get(url)
    return parse_vacancy_html(response.content, url)


def parse_vacancy_html(vacancy_html: bytes, vacancy_url: str) -> Vacancy:
    parser = get_vacancy_html_parser(vacancy_url)
    return parser(vacancy_html, vacancy_url)


async def fetch_vacancies_urls_with_filter(http_client: http.AsyncHTTPClient, filter_: JobSearchFilter) -> list[str]:
    response = await http_client.get(filter_.website_url, params=filter_.to_http_request_params())

    extractor = get_vacancy_urls_extractor(filter_)
    return extractor(response.content)[: settings.MAX_VACANCIES_PER_SOURCE]


def get_vacancy_urls_extractor(filter_: JobSearchFilter) -> Callable[[bytes], list[str]]:
    if isinstance(filter_, DouSearchFilter):
        return dou_parsers.extract_vacancy_urls
    elif isinstance(filter_, DjinniSearchFilter):
        return djinni_parsers.extract_vacancy_urls
    else:
        raise ValueError(f"cannot infer vacancy urls extractor from {filter_}")


def get_vacancy_html_parser(vacancy_url: str) -> Callable[[bytes, str], Vacancy]:
    if "dou" in vacancy_url:
        return dou_parsers.parse_vacancy_html
    elif "djinni" in vacancy_url:
        return djinni_parsers.parse_vacancy_html
    else:
        raise ValueError(f"cannot infer vacancy html parser from url: {vacancy_url}")
