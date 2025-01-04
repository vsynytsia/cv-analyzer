import logging
from collections.abc import Iterable

import httpx
from fake_useragent import UserAgent

from app.helpers import utils
from app.helpers.scraping import JobSiteScraperFactory
from app.models.domain import JobSearchFilter, Vacancy

__all__ = ["VacancyScraper"]


HTTP_TIMEOUT = 30


class VacancyScraper:
    def __init__(self) -> None:
        self._session = httpx.AsyncClient(
            timeout=httpx.Timeout(HTTP_TIMEOUT), headers={"User-Agent": UserAgent().random}
        )
        self._logger = logging.getLogger(self.__class__.__name__)

    async def fetch_vacancies(self, filters: Iterable[JobSearchFilter]) -> list[Vacancy]:
        filtered_vacancies_urls = await utils.gather(
            items=filters,
            coro_factory=lambda filter_: self._fetch_vacancies_urls(filter_),
            post_processor=lambda x: utils.flatten_list(utils.filter_exceptions(x)),
        )
        filtered_vacancies = await utils.gather(
            items=filtered_vacancies_urls,
            coro_factory=lambda url: self._fetch_vacancy_by_url(url),
            post_processor=lambda x: utils.filter_exceptions(x),
        )

        self._logger.info("Fetched %d vacancies from %d URLs", len(filtered_vacancies), len(filtered_vacancies_urls))
        return filtered_vacancies

    async def _fetch_vacancies_urls(self, filter_: JobSearchFilter, limit: int | None = None) -> list[str]:
        scraper = JobSiteScraperFactory.from_search_filter(filter_)
        response = await self._session.get(scraper.site_jobs_url, params=scraper.build_http_request_params(filter_))
        return scraper.extract_vacancy_urls(response.content, limit)

    async def _fetch_vacancy_by_url(self, url: str) -> Vacancy:
        response = await self._session.get(url)
        scraper = JobSiteScraperFactory.from_vacancy_url(url)
        return scraper.parse_vacancy_details(response.content, url)
