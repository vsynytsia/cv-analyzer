import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from app.api.serializers import ErrorSerializer
from app.core.exceptions import (
    BusinessError,
    CVAnalyzerException,
    ExternalServiceError,
    FileTooLarge,
    InternalError,
    UnsupportedFileType,
    UserInputError,
)

__all__ = ["register_error_handlers"]

logger = logging.getLogger(__name__)


def json_cv_analyzer_error_handler(error: CVAnalyzerException, status_code: int) -> JSONResponse:
    error_message = ErrorSerializer(code=error.code, message=str(error)).model_dump()
    return JSONResponse(status_code=status_code, content=error_message)


def register_error_handlers(app: FastAPI):
    @app.exception_handler(CVAnalyzerException)
    def handle_cv_analyzer_exception(req: Request, error: CVAnalyzerException):
        mapping = [
            (FileTooLarge, status.HTTP_413_REQUEST_ENTITY_TOO_LARGE),
            (UnsupportedFileType, status.HTTP_415_UNSUPPORTED_MEDIA_TYPE),
            (UserInputError, status.HTTP_400_BAD_REQUEST),
            (BusinessError, status.HTTP_400_BAD_REQUEST),
            (InternalError, status.HTTP_500_INTERNAL_SERVER_ERROR),
            (ExternalServiceError, status.HTTP_502_BAD_GATEWAY),
        ]

        for error_type, status_code in mapping:
            if issubclass(type(error), error_type):
                logging.error(f"Handled server error: {error}", exc_info=error)
                return json_cv_analyzer_error_handler(error, status_code)

        raise RuntimeError(f"Could not map exception {error} to proper HTTP type")

    @app.exception_handler(Exception)
    def handle_all_errors(req: Request, error: Exception):
        logger.error(f"Unhandled server error: {error}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=ErrorSerializer(code="unhandled_error", message=str(error)).model_dump(),
        )
