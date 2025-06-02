import logging

from app.core.interfaces.generative import GenerationConfig, IContentGenerator, IPromptManager
from app.core.interfaces.text import ITextLanguageDetector, ITextTranslator
from app.models.domain import DjinniSearchFilter, DouSearchFilter, VacancySearchFilter
from app.models.generative import ExtractVacancyFiltersLlmResponse, ExtractVacancyFiltersPromptParams

__all__ = ["CVAnalysisService"]


class CVAnalysisService:
    def __init__(
        self,
        translator: ITextTranslator,
        language_detector: ITextLanguageDetector,
        content_generator: IContentGenerator,
        prompt_manager: IPromptManager,
    ) -> None:
        self._translator = translator
        self._language_detector = language_detector
        self._content_generator = content_generator
        self._prompt_manager = prompt_manager
        self._logger = logging.getLogger(self.__class__.__name__)

    async def extract_search_filters(self, cv: str) -> list[VacancySearchFilter]:
        prompt = self._get_search_filters_extraction_prompt(cv)
        response = await self._content_generator.generate_structured_content(
            prompt=prompt,
            generation_config=GenerationConfig(temperature=0, response_model=ExtractVacancyFiltersLlmResponse),
        )
        search_filters = self._vacancy_search_filter_llm_response_to_job_search_filters(response)

        self._logger.info("Extracted search filters %s", [str(search_filter) for search_filter in search_filters])
        return search_filters

    def _get_search_filters_extraction_prompt(self, cv: str) -> str:
        return self._prompt_manager.render_prompt_template(
            prompt_template_path="extract_search_filters.tpl", **ExtractVacancyFiltersPromptParams(cv=cv)
        )

    @staticmethod
    def _vacancy_search_filter_llm_response_to_job_search_filters(
        response: ExtractVacancyFiltersLlmResponse,
    ) -> list[VacancySearchFilter]:
        return [
            DouSearchFilter(experience_years=response.years_of_experience, category=response.dou_category),
            DjinniSearchFilter(experience_years=response.years_of_experience, category=response.djinni_category),
        ]
