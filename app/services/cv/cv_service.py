import logging

import jinja2
from fastapi import UploadFile
from google import generativeai as genai

from app.core.exceptions import UnsupportedLanguageError
from app.schemas.vacancy import VacancySearchFilter
from app.services.file import file_service
from app.services.genai import genai_service
from app.services.language import language_service

from .converters import convert_llm_response_to_vacancy_search_filters
from .schemas import VacancySearchFilterLlmResponse

logger = logging.getLogger(__name__)


async def extract_and_standardize_cv_text(cv: UploadFile) -> str:
    cv_text = await file_service.extract_text_from_pdf(cv)
    cv_language = language_service.detect_text_language(cv_text)

    if cv_language == "en":
        return cv_text
    elif cv_language == "uk":
        return await language_service.translate_text(cv_text, source_language="uk", target_language="en")
    else:
        logger.exception(f"Got CV with unsupported language '{cv_language}': {cv_text}")
        raise UnsupportedLanguageError(cv_language)


async def extract_search_filters(
    gemini_client: genai.GenerativeModel, jinja_env: jinja2.Environment, cv: str
) -> list[VacancySearchFilter]:
    prompt = _get_search_filters_extraction_prompt(jinja_env, cv)
    response = await genai_service.generate_content_async_with_response_schema(
        gemini_client=gemini_client, contents=[prompt], response_schema=VacancySearchFilterLlmResponse
    )
    return convert_llm_response_to_vacancy_search_filters(response)


def _get_search_filters_extraction_prompt(jinja_env: jinja2.Environment, cv: str) -> str:
    prompt_template = jinja_env.get_template("search_filters.j2")
    return prompt_template.render(cv=cv)
