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
    CVAnalyzer,
    GoogleGenaiContentGenerator,
    GoogletransTextTranslator,
    LangdetectLanguageDetector,
    LanguageDetector,
    TextTranslator,
    VacancyProcessor,
    VacancyScorer,
    VacancyScraper,
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


async def get_cv_analyzer(
    translator: TextTranslatorDep,
    language_detector: LanguageDetectorDep,
    content_generator: ContentGeneratorDep,
    jinja_env: JinjaEnvDep,
) -> CVAnalyzer:
    return CVAnalyzer(translator, language_detector, content_generator, jinja_env)


async def get_vacancy_scraper() -> VacancyScraper:
    return VacancyScraper()


async def get_vacancy_processor(
    translator: TextTranslatorDep, language_detector: LanguageDetectorDep
) -> VacancyProcessor:
    return VacancyProcessor(translator, language_detector)


async def get_vacancy_scorer(content_generator: ContentGeneratorDep, jinja_env: JinjaEnvDep) -> VacancyScorer:
    return VacancyScorer(content_generator, jinja_env)


CVAnalyzerDep = Annotated[CVAnalyzer, Depends(get_cv_analyzer)]
VacancyScraperDep = Annotated[VacancyScraper, Depends(get_vacancy_scraper)]
VacancyProcessorDep = Annotated[VacancyProcessor, Depends(get_vacancy_processor)]
VacancyScorerDep = Annotated[VacancyScorer, Depends(get_vacancy_scorer)]

# ------ Service Dependencies ------

from app.services import CVOperationsService


async def get_cv_operations_service(
    cv_analyzer: CVAnalyzerDep,
    vacancy_scraper: VacancyScraperDep,
    vacancy_processor: VacancyProcessorDep,
    vacancy_scorer: VacancyScorerDep,
) -> CVOperationsService:
    return CVOperationsService(
        cv_analyzer=cv_analyzer,
        vacancy_scraper=vacancy_scraper,
        vacancy_processor=vacancy_processor,
        vacancy_scorer=vacancy_scorer,
    )


CVOperationsServiceDep = Annotated[CVOperationsService, Depends(get_cv_operations_service)]
