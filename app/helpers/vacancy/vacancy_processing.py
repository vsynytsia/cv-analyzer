import logging

from app.helpers.text import LanguageDetector, TextTranslator, TranslationConfig
from app.models.domain import Vacancy

__all__ = ["VacancyProcessor"]


class VacancyProcessor:
    def __init__(self, translator: TextTranslator, language_detector: LanguageDetector) -> None:
        self._translator = translator
        self._language_detector = language_detector
        self._logger = logging.getLogger(self.__class__.__name__)

    async def standardize_vacancies_language(self, vacancies: list[Vacancy]) -> list[Vacancy]:
        ukrainian_vacancies, english_vacancies = [], []

        for vacancy in vacancies:
            vacancy_lang = self._language_detector.detect_language(vacancy.description)
            if vacancy_lang == "uk":
                ukrainian_vacancies.append(vacancy)
            elif vacancy_lang == "en":
                english_vacancies.append(vacancy)
            else:
                self._logger.warning(f"Skipping vacancy with unexpected language '{vacancy_lang}': {vacancy}")

        self._logger.info(
            "Detected %d ukrainian and %d english vacancies", len(ukrainian_vacancies), len(english_vacancies)
        )

        translated_descriptions = await self._translator.batch_translate(
            texts=[vacancy.description for vacancy in ukrainian_vacancies],
            translation_config=TranslationConfig(source_language="uk", target_language="en"),
        )

        translated_ukrainian_vacancies = [
            Vacancy(**vacancy.model_dump(exclude={"description"}), description=translated_description)
            for vacancy, translated_description in zip(ukrainian_vacancies, translated_descriptions, strict=False)
        ]
        standardized_vacancies = english_vacancies + translated_ukrainian_vacancies

        self._logger.info("Standardized vacancies language")
        return standardized_vacancies
