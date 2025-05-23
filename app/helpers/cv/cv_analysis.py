import logging

import jinja2

from app.core.exceptions import UnsupportedCVLanguage
from app.helpers import utils
from app.helpers.generative import ContentGenerator, GenerationConfig
from app.helpers.text import LanguageDetector, TextTranslator, TranslationConfig
from app.models.domain import DjinniSearchFilter, DouSearchFilter, VacancySearchFilter
from app.models.generative import ExtractVacancyFiltersLlmResponse, ExtractVacancyFiltersPromptParams

__all__ = ["CVAnalyzer"]


class CVAnalyzer:
    def __init__(
        self,
        translator: TextTranslator,
        language_detector: LanguageDetector,
        content_generator: ContentGenerator,
        jinja_env: jinja2.Environment,
    ) -> None:
        self._translator = translator
        self._language_detector = language_detector
        self._content_generator = content_generator
        self._jinja_env = jinja_env
        self._logger = logging.getLogger(self.__class__.__name__)

    async def standardize_cv_language(self, cv: str) -> str:
        cv_language = self._language_detector.detect_language(cv)

        if cv_language == "en":
            self._logger.info("CV is already in English. No standardization needed.")
            return cv
        elif cv_language == "uk":
            self._logger.info("Translating CV from uk to en")
            return await self._translator.translate(
                cv, translation_config=TranslationConfig(source_language="uk", target_language="en")
            )
        else:
            raise UnsupportedCVLanguage(cv_language)

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
        return utils.get_rendered_template(
            env=self._jinja_env, template_path="extract_search_filters.tpl", **ExtractVacancyFiltersPromptParams(cv=cv)
        )

    @staticmethod
    def _vacancy_search_filter_llm_response_to_job_search_filters(
        response: ExtractVacancyFiltersLlmResponse,
    ) -> list[VacancySearchFilter]:
        return [
            DouSearchFilter(experience_years=response.years_of_experience, category=response.dou_category),
            DjinniSearchFilter(experience_years=response.years_of_experience, category=response.djinni_category),
        ]
