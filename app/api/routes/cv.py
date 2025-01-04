import logging

from fastapi import APIRouter, HTTPException, UploadFile, status

from app.api.deps import GeminiClientDep, HttpClientDep, JinjaEnvDep
from app.core.exceptions import GeminiAPIError, TranslationAPIError, UnsupportedLanguageError
from app.helpers.upload_file import file_size_exceeds_limit, is_pdf
from app.schemas.vacancies import ScoredVacancy
from app.services import cv_service, score_service, vacancy_service

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cv", tags=["CV"])


@router.post("/process", response_model=list[ScoredVacancy])
async def process_cv(
    cv: UploadFile, gemini_client: GeminiClientDep, http_client: HttpClientDep, jinja_env: JinjaEnvDep
) -> list[ScoredVacancy]:
    logger.info(f"Started processing {cv.filename}")

    if not is_pdf(cv):
        raise HTTPException(
            status.HTTP_415_UNSUPPORTED_MEDIA_TYPE, "Unsupported file type. Currently, only PDFs are supported."
        )
    if file_size_exceeds_limit(cv):
        raise HTTPException(status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, "Uploaded file is too large.")

    try:
        cv_str = await cv_service.extract_and_standardize_cv_text(cv)
        logger.info("Extracted text from CV")

        search_filters = await cv_service.extract_search_filters(gemini_client, jinja_env, cv_str)
        logger.info("Extracted search filters from CV")

        vacancies = await vacancy_service.fetch_filtered_vacancies(http_client, search_filters)
        logger.info("Fetched filtered vacancies")

        standardized_vacancies = await vacancy_service.standardize_vacancies_language(vacancies)
        logger.info("Standardized vacancies language")

        scored_vacancies = await score_service.score_vacancies(gemini_client, jinja_env, cv_str, standardized_vacancies)
        logger.info("Scored vacancies")
    except UnsupportedLanguageError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Uploaded CV has unsupported language.")
    except TranslationAPIError:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Upstream Translation API error.")
    except GeminiAPIError:
        raise HTTPException(status.HTTP_502_BAD_GATEWAY, "Upstream Gemini error.")
    except Exception as ex:
        logger.exception(ex)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, "Unknown internal error.")

    logger.info(f"Successfully processed {cv.filename}")
    return scored_vacancies
