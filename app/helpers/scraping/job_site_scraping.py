import abc

from app.models.domain import DjinniSearchFilter, DouSearchFilter, JobSearchFilter, Vacancy
from app.models.http_params import DjinniVacancySearchHttpParams, DouVacancySearchHttpParams, VacancySearchHttpParams

from .html_parsing import HtmlParser

__all__ = ["JobSiteScraperFactory"]

DOU_SITE_URL = "https://jobs.dou.ua/"
DJINNI_SITE_URL = "https://djinni.co/"


class JobSiteScraper(abc.ABC):
    @property
    @abc.abstractmethod
    def site_url(self) -> str:
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def site_jobs_url(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def build_http_request_params(self, search_filter: JobSearchFilter) -> VacancySearchHttpParams:
        raise NotImplementedError

    @abc.abstractmethod
    def extract_vacancy_urls(self, html_content: bytes, limit: int | None = None) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def parse_vacancy_details(self, html_content: bytes, vacancy_url: str) -> Vacancy:
        raise NotImplementedError


class DjinniJobScraper(JobSiteScraper):
    @property
    def site_url(self) -> str:
        return DJINNI_SITE_URL

    @property
    def site_jobs_url(self) -> str:
        return self.site_url + "jobs/"

    def build_http_request_params(self, search_filter: DjinniSearchFilter) -> DjinniVacancySearchHttpParams:
        return DjinniVacancySearchHttpParams(
            primary_keyword=search_filter.category, exp_level=search_filter.normalized_experience
        )

    def extract_vacancy_urls(self, html_content: bytes, limit: int | None = None) -> list[str]:
        parser = HtmlParser(html_content)
        vacancy_urls = [
            (self.site_url[:-1] + link["href"]) for link in parser.find_all("a", class_="job-item__title-link")
        ]
        return vacancy_urls[:limit] if limit is not None else vacancy_urls

    def parse_vacancy_details(self, html_content: bytes, vacancy_url: str) -> Vacancy:
        parser = HtmlParser(html_content)

        description = parser.extract_element_text_unsafe("div", separator="\n", class_="job-post__description")
        company_name = parser.extract_element_text_safe("a", class_="text-reset")
        salary = parser.extract_element_text_safe("span", class_="text-success text-nowrap")
        job_title = parser.extract_first_line_of_multiline_string_safe("h1")

        return Vacancy(
            url=vacancy_url, description=description, job_title=job_title, company_name=company_name, salary=salary
        )


class DouJobScraper(JobSiteScraper):
    @property
    def site_url(self) -> str:
        return DOU_SITE_URL

    @property
    def site_jobs_url(self):
        return self.site_url + "vacancies/"

    def build_http_request_params(self, search_filter: DouSearchFilter) -> DouVacancySearchHttpParams:
        return DouVacancySearchHttpParams(category=search_filter.category, exp=search_filter.normalized_experience)

    def extract_vacancy_urls(self, html_content: bytes, limit: int | None = None) -> list[str]:
        parser = HtmlParser(html_content)
        vacancy_urls = [link["href"] for link in parser.find_all("a", class_="vt")]
        return vacancy_urls[:limit] if limit is not None else vacancy_urls

    def parse_vacancy_details(self, html_content: bytes, vacancy_url: str) -> Vacancy:
        parser = HtmlParser(html_content)

        description = parser.extract_element_text_unsafe("div", separator=" ", class_="b-typo vacancy-section")
        job_title = parser.extract_element_text_safe("h1", class_="g-h2")
        salary = parser.extract_element_text_safe("span", class_="salary")
        company_name = parser.extract_first_line_of_multiline_string_safe("div", class_="l-n")

        return Vacancy(
            url=vacancy_url, description=description, job_title=job_title, company_name=company_name, salary=salary
        )


class JobSiteScraperFactory:
    @staticmethod
    def from_search_filter(search_filter: JobSearchFilter) -> JobSiteScraper:
        filter_to_scraper = {DouSearchFilter: DouJobScraper, DjinniSearchFilter: DjinniJobScraper}
        if (scraper := filter_to_scraper.get(type(search_filter))) is None:
            raise NotImplementedError(
                f"Job site scraper for search filter {type(search_filter).__name__} is not implemented"
            )

        return scraper()

    @staticmethod
    def from_vacancy_url(url: str) -> JobSiteScraper:
        if DJINNI_SITE_URL in url:
            return DjinniJobScraper()
        elif DOU_SITE_URL in url:
            return DouJobScraper()
        else:
            raise NotImplementedError(f"Job site scraper for url {url} is not implemented")
