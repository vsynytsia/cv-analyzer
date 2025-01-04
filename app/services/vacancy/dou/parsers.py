from app.helpers.bs4 import (
    extract_element_text_safe,
    extract_element_text_unsafe,
    extract_first_line_of_multiline_string_safe,
    get_bs4_html_parser,
)
from app.schemas.vacancies import Vacancy


def parse_vacancy_html(vacancy_html: bytes, vacancy_url: str) -> Vacancy:
    parser = get_bs4_html_parser(vacancy_html)

    description = extract_element_text_unsafe(parser, "div", separator=" ", class_="b-typo vacancy-section")
    job_title = extract_element_text_safe(parser, "h1", class_="g-h2")
    salary = extract_element_text_safe(parser, "span", class_="salary")
    company_name = extract_first_line_of_multiline_string_safe(parser, "div", class_="l-n")

    return Vacancy(
        url=vacancy_url, description=description, job_title=job_title, company_name=company_name, salary=salary
    )


def extract_vacancy_urls(search_result: bytes, limit: int | None = None) -> list[str]:
    soup = get_bs4_html_parser(search_result)
    vacancy_urls = [link["href"] for link in soup.find_all("a", class_="vt")]
    return vacancy_urls[:limit] if limit is not None else vacancy_urls
