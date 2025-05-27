from dependency_injector import containers, providers

from app.helpers.generative import ContentGenerator, GoogleGenaiContentGenerator, JinjaPromptManager, PromptManager
from app.helpers.text import (
    GoogletransTextTranslator,
    LangdetectTextLanguageDetector,
    TextLanguageDetector,
    TextLanguageStandardizer,
    TextTranslator,
)
from app.services import CVAnalysisService, CVOperationsService, VacancyScoringService, VacancyScrapingService

__all__ = ["Containers"]


class Helpers(containers.DeclarativeContainer):
    text_translator: providers.Singleton[TextTranslator] = providers.Singleton(GoogletransTextTranslator)

    text_language_detector: providers.Singleton[TextLanguageDetector] = providers.Singleton(
        LangdetectTextLanguageDetector
    )

    text_language_standardizer: providers.Singleton[TextLanguageStandardizer] = providers.Singleton(
        TextLanguageStandardizer, text_language_detector=text_language_detector, text_translator=text_translator
    )

    content_generator: providers.Singleton[ContentGenerator] = providers.Singleton(GoogleGenaiContentGenerator)

    prompt_manager: providers.Singleton[PromptManager] = providers.Singleton(JinjaPromptManager)


class Containers(containers.DeclarativeContainer):
    helpers: providers.Container[Helpers] = providers.Container(Helpers)

    cv_analysis_service: providers.Singleton[CVAnalysisService] = providers.Singleton(
        CVAnalysisService,
        translator=helpers.text_translator,
        language_detector=helpers.text_language_detector,
        content_generator=helpers.content_generator,
        prompt_manager=helpers.prompt_manager,
    )

    vacancy_scraping_service: providers.Singleton[VacancyScrapingService] = providers.Singleton(VacancyScrapingService)

    vacancy_scoring_service: providers.Singleton[VacancyScoringService] = providers.Singleton(
        VacancyScoringService, content_generator=helpers.content_generator, prompt_manager=helpers.prompt_manager
    )

    cv_operations_service: providers.Singleton[CVOperationsService] = providers.Singleton(
        CVOperationsService,
        cv_analyzer=cv_analysis_service,
        vacancy_scraper=vacancy_scraping_service,
        vacancy_scorer=vacancy_scoring_service,
        language_standardizer=helpers.text_language_standardizer,
    )
