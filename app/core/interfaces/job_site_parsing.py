import abc

from app.models import VacancyDetails

__all__ = ["IJobSiteHtmlParser"]


class IJobSiteHtmlParser(abc.ABC):
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
