import logging
from collections.abc import Sequence

from fastapi import UploadFile

from app.core.settings import settings
from app.helpers.text import TextLanguageStandardizationConfig, TextLanguageStandardizer
from app.helpers.upload_file import UploadFileProcessor
from app.models.domain import ScoredVacancy, Vacancy, VacancyDetails
from app.services.cv_analysis import CVAnalysisService
from app.services.vacancy_scoring import VacancyScoringService
from app.services.vacancy_scraping import VacancyScrapingService

__all__ = ["CVOperationsService"]


DEFAULT_STANDARDIZATION_CONFIG = TextLanguageStandardizationConfig(primary_language="en", secondary_languages=["uk"])


class CVOperationsService:
    def __init__(
        self,
        cv_analyzer: CVAnalysisService,
        vacancy_scraper: VacancyScrapingService,
        vacancy_scorer: VacancyScoringService,
        language_standardizer: TextLanguageStandardizer,
    ) -> None:
        self._cv_analyzer = cv_analyzer
        self._vacancy_scraper = vacancy_scraper
        self._vacancy_scorer = vacancy_scorer
        self._language_standardizer = language_standardizer

        self._logger = logging.getLogger(self.__class__.__name__)

    async def match_vacancies(self, cv: UploadFile) -> list[ScoredVacancy]:
        file_processor = UploadFileProcessor(cv, settings.MAX_UPLOAD_FILE_SIZE_BYTES)
        self._logger.info("Matching vacancies for file %s", file_processor.filename)

        cv_str = await file_processor.extract_text()
        standardized_cv_list = await self._language_standardizer.standardize_text_language(
            texts=[cv_str], standardization_config=DEFAULT_STANDARDIZATION_CONFIG
        )
        standardized_cv_str = standardized_cv_list[0]

        search_filters = await self._cv_analyzer.extract_search_filters(standardized_cv_str)

        vacancies = await self._vacancy_scraper.fetch_vacancies(search_filters)

        standardized_vacancies_descriptions = await self._language_standardizer.standardize_text_language(
            texts=[vacancy.details.description for vacancy in vacancies],
            standardization_config=DEFAULT_STANDARDIZATION_CONFIG,
        )
        standardized_vacancies = self._apply_translated_vacancies_descriptions(
            vacancies, standardized_vacancies_descriptions
        )

        scored_vacancies = await self._vacancy_scorer.score_vacancies(standardized_cv_str, standardized_vacancies)

        self._logger.info("Successfully matched vacancies for file %s", file_processor.filename)
        return scored_vacancies

    @staticmethod
    def _apply_translated_vacancies_descriptions(
        vacancies: Sequence[Vacancy], descriptions: Sequence[str]
    ) -> list[Vacancy]:
        return [
            Vacancy(
                url=vacancy.url,
                details=VacancyDetails(
                    **vacancy.details.model_dump(exclude={"description"}), description=standardized_description
                ),
            )
            for vacancy, standardized_description in zip(vacancies, descriptions, strict=False)
        ]
