import logging

import jinja2
from fastapi import UploadFile

from app.core.exceptions import UnsupportedLanguageError
from app.helpers import genai, language, upload_file
from app.schemas.filters import JobSearchFilter
from app.services.cv.converters import llm_response_to_job_search_filters
from app.services.cv.schemas import VacancySearchFilterLlmResponse

logger = logging.getLogger(__name__)


async def extract_and_standardize_cv_text(cv: UploadFile) -> str:
    cv_text = await upload_file.extract_text_from_pdf(cv)
    cv_language = language.detect_text_language(cv_text)

    if cv_language == "en":
        return cv_text
    elif cv_language == "uk":
        return await language.translate_text(cv_text, source_language="uk", target_language="en")
    else:
        logger.exception(f"Got CV with unsupported language '{cv_language}': {cv_text}")
        raise UnsupportedLanguageError(cv_language)


async def extract_search_filters(
    gemini_client: genai.GenerativeModel, jinja_env: jinja2.Environment, cv: str
) -> list[JobSearchFilter]:
    prompt = _get_search_filters_extraction_prompt(jinja_env, cv)
    response = await genai.generate_content_async_with_response_schema(
        model=gemini_client, contents=[prompt], response_schema=VacancySearchFilterLlmResponse
    )
    return llm_response_to_job_search_filters(response)


def _get_search_filters_extraction_prompt(jinja_env: jinja2.Environment, cv: str) -> str:
    prompt_template = jinja_env.get_template("cv/prompts/search_filters.j2")
    return prompt_template.render(cv=cv)
