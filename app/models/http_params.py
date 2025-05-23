from typing import TypedDict

__all__ = ["DouVacancySearchHttpParams", "DjinniVacancySearchHttpParams"]


class DouVacancySearchHttpParams(TypedDict):
    category: str
    exp: str


class DjinniVacancySearchHttpParams(TypedDict):
    primary_keyword: str
    exp_level: str
