import logging
from collections.abc import Iterable

from app.helpers import utils
from app.helpers.async_rest_client import AsyncRESTClient
from app.helpers.html_parsing import JobSiteHtmlParserFactory
from app.models.domain import Vacancy, VacancySearchFilter

__all__ = ["VacancyScrapingService"]


class VacancyScrapingService(AsyncRESTClient):
    def __init__(self) -> None:
        super().__init__()
        self._logger = logging.getLogger(self.__class__.__name__)

    async def fetch_vacancies(self, filters: Iterable[VacancySearchFilter]) -> list[Vacancy]:
        filtered_vacancies_urls = await utils.gather(
            items=filters,
            coro_factory=lambda filter_: self._fetch_vacancies_urls(filter_),
            post_processor=lambda x: utils.flatten_list(utils.filter_exceptions(x)),
        )

        filtered_vacancies = await utils.gather(
            items=filtered_vacancies_urls,
            coro_factory=lambda url: self._fetch_vacancy(url),
            post_processor=lambda x: utils.filter_exceptions(x),
        )

        self._logger.info("Fetched %d vacancies from %d URLs", len(filtered_vacancies), len(filtered_vacancies_urls))
        return filtered_vacancies

    async def _fetch_vacancies_urls(self, filter_: VacancySearchFilter) -> list[str]:
        parser = JobSiteHtmlParserFactory.from_search_filter(filter_)

        response = await self._session.get(parser.site_vacancies_url, params=filter_.to_http_request_params())

        return parser.parse_vacancy_urls(response.content)

    async def _fetch_vacancy(self, url: str) -> Vacancy:
        response = await self._session.get(url)

        parser = JobSiteHtmlParserFactory.from_vacancy_url(url)

        vacancy_details = parser.parse_vacancy_details(response.content)
        return Vacancy(url=url, details=vacancy_details)
