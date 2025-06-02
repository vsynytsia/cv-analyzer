from dependency_injector import containers, providers

from app.core.interfaces.generative import IContentGenerator, IPromptManager
from app.core.interfaces.text import ITextLanguageDetector, ITextTranslator
from app.core.settings import settings
from app.infrastructure.file import FileProcessor
from app.infrastructure.generative import GoogleGenaiContentGenerator, JinjaPromptManager
from app.infrastructure.text import (
    GoogletransTextTranslator,
    LangdetectTextLanguageDetector,
    TextLanguageStandardizer,
)
from app.services import CVAnalysisService, CVOperationsService, VacancyScoringService, VacancyScrapingService

__all__ = ["Containers"]


class Infrastructure(containers.DeclarativeContainer):
    text_translator: providers.Singleton[ITextTranslator] = providers.Singleton(GoogletransTextTranslator)

    text_language_detector: providers.Singleton[ITextLanguageDetector] = providers.Singleton(
        LangdetectTextLanguageDetector
    )

    text_language_standardizer: providers.Singleton[TextLanguageStandardizer] = providers.Singleton(
        TextLanguageStandardizer, text_language_detector=text_language_detector, text_translator=text_translator
    )

    content_generator: providers.Singleton[IContentGenerator] = providers.Singleton(GoogleGenaiContentGenerator)

    prompt_manager: providers.Singleton[IPromptManager] = providers.Singleton(JinjaPromptManager)

    file_processor: providers.Singleton[FileProcessor] = providers.Singleton(
        FileProcessor, max_file_size_bytes=settings.MAX_UPLOAD_FILE_SIZE_BYTES
    )


class Containers(containers.DeclarativeContainer):
    infrastructure: providers.Container[Infrastructure] = providers.Container(Infrastructure)

    cv_analysis_service: providers.Singleton[CVAnalysisService] = providers.Singleton(
        CVAnalysisService,
        translator=infrastructure.text_translator,
        language_detector=infrastructure.text_language_detector,
        content_generator=infrastructure.content_generator,
        prompt_manager=infrastructure.prompt_manager,
    )

    vacancy_scraping_service: providers.Singleton[VacancyScrapingService] = providers.Singleton(VacancyScrapingService)

    vacancy_scoring_service: providers.Singleton[VacancyScoringService] = providers.Singleton(
        VacancyScoringService,
        content_generator=infrastructure.content_generator,
        prompt_manager=infrastructure.prompt_manager,
    )

    cv_operations_service: providers.Singleton[CVOperationsService] = providers.Singleton(
        CVOperationsService,
        cv_analyzer=cv_analysis_service,
        vacancy_scraper=vacancy_scraping_service,
        vacancy_scorer=vacancy_scoring_service,
        language_standardizer=infrastructure.text_language_standardizer,
        file_processor=infrastructure.file_processor,
    )
