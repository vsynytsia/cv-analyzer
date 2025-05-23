import abc
from typing import TypedDict

from app.models.http_params import DjinniVacancySearchHttpParams, DouVacancySearchHttpParams

from .category import DjinniCategory, DouCategory

__all__ = ["VacancySearchFilter", "DouSearchFilter", "DjinniSearchFilter"]


class VacancySearchFilter(abc.ABC):
    @property
    @abc.abstractmethod
    def normalized_experience(self) -> str:
        raise NotImplementedError

    @abc.abstractmethod
    def to_http_request_params(self) -> TypedDict:
        raise NotImplementedError

    @abc.abstractmethod
    def __str__(self) -> str:
        raise NotImplementedError


class DjinniSearchFilter(VacancySearchFilter):
    def __init__(self, experience_years: int, category: DjinniCategory):
        self.experience_years = experience_years
        self.category = category

    def to_http_request_params(self) -> DjinniVacancySearchHttpParams:
        return DjinniVacancySearchHttpParams(primary_keyword=self.category, exp_level=self.normalized_experience)

    @property
    def normalized_experience(self) -> str:
        if self.experience_years <= 0:
            return "no_exp"
        else:
            return f"{min(self.experience_years, 10)}y"

    def __str__(self) -> str:
        return " ".join(
            (
                "<",
                f"class '{self.__class__.__name__}':",
                f"{self.experience_years = }",
                f"{self.category = }",
                ">",
            )
        )


class DouSearchFilter(VacancySearchFilter):
    def __init__(self, experience_years: int, category: DouCategory):
        self.experience_years = experience_years
        self.category = category

    def to_http_request_params(self) -> DouVacancySearchHttpParams:
        return DouVacancySearchHttpParams(category=self.category, exp=self.normalized_experience)

    @property
    def normalized_experience(self) -> str:
        if 0 <= self.experience_years < 1:
            return "0-1"
        elif 1 <= self.experience_years < 3:
            return "1-3"
        elif 3 <= self.experience_years < 5:
            return "3-5"
        else:
            return "5plus"

    def __str__(self) -> str:
        return " ".join(
            (
                "<",
                f"class '{self.__class__.__name__}':",
                f"{self.experience_years = }",
                f"{self.category = }",
                ">",
            )
        )
