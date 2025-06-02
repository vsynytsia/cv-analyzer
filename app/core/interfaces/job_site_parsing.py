from typing import Protocol

from app.models import VacancyDetails

__all__ = ["IJobSiteHtmlParser"]


class IJobSiteHtmlParser(Protocol):
    @property
    def site_url(self) -> str:
        pass

    @property
    def site_vacancies_url(self) -> str:
        pass

    def parse_vacancy_urls(self, html_content: bytes) -> list[str]:
        pass

    def parse_vacancy_details(self, vacancy_html_content: bytes) -> VacancyDetails:
        pass
