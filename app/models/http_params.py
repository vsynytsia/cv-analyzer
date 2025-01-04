from typing import TypeAlias, TypedDict

__all__ = ["VacancySearchHttpParams", "DouVacancySearchHttpParams", "DjinniVacancySearchHttpParams"]


class DouVacancySearchHttpParams(TypedDict):
    category: str
    exp: str


class DjinniVacancySearchHttpParams(TypedDict):
    primary_keyword: str
    exp_level: str


VacancySearchHttpParams: TypeAlias = DouVacancySearchHttpParams | DjinniVacancySearchHttpParams
