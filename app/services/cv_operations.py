import logging

from fastapi import UploadFile

from app.core.settings import settings
from app.helpers.upload_file import UploadFileProcessor
from app.models.domain import ScoredVacancy
from app.services.cv_analysis import CVAnalysisService
from app.services.vacancy_processing import VacancyProcessingService
from app.services.vacancy_scoring import VacancyScoringService
from app.services.vacancy_scraping import VacancyScrapingService

__all__ = ["CVOperationsService"]


class CVOperationsService:
    def __init__(
        self,
        cv_analyzer: CVAnalysisService,
        vacancy_scraper: VacancyScrapingService,
        vacancy_processor: VacancyProcessingService,
        vacancy_scorer: VacancyScoringService,
    ) -> None:
        self._cv_analyzer = cv_analyzer
        self._vacancy_scraper = vacancy_scraper
        self._vacancy_processor = vacancy_processor
        self._vacancy_scorer = vacancy_scorer
        self._logger = logging.getLogger(self.__class__.__name__)

    async def match_vacancies(self, cv: UploadFile) -> list[ScoredVacancy]:
        file_processor = UploadFileProcessor(cv, settings.MAX_UPLOAD_FILE_SIZE_BYTES)
        self._logger.info("Matching vacancies for file %s", file_processor.filename)

        cv_str = await file_processor.extract_text()
        cv_str = await self._cv_analyzer.standardize_cv_language(cv_str)

        search_filters = await self._cv_analyzer.extract_search_filters(cv_str)

        vacancies = await self._vacancy_scraper.fetch_vacancies(search_filters)
        vacancies = await self._vacancy_processor.standardize_vacancies_language(vacancies)

        scored_vacancies = await self._vacancy_scorer.score_vacancies(cv_str, vacancies)

        self._logger.info("Successfully matched vacancies for file %s", file_processor.filename)
        return scored_vacancies
