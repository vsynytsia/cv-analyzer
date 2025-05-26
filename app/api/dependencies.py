from typing import Annotated

import jinja2
from fastapi import Depends

__all__ = ["CVOperationsServiceDep"]

# ------ Core Application Dependencies ------


async def get_jinja_environment() -> jinja2.Environment:
    loader = jinja2.FileSystemLoader("app/prompts")
    return jinja2.Environment(loader=loader, trim_blocks=True, lstrip_blocks=True)


JinjaEnvDep = Annotated[jinja2.Environment, Depends(get_jinja_environment)]

# ------ Helpers Dependencies ------

from app.helpers import (
    ContentGenerator,
    GoogleGenaiContentGenerator,
    GoogletransTextTranslator,
    LangdetectLanguageDetector,
    LanguageDetector,
    TextLanguageStandardizer,
    TextTranslator,
)


async def get_text_translator() -> TextTranslator:
    return GoogletransTextTranslator()


async def get_language_detector() -> LanguageDetector:
    return LangdetectLanguageDetector()


async def get_content_generator() -> ContentGenerator:
    return GoogleGenaiContentGenerator()


TextTranslatorDep = Annotated[TextTranslator, Depends(get_text_translator)]
LanguageDetectorDep = Annotated[LanguageDetector, Depends(get_language_detector)]
ContentGeneratorDep = Annotated[ContentGenerator, Depends(get_content_generator)]


async def get_text_language_standardizer(
    language_detector: LanguageDetectorDep, text_translator: TextTranslatorDep
) -> TextLanguageStandardizer:
    return TextLanguageStandardizer(text_language_detector=language_detector, text_translator=text_translator)


TextLanguageStandardizerDep = Annotated[TextLanguageStandardizer, Depends(get_text_language_standardizer)]

# ------ Service Dependencies ------

from app.services import (
    CVAnalysisService,
    CVOperationsService,
    VacancyScoringService,
    VacancyScrapingService,
)


async def get_cv_analysis_service(
    translator: TextTranslatorDep,
    language_detector: LanguageDetectorDep,
    content_generator: ContentGeneratorDep,
    jinja_env: JinjaEnvDep,
) -> CVAnalysisService:
    return CVAnalysisService(translator, language_detector, content_generator, jinja_env)


async def get_vacancy_scraping_service() -> VacancyScrapingService:
    return VacancyScrapingService()


async def get_vacancy_scoring_service(
    content_generator: ContentGeneratorDep, jinja_env: JinjaEnvDep
) -> VacancyScoringService:
    return VacancyScoringService(content_generator, jinja_env)


CVAnalyzerDep = Annotated[CVAnalysisService, Depends(get_cv_analysis_service)]
VacancyScraperDep = Annotated[VacancyScrapingService, Depends(get_vacancy_scraping_service)]
VacancyScorerDep = Annotated[VacancyScoringService, Depends(get_vacancy_scoring_service)]


async def get_cv_operations_service(
    cv_analyzer: CVAnalyzerDep,
    vacancy_scraper: VacancyScraperDep,
    vacancy_scorer: VacancyScorerDep,
    text_language_standardizer: TextLanguageStandardizerDep,
) -> CVOperationsService:
    return CVOperationsService(
        cv_analyzer=cv_analyzer,
        vacancy_scraper=vacancy_scraper,
        vacancy_scorer=vacancy_scorer,
        language_standardizer=text_language_standardizer,
    )


CVOperationsServiceDep = Annotated[CVOperationsService, Depends(get_cv_operations_service)]
