from .base import ExternalServiceError

__all__ = ["TextTranslationError"]


class TextTranslationError(ExternalServiceError):
    code = "text_translation_error"

    def __init__(self) -> None:
        super().__init__("Error translating text")
