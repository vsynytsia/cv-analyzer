import abc

from app.models.domain.search_filter import DjinniSearchFilter, DouSearchFilter, VacancySearchFilter
from app.models.domain.vacancy import VacancyDetails

from .html_parsing import HtmlParser

__all__ = ["JobSiteHtmlParserFactory"]

DOU_SITE_URL = "https://jobs.dou.ua/"
DJINNI_SITE_URL = "https://djinni.co/"


class JobSiteHtmlParser(abc.ABC):
    @property
    @abc.abstractmethod
    def site_url(self) -> str:
        pass

    @property
    @abc.abstractmethod
    def site_vacancies_url(self) -> str:
        pass

    @abc.abstractmethod
    def parse_vacancy_urls(self, html_content: bytes) -> list[str]:
        raise NotImplementedError

    @abc.abstractmethod
    def parse_vacancy_details(self, vacancy_html_content: bytes) -> VacancyDetails:
        raise NotImplementedError


class DjinniHtmlParser(JobSiteHtmlParser):
    @property
    def site_url(self) -> str:
        return DJINNI_SITE_URL

    @property
    def site_vacancies_url(self) -> str:
        return self.site_url + "jobs/"

    def parse_vacancy_urls(self, html_content: bytes) -> list[str]:
        parser = HtmlParser(html_content)
        vacancy_urls = [
            (self.site_url[:-1] + link["href"]) for link in parser.find_all("a", class_="job-item__title-link")
        ]
        return vacancy_urls

    def parse_vacancy_details(self, vacancy_html_content: bytes) -> VacancyDetails:
        parser = HtmlParser(vacancy_html_content)

        description = parser.extract_element_text_unsafe("div", separator="\n", class_="job-post__description")
        company_name = parser.extract_element_text_safe("a", class_="text-reset")
        salary = parser.extract_element_text_safe("span", class_="text-success text-nowrap")
        job_title = parser.extract_first_line_of_multiline_string_safe("h1")

        return VacancyDetails(description=description, job_title=job_title, company_name=company_name, salary=salary)


class DouHtmlParser(JobSiteHtmlParser):
    @property
    def site_url(self) -> str:
        return DOU_SITE_URL

    @property
    def site_vacancies_url(self):
        return self.site_url + "vacancies/"

    def parse_vacancy_urls(self, html_content: bytes) -> list[str]:
        parser = HtmlParser(html_content)
        vacancy_urls = [link["href"] for link in parser.find_all("a", class_="vt")]
        return vacancy_urls

    def parse_vacancy_details(self, vacancy_html_content: bytes) -> VacancyDetails:
        parser = HtmlParser(vacancy_html_content)

        description = parser.extract_element_text_unsafe("div", separator=" ", class_="b-typo vacancy-section")
        job_title = parser.extract_element_text_safe("h1", class_="g-h2")
        salary = parser.extract_element_text_safe("span", class_="salary")
        company_name = parser.extract_first_line_of_multiline_string_safe("div", class_="l-n")

        return VacancyDetails(description=description, job_title=job_title, company_name=company_name, salary=salary)


class JobSiteHtmlParserFactory:
    @staticmethod
    def from_search_filter(search_filter: VacancySearchFilter) -> JobSiteHtmlParser:
        filter_to_parser = {DouSearchFilter: DouHtmlParser, DjinniSearchFilter: DjinniHtmlParser}
        if (parser := filter_to_parser.get(type(search_filter))) is None:
            raise NotImplementedError(
                f"Job site HTML parser for search filter {type(search_filter).__name__} is not implemented"
            )

        return parser()

    @staticmethod
    def from_vacancy_url(url: str) -> JobSiteHtmlParser:
        if DJINNI_SITE_URL in url:
            return DjinniHtmlParser()
        elif DOU_SITE_URL in url:
            return DouHtmlParser()
        else:
            raise NotImplementedError(f"Job site HTML parser for url {url} is not implemented")
